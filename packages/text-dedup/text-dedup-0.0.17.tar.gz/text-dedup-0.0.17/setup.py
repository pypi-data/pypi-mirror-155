# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['text_dedup', 'text_dedup.embedders', 'text_dedup.utils']

package_data = \
{'': ['*']}

install_requires = \
['annoy>=1.17.0,<2.0.0',
 'datasets>=2.2.2,<3.0.0',
 'datasketch>=1.5.7,<2.0.0',
 'hydra-core>=1.2.0,<2.0.0',
 'numpy==1.22.3',
 'redis>=4.3.3,<5.0.0',
 'sentencepiece>=0.1.96,<0.2.0',
 'torch>=1.11.0,<2.0.0',
 'tqdm>=4.64.0,<5.0.0',
 'transformers>=4.19.4,<5.0.0']

setup_kwargs = {
    'name': 'text-dedup',
    'version': '0.0.17',
    'description': '',
    'long_description': None,
    'author': 'Chenghao Mou',
    'author_email': 'mouchenghao@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
