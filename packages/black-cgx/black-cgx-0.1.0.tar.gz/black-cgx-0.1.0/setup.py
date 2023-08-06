# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['black_cgx']
install_requires = \
['black>=22.3', 'collagraph>=0.4']

extras_require = \
{':python_version < "3.11"': ['tomli>=1.1.0']}

entry_points = \
{'console_scripts': ['black-cgx = black_cgx:main']}

setup_kwargs = {
    'name': 'black-cgx',
    'version': '0.1.0',
    'description': 'Black for cgx files',
    'long_description': '# Black-cgx\n\nFormat CGX files with black.\n\n\n## Usage\n\n```sh\n# Install in your environment (for example with poetry)\npoetry add -D black-cgx\n# Show help for the tool\npoetry run black-cgx -h\n# By default, will format every cgx file in current folder (recursively)\npoetry run black-cgx\n# Just check if there would be any changes\npoetry run black-cgx --check\n# Format just a single file\npoetry run black-cgx my-component.cgx\n# Format a folder and file\npoetry run black-cgx ../folder_with_cgx_files my-component.cgx\n```\n',
    'author': 'Berend Klein Haneveld',
    'author_email': 'berendkleinhaneveld@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
