# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_qiyu_sso',
 'django_qiyu_sso.logic',
 'django_qiyu_sso.migrations',
 'django_qiyu_sso.views']

package_data = \
{'': ['*'], 'django_qiyu_sso': ['templates/user/*']}

install_requires = \
['django-qiyu-utils>=0.4,<0.5', 'django>=3.2,<4.1', 'qiyu-sso>=0.2.10,<0.3']

setup_kwargs = {
    'name': 'django-qiyu-sso',
    'version': '0.6.3',
    'description': 'QiYu SSO intergation for Django',
    'long_description': '# Django QiYu SSO\n\nQiYu SSO django integration\n\n![PyPI - Version](https://img.shields.io/pypi/v/django-qiyu-sso)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-qiyu-sso)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/py_apple_signin)\n![PyPI - Wheel](https://img.shields.io/pypi/wheel/django-qiyu-sso)\n![GitHub repo size](https://img.shields.io/github/repo-size/qiyutechdev/py_apple_signin)\n![Lines of code](https://img.shields.io/tokei/lines/github/qiyutechdev/py_apple_signin)\n\n## WARNING\n\n    This is a WIP project, is not stablized!\n    USE AT YOUR OWN RISK!\n\n## 警告\n\n    当前并不稳定.\n    使用风险自负!\n',
    'author': 'dev',
    'author_email': 'dev@qiyutech.tech',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.qiyutech.tech/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
