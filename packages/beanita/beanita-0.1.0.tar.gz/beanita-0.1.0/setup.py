# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['beanita']

package_data = \
{'': ['*']}

install_requires = \
['mongita>=1.1.1,<2.0.0']

setup_kwargs = {
    'name': 'beanita',
    'version': '0.1.0',
    'description': 'Local MongoDB-like database, based on Mongita and prepared to work with Beanie ODM',
    'long_description': '## Beanita\n\nLocal MongoDB-like database, based on [Mongita](https://github.com/scottrogowski/mongita) and prepared to work with [Beanie ODM](https://github.com/roman-right/beanie)\n\nI highly recommend using it only for experiment purposes. It is safer to use a real MongoDB database and for testing, and for production.\n\n### Init\n\n```python\nfrom beanie import init_beanie, Document\nfrom beanita import Client\n\n\nclass Sample(Document):\n    name: str\n\n\nasync def init_database():\n    cli = Client("LOCAL_DIRECTORY")\n    db = cli["DATABASE_NAME"]\n    await init_beanie(\n        database=db,\n        document_models=[Sample],\n    )\n```\n\n### Not supported\n\n- Links\n- Aggregations\n- Union Documents\n- other features, that were not implemented in Mongita',
    'author': 'Roman Right',
    'author_email': 'roman-right@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/roman-right/beanita',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
