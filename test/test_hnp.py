import pathlib
import json
from test.get_app import init_test_app


BASE_DIR = pathlib.Path(__file__).parent.parent
config_path = '/config/config.toml'


def start_app():
    return init_test_app(f'{BASE_DIR}{config_path}')


class TestHackerNewsParser:

    async def test_get_posts(self, aiohttp_client):
        app = start_app()
        client = await aiohttp_client(app)
        response = await client.get('/v1/posts')
        assert response.status == 200
        text = await response.text()
        print(text)
        body = response.__dict__
        data = json.loads(body.get("_body"))
        assert isinstance(data, list)
        assert len(data) == 5
        print(f'---------------------------------')

    async def test_get_10_posts(self, aiohttp_client):
        app = start_app()
        client = await aiohttp_client(app)
        response = await client.get('/v1/posts?limit=10')
        assert response.status == 200
        text = await response.text()
        print(text)
        body = response.__dict__
        data = json.loads(body.get("_body"))
        assert isinstance(data, list)
        assert len(data) == 10
        print(f'---------------------------------')

    async def test_get_offset_posts(self, aiohttp_client):
        app = start_app()
        client = await aiohttp_client(app)
        response = await client.get('/v1/posts?limit=7&offset=1')
        assert response.status == 200
        text = await response.text()
        print(text)
        body = response.__dict__
        data = json.loads(body.get("_body"))
        assert isinstance(data, list)
        assert len(data) == 7
        print(f'---------------------------------')

    async def test_get_asc_id_posts(self, aiohttp_client):
        app = start_app()
        client = await aiohttp_client(app)
        response = await client.get('/v1/posts?sort=asc')
        assert response.status == 200
        text = await response.text()
        print(text)
        body = response.__dict__
        data = json.loads(body.get("_body"))
        assert isinstance(data, list)
        assert len(data) == 5
        print(f'---------------------------------')

    async def test_get_desc_id_posts(self, aiohttp_client):
        app = start_app()
        client = await aiohttp_client(app)
        response = await client.get('/v1/posts?sort=desc')
        assert response.status == 200
        text = await response.text()
        print(text)
        body = response.__dict__
        data = json.loads(body.get("_body"))
        assert isinstance(data, list)
        assert len(data) == 5
        print(f'---------------------------------')

    async def test_get_title_desc_posts(self, aiohttp_client):
        app = start_app()
        client = await aiohttp_client(app)
        response = await client.get('/v1/posts?order=title')
        assert response.status == 200
        text = await response.text()
        print(text)
        body = response.__dict__
        data = json.loads(body.get("_body"))
        assert isinstance(data, list)
        assert len(data) == 5
        print(f'---------------------------------')

    async def test_get_title_asc_posts(self, aiohttp_client):
        app = start_app()
        client = await aiohttp_client(app)
        response = await client.get('/v1/posts?order=title&sort=asc')
        assert response.status == 200
        text = await response.text()
        print(text)
        body = response.__dict__
        data = json.loads(body.get("_body"))
        assert isinstance(data, list)
        assert len(data) == 5
        print(f'---------------------------------')

    async def test_get_combine_posts(self, aiohttp_client):
        app = start_app()
        client = await aiohttp_client(app)
        response = await client.get(
            '/v1/posts?order=title&sort=asc&limit=10&offset=2')
        assert response.status == 200
        text = await response.text()
        print(text)
        body = response.__dict__
        data = json.loads(body.get("_body"))
        assert isinstance(data, list)
        assert len(data) == 10
        print(f'---------------------------------')
