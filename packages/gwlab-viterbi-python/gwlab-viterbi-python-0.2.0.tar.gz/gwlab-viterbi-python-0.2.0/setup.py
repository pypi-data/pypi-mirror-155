# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gwlab_viterbi_python',
 'gwlab_viterbi_python.tests',
 'gwlab_viterbi_python.utils',
 'gwlab_viterbi_python.utils.tests']

package_data = \
{'': ['*']}

install_requires = \
['graphene-file-upload>=1.3.0,<2.0.0',
 'gwdc-python>=0.4.0,<0.5.0',
 'importlib-metadata>=4.5.0,<5.0.0',
 'jwt>=1.2.0,<2.0.0',
 'requests>=2.25.1,<3.0.0',
 'tqdm>=4.61.2,<5.0.0']

extras_require = \
{'docs': ['Sphinx>=4.0.2,<5.0.0', 'sphinx-rtd-theme>=0.5.2,<0.6.0']}

setup_kwargs = {
    'name': 'gwlab-viterbi-python',
    'version': '0.2.0',
    'description': 'Wrapper of GWDC API, used for interacting with the GWLab Viterbi endpoint',
    'long_description': None,
    'author': 'Thomas Reichardt',
    'author_email': 'treichardt@swin.edu.au',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
