# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['summon']

package_data = \
{'': ['*']}

install_requires = \
['pluggy>=1.0.0,<2.0.0',
 'typer>=0.4.1,<0.5.0',
 'typing-extensions>=4.2.0,<5.0.0']

entry_points = \
{'console_scripts': ['summon = summon.__main__:main']}

setup_kwargs = {
    'name': 'summon-tasks',
    'version': '0.2.0',
    'description': '',
    'long_description': "Summon\n======\n\nSummon is a task runner, inspired by [Invoke](https://www.pyinvoke.org/), but\nentirely type-hint compatible.\n\nSummon is built upon [Typer](https://github.com/tiangolo/typer). Summon's tasks are\nTyper [commands](https://typer.tiangolo.com/tutorial/commands/))!\n\nSummon will run tasks from a `tasks.py` file, but also accepts plugins, powered\nby [pluggy](https://pluggy.readthedocs.io/en/stable/), meaning that shared\ntasks can be separated on a plugin package.\n",
    'author': 'Tarcísio Eduardo Moreira Crocomo',
    'author_email': 'tarcisioe@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
