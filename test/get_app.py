from aiohttp import web
from aiohttp.web import Application
from aiohttp_rest_api.loader import \
    load_and_connect_all_endpoints_from_folder
import logging
import pytoml as toml
import pathlib
from connection import Connection


BASE_DIR = pathlib.Path(__file__).parent.parent


def load_config_test(config_path: str) -> dict:
    with open(config_path) as f:
        conf = toml.load(f)
    return conf


def init_test_app(config_path: str) -> Application:
    config = load_config_test(config_path)
    db_conf = config.get('db')
    dsn = f'{db_conf.get("driver")}://{db_conf.get("username")}:' \
        f'{db_conf.get("password")}@{db_conf.get("host")}:' \
        f'{db_conf.get("port")}/{db_conf.get("name")}'
    db = Connection(dsn=dsn)

    app = web.Application()
    app['db'] = db
    app['config'] = config

    load_and_connect_all_endpoints_from_folder(
        path='{0}/{1}'.format(BASE_DIR, 'endpoints'),
        app=app,
        version_prefix='v1'
    )
    logging.basicConfig(level=logging.DEBUG)
    return app
