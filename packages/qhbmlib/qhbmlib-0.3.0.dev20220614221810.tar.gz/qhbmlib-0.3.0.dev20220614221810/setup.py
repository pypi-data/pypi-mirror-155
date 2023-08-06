# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qhbmlib', 'qhbmlib.data', 'qhbmlib.inference', 'qhbmlib.models']

package_data = \
{'': ['*']}

install_requires = \
['tensorflow-probability==0.15.0',
 'tensorflow-quantum==0.6.1',
 'tensorflow==2.7.0']

extras_require = \
{':extra == "doc"': ['Sphinx>=4.5.0,<5.0.0',
                     'sphinx-rtd-theme>=1.0.0,<2.0.0',
                     'myst-parser>=0.17.2,<0.18.0']}

setup_kwargs = {
    'name': 'qhbmlib',
    'version': '0.3.0.dev20220614221810',
    'description': 'Quantum Hamiltonian-Based Models built on TensorFlow Quantum',
    'long_description': '# QHBM Library\n\nThis repository is a collection of tools for building and training\nQuantum Hamiltonian-Based Models.  These tools depend on\n[TensorFlow Quantum](https://www.tensorflow.org/quantum),\nand are thus compatible with both real and simulated quantum computers.\n\n[Installation instructions](https://github.com/google/qhbm-library/blob/main/docs/INSTALL.md) and [contribution instructions](https://github.com/google/qhbm-library/blob/main/docs/contributing.md) can be found in the docs folder.\n\nThis is not an officially supported Google product.\n',
    'author': 'The QHBM Library Authors',
    'author_email': 'no-reply@google.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/google/qhbm-library',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)
