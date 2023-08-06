# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sphinxcontrib']

package_data = \
{'': ['*']}

install_requires = \
['BudouX', 'Sphinx', 'beautifulsoup4']

setup_kwargs = {
    'name': 'sphinxcontrib-budoux',
    'version': '0.1.4',
    'description': 'This is Sphinx extension to break line of heading texts by BudouX.',
    'long_description': '====================\nsphinxcontrib-budoux\n====================\n\nOverview\n========\n\nThis is Sphinx extension to break line of heading texts by BudouX.\n\nSimple example\n--------------\n\nFrom source is:\n\n.. code-block:: rst\n\n   あなたに寄り添う最先端のテクノロジー\n   ====================================\n\nOutput without this is:\n\n.. code-block:: html\n\n   <h1>あなたに寄り添う最先端のテクノロジー</h1>\n\nOutput with this is:\n\n.. code-block:: html\n\n   <h1 style="word-break: keep-all; overflow-wrap: break-word;">あなたに<wbr/>寄り添う<wbr/>最先端の<wbr/>テクノロジー</h1>\n\nInstallation\n============\n\n.. code-block:: console\n\n   pip install sphinxcontrib-budoux\n\nUsage\n=====\n\n.. code-block:: python\n\n   extensions = [\n       "sphinxcontrib.budoux",\n   ]\n   \n   # Tag to ijnect for splitted texts\n   budoux_split_tag = "wbr"\n   # Style for splitted-tag\n   budoux_split_style = "budoux_split_style", "word-break: keep-all; overflow-wrap: break-word;"\n   # Target tags for apply BudouX\n   budoux_targets = ["h1", "h2"]\n\nNote\n====\n\nMain targets for edit are heading text, not but contents of paragraph.\n\nIf you set ``p``, ``li`` and others into `budoux_targets``, this may not work correctly that you think.\n\nExample\n=======\n\nSee `doc <doc/>`_ (written by Japanese).\n',
    'author': 'Kazuya Takei',
    'author_email': 'myself@attakei.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
