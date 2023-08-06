# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['matrix_photos']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'SQLAlchemy',
 'aiohttp',
 'aiosqlite',
 'asyncpg',
 'mautrix>=0.14.10,<0.15.0',
 'psycopg2-binary',
 'pycryptodome',
 'python-olm',
 'pyyaml>=6.0.0,<7.0.0',
 'unpaddedbase64']

setup_kwargs = {
    'name': 'matrix-photos',
    'version': '0.0.5b7',
    'description': 'A matrix client for the photOS DIY photoframe',
    'long_description': "# matrix-photos\n\n[![Latest PyPI version](https://img.shields.io/pypi/v/matrix-photos)](https://pypi.org/project/matrix-photos/)\n[![Development](https://github.com/universalappfactory/matrix-photos/actions/workflows/run-checks.yml/badge.svg)](https://github.com/universalappfactory/matrix-photos/actions/workflows/run-checks.yml)\n\nThis aims to be a simple [matrix](https://matrix.org/) client for the photOS DIY photoframe.\n\nMatrix is an open standard for secure, decentralised, real-time communication.\n\nFor photOS please checkout https://github.com/avanc/photOS for more information.\n\nThis client can be used to transfer files (pictures/photos) to the photoframe with end to end encryption support.\nThe idea is, that trusted users just can create a matrix room and invite the photoframe matrix user.\nThe photoframe user will automatically join this room and download all media sent to this room (You can specify which mimetypes are allowed).\n\n## Configuration\n\nThere is a config-example.yml in this project which should be mostly self-explaining.\n\nIt is possible to add textmessages to the images. This is done with the tool 'convert'.\nThe client automatically adds the first message after you post media content to the latest image when write_text_messages is set to true.\n\nYou can also optionally define an admin_user which can run some administration commands on the photoframe.\nIf you define an admin user then just send !help from the specified user to the chatroom and the client sends you a list of available commands.\n\n## Running\n\nJust create a virtual environement install the requirements and you can run the client.\n\n```\n    python -m matrix_photos -c /path/to/config.yml\n```\n\n## Development\n\nIf you want to develop or test the client, there is a docker-compose file in the docker directory which starts a matrix synapse homeserver,\na postgres database, an element matrix client and pgadmin if you want to check the database.\n",
    'author': 'universalappfactory',
    'author_email': 'info@universalappfactory.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/universalappfactory/matrix-photos',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
