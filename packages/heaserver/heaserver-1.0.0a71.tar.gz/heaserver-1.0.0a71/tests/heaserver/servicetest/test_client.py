from aiohttp.test_utils import AioHTTPTestCase
from aiohttp import web, TCPConnector, ClientSession
from heaserver.service import client, runner, response
from heaserver.service.aiohttp import AsyncReader
from heaobject.folder import Folder
from heaobject import user
import json
from heaobject.root import json_dumps
from heaserver.service import appproperty


class TestClient(AioHTTPTestCase):

    async def setUpAsync(self):
        await super().setUpAsync()
        self.__body = {
            'created': None,
            'derived_by': None,
            'derived_from': [],
            'description': None,
            'display_name': 'Reximus',
            'id': None,
            'invites': [],
            'modified': None,
            'name': 'reximus',
            'owner': user.NONE_USER,
            'shares': [],
            'source': None,
            'type': 'heaobject.folder.Folder',
            'version': None,
            'mime_type': 'application/x.folder'
        }
        self.app[appproperty.HEA_CLIENT_SESSION] = ClientSession(connector=TCPConnector(), connector_owner=True,
                                                                 json_serialize=json_dumps,
                                                                 raise_for_status=True)

    async def tearDownAsync(self) -> None:
        await super().tearDownAsync()
        await self.app[appproperty.HEA_CLIENT_SESSION].close()

    async def get_application(self):
        async def test_folder_get(request):
            return web.Response(status=200,
                                body=json.dumps([self.__body]),
                                content_type='application/json')

        async def test_get_content(request):
            return await response.get_streaming(request, AsyncReader(b'The quick brown fox jumped over the lazy dogs'))

        async def test_get_content_client(request):
            return await client.get_streaming(request, f'http://127.0.0.1:{request.url.port}/testgetcontent')

        async def test_get(request):
            obj = await client.get(request.app, f'http://127.0.0.1:{request.url.port}/folders', Folder)
            return web.Response(status=200,
                                body=obj.json_dumps() if obj is not None else None,
                                content_type='application/json')

        app = runner.get_application()
        app.router.add_get('/folders', test_folder_get)
        app.router.add_get('/testget', test_get)
        app.router.add_get('/testgetcontent', test_get_content)
        app.router.add_get('/testgetcontentclient', test_get_content_client)

        return app

    async def test_get(self):
        obj = await self.client.request('GET', '/testget')
        self.assertEqual(self.__body, await obj.json())

    async def test_get_content(self):
        obj = await self.client.request('GET', '/testgetcontentclient')
        self.assertEqual(b'The quick brown fox jumped over the lazy dogs', await obj.read())

