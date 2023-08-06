# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pygui']

package_data = \
{'': ['*'], 'pygui': ['fonts/*']}

install_requires = \
['PyOpenGL>=3.1.6,<4.0.0', 'glfw>=2.5.3,<3.0.0', 'imgui[glfw]>=1.4.1,<2.0.0']

setup_kwargs = {
    'name': 'py-gui-tool',
    'version': '1.0.0',
    'description': 'PyGui is an easy to use gui.',
    'long_description': None,
    'author': 'hostedposted',
    'author_email': 'hostedpostedsite@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
