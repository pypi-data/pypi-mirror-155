from aiohttp import hdrs
from ..representor import wstljson, cj, nvpjson, xwwwformurlencoded
from urllib.parse import urlencode
from typing import TYPE_CHECKING
from .microservicetestcase import MicroserviceTestCase
from .. import jsonschemavalidator
import logging


if TYPE_CHECKING:
    _Base = MicroserviceTestCase
else:
    _Base = object


class PostMixin(_Base):
    """Tester mixin for POST requests."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def test_post(self) -> None:
        """
        Checks if a POST request succeeds with a Collection+JSON template. The test is skipped if the body to POST
        (``_body_post``) is not defined.
        """
        if not self._body_post:
            self.skipTest('_body_post not defined')
        obj = await self.client.request('POST',
                                        (self._href / '').path,
                                        json=self._body_post,
                                        headers={**self._headers, hdrs.CONTENT_TYPE: cj.MIME_TYPE})
        self.assertEqual('201: Created', await obj.text())

    async def test_post_nvpjson(self) -> None:
        """
        Checks if a POST request succeeds with a name-value-pair JSON template. The test is skipped if the body to POST
        (``_body_post``) is not defined.
        """
        if self._body_post is not None:
            obj = await self.client.request('POST',
                                            (self._href / '').path,
                                            json=cj.to_nvpjson(self._body_post),
                                            headers={**self._headers, hdrs.CONTENT_TYPE: nvpjson.MIME_TYPE})
            self.assertEqual('201: Created', await obj.text())
        else:
            self.skipTest('_body_post not defined')

    async def test_post_xwwwformurlencoded(self) -> None:
        """
        Checks if a POST request succeeds with encoded form data. The test is skipped if either the body to POST
        (``_body_post``) is not defined or cannot be converted to encoded form data.
        """
        if not self._body_post:
            self.skipTest('_body_post not defined')
        try:
            data_ = self._post_data()
        except jsonschemavalidator.ValidationError:
            self.skipTest('_body_post cannot be converted xwwwformurlencoded form')
        obj = await self.client.request('POST',
                                        (self._href / '').path,
                                        data=data_,
                                        headers={**self._headers, hdrs.CONTENT_TYPE: xwwwformurlencoded.MIME_TYPE})
        self.assertEqual('201: Created', await obj.text())

    async def test_post_status(self) -> None:
        """
        Checks if a POST request succeeds with status 201 when the request body is in Collection+JSON form. The
        test is skipped if the body to POST (``_body_post``) is not defined.
        """
        if not self._body_post:
            self.skipTest('_body_post not defined')
        obj = await self.client.request('POST',
                                        (self._href / '').path,
                                        json=self._body_post,
                                        headers={**self._headers, hdrs.CONTENT_TYPE: cj.MIME_TYPE})
        self.assertEqual(201, obj.status)

    async def test_post_status_nvpjson(self) -> None:
        """
        Checks if a POST request succeeds with status 201 when the request body is in name-value-pair JSON form.
        The test is skipped if the body to POST (``_body_post``) is not defined.
        """
        if self._body_post is not None:
            obj = await self.client.request('POST',
                                            (self._href / '').path,
                                            json=cj.to_nvpjson(self._body_post),
                                            headers={**self._headers, hdrs.CONTENT_TYPE: nvpjson.MIME_TYPE})
            self.assertEqual(201, obj.status)
        else:
            self.skipTest('_body_post not defined')

    async def test_post_status_xwwwformurlencoded(self) -> None:
        """
        Checks if a POST request succeeds with status 201 when the request body is encoded form data. The test is
        skipped if either the body to POST (``_body_post``) is not defined or cannot be converted to encoded form data.
        """
        if not self._body_post:
            self.skipTest('_body_post not defined')
        try:
            data_ = self._post_data()
        except jsonschemavalidator.ValidationError:
            self.skipTest('_body_post cannot be converted xwwwformurlencoded form')
        obj = await self.client.request('POST',
                                        (self._href / '').path,
                                        data=data_,
                                        headers={**self._headers, hdrs.CONTENT_TYPE: xwwwformurlencoded.MIME_TYPE})
        self.assertEqual(201, obj.status)

    async def test_post_status_empty_body(self) -> None:
        """
        Checks if a POST request fails with status 400 when the request body is declared with type Collection+JSON but
        actually is empty. The test is skipped if the body that would normally be POSTed (``_body_post``) is not
        defined.
        """
        if not self._body_post:
            self.skipTest('_body_post not defined')
        obj = await self.client.request('POST',
                                        (self._href / '').path,
                                        headers={**self._headers, hdrs.CONTENT_TYPE: cj.MIME_TYPE})
        self.assertEqual(400, obj.status)

    async def test_post_status_empty_body_nvpjson(self) -> None:
        """
        Checks if a POST request fails with status 400 when the request body is declared with type name-value-pair JSON
        but actually is empty. The test is skipped if the body that would normally be POSTed (``_body_post``) is not
        defined.
        """
        if not self._body_post:
            self.skipTest('_body_post not defined')
        obj = await self.client.request('POST',
                                        (self._href / '').path,
                                        headers={**self._headers, hdrs.CONTENT_TYPE: nvpjson.MIME_TYPE})
        self.assertEqual(400, obj.status)

    async def test_post_status_empty_body_xwwwformurlencoded(self) -> None:
        """
        Checks if a POST request fails with status 400 when the request body is declared as encoded form data but
        actually is empty. The test is skipped if the body that would normally be POSTed (``_body_post``) is not
        defined.
        """
        if not self._body_post:
            self.skipTest('_body_post not defined')
        obj = await self.client.request('POST',
                                        (self._href / '').path,
                                        headers={**self._headers, hdrs.CONTENT_TYPE: xwwwformurlencoded.MIME_TYPE})
        self.assertEqual(400, obj.status)

    async def test_post_status_invalid_type(self) -> None:
        """
        Checks if a POST request fails with status 400 when the declared type is invalid. The test is skipped if the
        body (without modification) to POST (``_body_post``) is not defined.
        """
        if not self._body_post:
            self.skipTest('_body_post not defined')
        await self._test_invalid({'type': 'foo.bar'})

    async def test_invalid_url(self) -> None:
        """
        Checks if a POST request fails with status 405 when the URL has a desktop object ID. The test is skipped if the
        body to POST (``_body_post``) is not defined.
        """
        if not self._body_post:
            self.skipTest('_body_post not defined')
        obj = await self.client.request('POST',
                                        (self._href / '1').path,
                                        json=self._body_post,
                                        headers={**self._headers, hdrs.CONTENT_TYPE: cj.MIME_TYPE})
        self.assertEqual(405, obj.status)

    async def _test_invalid(self, changes) -> None:
        """
        Checks if a POST request with a name-value-pair JSON request body (``_body_put``) with the given change(s) fails
        with status 400. An ``AssertionError`` will be raised if the unmodified body to POST (``_body_post``) is not
        defined.

        This method is used by ``test_post_status_invalid_type`` to test if setting an invalid type fails with status
        400.

        :param changes: The changes made, expressed as a dictionary
        :except AssertionError: When ``_body_post`` is not defined
        """
        assert self._body_post is not None
        changed = _copy_heaobject_dict_with(cj.to_nvpjson(self._body_post), changes)
        obj = await self.client.request('POST',
                                        (self._href / '').path,
                                        json=changed,
                                        headers={**self._headers, hdrs.CONTENT_TYPE: nvpjson.MIME_TYPE})
        self.assertEqual(400, obj.status)

    def _post_data(self):
        """Converts the POST body to encoded form data."""
        return _to_xwwwformurlencoded_data(self._body_post)


class PutMixin(_Base):
    """Tester mixin for PUT requests."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def test_put(self) -> None:
        """
        Checks if a PUT request with a Collection+JSON request body succeeds when the target has the same format. The
        test is skipped if the body to PUT (``_body_put``) is not defined.
        """
        if not self._body_put:
            self.skipTest('_body_put not defined')
        obj = await self.client.request('PUT',
                                        (self._href / self._id()).path,
                                        json=self._body_put,
                                        headers={**self._headers, hdrs.CONTENT_TYPE: cj.MIME_TYPE})
        self.assertEqual('', await obj.text())

    async def test_put_nvpjson(self) -> None:
        """
        Checks if a PUT request with a name-value-pair JSON request body succeeds when the target has the same format.
        The test is skipped if the body to PUT (``_body_put``) is not defined.
        """
        if not self._body_put:
            self.skipTest('_body_put not defined')
        obj = await self.client.request('PUT',
                                        (self._href / self._id()).path,
                                        json=cj.to_nvpjson(self._body_put) if self._body_put is not None else None,
                                        headers={**self._headers, hdrs.CONTENT_TYPE: nvpjson.MIME_TYPE})
        self.assertEqual('', await obj.text())

    async def test_put_xwwwformurlencoded(self) -> None:
        """
        Checks if a PUT request with encoded form data succeeds when the target has the same format. The test is skipped
        if the body to PUT (``_body_put``) is not defined.
        """
        if not self._body_put:
            self.skipTest('_body_put not defined')
        try:
            data_ = self._put_data()
        except jsonschemavalidator.ValidationError:
            self.skipTest('_body_put cannot be converted xwwwformurlencoded form')
        else:
            obj = await self.client.request('PUT',
                                            (self._href / self._id()).path,
                                            data=data_,
                                            headers={**self._headers, hdrs.CONTENT_TYPE: xwwwformurlencoded.MIME_TYPE})
            self.assertEqual('', await obj.text())

    async def test_put_status(self) -> None:
        """
        Checks if a PUT request with a Collection+JSON request body succeeds with status 204 when the target has the
        same format. The test is skipped if the body to PUT (``_body_put``) is not defined.
        """
        if not self._body_put:
            self.skipTest('_body_put not defined')
        obj = await self.client.request('PUT',
                                        (self._href / self._id()).path,
                                        json=self._body_put,
                                        headers={**self._headers, hdrs.CONTENT_TYPE: cj.MIME_TYPE})
        self.assertEqual(204, obj.status)

    async def test_put_status_wrong_format(self) -> None:
        """
        Checks if a PUT request fails with status 400 when the request body is in name-value-pair JSON but the content
        type is Collection+JSON. The test is skipped if the body to PUT (``_body_put``) is not defined.
        """
        if not self._body_put:
            self.skipTest('_body_put not defined')
        else:
            obj = await self.client.request('PUT',
                                            (self._href / self._id()).path,
                                            json=cj.to_nvpjson(self._body_put),
                                            headers={**self._headers, hdrs.CONTENT_TYPE: cj.MIME_TYPE})
            self.assertEqual(400, obj.status)

    async def test_put_status_nvpjson(self) -> None:
        """
        Checks if a PUT request with a name-value-pair JSON request body succeeds with status 204 when the target has
        the same format. The test is skipped if the body to PUT (``_body_put``) is not defined.
        """
        if not self._body_put:
            self.skipTest('_body_put not defined')
        else:
            obj = await self.client.request('PUT',
                                            (self._href / self._id()).path,
                                            json=cj.to_nvpjson(self._body_put),
                                            headers={**self._headers, hdrs.CONTENT_TYPE: nvpjson.MIME_TYPE})
            self.assertEqual(204, obj.status)

    async def test_put_status_nvpjson_wrong_format(self) -> None:
        """
        Checks if a PUT request fails with status 400 when the request body is encoded form data but the content type is
        name-value-pair JSON. The test is skipped if either the body to PUT (``_body_put``) is not defined or the data
        cannot be converted to encoded form data.
        """
        if not self._body_put:
            self.skipTest('_body_put not defined')
        try:
            data_ = self._put_data()
        except jsonschemavalidator.ValidationError:
            self.skipTest('_body_put cannot be converted xwwwformurlencoded form')
        else:
            obj = await self.client.request('PUT',
                                            (self._href / self._id()).path,
                                            json=data_,
                                            headers={**self._headers, hdrs.CONTENT_TYPE: nvpjson.MIME_TYPE})
        self.assertEqual(400, obj.status)

    async def test_put_status_xwwwformurlencoded(self) -> None:
        """
        Checks if a PUT request with encoded form data succeeds with status 204 when the target has the same format.
        The test is skipped if either the body to PUT (``_body_put``) is not defined or the data cannot be converted to
        encoded form data.
        """
        if not self._body_put:
            self.skipTest('_body_put not defined')
        try:
            data_ = self._put_data()
        except jsonschemavalidator.ValidationError:
            self.skipTest('_body_put cannot be converted xwwwformurlencoded form')
        else:
            obj = await self.client.request('PUT',
                                            (self._href / self._id()).path,
                                            data=data_,
                                            headers={**self._headers, hdrs.CONTENT_TYPE: xwwwformurlencoded.MIME_TYPE})
            self.assertEqual(204, obj.status)

    async def test_put_status_xwwwformurlencoded_wrong_format(self) -> None:
        """
        Checks if a PUT request fails with status 400 when the request body is in Collection+JSON but the content type
        is encoded form data. The test is skipped if the body to PUT (``_body_put``) is not defined.
        """
        if not self._body_put:
            self.skipTest('_body_put not defined')
        obj = await self.client.request('PUT',
                                        (self._href / self._id()).path,
                                        json=self._body_put,
                                        headers={**self._headers, hdrs.CONTENT_TYPE: xwwwformurlencoded.MIME_TYPE})
        self.assertEqual(400, obj.status)

    async def test_put_status_empty_body(self) -> None:
        """
        Checks if a PUT request whose request body MIME type is declared to be Collection+JSON fails with status 400
        when the body is empty. The test is skipped if the body that would normally be PUT (``_body_put``) is not
        defined.
        """
        if not self._body_put:
            self.skipTest('_body_put not defined')
        obj = await self.client.request('PUT',
                                        (self._href / '1').path,
                                        headers={**self._headers, hdrs.CONTENT_TYPE: cj.MIME_TYPE})
        self.assertEqual(400, obj.status)

    async def test_put_status_empty_body_nvpjson(self) -> None:
        """
        Checks if a PUT request whose request body MIME type is declared to be name-value-pair JSON fails with status
        400 when the body is empty. The test is skipped if the body that would normally be PUT (``_body_put``) is not
        defined.
        """
        if not self._body_put:
            self.skipTest('_body_put not defined')
        obj = await self.client.request('PUT',
                                        (self._href / '1').path,
                                        headers={**self._headers, hdrs.CONTENT_TYPE: nvpjson.MIME_TYPE})
        self.assertEqual(400, obj.status)

    async def test_put_status_empty_body_xwwwformurlencoded(self) -> None:
        """
        Checks if a PUT request whose request body MIME type is declared to be encoded form data fails with status 400
        when the body is empty. The test is skipped if the body that would normally be PUT (``_body_put``) is not
        defined.
        """
        if not self._body_put:
            self.skipTest('_body_put not defined')
        obj = await self.client.request('PUT',
                                        (self._href / '1').path,
                                        headers={**self._headers, hdrs.CONTENT_TYPE: xwwwformurlencoded.MIME_TYPE})
        self.assertEqual(400, obj.status)

    async def test_put_status_missing_id(self) -> None:
        """
        Checks if a PUT request with a Collection+JSON request body fails with status 405 when the URL contains no ID.
        The test is skipped if the body to PUT (``_body_put``) is not defined.
        """
        obj = await self.client.request('PUT',
                                        self._href.path,
                                        headers={**self._headers, hdrs.CONTENT_TYPE: cj.MIME_TYPE})
        self.assertEqual(405, obj.status)

    async def test_put_status_missing_id_nvpjson(self) -> None:
        """
        Checks if a PUT request with a name-value-pair JSON request body fails with status 405 when the URL contains no
        ID. The test is skipped if the body to PUT (``_body_put``) _body_put is not defined.
        """
        obj = await self.client.request('PUT',
                                        self._href.path,
                                        headers={**self._headers, hdrs.CONTENT_TYPE: nvpjson.MIME_TYPE})
        self.assertEqual(405, obj.status)

    async def test_put_status_invalid_type(self) -> None:
        """
        Checks if a PUT request with a name-value-pair JSON request body fails with status 405 when the object in the
        request body has an invalid type. The test is skipped if the body (without modification) to PUT (``_body_put``)
        is not defined.
        """
        if not self._body_put:
            self.skipTest('_body_put not defined')
        await self._test_invalid({'type': 'foo.bar'})

    async def test_put_content(self) -> None:
        """
        Checks if a PUT request to plaintext content succeeds with the correct status (``_put_content_status``). The
        test is skipped if either the desired status (``_put_content_status``) is not defined or the content ID
        (``_content_id``) is not defined.
        """
        if self._put_content_status is None:
            self.skipTest('_put_content_status not defined')
        if self._content_id is None:
            self.skipTest('_content_id not defined')
        obj = await self.client.request('PUT',
                                        (self._href / self._content_id / 'content').path,
                                        data='The quick brown fox jumps over the lazy dog',
                                        headers={**self._headers, hdrs.CONTENT_TYPE: 'text/plain'})
        self.assertEquals(self._put_content_status, obj.status)

    async def _test_invalid(self, changes) -> None:
        """
        Checks if a PUT request with a name-value-pair JSON request body (``_body_put``) with the given change(s) fails
        with status 400.

        This method is used by ``test_put_status_invalid_type`` to test if setting an invalid type fails with status
        400.

        :param changes: The changes made, expressed as a dictionary
        """
        changed = _copy_heaobject_dict_with(self._body_put, changes)
        obj = await self.client.request('PUT',
                                        (self._href / self._id()).path,
                                        json=changed,
                                        headers={**self._headers, hdrs.CONTENT_TYPE: nvpjson.MIME_TYPE})
        self.assertEqual(400, obj.status)

    def _put_data(self):
        """Converts the PUT request body to encoded form data."""
        return _to_xwwwformurlencoded_data(self._body_put)

    def _id(self):
        """Gets the ID of the target of the PUT request, determined by the value of the template ``_body_put``."""
        logging.getLogger(__name__).debug('Template is %s', self._body_put)
        for e in self._body_put['template']['data']:
            if e['name'] == 'id':
                return e.get('value')


class GetOneMixin(_Base):
    """Tester mixin for GET requests that request a single object."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def test_get(self) -> None:
        """Checks if a GET request succeeds and returns the expected JSON (``_expected_one``)."""
        print(self._expected_one)
        obj = await self.client.request('GET',
                                        (self._href / self._id()).path,
                                        headers=self._headers)
        self.assertEqual(_ordered(self._expected_one), _ordered(await obj.json()))

    async def test_get_status(self) -> None:
        """Checks if a GET request succeeds with status 200."""
        obj = await self.client.request('GET',
                                        (self._href / self._id()).path,
                                        headers=self._headers)
        self.assertEqual(200, obj.status)

    async def test_get_wstl(self) -> None:
        """
        Checks if a GET request for WeSTL data succeeds and returns the expected JSON (``_expected_one_wstl``). The test
        will be skipped if the expected WeSTL data (``_expected_one_wstl``) is not defined.
        """
        if not self._expected_one_wstl:
            self.skipTest('self._expected_one_wstl is not defined')
        obj = await self.client.request('GET',
                                        (self._href / self._id()).path,
                                        headers={**self._headers, hdrs.ACCEPT: wstljson.MIME_TYPE})
        self.assertEqual(_ordered(self._expected_one_wstl), _ordered(await obj.json()))

    async def test_get_not_acceptable(self) -> None:
        """
        Checks if a GET request fails with status 406 when an unacceptable ACCEPT header is provided. The test will be
        skipped if the expected WeSTL data (``_expected_one_wstl``) is not defined.
        """
        if not self._expected_one_wstl:
            self.skipTest('self._expected_one_wstl is not defined')
        obj = await self.client.request('GET',
                                        (self._href / self._id()).path,
                                        headers={**self._headers, hdrs.ACCEPT: 'application/msword'})
        self.assertEqual(406, obj.status)

    async def test_get_duplicate_form(self) -> None:
        """
        Checks if a GET request for a copy of WeSTL data from the duplicator succeeds and returns the expected data
        (``_expected_one_wstl_duplicate_form``). The test will be skipped if the expected WeSTL data
        (``_expected_one_wstl_duplicate_form``) is not defined.
        """
        if not self._expected_one_duplicate_form:
            self.skipTest('self._expected_one_duplicate_wstl is not defined')
        obj = await self.client.request('GET',
                                        (self._href / self._id() / 'duplicator').path,
                                        headers=self._headers)
        self.assertEqual(_ordered(self._expected_one_duplicate_form), _ordered(await obj.json()))

    async def test_opener_header(self) -> None:
        """
        Checks if a GET request for the opener for the data succeeds and has the expected LOCATION header
        (``_expected_opener``). The test will be skipped if the expected header value (``_expected_opener``) is not
        defined.
        """
        if not self._expected_opener:
            self.skipTest('self._expected_opener is not defined')
        obj = await self.client.request('GET',
                                        (self._href / self._id() / 'opener').path,
                                        headers=self._headers)
        self.assertEqual(self._expected_opener, obj.headers[hdrs.LOCATION])

    async def test_opener_body(self) -> None:
        """
        Checks if a GET request for the opener for the data succeeds and has the expected body
        (``_expected_opener_body``). The test will be skipped if the expected body (``_expected_opener_body``) is not
        defined.
        """
        if not self._expected_opener_body:
            self.skipTest('self._expected_opener_body is not defined')
        obj = await self.client.request('GET',
                                        (self._href / self._id() / 'opener').path,
                                        headers=self._headers)
        self.assertEqual(_ordered(self._expected_opener_body), _ordered(await obj.json()))

    async def test_get_content(self) -> None:
        """
        Checks if a GET request for the content succeeds and returns the expected data (in ``_content``). The test will
        be skipped if either the expected content (``_content``) or the collection name (``_coll``) is not defined.
        """
        if not self._content:
            self.skipTest('self._content is not defined')
            return
        if not self._coll:
            self.skipTest('self._coll is not defined')
            return
        async with self.client.request('GET',
                                       (self._href / self._id() / 'content').path,
                                       headers=self._headers) as resp:
            expected = self._content[self._coll][self._id()]
            if isinstance(expected, (dict, list)):
                self.assertEqual(_ordered(expected), _ordered(await resp.json()))
            elif isinstance(expected, str):
                self.assertEqual(expected, await resp.text())
            else:
                self.assertEqual(expected, await resp.read())

    async def test_get_content_type(self) -> None:
        """
        Checks if a GET request for the content succeeds and returns the expected content type. The test will be skipped
        if either the expected content (``_content``) or the content type (``_content_type``) is not defined.
        """
        if not self._content:
            self.skipTest('self._content is not defined')
        if not self._content_type:
            self.skipTest('self._content_type is not defined')
        obj = await self.client.request('GET',
                                        (self._href / self._id() / 'content').path,
                                        headers=self._headers)
        flag = True
        try:
            self.assertEqual(self._content_type, obj.headers.get(hdrs.CONTENT_TYPE))
            obj.close()
            flag = False
        finally:
            if flag:
                try:
                    obj.close()
                except OSError:
                    pass

    def _id(self):
        """Get the ID for the expected JSON."""
        logging.getLogger(__name__).debug('Collection is %s', self._body_put)
        for e in self._expected_one[0]['collection']['items'][0]['data']:
            if e['name'] == 'id':
                return e.get('value')


class GetAllMixin(_Base):
    """Tester mixin for GET requests that request all the objects in some path."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def test_get_all(self) -> None:
        """Checks if a GET request for all the items succeeds with status 200."""
        obj = await self.client.request('GET',
                                        (self._href / '').path,
                                        headers=self._headers)
        self.assertEqual(200, obj.status)

    async def test_get_all_json(self) -> None:
        """
        Checks if a GET request for all the items as JSON succeeds and returns the expected value
        (``_expected_all``).
        """
        obj = await self.client.request('GET',
                                        (self._href / '').path,
                                        headers=self._headers)
        self.assertEqual(_ordered(self._expected_all), _ordered(await obj.json()))

    async def test_get_all_wstl(self) -> None:
        """
        Checks if a GET request for all the items as WeSTL JSON succeeds and returns the expected value
        (``_expected_all_wstl``). The test will be skipped if the expected WeSTL JSON (``_expected_all_wstl``) is not
        defined.
        """
        if not self._expected_all_wstl:
            self.skipTest('self._expected_all_wstl is not defined')
        obj = await self.client.request('GET',
                                        (self._href / '').path,
                                        headers={**self._headers, hdrs.ACCEPT: wstljson.MIME_TYPE})
        self.assertEqual(_ordered(self._expected_all_wstl), _ordered(await obj.json()))


class DeleteMixin(_Base):
    """Tester mixin for DELETE requests."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def test_delete_success(self) -> None:
        """Checks if a DELETE request for the expected GET target succeeds with status 204."""
        obj = await self.client.request('DELETE',
                                        (self._href / self._id()).path,
                                        headers=self._headers)
        self.assertEqual(204, obj.status)

    async def test_delete_fail(self) -> None:
        """Checks if a DELETE request for a target with an invalid ID fails with status 404."""
        obj = await self.client.request('DELETE',
                                        (self._href / '3').path,
                                        headers=self._headers)
        self.assertEqual(404, obj.status)

    def _id(self):
        """Gets the ID of the expected GET data."""
        logging.getLogger(__name__).debug('Collection is %s', self._body_put)
        for e in self._expected_one[0]['collection']['items'][0]['data']:
            if e['name'] == 'id':
                return e.get('value')


def _copy_heaobject_dict_with(d, changes):
    """
    Copies the given dictionary and updates it with the given changes.

    :param d: The HEA object dictionary that will be changed
    :param changes: The changes being made, expressed as a dictionary
    :return: A copy of the given dictionary with the given changes
    """
    copied_dict = dict(d)
    copied_dict.update(changes)
    return copied_dict


def _to_xwwwformurlencoded_data(template) -> str:
    """
    Converts data in the given template to encoded form data.

    :param template: The template that contains data that will be converted
    :return: The data from the template converted to encoded form data
    """
    _logger = logging.getLogger(__name__)
    _logger.debug('Encoding %s', template)
    e = {}
    jsonschemavalidator.CJ_TEMPLATE_SCHEMA_VALIDATOR.validate(template)
    for e_ in template['template']['data']:
        if 'section' in e_:
            raise jsonschemavalidator.ValidationError('XWWWFormUrlEncoded does not support the section property')
        if e_['value'] is not None:
            e[e_['name']] = e_['value']
    result = urlencode(e, True)
    _logger.debug('Returning %s', result)
    return result


def _ordered(obj):
    """
    Sorts the JSON dictionaries to ensure consistency when comparing values.

    :param obj: The object to be ordered
    :return: The ordered object
    :except TypeError: When the type of the contents of obj, if it is a list, cannot be sorted with ``sorted``
    """
    if isinstance(obj, dict):
        def _ordered_one(k, v):
            if k == 'rel' and isinstance(v, str):
                return k, _ordered(' '.join(sorted(v.split() if v else [])))
            else:
                return k, _ordered(v)
        return sorted((_ordered_one(k, v) for k, v in obj.items()))
    if isinstance(obj, list):
        try:
            return sorted(_ordered(x) for x in obj)
        except TypeError as t:
            print('obj is {}'.format(obj))
            raise t
    else:
        return str(obj)
