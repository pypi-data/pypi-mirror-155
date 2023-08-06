# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyariable']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyariable',
    'version': '0.5.0',
    'description': 'Placeholder variables to aid in testing.',
    'long_description': 'pyariable\n#########\n\nSimplify your test assertions forever.\n\n.. code-block:: python\n   :class: ignore\n\n   from pyariable import Variable\n\n   def test_dict():\n       x = Variable()\n       y = Variable()\n       assert {1: "XXX", 2: "XXX", 3: "YYY"} == {1: x, 2: x, 3: y}\n       assert x != y\n\nIn some tests it\'s common to get a random ID back from a database. Your assertions are simpler when you substitute a `Variable` object for the expected value.\n\n.. code-block:: python\n   :class: ignore\n\n   from pyariable import Variable\n\n   def test_list():\n       x = Variable()\n       y = Variable()\n       assert [\n           {"db_id": 590, "name": "alice"},\n           {"db_id": 590, "name": "bob"},\n           {"db_id": 999, "name": "charlie"},\n       ] == [\n           {"db_id": x, "name": "alice"},\n           {"db_id": x, "name": "bob"},\n           {"db_id": y, "name": "charlie"},\n       ]\n       assert x != y\n       assert x < y\n\n\nInstallation\n------------\n.. code-block:: bash\n   :class: ignore\n\n   pip install pyariable\n',
    'author': 'Willem Thiart',
    'author_email': 'himself@willemthiart.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/willemt/pyariable',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
