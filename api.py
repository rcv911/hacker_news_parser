from aiohttp import web
from aiohttp.web import Application
from aiohttp_rest_api.loader import \
    load_and_connect_all_endpoints_from_folder
import logging
import pathlib
import pytoml as toml
import os
import requests
from bs4 import BeautifulSoup
import datetime
import time
import asyncio
from connection import Connection
from models.posts import Posts


BASE_DIR = pathlib.Path(__file__).parent.parent
PACKAGE_NAME = 'app'
log = logging.getLogger(__name__)


def load_config(config_path: str) -> dict:
    """
    Загрузка конфигурации приложения

    :param
        * *config_path* (``str``) -- путь к конфигу

    :rtype: (``dict``)
    :return: конфиг приложения
    """
    with open(f'{os.getcwd()}{config_path}') as f:
        conf = toml.load(f)
    return conf


def init_app(config: dict) -> Application:
    """
    Инициализация web приложения

    :param
        * *config* (``dict``) -- конфиг приложения

    :rtype: (``Application``)
    :return: web приложение
    """
    parser_config = config.get('parser', {})
    db_conf = config.get('db')
    dsn = f'{db_conf.get("driver")}://{db_conf.get("username")}:' \
        f'{db_conf.get("password")}@{db_conf.get("host")}:' \
        f'{db_conf.get("port")}/{db_conf.get("name")}'
    db = Connection(dsn=dsn)

    loop = asyncio.get_event_loop()
    app = web.Application()
    app['db'] = db
    app['config'] = config
    loop.create_task(timer(loop, app['db'], parser_config))

    load_and_connect_all_endpoints_from_folder(
        path='{0}/{1}'.format(os.path.dirname(os.path.realpath(__file__)),
                              'endpoints'),
        app=app,
        version_prefix='v1'
    )

    log.debug(app['config'])
    return app


def to_dict(obj, class_name=Posts):
    """ Превращение в словарь """
    res = dict()
    for col in class_name.__table__.columns:
        res[col.name] = getattr(obj, col.name)
    return res


def get_data(db: Connection, url: str):
    """
    Получение данных из парсинга сайта

    :param
        * *db* (``Connection``) -- соединение к БД
    :param
        * *url* (``str``) -- url сайта для парсинга

    :rtype (``None``)
    :return:
    """
    query = db.session.query(Posts).order_by(Posts.id.desc()).limit(30)
    titles = tuple(x.title for x in query)

    response = requests.get(url, headers={'Connection': 'close'})
    soup = BeautifulSoup(response.text, "html.parser")

    data = soup.find_all('tr', class_='athing')
    for el in data:
        soup_content = el.find('a', class_='storylink')
        if soup_content.text not in titles:
            content = Posts(**{
                'title': soup_content.text,
                'url': soup_content.get('href'),
                'created': datetime.datetime.now().isoformat(),
            })
            to_database(db, content)

    db.session.commit()


async def timer(loop, db: Connection, parser_config: dict):
    """
    Таймер, который запускает парсинг данных через заданный промежуток времени

    :param
        * *loop* (``asyncio EventLoop``) -- текущий event loop
    :param
        * *db* (``Connection``) -- соединение к БД
    :param
        * *parser_config* (``dict``) -- конфиг парсера

    :rtype (``None``)
    :return:
    """
    now = loop.time()
    delay = parser_config.get('delay')
    url = parser_config.get('url')
    log.info(f'clock time: {time.time()}')
    log.info(f'loop  time: {now}')
    while True:
        loop.call_soon(get_data, db, url)
        await asyncio.sleep(delay)


def to_database(db: Connection, obj: Posts):
    """ Запись в БД """
    db.session.add(obj)
    try:
        db.session.flush()
    except Exception as e:
        db.session.rollback()
        log.info(e)


def main(config_path: str):
    """
    Запуск REST API

    :param
        * *config_path* (``str``) -- путь к конфигу

    :rtype (``None``)
    :return:
    """
    log.debug(f'config_path - {config_path}')

    config = load_config(config_path)

    logging.basicConfig(level=logging.DEBUG)
    app = init_app(config)
    app_config = config.get('app', None)

    web.run_app(app, port=app_config.get('port', 9999))


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="Provide path to config file")
    args = parser.parse_args()

    if args.config:
        main(args.config)
    else:
        parser.print_help()
