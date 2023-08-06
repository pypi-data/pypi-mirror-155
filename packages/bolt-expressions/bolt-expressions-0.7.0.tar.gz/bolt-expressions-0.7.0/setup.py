# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bolt_expressions']

package_data = \
{'': ['*']}

install_requires = \
['beet>=0.55.0', 'bolt>=0.3.3', 'mecha>=0.48.1', 'nbtlib==1.12.1']

setup_kwargs = {
    'name': 'bolt-expressions',
    'version': '0.7.0',
    'description': 'Provides pandas-like expressions capabilities to the bolt extension of mecha',
    'long_description': '# bolt-expressions\n\n[![GitHub Actions](https://github.com/rx-modules/bolt-expressions/workflows/CI/badge.svg)](https://github.com/rx-modules/bolt-expressions/actions)\n[![PyPI](https://img.shields.io/pypi/v/bolt-expressions.svg)](https://pypi.org/project/bolt-expressions/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/bolt-expressions.svg)](https://pypi.org/project/bolt-expressions/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n[![Discord](https://img.shields.io/discord/900530660677156924?color=7289DA&label=discord&logo=discord&logoColor=fff)](https://discord.gg/98MdSGMm8j)\n\n> a `pandas`-esque API for creating expressions within bolt\n\n## Introduction\n\nBolt is a scripting language which mixes both python and mcfunction. This package amplifies this language by adding an API for creating fluent expressions loosely based off of the `pandas` syntax. These expressions are use for simplifying large bits of scoreboard and storage operation allowing you to swiftly create complex operations with the ease of normal programming.\n\n```py\nfrom bolt_expressions import Scoreboard\n\nmath = Scoreboard.objective("math")\n# or `math = Scoreboard("math")`\n\nmath["@s"] = math["@r"] * 10 + math["@r"] + 100\n```\n->\n```mcfunction\nscoreboard players operations $i0 bolt.expressions.temp = @r math\nscoreboard players operations $i0 bolt.expressions.temp *= #10 bolt.expressions.int\nscoreboard players operations $i1 bolt.expressions.temp = @r math\nscoreboard players add $i1 bolt.expressions.temp 100\nscoreboard players operations $i0 bolt.expressions.temp += $i1 bolt.expressions.temp\nscoreboard players operations @s math = $i0 bolt.expressions.temp\n```\n\n## Installation\n\nThe package can be installed with `pip`. Note, you must have `beet`, `mecha` and `bolt` installed to use this package.\n\n```bash\n$ pip install bolt-expressions\n```\n\n## Getting started\n\nThis package is designed to be used within any `bolt` script (either a `.mcfunction` or `bolt` file) inside a `bolt` enabled project.\n\n```yaml\nrequire:\n    - bolt\n\npipeline:\n    - mecha\n```\n\nOnce you\'ve enabled bolt, you are able to import the python package directly inside your bolt script.\n\n```py\nfrom bolt_expressions import Scoreboard, Storage\n```\n\nAny usage of the `bolt_expressions` package will require you to inject the current beet context into the API objects. Then, you can create an objective and start creating expressions.\n\n```py\nmath = Scoreboard.objective("math")\nentity_id = Scoreboard.objective("entity_id")\n\nmath["@s"] += 10\n```\n\n## Features\n\n- Robust API supporting Scoreboards, Storage, Blocks, and Entities\n- Provides an interface to manipulate large, complex mathematical expressions simplily\n- Allows you to interopt custom variables with normal commands *(soon)*\n\nCheckout some examples over at our [docs](https://rx-modules.github.io/bolt-expressions/)!\n\n## Contributing\n\nContributions are welcome. Make sure to first open an issue discussing the problem or the new feature before creating a pull request. The project uses [`poetry`](https://python-poetry.org).\n\n```bash\n$ poetry install\n```\n\nYou can run the tests with `poetry run pytest`.\n\n```bash\n$ poetry run pytest\n```\n\nThe project must type-check with [`pyright`](https://github.com/microsoft/pyright). If you\'re using VSCode the [`pylance`](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) extension should report diagnostics automatically. You can also install the type-checker locally with `npm install` and run it from the command-line.\n\n```bash\n$ npm run watch\n$ npm run check\n```\n\nThe code follows the [`black`](https://github.com/psf/black) code style. Import statements are sorted with [`isort`](https://pycqa.github.io/isort/).\n\n```bash\n$ poetry run isort bolt_expressions examples tests\n$ poetry run black bolt_expressions examples tests\n$ poetry run black --check bolt_expressions examples tests\n```\n\n---\n\nLicense - [MIT](https://github.com/rx-modules/bolt-expressions/blob/main/LICENSE)\n',
    'author': 'rx97',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rx-modules/bolt-expressions',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
