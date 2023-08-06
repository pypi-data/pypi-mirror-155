# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['asqlite']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'rapptz-asqlite',
    'version': '1.0.1',
    'description': 'A simple async wrapper for sqlite3',
    'long_description': '### asqlite\n\nThis package is a fork of rapptz\'s asqlite. asqlite is a simple and easy to use async wrapper for `sqlite3`.\n\nThis is basically the same as `sqlite3` except you use `async with` and `await` in front of most operations.\n\n```python\nimport asyncio\nimport asqlite\n\nasync def main():\n    async with asqlite.connect(\'example.db\') as conn:\n        async with conn.cursor() as cursor:\n            # Create table\n            await cursor.execute(\'\'\'CREATE TABLE stocks\n                                    (date text, trans text, symbol text, qty real, price real)\'\'\')\n\n            # Insert a row of data\n            await cursor.execute("INSERT INTO stocks VALUES (\'2006-01-05\',\'BUY\',\'RHAT\',100,35.14)")\n\n            # Save (commit) the changes\n            await conn.commit()\n\nasyncio.run(main())\n```\n\n### Differences from `sqlite3`\n\nThis module differs from `sqlite3` in a few ways:\n\n1. Connections are created with `journal_mode` set to `wal`.\n2. Connections have foreign keys enabled by default.\n3. [Implicit transactions are turned off][implicit-transactions]\n4. The [`row_factory`][row_factory] is set to [`sqlite3.Row`][Row].\n\n[implicit-transactions]: https://docs.python.org/3/library/sqlite3.html#controlling-transactions\n[row_factory]: https://docs.python.org/3/library/sqlite3.html#sqlite3.Connection.row_factory\n[Row]: https://docs.python.org/3/library/sqlite3.html#sqlite3.Row\n\n### License\n\nMIT\n',
    'author': 'Rapptz',
    'author_email': None,
    'maintainer': 'Seon82',
    'maintainer_email': None,
    'url': 'https://github.com/Rapptz/asqlite',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.5',
}


setup(**setup_kwargs)
