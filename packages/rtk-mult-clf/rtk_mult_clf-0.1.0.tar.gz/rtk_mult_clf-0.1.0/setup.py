# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rtk_mult_clf',
 'rtk_mult_clf.datamodules',
 'rtk_mult_clf.features',
 'rtk_mult_clf.models',
 'rtk_mult_clf.predictor',
 'rtk_mult_clf.utils']

package_data = \
{'': ['*']}

install_requires = \
['catboost>=1.0.6,<2.0.0',
 'dvc[gdrive]>=2.11.0,<3.0.0',
 'hydra-colorlog>=1.2.0,<2.0.0',
 'hydra-core>=1.2.0,<2.0.0',
 'numpy>=1.22.4,<2.0.0',
 'openpyxl>=3.0.10,<4.0.0',
 'pandas>=1.4.2,<2.0.0',
 'python-dotenv>=0.20.0,<0.21.0',
 'pytorch-lightning>=1.6.4,<2.0.0',
 'razdel>=0.5.0,<0.6.0',
 'rich>=12.4.4,<13.0.0',
 'scikit-learn>=1.1.1,<2.0.0',
 'sentence-transformers>=2.2.0,<3.0.0',
 'torch>=1.11.0,<2.0.0',
 'tqdm>=4.64.0,<5.0.0',
 'wandb>=0.12.18,<0.13.0']

setup_kwargs = {
    'name': 'rtk-mult-clf',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'exotol',
    'author_email': 'artem.bardakov@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
