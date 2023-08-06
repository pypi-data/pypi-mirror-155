# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scraping_subsystem',
 'scraping_subsystem.kafka_handler',
 'scraping_subsystem.scraper',
 'scraping_subsystem.scraper.spiders',
 'scraping_subsystem.sentiment_analyzer']

package_data = \
{'': ['*']}

modules = \
['README']
install_requires = \
['Scrapy==2.6.1',
 'bs4==0.0.1',
 'dostoevsky==0.6.0',
 'fasttext==0.9.2',
 'kafka-python==2.0.2',
 'nltk==3.7',
 'pandas==1.3.2']

setup_kwargs = {
    'name': 'scrapingsubsystem',
    'version': '0.1.5',
    'description': 'scraping subsystem library for airflow',
    'long_description': None,
    'author': 'DieNice',
    'author_email': 'DailyPlanning@bk.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8.0,<3.9.0',
}


setup(**setup_kwargs)
