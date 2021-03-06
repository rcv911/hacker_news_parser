from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='hacker_news_parser',
    version='0.1.0',
    url='https://github.com/rcv911/hacker_news_parser.git',
    install_requires=[
        'requests',
        'aiohttp',
        'aiohttp-rest-api',
        'beautifulsoup4',
        'pytest',
        'pytest-aiohttp'
    ],
    include_package_data=True,
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    license='Free',
    author='chub',
    author_email='r.chub90@yandex.ru',
    description='',
)
