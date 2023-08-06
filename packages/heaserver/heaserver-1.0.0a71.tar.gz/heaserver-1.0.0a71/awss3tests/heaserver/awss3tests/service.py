from heaserver.service.runner import init_cmd_line, routes, start
from heaserver.service.db import awsservicelib, aws
from heaserver.service.wstl import builder_factory, action
from heaserver.service import response
from heaserver.service.heaobjectsupport import new_heaobject_from_type, PermissionGroup
from heaobject.folder import Folder, Item
from heaobject.error import DeserializeException
from heaobject.root import ShareImpl
from heaobject.user import ALL_USERS
from aiohttp import web, hdrs
import logging

_logger = logging.getLogger(__name__)

ROOT_FOLDER = Folder()
ROOT_FOLDER.id = 'root'
ROOT_FOLDER.name = 'root'
ROOT_FOLDER.display_name = 'Root'
_root_share = ShareImpl()
_root_share.user = ALL_USERS
_root_share.permissions = PermissionGroup.POSTER_PERMS.perms
ROOT_FOLDER.shares = [_root_share]


@routes.get('/ping')
async def ping(request: web.Request) -> web.Response:
    """
    For testing whether the service is up.

    :param request: the HTTP request.
    :return: Always returns status code 200.
    """
    return response.status_ok()


@routes.get('/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/{folder_id}/items')
@routes.get('/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/{folder_id}/items/')
@action(name='heaserver-awss3folders-item-move', path='/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/{folder_id}/items/mover', rel='hea-mover')
@action(name='heaserver-awss3folders-item-duplicate', rel='hea-duplicator',
        path='/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/{folder_id}/items/{id}/duplicator')
@action(name='heaserver-awss3folders-item-get-properties', rel='hea-properties')
@action(name='heaserver-awss3folders-item-get-open-choices', rel='hea-opener-choices', path='/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/{folder_id}/items/{id}/opener')
async def get_items(request: web.Request) -> web.Response:
    """
    Gets the items of the folder with the specified id.
    :param request: the HTTP request.
    :return: the requested items, or Not Found if the folder was not found.
    ---
    summary: All items in a folder.
    tags:
        - heaserver-awss3folders-folder-items
    parameters:
        - name: volume_id
          in: path
          required: true
          description: The id of the volume to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
        - name: bucket_id
          in: path
          required: true
          description: The id of the bucket to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: A bucket id
              value: my-bucket
        - name: folder_id
          in: path
          required: true
          description: The id of the folder to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: A folder id
              value: root
    responses:
      '200':
        $ref: '#/components/responses/200'
      '403':
        $ref: '#/components/responses/403'
    """
    return await awsservicelib.get_items(request)


@routes.route('OPTIONS', '/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/{folder_id}/items/{id}')
async def get_item_options(request: web.Request) -> web.Response:
    """
    ---
    summary: Allowed HTTP methods.
    tags:
        - heaserver-awss3folders-folder-items
    parameters:
        - name: volume_id
          in: path
          required: true
          description: The id of the volume to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
        - name: bucket_id
          in: path
          required: true
          description: The id of the bucket to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: A bucket id
              value: my-bucket
        - name: folder_id
          in: path
          required: true
          description: The id of the folder to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: A folder id
              value: root
        - $ref: '#/components/parameters/id'
    responses:
      '200':
        description: Expected response to a valid request.
        content:
            text/plain:
                schema:
                    type: string
                    example: "200: OK"
      '403':
        $ref: '#/components/responses/403'
      '404':
        $ref: '#/components/responses/404'
    """
    resp = await awsservicelib.has_item(request)
    if resp.status == 200:
        return await response.get_options(request, ['GET', 'POST', 'DELETE', 'HEAD', 'OPTIONS'])
    else:
        headers = {}
        headers[hdrs.CONTENT_TYPE] = 'text/plain; charset=utf-8'
        return response.status_generic(status=resp.status, body=resp.text, headers=headers)


@routes.route('OPTIONS', '/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/{folder_id}/items')
@routes.route('OPTIONS', '/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/{folder_id}/items/')
async def get_items_options(request: web.Request) -> web.Response:
    """
    Gets the allowed HTTP methods for a folder items resource.

    :param request: the HTTP request (required).
    :return: the HTTP response.
    ---
    summary: Allowed HTTP methods.
    tags:
        - heaserver-awss3folders-folder-items
    parameters:
        - name: volume_id
          in: path
          required: true
          description: The id of the volume to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
        - name: bucket_id
          in: path
          required: true
          description: The id of the bucket to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: A bucket id
              value: my-bucket
        - name: folder_id
          in: path
          required: true
          description: The id of the folder to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: A folder id
              value: root
    responses:
      '200':
        description: Expected response to a valid request.
        content:
            text/plain:
                schema:
                    type: string
                    example: "200: OK"
      '403':
        $ref: '#/components/responses/403'
      '404':
        $ref: '#/components/responses/404'
    """
    resp = await awsservicelib.has_folder(request)
    if resp.status == 200:
        return await response.get_options(request, ['GET', 'POST', 'DELETE', 'HEAD', 'OPTIONS'])
    else:
        headers = {hdrs.CONTENT_TYPE: 'text/plain; charset=utf-8'}
        return response.status_generic(status=resp.status, body=resp.text, headers=headers)


@routes.route('OPTIONS', '/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/{id}')
async def get_folder_options(request: web.Request) -> web.Response:
    """
    Gets the allowed HTTP methods for a folder resource.

    :param request: the HTTP request (required).
    :return: the HTTP response.
    ---
    summary: Allowed HTTP methods.
    tags:
        - heaserver-awss3folders-folders
    parameters:
        - name: volume_id
          in: path
          required: true
          description: The id of the volume to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
        - name: bucket_id
          in: path
          required: true
          description: The id of the bucket to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: A bucket id
              value: my-bucket
        - $ref: '#/components/parameters/id'
    responses:
      '200':
        description: Expected response to a valid request.
        content:
            text/plain:
                schema:
                    type: string
                    example: "200: OK"
      '404':
        $ref: '#/components/responses/404'
    """
    resp = await awsservicelib.has_folder(request)
    if resp.status == 200:
        return await response.get_options(request, ['GET', 'POST', 'DELETE', 'HEAD', 'OPTIONS'])
    else:
        headers = {hdrs.CONTENT_TYPE: 'text/plain; charset=utf-8'}
        return response.status_generic(status=resp.status, body=resp.text, headers=headers)


@routes.get('/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/{folder_id}/items/{id}')
@action(name='heaserver-awss3folders-item-move', path='/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/{folder_id}/items/{id}/mover', rel='hea-mover')
@action(name='heaserver-awss3folders-item-duplicate', rel='hea-duplicator',
        path='/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/{folder_id}/items/{id}/duplicator')
@action(name='heaserver-awss3folders-item-get-properties', rel='hea-properties')
@action(name='heaserver-awss3folders-item-get-open-choices', rel='hea-opener-choices', path='/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/{folder_id}/items/{id}/opener')
async def get_item(request: web.Request) -> web.Response:
    """
    Gets the requested item from the given folder.

    :param request: the HTTP request. Required.
    :return: the requested item, or Not Found if it was not found.
    ---
    summary: A specific folder item.
    tags:
        - heaserver-awss3folders-folder-items
    parameters:
        - name: volume_id
          in: path
          required: true
          description: The id of the volume to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
        - name: bucket_id
          in: path
          required: true
          description: The id of the bucket to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: A bucket id
              value: my-bucket
        - name: folder_id
          in: path
          required: true
          description: The id of the folder to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: A folder id
              value: root
        - $ref: '#/components/parameters/id'
    responses:
      '200':
        $ref: '#/components/responses/200'
      '403':
        $ref: '#/components/responses/403'
      '404':
        $ref: '#/components/responses/404'
    """
    return await _get_item_response(request)


@routes.get('/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/{folder_id}/items/{id}/duplicator')
@action(name='heaserver-awss3folders-item-duplicate-form', path='/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/{folder_id}/items/{id}')
async def get_item_duplicator(request: web.Request) -> web.Response:
    """
    Gets a form template for duplicating the requested item.

    :param request: the HTTP request. Required.
    :return: the requested form, or Not Found if the requested item was not found.
    """
    return await _get_item_response(request)


@routes.get('/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/{id}/duplicator')
@action(name='heaserver-awss3folders-folder-duplicate-form', path='/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/{folder_id}/items/{id}')
async def get_folder_duplicator(request: web.Request) -> web.Response:
    """
    Gets a form template for duplicating the requested folder.

    :param request: the HTTP request. Required.
    :return: the requested form, or Not Found if the requested folder was not found.
    """
    return await _get_folder(request)


@routes.post('/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/{folder_id}/duplicator')
async def post_item_duplicator(request: web.Request) -> web.Response:
    """
    Posts the provided item for duplication.

    :param request: the HTTP request.
    :return: a Response object with a status of Created and the object's URI in the
    """
    return post_item_in_folder(request)


@routes.post('/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/{folder_id}/items')
@routes.post('/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/{folder_id}/items/')
async def post_item_in_folder(request: web.Request) -> web.Response:
    """
    Creates a new folder item.

    :param request: the HTTP request. The body of the request is expected to be an item or an actual object.
    :return: the response, with a 204 status code if an item was created or a 400 if not. If an item was created, the
    Location header will contain the URL of the created item.
    ---
    summary: A specific folder item.
    tags:
        - heaserver-awss3folders-folder-items
    parameters:
        - name: volume_id
          in: path
          required: true
          description: The id of the volume.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
        - name: bucket_id
          in: path
          required: true
          description: The id of the bucket.
          schema:
            type: string
          examples:
            example:
              summary: A bucket id
              value: my-bucket
        - name: folder_id
          in: path
          required: true
          description: The id of the folder.
          schema:
            type: string
          examples:
            example:
              summary: A folder id
              value: root
    requestBody:
        description: A new folder item object.
        required: true
        content:
            application/vnd.collection+json:
              schema:
                type: object
              examples:
                example:
                  summary: Item example
                  value: {
                    "template": {
                      "data": [{
                        "name": "created",
                        "value": null
                      },
                      {
                        "name": "derived_by",
                        "value": null
                      },
                      {
                        "name": "derived_from",
                        "value": []
                      },
                      {
                        "name": "description",
                        "value": null
                      },
                      {
                        "name": "display_name",
                        "value": "Bob"
                      },
                      {
                        "name": "invited",
                        "value": []
                      },
                      {
                        "name": "modified",
                        "value": null
                      },
                      {
                        "name": "name",
                        "value": "bob"
                      },
                      {
                        "name": "owner",
                        "value": "system|none"
                      },
                      {
                        "name": "shares",
                        "value": []
                      },
                      {
                        "name": "source",
                        "value": null
                      },
                      {
                        "name": "version",
                        "value": null
                      },
                      {
                        "name": "actual_object_id",
                        "value": "666f6f2d6261722d71757578"
                      },
                      {
                        "name": "actual_object_type_name",
                        "value": "heaobject.data.AWSS3FileObject"
                      },
                      {
                        "name": "actual_object_uri",
                        "value": "/volumes/666f6f2d6261722d71757578/buckets/my-bucket/awss3folders/666f6f2d6261722d71757578"
                      }]
                    }
                  }
            application/json:
              schema:
                type: object
              examples:
                example:
                  summary: Item example
                  value: {
                    "created": null,
                    "derived_by": null,
                    "derived_from": [],
                    "description": null,
                    "display_name": "Joe",
                    "invited": [],
                    "modified": null,
                    "name": "joe",
                    "owner": "system|none",
                    "shares": [],
                    "source": null,
                    "type": "heaobject.folder.Item",
                    "version": null,
                    "folder_id": "root",
                    "actual_object_id": "666f6f2d6261722d71757578",
                    "actual_object_type_name": "heaobject.registry.Component",
                    "actual_object_uri": "/volumes/666f6f2d6261722d71757578/buckets/my-bucket/awss3folders/666f6f2d6261722d71757578"
                  }
    responses:
      '201':
        $ref: '#/components/responses/201'
      '400':
        $ref: '#/components/responses/400'
      '404':
        $ref: '#/components/responses/404'
    """
    try:
        item = await new_heaobject_from_type(request, Item)
    except DeserializeException as e:
        return response.status_bad_request(str(e).encode())

    return await awsservicelib.post_object(request, item)



@routes.delete('/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/{folder_id}/items/{id}')
async def delete_item(request: web.Request) -> web.Response:
    """
    Deletes the item with the specified id.

    :param request: the HTTP request.
    :return: No Content or Not Found.
    ---
    summary: Folder item deletion
    tags:
        - heaserver-awss3folders-folder-items
    parameters:
        - name: volume_id
          in: path
          required: true
          description: The id of the volume.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
        - name: bucket_id
          in: path
          required: true
          description: The id of the bucket.
          schema:
            type: string
          examples:
            example:
              summary: A bucket id
              value: my-bucket
        - name: folder_id
          in: path
          required: true
          description: The id of the folder.
          schema:
            type: string
          examples:
            example:
              summary: A folder id
              value: root
        - $ref: '#/components/parameters/id'
    responses:
      '204':
        $ref: '#/components/responses/204'
      '404':
        $ref: '#/components/responses/404'
    """
    return await awsservicelib.delete_object(request)


@routes.get('/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/{id}')
@action(name='heaserver-awss3folders-folder-get-properties', rel='hea-properties')
@action(name='heaserver-awss3folders-folder-duplicate', rel='hea-duplicator', path='/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/{id}/duplicator')
@action('heaserver-awss3folders-folder-get-open-choices', rel='hea-opener-choices',
        path='/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/{id}/opener')
async def get_folder(request: web.Request) -> web.Response:
    """
    Gets the folder with the specified id.

    :param request: the HTTP request.
    :return: the requested folder or Not Found.
    ---
    summary: A specific folder.
    tags:
        - heaserver-awss3folders-folders
    parameters:
        - name: volume_id
          in: path
          required: true
          description: The id of the volume to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
        - name: bucket_id
          in: path
          required: true
          description: The id of the bucket to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: A bucket id
              value: my-bucket
        - $ref: '#/components/parameters/id'
    responses:
      '200':
        $ref: '#/components/responses/200'
      '404':
        $ref: '#/components/responses/404'
    """
    return await _get_folder(request)


@routes.get('/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/byname/{name}')
async def get_folder_by_name(request: web.Request) -> web.Response:
    """
    Gets the folder with the specified name.

    :param request: the HTTP request.
    :return: the requested folder or Not Found.
    ---
    summary: A specific folder.
    tags:
        - heaserver-awss3folders-folders
    parameters:
        - name: volume_id
          in: path
          required: true
          description: The id of the volume to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
        - name: bucket_id
          in: path
          required: true
          description: The id of the bucket to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: A bucket id
              value: my-bucket
        - $ref: '#/components/parameters/name'
    responses:
      '200':
        $ref: '#/components/responses/200'
      '404':
        $ref: '#/components/responses/404'
    """
    return await _get_folder_by_name(request)


@routes.get('/volumes/{volume_id}/buckets/{bucket_id}/awss3folders')
@routes.get('/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/')
@action(name='heaserver-awss3folders-folder-get-properties', rel='hea-properties')
@action(name='heaserver-awss3folders-folder-duplicate', rel='hea-duplicator', path='/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/{id}/duplicator')
@action('heaserver-awss3folders-folder-get-open-choices', rel='hea-opener-choices',
        path='/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/{id}/opener')
async def get_folders(request: web.Request) -> web.Response:
    """
    Gets the folder with the specified id.

    :param request: the HTTP request.
    :return: the requested folder or Not Found.
    ---
    summary: A specific folder.
    tags:
        - heaserver-awss3folders-folders
    parameters:
        - name: volume_id
          in: path
          required: true
          description: The id of the volume to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
        - name: bucket_id
          in: path
          required: true
          description: The id of the bucket to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: A bucket id
              value: my-bucket
    responses:
      '200':
        $ref: '#/components/responses/200'
      '404':
        $ref: '#/components/responses/404'
    """
    return await awsservicelib.get_all_folders(request)

@routes.route('OPTIONS', '/volumes/{volume_id}/buckets/{bucket_id}/awss3folders')
@routes.route('OPTIONS', '/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/')
async def get_folders_options(request: web.Request) -> web.Response:
    """
    Gets the allowed HTTP methods for a folders resource.

    :param request: the HTTP request (required).
    :response: the HTTP response.
    ---
    summary: Allowed HTTP methods.
    tags:
        - heaserver-awss3folders-folders
    parameters:
        - name: volume_id
          in: path
          required: true
          description: The id of the volume to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
        - name: bucket_id
          in: path
          required: true
          description: The id of the bucket to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: A bucket id
              value: my-bucket
    responses:
      '200':
        description: Expected response to a valid request.
        content:
            text/plain:
                schema:
                    type: string
                    example: "200: OK"
      '403':
        $ref: '#/components/responses/403'
      '404':
        $ref: '#/components/responses/404'
    """
    return await awsservicelib.get_options(request, ['GET', 'DELETE', 'HEAD', 'OPTIONS'], awsservicelib.has_bucket)


@routes.delete('/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/{id}')
async def delete_folder(request: web.Request) -> web.Response:
    """
    Deletes the folder with the specified id.

    :param request: the HTTP request.
    :return: No Content or Not Found.
    ---
    summary: Folder deletion
    tags:
        - heaserver-awss3folders-folders
    parameters:
        - name: volume_id
          in: path
          required: true
          description: The id of the volume to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
        - name: bucket_id
          in: path
          required: true
          description: The id of the bucket to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: A bucket id
              value: my-bucket
        - $ref: '#/components/parameters/id'
    responses:
      '204':
        $ref: '#/components/responses/204'
      '404':
        $ref: '#/components/responses/404'
    """
    return await awsservicelib.delete_folder(request)


@routes.get('/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/{id}/opener')
@action('heaserver-awss3folders-folder-open-default', rel='hea-opener hea-default application/x.folder',
        path='/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/{id}/items/')
async def get_folder_opener(request: web.Request) -> web.Response:
    """
    Opens the requested folder.

    :param request: the HTTP request. Required.
    :return: the opened folder, or Not Found if the requested item does not exist.
    ---
    summary: Folder opener choices
    tags:
        - heaserver-awss3folders-folders
    parameters:
        - name: volume_id
          in: path
          required: true
          description: The id of the volume to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
        - name: bucket_id
          in: path
          required: true
          description: The id of the bucket to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: A bucket id
              value: my-bucket
        - $ref: '#/components/parameters/id'
    responses:
      '300':
        $ref: '#/components/responses/300'
      '404':
        $ref: '#/components/responses/404'
    """
    return await _get_folder(request)


def main():
    config = init_cmd_line(description='Repository of folders', default_port=8080)
    start(db=aws.S3, wstl_builder_factory=builder_factory(__package__), config=config)


async def _get_folder(request: web.Request) -> web.Response:
    """
    Gets the folder with the specified id.

    :param request: the HTTP request.
    :return: the requested folder or Not Found.
    """
    if request.match_info['id'] == 'root':
        return await response.get(request, ROOT_FOLDER.to_dict())
    else:
        return await awsservicelib.get_folder(request)


async def _get_folder_by_name(request: web.Request) -> web.Response:
    """
    Gets the folder with the specified id.

    :param request: the HTTP request.
    :return: the requested folder or Not Found.
    """
    if request.match_info['name'] == 'root':
        return await response.get(request, ROOT_FOLDER.to_dict())
    else:
        return await awsservicelib.get_folder_by_name(request)


async def _get_item_response(request) -> web.Response:
    """
    Gets the item with the specified id and in the specified folder.

    :param request: the HTTP request.
    :return: a response containing the returned item or an empty body.
    """
    return await awsservicelib.get_item(request)
