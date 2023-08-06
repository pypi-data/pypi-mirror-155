"""
Functions for interacting with Amazon Web Services.

This module supports management of AWS accounts, S3 buckets, and objects in S3 buckets. It uses Amazon's boto3 library
behind the scenes.

In order for HEA to access AWS accounts, buckets, and objects, there must be a volume accessible to the user through
the volumes microservice with an AWSFileSystem for its file system. Additionally, credentials must either be stored
in the keychain microservice and associated with the volume through the volume's credential_id attribute,
or stored on the server's file system in a location searched by the AWS boto3 library. Users can only see the
accounts, buckets, and objects to which the provided AWS credentials allow access, and HEA may additionally restrict
the returned objects as documented in the functions below. The purpose of volumes in this case is to supply credentials
to AWS service calls. Support for boto3's built-in file system search for credentials is only provided for testing and
should not be used in a production setting. This module is designed to pass the current user's credentials to AWS3, not
to have application-wide credentials that everyone uses.

The request argument to these functions is expected to have a OIDC_CLAIM_sub header containing the user id for
permissions checking. No results will be returned if this header is not provided or is empty.

In general, there are two flavors of functions for getting accounts, buckets, and objects. The first expects the id
of a volume as described above. The second expects the id of an account, bucket, or bucket and object. The latter
attempts to match the request up to any volumes with an AWSFileSystem that the user has access to for the purpose of
determine what AWS credentials to use. They perform the
same except when the user has access to multiple such volumes, in which case supplying the volume id avoids a search
through the user's volumes.
"""
import asyncio
import logging
from botocore.exceptions import ClientError
from aiohttp import web

from .awss3bucketobjectkey import KeyDecodeException, encode_key, decode_key, is_folder
from heaserver.service.heaobjectsupport import new_heaobject_from_type

from .. import response, client
from ..heaobjectsupport import type_to_resource_url, PermissionGroup
from ..oidcclaimhdrs import SUB
from ..aiohttp import StreamResponseFileLikeWrapper, RequestFileLikeWrapper
from ..mimetypes import guess_mime_type
from ..appproperty import HEA_DB
from typing import Any, Optional, List, Dict
from aiohttp.web import Response
from aiohttp.web import Request
from heaobject.volume import AWSFileSystem, Volume
from heaobject.user import NONE_USER, ALL_USERS
from heaobject.bucket import AWSBucket
from heaobject.root import DesktopObjectDict, ShareImpl, EnumAutoName
from heaobject.folder import AWSS3Folder, AWSS3Item, Folder
from heaobject.data import AWSS3FileObject
from heaobject.account import AWSAccount
from heaobject.aws import S3StorageClass
from heaobject.error import DeserializeException
from yarl import URL
from asyncio import gather
from heaobject.root import Tag
from enum import auto
from functools import partial

from ..sources import AWS_S3, HEA
from mypy_boto3_s3.client import S3Client
from mypy_boto3_s3.service_resource import S3ServiceResource
from mypy_boto3_s3.type_defs import TagTypeDef
from datetime import datetime

from collections import defaultdict
from heaobject.storage import AWSStorage

"""
Available functions
AWS object
- get_account
- post_account                    NOT TESTED
- put_account                     NOT TESTED
- delete_account                  CANT https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_accounts_close.html
                                  One solution would be to use beautiful soup : https://realpython.com/beautiful-soup-web-scraper-python/

- users/policies/roles : https://www.learnaws.org/2021/05/12/aws-iam-boto3-guide/

- change_storage_class            TODO
- copy_object
- delete_bucket_objects
- delete_bucket
- delete_folder
- delete_object
- download_object
- download_archive_object         TODO
- generate_presigned_url
- get_object_meta
- get_object_content
- get_all_buckets
- get all
- opener                          TODO -> return file format -> returning metadata containing list of links following collection + json format
-                                         need to pass back collection - json format with link with content type, so one or more links, most likely
- post_bucket
- post_folder
- post_object
- post_object_archive             TODO
- put_bucket
- put_folder
- put_object
- put_object_archive              TODO
- transfer_object_within_account
- transfer_object_between_account TODO
- rename_object
- update_bucket_policy            TODO

TO DO
- accounts?
"""
MONGODB_BUCKET_COLLECTION = 'buckets'

CLIENT_ERROR_NO_SUCH_BUCKET = 'NoSuchBucket'
CLIENT_ERROR_ACCESS_DENIED = 'AccessDenied'
CLIENT_ERROR_FORBIDDEN = '403'
CLIENT_ERROR_404 = '404'
CLIENT_ERROR_ALL_ACCESS_DISABLED = 'AllAccessDisabled'

ROOT_FOLDER = Folder()
ROOT_FOLDER.id = 'root'
ROOT_FOLDER.name = 'root'
ROOT_FOLDER.display_name = 'Root'
ROOT_FOLDER.description = "The root folder for an AWS S3 bucket's objects."
_root_share = ShareImpl()
_root_share.user = ALL_USERS
_root_share.permissions = PermissionGroup.POSTER_PERMS.perms
ROOT_FOLDER.shares = [_root_share]
ROOT_FOLDER.source = HEA

async def get_account(request: Request, volume_id: str) -> Response:
    """
    Gets the AWS account associated with the provided volume id.

    Only get since you can't delete or put id information
    currently being accessed. If organizations get included, then the delete, put, and post will be added for name,
    phone, email, ,etc.
    NOTE: maybe get email from the login portion of the application?

    :param request: the aiohttp Request (required).
    :param volume_id: the id string of the volume representing the user's AWS account.
    :return: an HTTP response with an AWSAccount object in the body.
    FIXME: a bad volume_id should result in a 400 status code; currently has status code 500.
    """
    aws_object_dict = await _get_account(request, volume_id)
    return await response.get(request, aws_object_dict)


async def get_account_by_id(request: web.Request) -> Optional[DesktopObjectDict]:
    """
    Gets an account by its id. The id is expected to be the request object's match_info mapping, with key 'id'.

    :param request: an aiohttp Request object (required).
    :return: an AWSAccount dict.
    """
    return next((a for a in await gather(
        *[_get_account(request, v.id) async for v in request.app[HEA_DB].get_volumes(request, AWSFileSystem)])
                 if
                 a['id'] == request.match_info['id']), None)


async def get_volume_id_for_account_id(request: web.Request) -> Optional[str]:
    """
    Gets the id of the volume associated with an AWS account. The account id is expected to be in the request object's
    match_info mapping, with key 'id'.

    :param request: an aiohttp Request object (required).
    :return: a volume id string, or None if no volume was found associated with the AWS account.
    """
    async def get_one(request, volume_id):
        return volume_id, await _get_account(request, volume_id)

    return next((volume_id for (volume_id, a) in await gather(
        *[get_one(request, v.id) async for v in request.app[HEA_DB].get_volumes(request, AWSFileSystem)])
                 if
                 a['id'] == request.match_info['id']), None)


async def get_all_accounts(request: web.Request) -> List[DesktopObjectDict]:
    """
    Gets all AWS accounts for the current user.

    In order for HEA to access an AWS account, there must be a volume accessible to the user through the volumes
    microservice with an AWSFileSystem for its file system, and credentials must either be stored in the keychain
    microservice and associated with the volume, or stored on the server's file system in a location searched by the
    AWS boto3 library.

    :param request: an aiohttp Request object (required).
    :return: a list of AWSAccount objects, or the empty list of the current user has no accounts.
    """
    return [a for a in await gather(
        *[_get_account(request, v.id) async for v in request.app[HEA_DB].get_volumes(request, AWSFileSystem)])]


async def put_account(request: Request) -> Response:
    """
    Since name and email can only be done from console, then the alternate contact is the only updatable information on the account.
    TODO: should parameters should be passed as a dict? So put can change only parts of it and not all of it.
    TODO: email can only be done from console: maybe try beautiful soup?
    TODO: name can only be done from console: https://aws.amazon.com/premiumsupport/knowledge-center/change-organizations-name/
    alt_contact_type (str) : 'BILLING' | 'OPERATIONS' | 'SECURITY'
    """
    try:
        volume_id = request.match_info.get("volume_id", None)
        alt_contact_type = request.match_info.get("alt_contact_type", None)
        email_address = request.match_info.get("email_address", None)
        name = request.match_info.get("name", None)
        phone = request.match_info.get("phone", None)
        title = request.match_info.get("title", None)
        if not volume_id:
            return web.HTTPBadRequest(body="volume_id is required")

        acc_client = await request.app[HEA_DB].get_client(request, 'account', volume_id)
        sts_client = await request.app[HEA_DB].get_client(request, 'sts', volume_id)
        account_id = sts_client.get_caller_identity().get('Account')
        acc_client.put_alternate_contact(AccountId=account_id, AlternateContactType=alt_contact_type,
                                         EmailAddress=email_address, Name=name, PhoneNumber=phone, Title=title)
        return web.HTTPNoContent()
    except ClientError as e:
        return web.HTTPBadRequest()


async def post_account(request: Request) -> Response:
    """
    Called this create since the put, get, and post account all handle information about accounts, while create and delete handle creating/deleting new accounts

    account_email (str)     : REQUIRED: The email address of the owner to assign to the new member account. This email address must not already be associated with another AWS account.
    account_name (str)      : REQUIRED: The friendly name of the member account.
    account_role (str)      : If you don't specify this parameter, the role name defaults to OrganizationAccountAccessRole
    access_to_billing (str) : If you don't specify this parameter, the value defaults to ALLOW

    source: https://github.com/aws-samples/account-factory/blob/master/AccountCreationLambda.py

    Note: Creates an AWS account that is automatically a member of the organization whose credentials made the request.
    This is an asynchronous request that AWS performs in the background. Because CreateAccount operates asynchronously,
    it can return a successful completion message even though account initialization might still be in progress.
    You might need to wait a few minutes before you can successfully access the account
    The user who calls the API to create an account must have the organizations:CreateAccount permission

    When you create an account in an organization using the AWS Organizations console, API, or CLI commands, the information required for the account to operate as a standalone account,
    such as a payment method and signing the end user license agreement (EULA) is not automatically collected. If you must remove an account from your organization later,
    you can do so only after you provide the missing information.
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Client.create_account

    You can only close an account from the Billing and Cost Management Console, and you must be signed in as the root user.
    """
    try:
        volume_id = request.match_info.get("volume_id", None)
        account_email = request.match_info.get("account_email", None)
        account_name = request.match_info.get("account_name", None)
        account_role = request.match_info.get("account_role", None)
        access_to_billing = request.match_info.get("access_to_billing", None)
        if not volume_id:
            return web.HTTPBadRequest(body="volume_id is required")
        org_client = await request.app[HEA_DB].get_client(request, 'organizations', volume_id)
        org_client.create_account(Email=account_email, AccountName=account_name, RoleName=account_role,
                                  IamUserAccessToBilling=access_to_billing)
        return web.HTTPAccepted()
        # time.sleep(60)        # this is here as it  takes some time to create account, and the status would always be incorrect if it went immediately to next lines of code
        # account_status = org_client.describe_create_account_status(CreateAccountRequestId=create_account_response['CreateAccountStatus']['Id'])
        # if account_status['CreateAccountStatus']['State'] == 'FAILED':    # go to boto3 link above to see response syntax
        #     web.HTTPBadRequest()      # the response syntax contains reasons for failure, see boto3 link above to see possible reasons
        # else:
        #     return web.HTTPCreated()  # it may not actually be created, but it likely isn't a failure which means it will be created after a minute or two more, see boto3 docs
    except ClientError as e:
        return web.HTTPBadRequest()  # see boto3 link above to see possible  exceptions


async def delete_account(request: Request, volume_id: str) -> Response:
    """
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Client.create_account
    You can only close an account from the Billing and Cost Management Console, and you must be signed in as the root user..
    """
    # TODO: maybe try Beautiful soup to do this?
    return response.status_not_found()


def change_storage_class():
    """
    change storage class (Archive, un-archive) (copy and delete old)

    S3 to archive -> https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Client.upload_archive
        save archive id for future access?
        archived gets charged minimum 90 days
        buckets = vault?
        delete bucket
    archive to S3
        create vault? link vault to account as attribute?
        delete vault
    """


async def copy_object(request: Request, volume_id: str, source_path: str, destination_path: str) -> Response:
    """
    copy/paste (duplicate), throws error if destination exists, this so an overwrite isn't done
    throws another error is source doesn't exist
    https://medium.com/plusteam/move-and-rename-objects-within-an-s3-bucket-using-boto-3-58b164790b78
    https://stackoverflow.com/questions/47468148/how-to-copy-s3-object-from-one-bucket-to-another-using-python-boto3

    :param request: the aiohttp Request (required).
    :param volume_id: the id string of the volume representing the user's AWS account.
    :param source_path: (str) s3 path of object, includes bucket and key values together
    :param destination_path: (str) s3 path of object, includes bucket and key values together
    :return: the HTTP response.
    """
    # Copy object A as object B
    s3_resource = await request.app[HEA_DB].get_resource(request, 's3', volume_id)
    source_bucket_name = source_path.partition("/")[0]
    source_key_name = source_path.partition("/")[2]
    copy_source = {'Bucket': source_bucket_name, 'Key': source_key_name}
    destination_bucket_name = destination_path.partition("/")[0]
    destination_key_name = destination_path.partition("/")[2]
    try:
        s3_client = await request.app[HEA_DB].get_client(request, 's3', volume_id)
        s3_client.head_object(Bucket=destination_bucket_name,
                              Key=destination_key_name)  # check if destination object exists, if doesn't throws an exception
        return web.HTTPBadRequest()
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == '404':  # object doesn't exist
            try:
                s3_client = await request.app[HEA_DB].get_client(request, 's3', volume_id)
                s3_client.head_object(Bucket=source_bucket_name,
                                      Key=source_key_name)  # check if source object exists, if not throws an exception
                s3_resource.meta.client.copy(copy_source, destination_path.partition("/")[0],
                                             destination_path.partition("/")[2])
                logging.info(e)
                return web.HTTPCreated()
            except ClientError as e_:
                logging.error(e_)
                return web.HTTPBadRequest()
        else:
            logging.info(e)
            return web.HTTPBadRequest()


async def delete_bucket_objects(request: Request, volume_id: str, bucket_name: str,
                                delete_versions: bool = False) -> Response:
    """
    Deletes all objects inside a bucket

    :param request: the aiohttp Request (required).
    :param volume_id: the id string of the volume representing the user's AWS account.
    :param bucket_name: Bucket to delete
    :param delete_versions: Boolean indicating if the versioning should be deleted as well, defaults to False
    :return: the HTTP response with a 204 status code if successful, or 404 if the bucket was not found.
    """
    try:
        s3_resource = await request.app[HEA_DB].get_resource(request, 's3', volume_id)
        s3_client = await request.app[HEA_DB].get_client(request, 's3', volume_id)
        s3_client.head_bucket(Bucket=bucket_name)
        s3_bucket = s3_resource.Bucket(bucket_name)
        if delete_versions:
            bucket_versioning = s3_resource.BucketVersioning(bucket_name)
            if bucket_versioning.status == 'Enabled':
                del_obj_all_result = s3_bucket.object_versions.delete()
                logging.info(del_obj_all_result)
            else:
                del_obj_all_result = s3_bucket.objects.all().delete()
                logging.info(del_obj_all_result)
        else:
            del_obj_all_result = s3_bucket.objects.all().delete()
            logging.info(del_obj_all_result)
        return web.HTTPNoContent()
    except ClientError as e:
        logging.error(e)
        return web.HTTPNotFound()


async def delete_bucket(request: Request) -> Response:
    """
    Deletes bucket and all contents

    :param request: the aiohttp Request (required).
    :return: the HTTP response.
    """
    volume_id = request.match_info.get("volume_id", None)
    bucket_id = request.match_info.get("id", None)
    if not volume_id:
        return web.HTTPBadRequest(body="volume_id is required")
    if not bucket_id:
        return web.HTTPBadRequest(body="bucket_id is required")

    s3_client = await request.app[HEA_DB].get_client(request, 's3', volume_id)
    try:
        s3_client.head_bucket(Bucket=bucket_id)
        await delete_bucket_objects(request, volume_id, bucket_id)
        del_bucket_result = s3_client.delete_bucket(Bucket=bucket_id)
        logging.info(del_bucket_result)
        return web.HTTPNoContent()
    except ClientError as e:
        logging.error(e)
        return web.HTTPNotFound()


async def get_folder(request: Request) -> web.Response:
    """
    Gets the requested folder. The volume id must be in the volume_id entry of the request's match_info dictionary.
    The bucket id must be in the bucket_id entry of the request's match_info dictionary. Either The folder id must be
    in the id entry of the request's match_info dictionary, or the folder name must be in the name entry of the
    request's match_info dictionary.

    :param request: the HTTP request (required).
    :return: the HTTP response containing a heaobject.folder.AWSS3Folder object in the body.
    """
    if 'volume_id' not in request.match_info:
        return response.status_bad_request('volume_id is required')
    if 'bucket_id' not in request.match_info:
        return response.status_bad_request('bucket_id is required')
    if 'id' not in request.match_info and 'name' not in request.match_info:
        return response.status_bad_request('either id or name is required')
    volume_id = request.match_info['volume_id']
    bucket_name = request.match_info['bucket_id']
    folder_name = request.match_info['id'] if 'id' in request.match_info else request.match_info['name']

    s3_client = await request.app[HEA_DB].get_client(request, 's3', volume_id)
    try:
        folder_id: Optional[str] = decode_key(folder_name)
        if not is_folder(folder_id):
            folder_id = None
    except KeyDecodeException:
        # Let the bucket query happen so that we consistently return Forbidden if the user lacks permissions
        # for the bucket.
        folder_id = None
    try:
        if folder_id is None:
            # We couldn't decode the folder_id, and we need to check if the user can access the bucket in order to
            # decide which HTTP status code to respond with (Forbidden vs Not Found).
            s3_client.head_bucket(Bucket=bucket_name)
            return response.status_not_found()
        response_ = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=folder_id, MaxKeys=1)
        logging.debug('Result of get_folder: %s', response_)
        if folder_id is None or response_['KeyCount'] == 0:
            return response.status_not_found()
        contents = response_['Contents'][0]
        key = contents['Key']
        encoded_key = encode_key(key)
        folder = _get_folder(bucket_name, contents, key, encoded_key, request)

        return await response.get(request, folder.to_dict())
    except ClientError as e:
        return _handle_client_error(e)


async def get_file(request: Request) -> Response:
    """
    Gets the requested file. The volume id must be in the volume_id entry of the request's match_info dictionary.
    The bucket id must be in the bucket_id entry of the request's match_info dictionary. The file id must be in
    the id entry of the request's match_info dictionary, or the file name must be in the name entry of the request's
    match_info dictionary.

    :param request: the HTTP request (required).
    :return: the HTTP response containing a heaobject.data.AWSS3FileObject object in the body.
    """
    if 'volume_id' not in request.match_info:
        return response.status_bad_request('volume_id is required')
    if 'bucket_id' not in request.match_info:
        return response.status_bad_request('bucket_id is required')
    if 'id' not in request.match_info and 'name' not in request.match_info:
        return response.status_bad_request('either id or name is required')
    volume_id = request.match_info['volume_id']
    bucket_name = request.match_info['bucket_id']
    file_name = request.match_info['id'] if 'id' in request.match_info else request.match_info['name']

    s3_client = await request.app[HEA_DB].get_client(request, 's3', volume_id)
    try:
        file_id: Optional[str] = decode_key(file_name)
        if is_folder(file_id):
            file_id = None
    except KeyDecodeException:
        # Let the bucket query happen so that we consistently return Forbidden if the user lacks permissions
        # for the bucket.
        file_id = None
    try:
        if file_id is None:
            # We couldn't decode the file_id, and we need to check if the user can access the bucket in order to
            # decide which HTTP status code to respond with (Forbidden vs Not Found).
            s3_client.head_bucket(Bucket=bucket_name)
            return response.status_not_found()
        response_ = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=file_id, MaxKeys=1)
        logging.debug('Result of get_file: %s', response_)
        if file_id is None or response_['KeyCount'] == 0:
            return response.status_not_found()
        contents = response_['Contents'][0]
        key = contents['Key']
        encoded_key = encode_key(key)
        display_name = key[key.rfind('/', 1) + 1:]
        file = _get_file(bucket_name, contents, display_name, key, encoded_key, request)
        return await response.get(request, file.to_dict())
    except ClientError as e:
        return _handle_client_error(e)


async def has_folder(request: Request) -> web.Response:
    """
    Checks for the existence of the requested folder. The volume id must be in the volume_id entry of the request's
    match_info dictionary. The bucket id must be in the bucket_id entry of the request's match_info dictionary. The
    folder id must be in the id entry of the request's match_info dictionary.

    :param request: the HTTP request (required).
    :return: the HTTP response with a 200 status code if the folder exists, 403 if access was denied, 404 if the folder
    was not found, or 500 if an internal error occurred.
    """
    if 'volume_id' not in request.match_info:
        return response.status_bad_request('volume_id is required')
    if 'bucket_id' not in request.match_info:
        return response.status_bad_request('bucket_id is required')
    if 'id' not in request.match_info and 'folder_id' not in request.match_info:
        return response.status_bad_request('id or folder_id is required')
    volume_id = request.match_info['volume_id']
    bucket_name = request.match_info['bucket_id']
    folder_name = request.match_info['id'] if 'id' in request.match_info else request.match_info['folder_id']

    s3_client = await request.app[HEA_DB].get_client(request, 's3', volume_id)
    if folder_name == ROOT_FOLDER.id:
        return response.status_ok()
    else:
        try:
            folder_id: Optional[str] = decode_key(folder_name)
            if not is_folder(folder_id):
                folder_id = None
        except KeyDecodeException:
            # Let the bucket query happen so that we consistently return Forbidden if the user lacks permissions
            # for the bucket.
            folder_id = None

    try:
        if folder_id is None:
            # We couldn't decode the folder_id, and we need to check if the user can access the bucket in order to
            # decide which HTTP status code to respond with (Forbidden vs Not Found).
            s3_client.head_bucket(Bucket=bucket_name)
            return response.status_not_found()
        response_ = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=folder_id, MaxKeys=1)
        logging.debug('Result of has_folder: %s', response_)
        if response_['KeyCount'] == 0:
            return response.status_not_found()
        return response.status_ok()
    except ClientError as e:
        return _handle_client_error(e)


async def bucket_opener(request: Request) -> web.Response:
    """
    Returns links for opening the bucket. The volume id must be in the volume_id entry of the request's
    match_info dictionary. The bucket id must be in the id entry of the request's match_info dictionary.

    :param request: the HTTP request (required).
    :return: the HTTP response with a 200 status code if the bucket exists and a Collection+JSON document in the body
    containing an heaobject.bucket.AWSBucket object and links, 403 if access was denied, 404 if the bucket
    was not found, or 500 if an internal error occurred.
    """
    if 'volume_id' not in request.match_info:
        return response.status_bad_request('volume_id is required')
    if 'id' not in request.match_info:
        return response.status_bad_request('id is required')
    volume_id = request.match_info['volume_id']
    bucket_id = request.match_info['id']
    bucket_name = request.match_info.get('bucket_name', None)

    s3_client = await request.app[HEA_DB].get_client(request, 's3', volume_id)
    s3_resource = await request.app[HEA_DB].get_resource(request, 's3', volume_id)

    try:
        bucket_result = await _get_bucket(volume_id=volume_id, s3_resource=s3_resource, s3_client=s3_client,
                                          bucket_name=bucket_name, bucket_id=bucket_id)
        return await response.get_multiple_choices(request,
                                                   bucket_result.to_dict() if bucket_result is not None else None)
    except ClientError as e:
        return _handle_client_error(e)


async def get_all_folders(request: Request) -> web.Response:
    """
    Gets all folders in a bucket. The volume id must be in the volume_id entry of the request's
    match_info dictionary. The bucket id must be in the bucket_id entry of the request's match_info dictionary.

    :param request: the HTTP request (required).
    :return: the HTTP response with a 200 status code if the bucket exists and a Collection+JSON document in the body
    containing any heaobject.folder.AWSS3Folder objects, 403 if access was denied, or 500 if an internal error occurred. The
    body's format depends on the Accept header in the request.
    """
    logger = logging.getLogger(__name__)
    if 'volume_id' not in request.match_info:
        return response.status_bad_request('volume_id is required')
    if 'bucket_id' not in request.match_info:
        return response.status_bad_request('bucket_id is required')
    volume_id = request.match_info['volume_id']
    bucket_name = request.match_info['bucket_id']
    s3 = await request.app[HEA_DB].get_client(request, 's3', volume_id)
    loop = asyncio.get_running_loop()
    try:
        logger.debug('Getting all folders from bucket %s', bucket_name)
        response_ = await loop.run_in_executor(None, partial(s3.list_objects_v2, Bucket=bucket_name))
        folders = []
        if response_['KeyCount'] > 0:
            for obj in response_['Contents']:
                key = obj['Key']
                if is_folder(key):
                    encoded_key = encode_key(key)
                    logger.debug('Found folder %s in bucket %s', key[:-1], bucket_name)
                    folder = _get_folder(bucket_name, obj, key, encoded_key, request)
                    folders.append(folder.to_dict())
        return await response.get_all(request, folders)
    except ClientError as e:
        return _handle_client_error(e)


async def get_all_files(request: Request) -> web.Response:
    """
    Gets all files in a bucket. The volume id must be in the volume_id entry of the request's
    match_info dictionary. The bucket id must be in the bucket_id entry of the request's match_info dictionary.

    :param request: the HTTP request (required).
    :return: the HTTP response with a 200 status code if the bucket exists and a Collection+JSON document in the body
    containing any heaobject.data.AWSS3FileObject objects, 403 if access was denied, or 500 if an internal error occurred. The
    body's format depends on the Accept header in the request.
    """
    logger = logging.getLogger(__name__)
    if 'volume_id' not in request.match_info:
        return response.status_bad_request('volume_id is required')
    if 'bucket_id' not in request.match_info:
        return response.status_bad_request('bucket_id is required')
    volume_id = request.match_info['volume_id']
    bucket_name = request.match_info['bucket_id']
    s3 = await request.app[HEA_DB].get_client(request, 's3', volume_id)
    loop = asyncio.get_running_loop()
    try:
        logger.debug('Getting all files from bucket %s', bucket_name)
        response_ = await loop.run_in_executor(None, partial(s3.list_objects_v2, Bucket=bucket_name))
        files = []
        if response_['KeyCount'] > 0:
            for obj in response_['Contents']:
                key = obj['Key']
                if not is_folder(key):
                    encoded_key = encode_key(key)
                    logger.debug('Found file %s in bucket %s', key, bucket_name)
                    display_name = key.split('/')[-1]
                    file = _get_file(bucket_name, obj, display_name, key, encoded_key, request)
                    files.append(file.to_dict())
        return await response.get_all(request, files)
    except ClientError as e:
        return _handle_client_error(e)


async def get_folder_by_name(request: Request) -> web.Response:
    """
    Gets the requested folder. The volume id must be in the volume_id entry of the request's match_info dictionary.
    The bucket id must be in the bucket_id entry of the request's match_info dictionary. The folder name must be in the
    name entry of the request's match_info dictionary.

    :param request: the HTTP request (required).
    :return: the HTTP response with a 200 status code if the bucket exists and the heaobject.folder.AWSS3Folder in the body,
    403 if access was denied, 404 if no such folder was found, or 500 if an internal error occurred. The body's format
    depends on the Accept header in the request.
    """
    return await get_folder(request)


async def get_file_by_name(request: Request) -> web.Response:
    """
    Gets the requested file. The volume id must be in the volume_id entry of the request's match_info dictionary.
    The bucket id must be in the bucket_id entry of the request's match_info dictionary. The file name must be in the
    name entry of the request's match_info dictionary.

    :param request: the HTTP request (required).
    :return: the HTTP response with a 200 status code if the bucket exists and the heaobject.data.AWSS3FileObject in the body,
    403 if access was denied, 404 if no such file was found, or 500 if an internal error occurred. The body's format
    depends on the Accept header in the request.
    """
    return await get_file(request)


async def get_items(request: Request) -> web.Response:
    """
    Gets the requested folder items. The volume id must be in the volume_id entry of the request's match_info dictionary.
    The bucket id must be in the bucket_id entry of the request's match_info dictionary. The folder id must be in the
    folder_id entry of the request's match_info dictionary.

    :param request: the HTTP request (required).
    :return: the HTTP response with a 200 status code if the bucket exists and a list of heaobject.folder.AWSS3Item objects
    in the body, 403 if access was denied, or 500 if an internal error occurred. The body's format depends on the
    Accept header in the request.
    """

    logger = logging.getLogger(__name__)

    if 'volume_id' not in request.match_info:
        return response.status_bad_request('volume_id is required')
    if 'bucket_id' not in request.match_info:
        return response.status_bad_request('bucket_id is required')
    if 'folder_id' not in request.match_info:
        return response.status_bad_request('folder_id is required')
    volume_id = request.match_info['volume_id']
    bucket_name = request.match_info['bucket_id']
    folder_id_ = request.match_info['folder_id']

    s3 = await request.app[HEA_DB].get_client(request, 's3', volume_id)
    folder_id = _decode_folder(folder_id_)
    loop = asyncio.get_running_loop()
    try:
        if folder_id is None:
            # We couldn't decode the folder_id, and we need to check if the user can access the bucket in order to
            # decide which HTTP status code to respond with (Forbidden vs Not Found).
            return await _return_bucket_status_or_not_found(bucket_name, loop, s3)
        logger.debug('Getting all folders in item %s in bucket %s', folder_id, bucket_name)
        response_ = await loop.run_in_executor(None, partial(s3.list_objects_v2, Bucket=bucket_name, Prefix=folder_id))
        folders: Dict[str, AWSS3Item] = {}
        if response_['KeyCount'] > 0:
            for obj in response_['Contents']:
                id_ = obj['Key']
                id__ = id_.removeprefix(folder_id)
                try:
                    if id__ == '':  # The folder
                        continue
                    actual_id = id__[:id__.index('/') + 1]  # A folder
                    is_folder_ = True
                    display_name = actual_id[:-1]
                except ValueError:
                    actual_id = id__  # Not a folder
                    is_folder_ = False
                    display_name = actual_id
                id_encoded = encode_key(folder_id + actual_id)
                logger.debug('Found item %s in bucket %s', actual_id, bucket_name)
                item = AWSS3Item()
                item.id = id_encoded
                item.name = id_encoded
                item.display_name = display_name
                item.modified = obj['LastModified']
                item.created = obj['LastModified']
                item.owner = request.headers.get(SUB, NONE_USER)
                item.actual_object_id = id_encoded
                item.folder_id = folder_id_
                item.storage_class = S3StorageClass[obj['StorageClass']]
                item.set_s3_uri_from_bucket_and_key(bucket_name, id_)
                item.source = AWS_S3
                if is_folder_:
                    item.actual_object_uri = str(
                        URL('/volumes') / volume_id / 'buckets' / bucket_name / 'awss3folders' / id_encoded)
                    item.actual_object_type_name = AWSS3Folder.get_type_name()
                else:
                    item.actual_object_uri = str(
                        URL('/volumes') / volume_id / 'buckets' / bucket_name / 'awss3files' / id_encoded)
                    item.actual_object_type_name = AWSS3FileObject.get_type_name()
                    item.size = obj['Size']
                if actual_id in folders:
                    item_ = folders[actual_id]
                    if item_.modified is not None and item.modified is not None:
                        item_.modified = max(item_.modified, item.modified)
                    elif item.modified is not None:
                        item_.modified = item.modified
                else:
                    folders[actual_id] = item
            return await response.get_all(request, list(i.to_dict() for i in folders.values()))
        return await response.get_all(request, [])
    except ClientError as e:
        return _handle_client_error(e)


async def has_file(request: Request) -> Response:
    """
    Checks for the existence of the requested file object. The volume id must be in the volume_id entry of the
    request's match_info dictionary. The bucket id must be in the bucket_id entry of the request's match_info
    dictionary. The file id must be in the id entry of the request's match_info dictionary.

    :param request: the HTTP request (required).
    :return: the HTTP response with a 200 status code if the file exists, 403 if access was denied, or 500 if an
    internal error occurred.
    """
    logger = logging.getLogger(__name__)

    if 'volume_id' not in request.match_info:
        return response.status_bad_request('volume_id is required')
    if 'bucket_id' not in request.match_info:
        return response.status_bad_request('bucket_id is required')
    if 'id' not in request.match_info:
        return response.status_bad_request('id is required')

    volume_id = request.match_info['volume_id']
    bucket_name = request.match_info['bucket_id']

    s3 = await request.app[HEA_DB].get_client(request, 's3', volume_id)

    try:
        file_id: Optional[str] = decode_key(request.match_info['id'])
        if is_folder(file_id):
            file_id = None
    except KeyDecodeException:
        # Let the bucket query happen so that we consistently return Forbidden if the user lacks permissions
        # for the bucket.
        file_id = None
    loop = asyncio.get_running_loop()
    try:
        if file_id is None:
            # We couldn't decode the file_id, and we need to check if the user can access the bucket in order to
            # decide which HTTP status code to respond with (Forbidden vs Not Found).
            await loop.run_in_executor(None, partial(s3.head_bucket, Bucket=bucket_name))
            return response.status_not_found()
        logger.debug('Checking if file %s in bucket %s exists', file_id, bucket_name)
        response_ = await loop.run_in_executor(None, partial(s3.list_objects_v2, Bucket=bucket_name, Prefix=file_id,
                                                             MaxKeys=1))
        if response_['KeyCount'] > 0:
            return response.status_ok()
        return await response.get(request, None)
    except ClientError as e:
        return _handle_client_error(e)
    except KeyDecodeException:
        return response.status_not_found()


async def has_item(request: Request) -> web.Response:
    """
    Checks for the existence of the requested folder item. The volume id must be in the volume_id entry of the
    request's match_info dictionary. The bucket id must be in the bucket_id entry of the request's match_info
    dictionary. The folder id must be in the folder_id entry of the request's match_info dictionary. The item id must
    be in the id entry of the request's match_info dictionary.

    :param request: the HTTP request (required).
    :return: the HTTP response with a 200 status code if the item exists, 403 if access was denied, or 500 if an
    internal error occurred.
    """
    logger = logging.getLogger(__name__)

    if 'volume_id' not in request.match_info:
        return response.status_bad_request('volume_id is required')
    if 'bucket_id' not in request.match_info:
        return response.status_bad_request('bucket_id is required')
    if 'folder_id' not in request.match_info:
        return response.status_bad_request('folder_id is required')
    if 'id' not in request.match_info:
        return response.status_bad_request('id is required')

    volume_id = request.match_info['volume_id']
    folder_id_ = request.match_info['folder_id']
    bucket_name = request.match_info['bucket_id']

    s3 = await request.app[HEA_DB].get_client(request, 's3', volume_id)

    loop = asyncio.get_running_loop()

    if folder_id_ == ROOT_FOLDER.id:
        folder_id = ''
    else:
        try:
            folder_id = decode_key(folder_id_)
            if not is_folder(folder_id):
                folder_id = None
        except KeyDecodeException:
            # Let the bucket query happen so that we consistently return Forbidden if the user lacks permissions
            # for the bucket.
            folder_id = None
    try:
        if folder_id is None:
            # We couldn't decode the folder_id, and we need to check if the user can access the bucket in order to
            # decide which HTTP status code to respond with (Forbidden vs Not Found).
            await loop.run_in_executor(None, partial(s3.head_bucket, Bucket=bucket_name))
            return response.status_not_found()
        item_id = decode_key(request.match_info['id'])
        if item_id.startswith(folder_id):
            item_id_ = item_id.removeprefix(folder_id)
            if len(item_id_) > 1 and '/' in item_id_[:-1]:
                return response.status_not_found()
        else:
            return response.status_not_found()
        logger.debug('Checking if item %s in folder %s in bucket %s exists', item_id, folder_id, bucket_name)
        response_ = await loop.run_in_executor(None, partial(s3.list_objects_v2, Bucket=bucket_name, Prefix=item_id,
                                                             MaxKeys=1))
        if response_['KeyCount'] > 0:
            return response.status_ok()
        return await response.get(request, None)
    except ClientError as e:
        return _handle_client_error(e)
    except KeyDecodeException:
        return response.status_not_found()


async def get_item(request: Request) -> web.Response:
    """
    Gets the requested folder item. The volume id must be in the volume_id entry of the request's match_info dictionary.
    The bucket id must be in the bucket_id entry of the request's match_info dictionary. The folder id must be in the
    folder_id entry of the request's match_info dictionary. The item id must be in the id entry of the request's
    match_info dictionary.

    :param request: the HTTP request (required).
    :return: the HTTP response with a 200 status code if the bucket exists and the heaobject.folder.AWSS3Item object in the
    body, 403 if access was denied, or 500 if an internal error occurred. The body's format depends on the Accept
    header in the request.
    """
    logger = logging.getLogger(__name__)

    if 'volume_id' not in request.match_info:
        return response.status_bad_request('volume_id is required')
    if 'bucket_id' not in request.match_info:
        return response.status_bad_request('bucket_id is required')
    if 'folder_id' not in request.match_info:
        return response.status_bad_request('folder_id is required')
    if 'id' not in request.match_info:
        return response.status_bad_request('id is required')

    volume_id = request.match_info['volume_id']
    folder_id_ = request.match_info['folder_id']
    bucket_name = request.match_info['bucket_id']

    decoded_folder_key, decoded_key, folder_or_item_not_found = await check_folder_and_object_keys(folder_id_, request)

    s3 = await request.app[HEA_DB].get_client(request, 's3', volume_id)

    loop = asyncio.get_running_loop()

    if folder_or_item_not_found:
        return await _return_bucket_status_or_not_found(bucket_name, loop, s3)

    try:
        logger.debug('Getting item %s in folder %s in bucket %s', decoded_key, decoded_folder_key, bucket_name)
        response_ = await loop.run_in_executor(None, partial(s3.list_objects_v2, Bucket=bucket_name, Prefix=decoded_key,
                                                             MaxKeys=1))
        if response_['KeyCount'] > 0:
            for obj in response_['Contents']:
                id_ = obj['Key']
                is_folder_ = is_folder(id_)
                id_encoded = encode_key(id_)
                if is_folder_:
                    display_name = id_[_second_to_last(id_, '/') + 1:][:-1]
                else:
                    display_name = id_[id_.rfind('/') + 1:]
                logger.debug('Found item %s in bucket %s', id_, bucket_name)

                item = AWSS3Item()
                item.id = id_encoded
                item.name = id_encoded
                item.display_name = display_name
                item.modified = obj['LastModified']
                item.created = obj['LastModified']
                item.owner = request.headers.get(SUB, NONE_USER)
                item.folder_id = folder_id_
                item.actual_object_id = id_encoded
                item.storage_class = S3StorageClass[obj['StorageClass']]
                item.set_s3_uri_from_bucket_and_key(bucket_name, id_)
                item.source = AWS_S3
                if is_folder_:
                    item.actual_object_uri = str(
                        URL('/volumes') / volume_id / 'buckets' / bucket_name / 'awss3folders' / id_encoded)
                    item.actual_object_type_name = AWSS3Folder.get_type_name()
                else:
                    item.actual_object_uri = str(
                        URL('/volumes') / volume_id / 'buckets' / bucket_name / 'awss3files' / id_encoded)
                    item.actual_object_type_name = AWSS3FileObject.get_type_name()
                    item.size = obj['Size']

                return await response.get(request, item.to_dict())
        return await response.get(request, None)
    except ClientError as e:
        return _handle_client_error(e)


async def check_folder_and_object_keys(folder_id_: Optional[str], request: Request):
    folder_or_item_not_found = False
    decoded_folder_key = _decode_folder(folder_id_)
    if decoded_folder_key is None:
        folder_or_item_not_found = True
    try:
        decoded_key = decode_key(request.match_info['id'])
    except KeyDecodeException:
        folder_or_item_not_found = True
    if not _key_in_folder(decoded_key, decoded_folder_key):
        folder_or_item_not_found = True
    return decoded_folder_key, decoded_key, folder_or_item_not_found


class ObjectType(EnumAutoName):
    """
    Divides the world of AWS S3 bucket objects into files and folders.
    """
    FILE = auto()
    FOLDER = auto()
    ANY = auto()


async def delete_folder(request: Request, recursive=False) -> Response:
    """
    Deletes the requested folder and optionally all contents. The volume id must be in the volume_id entry of the
    request's match_info dictionary. The bucket id must be in the bucket_id entry of the request's match_info
    dictionary. The folder id must be in the id entry of the request's match_info dictionary.

    :param request: the aiohttp Request (required).
    :param recursive: if True, this function will delete the folder and all of its contents, otherwise it will return
    a 400 error if the folder is not empty.
    :return: the HTTP response with a 204 status code if the folder was successfully deleted, 403 if access was denied,
    404 if the folder was not found, or 500 if an internal error occurred.
    """
    # https://izziswift.com/amazon-s3-boto-how-to-delete-folder/
    return await delete_object(request, object_type=ObjectType.FOLDER, recursive=recursive)


async def delete_file(request: Request) -> Response:
    """
    Deletes the requested file. The volume id must be in the volume_id entry of the
    request's match_info dictionary. The bucket id must be in the bucket_id entry of the request's match_info
    dictionary. The file id must be in the id entry of the request's match_info dictionary.

    :param request: the aiohttp Request (required).
    :param recursive: if True, this function will delete the file.
    :return: the HTTP response with a 204 status code if the file was successfully deleted, 403 if access was denied,
    404 if the file was not found, or 500 if an internal error occurred.
    """
    return await delete_object(request, object_type=ObjectType.FILE)


async def delete_object(request: Request, object_type: Optional[ObjectType] = None, recursive=False) -> Response:
    """
    Deletes a single object. The volume id must be in the volume_id entry of the request's match_info dictionary. The
    bucket id must be in the bucket_id entry of the request's match_info dictionary. The item id must be in the id
    entry of the request's match_info dictionary. An optional folder id may be passed in the folder_id entry of the
    request's match_info_dictinary.

    :param request: the aiohttp Request (required).
    :param object_type: only delete the requested object only if it is a file or only if it is a folder. Pass in
    ObjectType.ANY or None (the default) to signify that it does not matter.
    :param recursive: if True, and the object is a folder, this function will delete the folder and all of its
    contents, otherwise it will return a 400 error if the folder is not empty. If the object to delete is not a folder,
    this flag will have no effect.
    :return: the HTTP response with a 204 status code if the item was successfully deleted, 403 if access was denied,
    404 if the item was not found, or 500 if an internal error occurred.
    """
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.delete_object
    # TODO: bucket.object_versions.filter(Prefix="myprefix/").delete()     add versioning option like in the delete bucket?
    if 'volume_id' not in request.match_info:
        return response.status_bad_request('volume_id is required')
    if 'bucket_id' not in request.match_info:
        return response.status_bad_request('bucket_id is required')
    if 'id' not in request.match_info:
        return response.status_bad_request('id is required')

    bucket_name = request.match_info['bucket_id']
    encoded_key = request.match_info['id']
    volume_id = request.match_info['volume_id']
    encoded_folder_key = request.match_info.get('folder_id', None)
    try:
        key: Optional[str] = decode_key(encoded_key)
        if object_type == ObjectType.FOLDER and not is_folder(key):
            key = None
        elif object_type == ObjectType.FILE and is_folder(key):
            key = None
    except KeyDecodeException:
        key = None
    s3_client = await request.app[HEA_DB].get_client(request, 's3', volume_id)
    loop = asyncio.get_running_loop()
    try:
        if key is None:
            return await _return_bucket_status_or_not_found(bucket_name, loop, s3_client)
        if encoded_folder_key is not None:
            folder_key = _decode_folder(encoded_folder_key)
            if folder_key is None or not _key_in_folder(key, folder_key):
                return await _return_bucket_status_or_not_found(bucket_name, loop, s3_client)

        response_ = await loop.run_in_executor(None, partial(s3_client.list_objects_v2, Bucket=bucket_name,
                                                             Prefix=key))
        # A key count of 0 means the folder doesn't exist. A key count of 1 just has the folder itself. A key count > 1
        # means the folder has contents.
        key_count = response_['KeyCount']
        if key_count == 0:
            return await _return_bucket_status_or_not_found(bucket_name, loop, s3_client)
        if is_folder(key):
            if not recursive and key_count > 1:
                return response.status_bad_request(f'The folder {encoded_key} is not empty')
            for object_f in response_['Contents']:
                s3_client.delete_object(Bucket=bucket_name, Key=object_f['Key'])
        else:
            s3_client.delete_object(Bucket=bucket_name, Key=key)
        return await response.delete(True)
    except ClientError as e:
        return _handle_client_error(e)


def download_archive_object(length=1):
    """

    """


def get_archive():
    """
    Don't think it is worth it to have a temporary view of data, expensive and very slow
    """


async def account_opener(request: Request, volume_id: str) -> Response:
    """
    Gets choices for opening an account object.

    :param request: the HTTP request. Required. If an Accepts header is provided, MIME types that do not support links
    will be ignored.
    :param volume_id: the id string of the volume containing the requested HEA object. If None, the root volume is
    assumed.
    :return: a Response object with status code 300, and a body containing the HEA desktop object and links
    representing possible choices for opening the HEA desktop object; or Not Found.
    """
    result = await _get_account(request, volume_id)
    if result is None:
        return response.status_not_found()
    return await response.get_multiple_choices(request, result)


async def account_opener_by_id(request: web.Request) -> web.Response:
    """
    Gets choices for opening an account object, using the 'id' value in the match_info attribute of the request.

    :param request: the HTTP request, must contain an id value in its match_info attribute. Required. If an Accepts
    header is provided, MIME types that do not support links will be ignored.
    :return: a Response object with status code 300, and a body containing the HEA desktop object and links
    representing possible choices for opening the HEA desktop object; or Not Found.
    """
    result = await get_account_by_id(request)
    if result is None:
        return response.status_not_found()
    return await response.get_multiple_choices(request, result)


async def generate_presigned_url(request: Request, volume_id: str, path_name: str, expiration: int = 3600):
    """Generate a presigned URL to share an S3 object

    :param request: the aiohttp Request (required).
    :param volume_id: the id string of the volume representing the user's AWS account.
    :param path_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.

    https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-presigned-urls.html
    """
    # Generate a presigned URL for the S3 object
    try:
        s3_client = await request.app[HEA_DB].get_client(request, 's3', volume_id)
        loop = asyncio.get_running_loop()
        bucket_name = path_name.partition("/")[0]
        folder_name = path_name.partition("/")[2]
        response = await loop.run_in_executor(None, partial(s3_client.generate_presigned_url, 'get_object',
                                                            Params={'Bucket': bucket_name, 'Key': folder_name},
                                                            ExpiresIn=expiration))
        logging.info(response)
    except ClientError as e:
        logging.error(e)
        return None
    # The response contains the presigned URL
    return response


async def get_object_content(request: Request) -> web.StreamResponse:
    """
    preview object in object explorer
    :param request: the aiohttp Request (required).
    """
    logger = logging.getLogger(__name__)
    if 'volume_id' not in request.match_info:
        return response.status_bad_request('volume_id is required')
    if 'bucket_id' not in request.match_info:
        return response.status_bad_request('bucket_id is required')
    if 'id' not in request.match_info:
        return response.status_bad_request('id is required')
    volume_id = request.match_info['volume_id']
    bucket_name = request.match_info['bucket_id']
    file_name = request.match_info['id']

    s3_client = await request.app[HEA_DB].get_client(request, 's3', volume_id)

    try:
        key: Optional[str] = decode_key(file_name)
        if is_folder(key):
            key = None
    except KeyDecodeException:
        # Let the bucket query happen so that we consistently return Forbidden if the user lacks permissions
        # for the bucket.
        key = None

    try:
        loop = asyncio.get_running_loop()
        if key is None:
            # We couldn't decode the file_id, and we need to check if the user can access the bucket in order to
            # decide which HTTP status code to respond with (Forbidden vs Not Found).
            await loop.run_in_executor(None, partial(s3_client.head_bucket, Bucket=bucket_name))
            return response.status_not_found()
        resp = await loop.run_in_executor(None, partial(s3_client.head_object, Bucket=bucket_name, Key=key))
        logger.debug('Downloading object %s', resp)
        response_ = web.StreamResponse(status=200, reason='OK')
        mime_type = guess_mime_type(key)
        if mime_type is None:
            mime_type = 'application/octet-stream'
        response_.content_type = mime_type
        response_.last_modified = resp['LastModified']
        response_.content_length = resp['ContentLength']
        response_.etag = resp['ETag'].strip('"')
        await response_.prepare(request)
        fileobj = StreamResponseFileLikeWrapper(response_)
        fileobj.initialize()
        await loop.run_in_executor(None, s3_client.download_fileobj, bucket_name, key, fileobj)
        await fileobj.close()
        await response_.write_eof()
        logger.debug('Body length is %d bytes', response_.body_length)
        return response_
    except ClientError as e:
        logging.error(e)
        return response.status_not_found()


async def get_bucket(request: Request) -> web.Response:
    """
    List a single bucket's attributes

    :param request: the aiohttp Request (required).
    :return:  return the single bucket object requested or HTTP Error Response
    """
    if 'volume_id' not in request.match_info:
        raise ValueError('volume_id is required')
    if'id' not in request.match_info and 'bucket_name' not in request.match_info:
        raise ValueError('id or bucket_name is required')
    volume_id = request.match_info['volume_id']
    bucket_id = request.match_info.get('id')
    bucket_name = request.match_info.get('bucket_name')
    s3_client = await request.app[HEA_DB].get_client(request, 's3', volume_id)
    s3_resource = await request.app[HEA_DB].get_resource(request, 's3', volume_id)

    try:
        bucket_result = await _get_bucket(volume_id=volume_id, s3_resource=s3_resource, s3_client=s3_client,
                                          bucket_name=bucket_name, bucket_id=bucket_id, )
        if type(bucket_result) is AWSBucket:
            return await response.get(request=request, data=bucket_result.to_dict())
        return await response.get(request, data=None)
    except ClientError as e:
        return _handle_client_error(e)


async def has_bucket(request: Request) -> web.Response:
    """
    Checks for the existence of the requested bucket. The volume id must be in the volume_id entry of the
    request's match_info dictionary. The bucket id must be in the id entry of the request's match_info
    dictionary.

    :param request: the HTTP request (required).
    :return: the HTTP response with a 200 status code if the bucket exists, 403 if access was denied, or 500 if an
    internal error occurred.
    """
    if 'volume_id' not in request.match_info:
        return response.status_bad_request('volume_id is required')
    if 'id' not in request.match_info and 'bucket_id' not in request.match_info:
        return response.status_bad_request('id or bucket_id must be provided')
    volume_id = request.match_info['volume_id']
    bucket_id = request.match_info.get('id', request.match_info.get('bucket_id', None))
    s3_client = await request.app[HEA_DB].get_client(request, 's3', volume_id)
    s3_resource = await request.app[HEA_DB].get_resource(request, 's3', volume_id)

    try:
        bucket_result = await _get_bucket(volume_id=volume_id, s3_resource=s3_resource, s3_client=s3_client,
                                          bucket_id=bucket_id)
        if type(bucket_result) is AWSBucket:
            return response.status_ok()
        else:
            return response.status_not_found()
    except ClientError as e:
        return _handle_client_error(e)


async def get_all_buckets(request: web.Request) -> web.Response:
    """
    List available buckets by name

    :param request: the aiohttp Request (required).
    :return: An HTTP response with a list of available buckets.
    """

    try:
        volume_id = request.match_info.get("volume_id", None)
        if not volume_id:
            return web.HTTPBadRequest(body="volume_id is required")
        s3_client = await request.app[HEA_DB].get_client(request, 's3', volume_id)
        s3_resource = await request.app[HEA_DB].get_resource(request, 's3', volume_id)

        resp = s3_client.list_buckets()
        async_bucket_list = []
        for bucket in resp['Buckets']:
            bucket_ = _get_bucket(volume_id=volume_id, bucket_name=bucket["Name"],
                                  s3_client=s3_client, s3_resource=s3_resource,
                                  creation_date=bucket['CreationDate'])
            if bucket_ is not None:
                async_bucket_list.append(bucket_)

        buck_list = await asyncio.gather(*async_bucket_list)
    except ClientError as e:
        logging.error(e)
        return response.status_bad_request()
    bucket_dict_list = [buck.to_dict() for buck in buck_list if buck is not None]

    return await response.get_all(request, bucket_dict_list)


# async def get_all(request: Request, by_dir_level: bool = False):
#     """
#     List all objects in  a folder or entire bucket.
#     :param by_dir_level: (str) used to switch off recursive nature get all object/folder within level
#     :param request: the aiohttp Request (required).
#     """
#     bucket_name = request.match_info.get('bucket_name', None)
#     volume_id = request.match_info.get("volume_id", None)
#     if not volume_id:
#         return web.HTTPBadRequest(body="volume_id is required")
#     if not bucket_name:
#         return web.HTTPBadRequest(body="bucket_name is required")
#
#     query_keys = {'max_keys': 500, 'page_size': 50}
#     if request.rel_url and request.rel_url.query:
#         for key in request.rel_url.query:
#             query_keys[key] = request.rel_url.query[key]
#
#     try:
#         object_list = []
#         pag_request_params = {}
#         s3_client = await request.app[HEA_DB].get_client(request, 's3', volume_id)
#         paginator = s3_client.get_paginator('list_objects_v2')
#
#         pag_request_params['Bucket'] = bucket_name
#         pag_request_params['PaginationConfig'] = {'MaxItems': query_keys['max_keys'],
#                                                   'PageSize': query_keys['page_size']}
#
#         if 'folder_name' in query_keys and query_keys['folder_name']:
#             folder_name = query_keys['folder_name']
#             pag_request_params['Prefix'] = folder_name if is_folder(folder_name) else folder_name + '/'
#             pag_request_params['Delimiter'] = '/'
#         elif by_dir_level:
#             pag_request_params['Delimiter'] = '/'
#
#         if 'start_after_key' in query_keys:
#             pag_request_params['StartAfter'] = query_keys['start_after_key']
#
#         if 'starting_token' in query_keys:
#             pag_request_params['PaginationConfig']['StartingToken'] = query_keys['starting_token']
#
#         pag_iter = paginator.paginate(**pag_request_params)
#         # response = s3_client.list_objects_v2(Bucket=bucket_name, MaxKeys=max_keys)
#
#         results = []
#         for page in pag_iter:
#             object_list = []
#             folder_list = []
#             next_token = page['NextContinuationToken'] if page['IsTruncated'] else None
#             current_token = page['ContinuationToken'] if 'ContinuationToken' in page else None
#             content = page.get('Contents', [])
#             common_prefixes = page.get('CommonPrefixes', {})
#             for pre in common_prefixes:
#                 folder: str = pre['Prefix']
#                 level = len(page['Prefix'].split('/'))
#                 if level == 1:
#                     folder_list.append({'type': 'project', 'folder': folder})
#                 elif level == 2:
#                     folder_list.append({'type': 'analysis', 'folder': folder})
#                 else:
#                     folder_list.append({'type': 'general', 'folder': folder})
#
#             start_after_key = content[len(content) - 1]['Key'] if len(content) > 0 else None
#             for val in content:
#                 object_list.append(val)
#
#             results.append({'NextContinuationToken': next_token,
#                             'ContinuationToken': current_token,
#                             'StartAfter': start_after_key,
#                             'Objects': object_list,
#                             'Folders': folder_list
#                             })
#     except ClientError as e:
#         logging.error(e)
#         return web.HTTPNotFound
#     return await response.get(request, results)


async def get_all_storages(request: web.Request) -> web.Response:
    """
    List available storage classes by name

    :param request: the aiohttp Request (required).
    :return: (list) list of available storage classes
    """

    logger = logging.getLogger(__name__)
    volume_id = request.match_info.get("volume_id", None)
    bucket_id = request.match_info.get('id', None)
    bucket_name = request.match_info.get('bucket_name', None)
    if not volume_id:
        return web.HTTPBadRequest(body="volume_id is required")
    s3_client = await request.app[HEA_DB].get_client(request, 's3', volume_id)
    s3_resource = await request.app[HEA_DB].get_resource(request, 's3', volume_id)

    try:
        resp = []
        if bucket_id or bucket_name:
            bucket_result = await _get_bucket(volume_id=volume_id, s3_resource=s3_resource, s3_client=s3_client,
                                              bucket_name=bucket_name, bucket_id=bucket_id)
            if bucket_result is not None and type(bucket_result) is AWSBucket:
                resp.append({'Name': bucket_result.name})
        else:
            resp = s3_client.list_buckets()['Buckets']

        groups = defaultdict(list)
        for bucket in resp:
            s3_bucket = s3_resource.Bucket(bucket['Name'])
            if s3_bucket is not None:
                for obj in s3_bucket.objects.all():
                    if obj.storage_class is not None:
                        groups[obj.storage_class].append(obj)

        async_storage_class_list = []
        for item in groups.items():
            item_key = item.__getitem__(0)
            item_values = item.__getitem__(1)
            storage_class = _get_storage_class(volume_id=volume_id, item_key=item_key, item_values=item_values)
            if storage_class is not None:
                async_storage_class_list.append(storage_class)

        storage_class_list = await asyncio.gather(*async_storage_class_list)

    except ClientError as e:
        logging.error(e)
        return response.status_bad_request()

    storage_class_dict_list = [storage.to_dict() for storage in storage_class_list if storage is not None]
    return await response.get_all(request, storage_class_dict_list)


async def post_bucket(request: Request):
    """
    Create an S3 bucket in a specified region, checks that it is the first, if already exists errors are thrown
    If a region is not specified, the bucket is created in the S3 default region (us-east-1).

    :param request: the aiohttp Request (required).
    :param volume_id: the id string of the volume representing the user's AWS account.
    """
    logger = logging.getLogger(__name__)
    volume_id = request.match_info.get('volume_id', None)
    if not volume_id:
        return web.HTTPBadRequest(body="volume_id is required")
    try:
        b = await new_heaobject_from_type(request=request, type_=AWSBucket)
        if not b:
            return web.HTTPBadRequest(body="Post body is not an HEAObject AWSBUCKET")
        if not b.name:
            return web.HTTPBadRequest(body="Bucket name is required")
    except DeserializeException as e:
        return web.HTTPBadRequest(body=str(e))

    s3_client: S3Client = await request.app[HEA_DB].get_client(request, 's3', volume_id)
    try:
        s3_client.head_bucket(Bucket=b.name)  # check if bucket exists, if not throws an exception
    except ClientError as e:
        try:
            # todo this is a privileged actions need to check if authorized
            error_code = e.response['Error']['Code']

            if error_code == '404':  # bucket doesn't exist
                create_bucket_params: Dict[str, Any] = {'Bucket': b.name}
                put_bucket_policy_params = {
                    'BlockPublicAcls': True,
                    'IgnorePublicAcls': True,
                    'BlockPublicPolicy': True,
                    'RestrictPublicBuckets': True
                }
                if b.region:
                    create_bucket_params['CreateBucketConfiguration'] = {'LocationConstraint': b.region}
                if b.locked:
                    create_bucket_params['ObjectLockEnabledForBucket'] = True

                loop = asyncio.get_running_loop()

                await loop.run_in_executor(None, partial(s3_client.create_bucket, **create_bucket_params))
                # make private bucket
                await loop.run_in_executor(None, partial(s3_client.put_public_access_block, Bucket=b.name,
                                                         PublicAccessBlockConfiguration=put_bucket_policy_params))

                await _put_bucket_encryption(b, loop, s3_client)
                # todo this is a privileged action need to check if authorized ( may only be performed by bucket owner)

                await _put_bucket_versioning(bucket_name=b.name, s3_client=s3_client, is_versioned=b.versioned)

                await _put_bucket_tags(request=request, volume_id=volume_id,
                                       bucket_name=b.name, new_tags=b.tags)

            elif error_code == '403':  # already exists
                logger.exception("bucket exists, no permission to access")
                return web.HTTPBadRequest(body="bucket exists, no permission to access")
            else:
                logger.exception(str(e))
                return response.status_bad_request(str(e))
        except ClientError as e2:
            logger.error(e2.response)
            try:
                await loop.run_in_executor(None, partial(s3_client.head_bucket, Bucket=b.name))
                del_bucket_result = await loop.run_in_executor(None, partial(s3_client.delete_bucket, Bucket=b.name))
                logging.info(f"deleted failed bucket {b.name} details: \n{del_bucket_result}")
            except ClientError:  # bucket doesn't exist so no clean up needed
                pass
            return web.HTTPBadRequest(body="New bucket was NOT created")
        return await response.post(request, b.name, f'volumes/{volume_id}/buckets')


async def _put_bucket_encryption(b, loop, s3_client):
    if b.encrypted:
        try:
            SSECNF = 'ServerSideEncryptionConfigurationNotFoundError'
            await loop.run_in_executor(None, partial(s3_client.get_bucket_encryption, Bucket=b.name))
        except ClientError as e:
            if e.response['Error']['Code'] == SSECNF:
                config = \
                    {'Rules': [{'ApplyServerSideEncryptionByDefault':
                                    {'SSEAlgorithm': 'AES256'}, 'BucketKeyEnabled': False}]}
                await loop.run_in_executor(None, partial(s3_client.put_bucket_encryption, Bucket=b.name,
                                                         ServerSideEncryptionConfiguration=config))
            else:
                logging.error(e.response['Error']['Code'])
                raise e


async def _put_bucket_versioning(bucket_name: str, is_versioned: Optional[bool], s3_client: S3Client):
    """
    Use To change turn on or off bucket versioning settings. Note that if the Object Lock
    is turned on for the bucket you can't change these settings.

    :param bucket_name: The bucket name
    :param is_versioned: For toggling on or off the versioning
    :param s3_client: Pass the active client if exists (optional)
    :raises ClientError: if an error occurred setting version information.
    """
    logger = logging.getLogger(__name__)
    loop = asyncio.get_running_loop()
    vconfig = {
        'MFADelete': 'Disabled',
        'Status': 'Enabled' if is_versioned else 'Suspended',
    }
    vresp = await loop.run_in_executor(None, partial(s3_client.put_bucket_versioning, Bucket=bucket_name,
                                                     VersioningConfiguration=vconfig))
    logger.debug(vresp)


async def _put_bucket_tags(request: Request, volume_id: str, bucket_name: str,
                           new_tags: List[Tag]):
    """
    Creates or adds to a tag list for bucket

    :param request: the aiohttp Request (required).
    :param volume_id: the id string of the volume representing the user's AWS account.
    :param bucket_name: Bucket to create
    :param new_tags: new tags to be added tag list on specified bucket
    """
    if not new_tags:
        return web.HTTPNotModified()
    aws_new_tags = await _to_aws_tags(new_tags)

    if not bucket_name:
        return web.HTTPBadRequest(body="Bucket name is required")
    s3_resource = await request.app[HEA_DB].get_resource(request, 's3', volume_id)
    loop = asyncio.get_running_loop()
    bucket_tagging = await loop.run_in_executor(None, s3_resource.BucketTagging, bucket_name)
    tags = []

    try:
        tags = bucket_tagging.tag_set
    except ClientError as ce:
        if ce.response['Error']['Code'] != 'NoSuchTagSet':
            logging.error(ce)
            raise ce
    tags = tags + aws_new_tags
    # boto3 tagging.put only accepts dictionaries of Key Value pairs(Tags)
    bucket_tagging.put(Tagging={'TagSet': tags})


async def post_object(request: Request, item: AWSS3Item) -> web.Response:
    """
    Creates a new object in a bucket. The volume id must be in the volume_id entry of the request.match_info dictionary.
    The bucket id must be in the bucket_id entry of request.match_info. The folder id must be in the folder_id entry of
    request.match_info.

    :param request: the HTTP request (required).
    :param item: the heaobject.folder.AWSS3Item to create (required).
    :return: the HTTP response, with a 201 status code if successful with the URL to the new item in the Location
    header, 403 if access was denied, 404 if the volume or bucket could not be found, or 500 if an internal error
    occurred.
    """
    logger = logging.getLogger(__name__)
    if item.display_name is None:
        return response.status_bad_request("display_name is required")
    if 'volume_id' not in request.match_info:
        return response.status_bad_request('volume_id is required')
    if 'bucket_id' not in request.match_info:
        return response.status_bad_request('bucket_id is required')
    if 'folder_id' not in request.match_info:
        return response.status_bad_request('folder_id is required')
    if item is None:
        return response.status_bad_request('item is a required field')
    volume_id = request.match_info['volume_id']
    bucket_id = request.match_info['bucket_id']
    folder_id = request.match_info['folder_id']

    if item.folder_id is not None and folder_id != item.folder_id:
        return response.status_bad_request(
            f'folder_id in object was {item.folder_id} but folder_id in URL was {folder_id}')
    if folder_id is None:
        return response.status_bad_request('folder_id cannot be None')
    if item.folder_id is not None and item.folder_id != folder_id:
        return response.status_bad_request(
            f'Inconsistent folder_id in URL versus item: {folder_id} vs {item.folder_id}')
    if '/' in item.display_name:
        return response.status_bad_request(f"The item's display name may not have slashes in it")
    if folder_id == ROOT_FOLDER.id:
        item_folder_id = ''
    else:
        try:
            item_folder_id = decode_key(folder_id)
            if not is_folder(item_folder_id):
                item_folder_id = None
        except KeyDecodeException:
            item_folder_id = None

    s3_client = await request.app[HEA_DB].get_client(request, 's3', volume_id)
    loop = asyncio.get_running_loop()
    try:
        if item_folder_id is None:
            await loop.run_in_executor(None, partial(s3_client.head_bucket, Bucket=bucket_id))
            return response.status_not_found()
        item_name = f'{item_folder_id}{item.display_name}'
        if item.actual_object_type_name == AWSS3Folder.get_type_name():
            item_name += '/'
        elif item.actual_object_type_name == AWSS3FileObject.get_type_name():
            pass
        else:
            return response.status_bad_request(f'Unsupported actual_object_type_name {item.actual_object_type_name}')
        response_ = await loop.run_in_executor(None, partial(s3_client.head_object, Bucket=bucket_id,
                                                             Key=item_name))  # check if item exists, if not throws an exception
        logger.debug('Result of post_object: %s', response_)
        return response.status_bad_request(body=f"Item {item_name} already exists")
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == CLIENT_ERROR_404:  # folder doesn't exist
            await loop.run_in_executor(None, partial(s3_client.put_object, Bucket=bucket_id, Key=item_name))
            logger.info('Added folder %s', item_name)
            return await response.post(request, encode_key(item_name),
                                       f"volumes/{request.match_info['volume_id']}/buckets/{request.match_info['bucket_id']}/awss3folders/{folder_id}/items")
        elif error_code == CLIENT_ERROR_NO_SUCH_BUCKET:
            return response.status_not_found()
        else:
            return response.status_bad_request(str(e))


async def put_object_content(request: Request):
    """Upload a file to an S3 bucket, checks that it is the first, if already exists errors are thrown
    query params:
    file_path (str) path to file on local disk (required),
    path_name (str) path for object to be post on bucket (required),
    object_name (str) name of object to be post on bucket, if not provided name will be extracted from file_path (optional)

    :param request: the aiohttp Request (required).
    https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-uploading-files.html
    """
    logger = logging.getLogger(__name__)
    if 'volume_id' not in request.match_info:
        return response.status_bad_request("volume_id is required")
    if 'bucket_id' not in request.match_info:
        return response.status_bad_request("bucket_id is required")
    if 'id' not in request.match_info:
        return response.status_bad_request('id is required')
    volume_id = request.match_info['volume_id']
    bucket_name = request.match_info['bucket_id']
    file_name = request.match_info['id']

    s3_client = await request.app[HEA_DB].get_client(request, 's3', volume_id)
    loop = asyncio.get_running_loop()

    try:
        file_id: Optional[str] = decode_key(file_name)
        if is_folder(file_id):
            file_id = None
    except KeyDecodeException:
        # Let the bucket query happen so that we consistently return Forbidden if the user lacks permissions
        # for the bucket.
        file_id = None

    try:
        if file_id is None:
            # We couldn't decode the file_id, and we need to check if the user can access the bucket in order to
            # decide which HTTP status code to respond with (Forbidden vs Not Found).
            await loop.run_in_executor(None, partial(s3_client.head_bucket, Bucket=bucket_name))
            return response.status_not_found()
    except ClientError as e:
        return _handle_client_error(e)

    s3_client = await request.app[HEA_DB].get_client(request, 's3', volume_id)
    try:
        await loop.run_in_executor(None, partial(s3_client.head_object, Bucket=bucket_name, Key=file_id))
        fileobj = RequestFileLikeWrapper(request)
        done = False
        try:
            fileobj.initialize()
            from concurrent.futures import ThreadPoolExecutor
            upload_response = await loop.run_in_executor(None, s3_client.upload_fileobj, fileobj, bucket_name, file_id)
            fileobj.close()
            done = True
        except Exception as e:
            if not done:
                try:
                    fileobj.close()
                except:
                    pass
                done = True
                raise e

        logger.info(upload_response)
    except ClientError as e:
        return _handle_client_error(e)
    return response.status_no_content()


def post_object_archive():
    """
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html
    """


async def put_bucket(request: Request, volume_id: str, bucket_name: str, region: Optional[str] = None):
    """
    Create an S3 bucket in a specified region, if it doesn't exist an error will be thrown
    If a region is not specified, the bucket is created in the S3 default region (us-east-1).

    :param request: the aiohttp Request (required).
    :param volume_id: the id string of the volume representing the user's AWS account.
    :param bucket_name: Bucket to create
    :param region: String region to create bucket in, e.g., 'us-west-2'
    """
    logger = logging.getLogger(__name__)
    s3_client = await request.app[HEA_DB].get_client(request, 's3', volume_id)
    loop = asyncio.get_running_loop()
    try:
        await loop.run_in_executor(None, partial(s3_client.head_bucket,
                                                 Bucket=bucket_name))  # check if bucket exists, if not throws an exception
        if region is None:
            create_bucket_result = await loop.run_in_executor(None,
                                                              partial(s3_client.create_bucket, Bucket=bucket_name))
            logger.info(create_bucket_result)
            return web.HTTPCreated()
        else:
            create_bucket_result = await loop.run_in_executor(None, partial(s3_client.create_bucket, Bucket=bucket_name,
                                                                            CreateBucketConfiguration={
                                                                                'LocationConstraint': region}))
            logger.info(create_bucket_result)
            return web.HTTPCreated()
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == '404':
            logger.exception("bucket doesn't exist")
            return response.status_bad_request(body="bucket doesn't exist")
        elif error_code == '403':
            logger.exception("bucket exists, no permission to access")
            return response.status_bad_request(body="bucket exists, no permission to access")
        else:
            logger.exception("error updating bucket")
            return response.status_bad_request("error updating bucket")


# def put_object_archive():
#     """
#     https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html
#     """


# async def transfer_object_within_account(request: Request, volume_id: str, object_path, new_path):
#     """
#     same as copy_object, but also deletes the object
#
#     :param request: the aiohttp Request (required).
#     :param volume_id: the id string of the volume representing the user's AWS account.
#     :param object_path (str) gives the old location of the object, input as the bucket and key together
#     :param new_path: (str) gives the new location to put the object
#     """
#     await copy_object(request, volume_id, object_path, new_path)
#     await delete_object(request, volume_id, object_path)


# def transfer_object_between_account():
#     """
#     https://markgituma.medium.com/copy-s3-bucket-objects-across-separate-aws-accounts-programmatically-323862d857ed
#     """
#     # TODO: use update_bucket_policy to set up "source" bucket policy correctly
#     """
#     {
#     "Version": "2012-10-17",
#     "Id": "Policy1546558291129",
#     "Statement": [
#         {
#             "Sid": "Stmt1546558287955",
#             "Effect": "Allow",
#             "Principal": {
#                 "AWS": "arn:aws:iam::<AWS_IAM_USER>"
#             },
#             "Action": [
#               "s3:ListBucket",
#               "s3:GetObject"
#             ],
#             "Resource": "arn:aws:s3:::<SOURCE_BUCKET>/",
#             "Resource": "arn:aws:s3:::<SOURCE_BUCKET>/*"
#         }
#     ]
#     }
#     """
#     # TODO: use update_bucket_policy to set up aws "destination" bucket policy
#     """
#     {
#     "Version": "2012-10-17",
#     "Id": "Policy22222222222",
#     "Statement": [
#         {
#             "Sid": "Stmt22222222222",
#             "Effect": "Allow",
#             "Principal": {
#                 "AWS": [
#                   "arn:aws:iam::<AWS_IAM_DESTINATION_USER>",
#                   "arn:aws:iam::<AWS_IAM_LAMBDA_ROLE>:role/
#                 ]
#             },
#             "Action": [
#                 "s3:ListBucket",
#                 "s3:PutObject",
#                 "s3:PutObjectAcl"
#             ],
#             "Resource": "arn:aws:s3:::<DESTINATION_BUCKET>/",
#             "Resource": "arn:aws:s3:::<DESTINATION_BUCKET>/*"
#         }
#     ]
#     }
#     """
#     # TODO: code
#     source_client = boto3.client('s3', "SOURCE_AWS_ACCESS_KEY_ID", "SOURCE_AWS_SECRET_ACCESS_KEY")
#     source_response = source_client.get_object(Bucket="SOURCE_BUCKET", Key="OBJECT_KEY")
#     destination_client = boto3.client('s3', "DESTINATION_AWS_ACCESS_KEY_ID", "DESTINATION_AWS_SECRET_ACCESS_KEY")
#     destination_client.upload_fileobj(source_response['Body'], "DESTINATION_BUCKET",
#                                       "FOLDER_LOCATION_IN_DESTINATION_BUCKET")


# async def rename_object(request: Request, volume_id: str, object_path: str, new_name: str):
#     """
#     BOTO3, the copy and rename is the same
#     https://medium.com/plusteam/move-and-rename-objects-within-an-s3-bucket-using-boto-3-58b164790b78
#     https://stackoverflow.com/questions/47468148/how-to-copy-s3-object-from-one-bucket-to-another-using-python-boto3
#
#     :param request: the aiohttp Request (required).
#     :param volume_id: the id string of the volume representing the user's AWS account.
#     :param object_path: (str) path to object, includes both bucket and key values
#     :param new_name: (str) value to rename the object as, will only replace the name not the path. Use transfer object for that
#     """
#     # TODO: check if ACL stays the same and check existence
#     try:
#         s3_resource = await request.app[HEA_DB].get_resource(request, 's3', volume_id)
#         copy_source = {'Bucket': object_path.partition("/")[0], 'Key': object_path.partition("/")[2]}
#         bucket_name = object_path.partition("/")[0]
#         old_name = object_path.rpartition("/")[2]
#         s3_resource.meta.client.copy(copy_source, bucket_name,
#                                      object_path.partition("/")[2].replace(old_name, new_name))
#     except ClientError as e:
#         logging.error(e)


# def update_bucket_policy():
#     """
#
#     """


async def _get_account(request: Request, volume_id: str) -> Optional[DesktopObjectDict]:
    """
    Gets the current user's AWS account dict associated with the provided volume_id.

    :param request: the HTTP request object (required).
    :param volume_id: the volume id (required).
    :return: the AWS account dict, or None if not found.
    """
    aws_object_dict = {}
    sts_client = await request.app[HEA_DB].get_client(request, 'sts', volume_id)
    iam_client = await request.app[HEA_DB].get_client(request, 'iam', volume_id)
    account = AWSAccount()

    loop = asyncio.get_running_loop()
    identity_future = loop.run_in_executor(None, sts_client.get_caller_identity)
    user_future = loop.run_in_executor(None, iam_client.get_user)
    await asyncio.wait([identity_future, user_future])
    aws_object_dict['account_id'] = identity_future.result().get('Account')
    # aws_object_dict['alias'] = next(iam_client.list_account_aliases()['AccountAliases'], None)  # Only exists for IAM accounts.
    user = user_future.result()['User']
    # aws_object_dict['account_name'] = user.get('UserName')  # Only exists for IAM accounts.

    account.id = aws_object_dict['account_id']
    account.name = aws_object_dict['account_id']
    account.display_name = aws_object_dict['account_id']
    account.owner = request.headers.get(SUB, NONE_USER)
    account.created = user['CreateDate']
    # FIXME this info coming from Alternate Contact(below) gets 'permission denied' with IAMUser even with admin level access
    # not sure if only root account user can access. This is useful info need to investigate different strategy
    # alt_contact_resp = account_client.get_alternate_contact(AccountId=account.id, AlternateContactType='BILLING' )
    # alt_contact =  alt_contact_resp.get("AlternateContact ", None)
    # if alt_contact:
    # account.full_name = alt_contact.get("Name", None)

    return account.to_dict()


def _from_aws_tags(aws_tags: List[TagTypeDef]) -> List[Tag]:
    """
    :param aws_tags: Tags obtained from boto3 Tags api
    :return: List of HEA Tags
    """
    hea_tags = []
    for t in aws_tags:
        tag = Tag()
        tag.key = t['Key']
        tag.value = t['Value']
        hea_tags.append(tag)
    return hea_tags


async def _get_bucket(volume_id: str, s3_resource: S3ServiceResource, s3_client: S3Client,
                      bucket_name: Optional[str] = None, bucket_id: Optional[str] = None,
                      creation_date: Optional[datetime] = None) -> Optional[AWSBucket]:
    """
    :param volume_id: the volume id
    :param s3_client:  the boto3 client
    :param bucket_name: str the bucket name (optional)
    :param bucket_id: str the bucket id (optional)
    :param creation_date: str the bucket creation date (optional)
    :return: Returns either the AWSBucket or None for Not Found or Forbidden, else raises ClientError
    """
    logger = logging.getLogger(__name__)
    try:
        loop = asyncio.get_running_loop()
        if not volume_id or (not bucket_id and not bucket_name):
            raise ValueError("volume_id is required and either bucket_name or bucket_id")
        # id_type = 'id' if bucket_id else 'name'
        # user = request.headers.get(SUB)
        # bucket_dict = await request.app[HEA_DB].get(request, MONGODB_BUCKET_COLLECTION, var_parts=id_type, sub=user)
        # if not bucket_dict:
        #     return web.HTTPBadRequest()

        b = AWSBucket()
        b.name = bucket_id if bucket_id else bucket_name
        b.id = bucket_id if bucket_id else bucket_name
        if bucket_id is not None:
            b.display_name = bucket_id
        elif bucket_name is not None:
            b.display_name = bucket_name
        async_bucket_methods = []

        b.created = creation_date if creation_date else (
            await loop.run_in_executor(None, s3_resource.Bucket, b.name)).creation_date
        b.set_s3_uri_from_bucket_and_key(b.name)
        b.source = AWS_S3

        async def _get_version_status(b: AWSBucket):
            logger.debug('Getting version status of bucket %s', b.name)
            try:
                bucket_versioning = await loop.run_in_executor(None,
                                                               partial(s3_client.get_bucket_versioning, Bucket=b.name))
                logger.debug('bucket_versioning=%s', bucket_versioning)
                if 'Status' in bucket_versioning:
                    b.versioned = bucket_versioning['Status'] == 'Enabled'
                    logger.debug('Got version status of bucket %s successfully', b.name)
                else:
                    logger.debug('No version status information for bucket %s', b.name)
            except ClientError as ce:
                logger.exception('Error getting the version status of bucket %s')
                raise ce

        async_bucket_methods.append(_get_version_status(b))

        async def _get_region(b: AWSBucket):
            logger.debug('Getting region of bucket %s', b.name)
            try:
                loc = await loop.run_in_executor(None, partial(s3_client.get_bucket_location, Bucket=b.name))
                b.region = loc['LocationConstraint']
            except ClientError as ce:
                logging.exception('Error getting the region of bucket %s', b.name)
                raise ce
            logger.debug('Got region of bucket %s successfully', b.name)

        async_bucket_methods.append(_get_region(b))

        # todo how to find partition dynamically. The format is arn:PARTITION:s3:::NAME-OF-YOUR-BUCKET
        # b.arn = "arn:"+"aws:"+":s3:::"

        async def _get_tags(b: AWSBucket):
            logger.debug('Getting tags of bucket %s', b.name)
            try:
                tagging = await loop.run_in_executor(None, partial(s3_client.get_bucket_tagging, Bucket=b.name))
                b.tags = _from_aws_tags(aws_tags=tagging['TagSet'])
            except ClientError as ce:
                if ce.response['Error']['Code'] != 'NoSuchTagSet':
                    logging.exception('Error getting the tags of bucket %s', b.name)
                    raise ce
            logger.debug('Got tags of bucket %s successfully', b.name)

        async_bucket_methods.append(_get_tags(b))

        async def _get_encryption_status(b: AWSBucket):
            logger.debug('Getting encryption status of bucket %s', b.name)
            try:
                encrypt = await loop.run_in_executor(None, partial(s3_client.get_bucket_encryption, Bucket=b.name))
                rules: list = encrypt['ServerSideEncryptionConfiguration']['Rules']
                b.encrypted = len(rules) > 0
            except ClientError as e:
                if e.response['Error']['Code'] == 'ServerSideEncryptionConfigurationNotFoundError':
                    b.encrypted = False
                else:
                    logger.exception('Error getting the encryption status of bucket %s', b.name)
                    raise e
            logger.debug('Got encryption status of bucket %s successfully', b.name)

        async_bucket_methods.append(_get_encryption_status(b))

        async def _get_bucket_policy(b: AWSBucket):
            logger.debug('Getting bucket policy of bucket %s', b.name)
            try:
                bucket_policy = await loop.run_in_executor(None, partial(s3_client.get_bucket_policy, Bucket=b.name))
                b.permission_policy = bucket_policy['Policy']
            except ClientError as e:
                if e.response['Error']['Code'] != 'NoSuchBucketPolicy':
                    logging.exception('Error getting the bucket policy of bucket %s', b.name)
                    raise e
            logger.debug('Got bucket policy of bucket %s successfully', b.name)

        async_bucket_methods.append(_get_bucket_policy(b))

        async def _get_bucket_lock_status(b: AWSBucket):
            logger.debug('Getting bucket lock status of bucket %s', b.name)
            try:
                lock_config = await loop.run_in_executor(None, partial(s3_client.get_object_lock_configuration,
                                                                       Bucket=b.name))
                b.locked = lock_config['ObjectLockConfiguration']['ObjectLockEnabled'] == 'Enabled'
            except ClientError as e:
                if e.response['Error']['Code'] != 'ObjectLockConfigurationNotFoundError':
                    logger.exception('Error getting the lock status of bucket %s', b.name)
                    raise e
                b.locked = False
            logger.debug('Got bucket lock status of bucket %s successfully', b.name)

        async_bucket_methods.append(_get_bucket_lock_status(b))

        # todo need to lazy load this these metrics
        total_size = None
        obj_count = None
        mod_date = None
        # FIXME need to calculate this metric data in a separate call. Too slow
        # s3bucket = s3_resource.Bucket(b.name)
        # for obj in s3bucket.objects.all():
        #     total_size += obj.size
        #     obj_count += 1
        #     mod_date = obj.last_modified if mod_date is None or obj.last_modified > mod_date else mod_date
        b.size = total_size
        b.object_count = obj_count
        b.modified = mod_date
        await asyncio.gather(*async_bucket_methods)
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code in ('403', '404', 'NoSuchBucket'):
            return None
        logger.exception(f'Error getting bucket %s', b.name)
        raise e
    return b


async def _to_aws_tags(hea_tags: List[Tag]) -> List[Dict[str, str]]:
    """
    :param hea_tags: HEA tags to converted to aws tags compatible with boto3 api
    :return: aws tags
    """
    aws_tag_dicts = []
    for hea_tag in hea_tags:
        aws_tag_dict = {}
        aws_tag_dict['Key'] = hea_tag.key
        aws_tag_dict['Value'] = hea_tag.value
        aws_tag_dicts.append(aws_tag_dict)
    return aws_tag_dicts


async def _get_storage_class(volume_id: str, item_key: str, item_values: Optional[list] = None) -> Optional[AWSStorage]:
    """
    :param item_key: the item_key
    :param item_values:  item_values
    :return: Returns either the AWSStorage or None for Not Found
    """
    logger = logging.getLogger(__name__)

    if not volume_id:
        return None
    if not item_key:
        return None

    total_size = 0
    object_count = 0
    init_mod = None
    last_mod = None

    for val in item_values or []:
        total_size += val.size
        object_count += 1
        init_mod = val.last_modified if init_mod is None or val.last_modified < init_mod else init_mod
        last_mod = val.last_modified if last_mod is None or val.last_modified > last_mod else last_mod

    s = AWSStorage()
    s.name = item_key
    s.id = item_key
    s.display_name = item_key
    s.object_init_modified = init_mod
    s.object_last_modified = last_mod
    s.storage_bytes = total_size
    s.object_count = object_count
    s.created = datetime.now()
    s.modified = datetime.now()
    s.volume_id = volume_id
    return s


# if __name__ == "__main__":
# print(get_account())
# print(post_bucket('richardmtest'))
# print(put_bucket("richardmtest"))
# print(get_all_buckets())
# print(get_all("richardmtest"))
# print(post_folder('richardmtest/temp'))
# print(put_folder("richardmtest/temp"))
# print(post_object(r'richardmtest/temp/', r'C:\Users\u0933981\IdeaProjects\heaserver\README.md'))
# print(put_object(r'richardmtest/temp/', r'C:\Users\u0933981\IdeaProjects\heaserver\README.md'))
# download_object(r'richardmtest/temp/README.md', r'C:\Users\u0933981\Desktop\README.md')
# rename_object(r'richardmtest/README.md', 'readme2.md')
# print(copy_object(r'richardmtest/temp/README.md', r'richardmtest/temp/README.md'))
# print(transfer_object_within_account(r'richardmtest/temp/readme2.md', r'timmtest/temp/README.md'))
# print(generate_presigned_url(r'richardmtest/temp/'))
# print(get_object_content(r'richardmtest/temp/README.md'))  # ["Body"].read())
# print(delete_object('richardmtest/temp/README.md'))
# print(delete_folder('richardmtest/temp'))
# print(delete_bucket_objects("richardmtest"))
# print(delete_bucket('richardmtest'))
# print("done")


def _second_to_last(text, pattern):
    return text.rfind(pattern, 0, text.rfind(pattern))


def _handle_client_error(e):
    logger = logging.getLogger(__name__)
    error_code = e.response['Error']['Code']
    if error_code in (CLIENT_ERROR_404, CLIENT_ERROR_NO_SUCH_BUCKET):  # folder doesn't exist
        logger.debug('Error from boto3: %s', exc_info=True)
        return response.status_not_found()
    elif error_code in (CLIENT_ERROR_ACCESS_DENIED, CLIENT_ERROR_FORBIDDEN, CLIENT_ERROR_ALL_ACCESS_DISABLED):
        logger.debug('Error from boto3: %s', exc_info=True)
        return response.status_forbidden()
    else:
        logger.exception('Error from boto3')
        return response.status_internal_error(str(e))


def _get_file(bucket_name: str, contents: Dict[str, Any], display_name: str, key: str, encoded_key: str,
              request: Request):
    file = AWSS3FileObject()
    file.id = encoded_key
    file.name = encoded_key
    file.display_name = display_name
    file.modified = contents['LastModified']
    file.created = contents['LastModified']
    file.owner = request.headers.get(SUB, NONE_USER)
    file.mime_type = guess_mime_type(display_name)
    file.size = contents['Size']
    file.storage_class = S3StorageClass[contents['StorageClass']]
    file.source = AWS_S3
    file.set_s3_uri_from_bucket_and_key(bucket_name, key)
    return file


def _get_folder(bucket_name: str, contents: Dict[str, Any], key: str, encoded_key: str, request: Request):
    folder = AWSS3Folder()
    folder.id = encoded_key
    folder.name = encoded_key
    folder.display_name = key[_second_to_last(key, '/') + 1:-1]
    folder.modified = contents['LastModified']
    folder.created = contents['LastModified']
    folder.owner = request.headers.get(SUB, NONE_USER)
    folder.storage_class = S3StorageClass[contents['StorageClass']]
    folder.set_s3_uri_from_bucket_and_key(bucket_name, key)
    folder.source = AWS_S3
    return folder


def _decode_folder(folder_id_):
    if folder_id_ == ROOT_FOLDER.id:
        folder_id = ''
    else:
        try:
            folder_id = decode_key(folder_id_)
            if not is_folder(folder_id):
                folder_id = None
        except KeyDecodeException:
            # Let the bucket query happen so that we consistently return Forbidden if the user lacks permissions
            # for the bucket.
            folder_id = None
    return folder_id


def _key_in_folder(decoded_key, decoded_folder_key):
    if decoded_key.startswith(decoded_folder_key):
        item_id_ = decoded_key.removeprefix(decoded_folder_key)
        if len(item_id_) > 1 and '/' in item_id_[:-1]:
            return False
    else:
        return False
    return True


async def _return_bucket_status_or_not_found(bucket_name, loop, s3):
    try:
        await loop.run_in_executor(None, partial(s3.head_bucket, Bucket=bucket_name))
        return response.status_not_found()
    except ClientError as e:
        return _handle_client_error(e)
