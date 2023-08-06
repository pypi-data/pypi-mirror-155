# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hisoka']

package_data = \
{'': ['*']}

install_requires = \
['catboost>=1.0,<2.0',
 'pandas>=1.3,<2.0',
 'scikit-learn>=0.23,<0.24',
 'shap>=0.40,<0.41',
 'xgboost>=1.5,<2.0']

setup_kwargs = {
    'name': 'hisoka',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Caio Martins',
    'author_email': 'caio.outmatched@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.2,<4.0.0',
}


setup(**setup_kwargs)
