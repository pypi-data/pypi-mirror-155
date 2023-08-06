# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['word2quiz']

package_data = \
{'': ['*'], 'word2quiz': ['locales/en/LC_MESSAGES/*']}

install_requires = \
['Pillow>=9.1.0,<10.0.0',
 'attrs>=21.4.0,<22.0.0',
 'docx2python>=2.0.4,<3.0.0',
 'python-docx>=0.8.11,<0.9.0',
 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'word2quiz',
    'version': '0.1.10',
    'description': 'Create quizzes in Canvas from simple Word docx files uaing Canvasapi. Not complete yet.',
    'long_description': '# word2quiz\nCreate quizzes in Canvas from simple Word docx files uaing Canvasapi.\nA library to use in webapp, commandline or gui program. I will add the canvasapi part and make \nit into a standalone tool\n\n\n',
    'author': 'Nico de Groot',
    'author_email': 'ndegroot0@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ndegroot/word2quiz',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
