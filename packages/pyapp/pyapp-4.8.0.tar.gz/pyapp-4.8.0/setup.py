# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pyapp',
 'pyapp.app',
 'pyapp.checks',
 'pyapp.conf',
 'pyapp.conf.helpers',
 'pyapp.conf.loaders',
 'pyapp.extensions',
 'pyapp.utils',
 'tests',
 'tests.app',
 'tests.checks',
 'tests.conf',
 'tests.conf.helpers',
 'tests.conf.loaders',
 'tests.extensions',
 'tests.factory',
 'tests.sample_app',
 'tests.sample_ext',
 'tests.sample_ext_simple',
 'tests.utils']

package_data = \
{'': ['*'], 'tests': ['fixtures/*']}

install_requires = \
['argcomplete', 'colorama', 'yarl']

extras_require = \
{'toml': ['toml'], 'yaml': ['pyyaml']}

setup_kwargs = {
    'name': 'pyapp',
    'version': '4.8.0',
    'description': 'A Python application framework - Let us handle the boring stuff!',
    'long_description': '######################################\npyApp - A python application framework\n######################################\n\n*Let us handle the boring stuff!*\n\n+---------+------------------------------------------------------------------------------------------------------------+\n| Docs    | .. image:: https://readthedocs.org/projects/pyapp/badge/?version=latest                                    |\n|         |    :target: https://docs.pyapp.info/                                                                       |\n|         |    :alt: ReadTheDocs                                                                                       |\n+---------+------------------------------------------------------------------------------------------------------------+\n| Build   | .. image:: https://api.dependabot.com/badges/status?host=github&repo=pyapp-org/pyapp                       |\n|         |    :target: https://dependabot.com                                                                         |\n|         |    :alt: Dependabot Status                                                                                 |\n+---------+------------------------------------------------------------------------------------------------------------+\n| Quality | .. image:: https://sonarcloud.io/api/project_badges/measure?project=pyapp-org_pyapp&metric=sqale_rating    |\n|         |    :target: https://sonarcloud.io/dashboard?id=pyapp-org_pyapp                                             |\n|         |    :alt: Maintainability                                                                                   |\n|         | .. image:: https://sonarcloud.io/api/project_badges/measure?project=pyapp-org_pyapp&metric=security_rating |\n|         |    :target: https://sonarcloud.io/project/security_hotspots                                                |\n|         |    :alt: Security                                                                                          |\n|         | .. image:: https://sonarcloud.io/api/project_badges/measure?project=pyapp-org_pyapp&metric=coverage        |\n|         |    :target: https://sonarcloud.io/code?id=pyapp-org_pyapp                                                  |\n|         |    :alt: Test Coverage                                                                                     |\n|         | .. image:: https://img.shields.io/badge/code%20style-black-000000.svg                                      |\n|         |    :target: https://github.com/ambv/black                                                                  |\n|         |    :alt: Once you go Black...                                                                              |\n+---------+------------------------------------------------------------------------------------------------------------+\n| Package | .. image:: https://img.shields.io/pypi/v/pyapp                                                             |\n|         |    :target: https://pypi.io/pypi/pyapp/                                                                    |\n|         |    :alt: Latest Version                                                                                    |\n|         | .. image:: https://img.shields.io/pypi/pyversions/pyapp                                                    |\n|         |    :target: https://pypi.io/pypi/pyapp/                                                                    |\n|         | .. image:: https://img.shields.io/pypi/l/pyapp                                                             |\n|         |    :target: https://pypi.io/pypi/pyapp/                                                                    |\n|         | .. image:: https://img.shields.io/pypi/wheel/pyapp                                                         |\n|         |    :alt: PyPI - Wheel                                                                                      |\n|         |    :target: https://pypi.io/pypi/pyapp/                                                                    |\n+---------+------------------------------------------------------------------------------------------------------------+\n\npyApp takes care of the boring boilerplate code for building a CLI, managing\nsettings and much more so you can focus on your application logic.\n\nSo what does pyApp handle?\n==========================\n\n- **Configuration** - Loading, merging your settings from different sources\n\n  + Python modules\n  + File and HTTP(S) endpoints for JSON and YAML files.\n\n- **Instance Factories** - Configuration of plugins, database connections, or just\n  implementations of an ``ABC``.\n  Leveraging settings to make setup of your application easy and reduce coupling.\n\n- **Dependency Injection** - Easy to use dependency injection without complicated setup.\n\n- **Checks** - A framework for checking settings are correct and environment is\n  operating correctly (your ops team will love you)?\n\n- **Extensions** - Extend the basic framework with extensions. Provides deterministic\n  startup, extension of the CLI and the ability to register checks and extension\n  specific default settings.\n\n- **Application** - Provides a extensible and simple CLI interface for running\n  commands (including async), comes with built-in commands to execute check, setting\n  and extension reports.\n\n- **Logging** - Initialise and apply sane logging defaults.\n\n- Highly tested and ready for production use.\n\n\nExtensions\n==========\n\n- 🔌 SQLAlchemy - `pyapp.sqlalchemy`_\n- 🔌 Redis - `pyapp.redis`_\n\nIn Beta\n-------\n\n- 🐛 Rollbar - `pyapp.rollbar`_\n\n- 📧 AIO SMTPlib - `pyapp.aiosmtplib`_ Extension for aiosmtplib\n\n- ☁ Boto3 - `pyapp.boto3`_\n\n- ☁ AIOBotocore - `pyapp.aiobotocore`_\n\n- 📨 Messaging - `pyapp.messaging`_ - Extension to provide abstract interfaces for Message Queues.\n\n  - 📨 AWS Messaging - `pyapp.messaging-aws`_ - Messaging extension for AWS (SQS/SNS)\n\nIn development\n--------------\n\n- 📧 SMTP - `pyapp.SMTP`_\n\n- 📨 Aio-Pika - `pyapp.aiopika`_ - Messaging extension for pika (RabbitMQ/AMQP)\n\n- 🔌 PySpark - `pyapp.pyspark`_ - Extension for PySpark\n\n- 🔎 Elastic Search - `pyapp.elasticsearch`_ - Extension for Elasticsearch\n\nComing soon\n-----------\n\n- 📨 AMQP Messaging - Messaging extension for AMQP (RabbitMQ)\n\n\n.. _pyapp.sqlalchemy: https://www.github.com/pyapp-org/pyapp.sqlalchemy\n.. _pyapp.redis: https://www.github.com/pyapp-org/pyapp.redis\n.. _pyapp.aiobotocore: https://www.github.com/pyapp-org/pyapp.aiobotocore\n.. _pyapp.SMTP: https://www.github.com/pyapp-org/pyapp.SMTP\n.. _pyapp.boto3: https://www.github.com/pyapp-org/pyapp.boto3\n.. _pyapp.rollbar: https://www.github.com/pyapp-org/pyapp.rollbar\n.. _pyapp.aiosmtplib: https://www.github.com/pyapp-org/pyapp.aiosmtplib\n.. _pyapp.messaging: https://www.github.com/pyapp-org/pyapp-messaging\n.. _pyapp.messaging-aws: https://www.github.com/pyapp-org/pyapp-messaging-aws\n.. _pyapp.aiopika: https://www.github.com/pyapp-org/pyapp.aiopika\n.. _pyapp.pyspark: https://www.github.com/pyapp-org/pyapp.pyspark\n.. _pyapp.elasticsearch: https://www.github.com/pyapp-org/pyapp.elasticsearch\n\n\nContributions\n=============\n\nContributions are most welcome, be it in the form of a extension and factories\nfor your favourite service client of bug reports, feature enhancements.\n\nThe core of pyApp is intended to remain simple and only provide required features\nwith extensions providing optional more specific functionality.\n\n',
    'author': 'Tim Savage',
    'author_email': 'tim@savage.company',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pyapp-org/pyapp',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
