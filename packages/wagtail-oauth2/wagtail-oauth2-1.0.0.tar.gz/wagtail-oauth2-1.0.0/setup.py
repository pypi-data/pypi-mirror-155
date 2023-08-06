# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['wagtail_oauth2', 'wagtail_oauth2.tests']

package_data = \
{'': ['*'], 'wagtail_oauth2': ['templates/*']}

install_requires = \
['Django>=3.2.0,<5', 'requests>=2.26.0', 'wagtail>=2.14,<4.0']

setup_kwargs = {
    'name': 'wagtail-oauth2',
    'version': '1.0.0',
    'description': 'OAuth2.0 authentication fo wagtail',
    'long_description': '==============\nWagtail OAuth2\n==============\n\n.. image:: https://readthedocs.org/projects/wagtail-oauth2/badge/?version=latest\n   :target: https://wagtail-oauth2.readthedocs.io/en/latest/?badge=latest\n   :alt: Documentation Status\n\n.. image:: https://github.com/Gandi/wagtail-oauth2/actions/workflows/main.yml/badge.svg\n   :target: https://github.com/Gandi/wagtail-oauth2/actions/workflows/main.yml\n   :alt: Build Status\n\n\n.. image:: https://codecov.io/gh/Gandi/wagtail-oauth2/branch/main/graph/badge.svg?token=VN14GVV3Y0\n   :target: https://codecov.io/gh/Gandi/wagtail-oauth2\n   :alt: Coverage\n\n\nPlugin to replace Wagtail default login by an OAuth2.0 Authorization Server.\n\nWhat is wagtail-oauth2\n----------------------\n\nOAuth2.0 is an authorization framework widely used and usually,\nOAuth2.0 authorization servers grant authorization on authenticated user.\n\n\nThe OAuth2 Authorization is used as an **identity provider**.\n\n\nRead More\n---------\n\nYou can read the `full documentation of this library here`_.\n\n\n.. _`full documentation of this library here`: https://wagtail-oauth2.readthedocs.io/en/latest/',
    'author': 'Guillaume Gauvrit',
    'author_email': 'guillaume@gandi.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://wagtail-oauth2.readthedocs.io/en/latest/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
