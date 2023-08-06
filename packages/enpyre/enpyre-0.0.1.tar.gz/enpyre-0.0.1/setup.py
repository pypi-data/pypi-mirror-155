# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['engine']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'enpyre',
    'version': '0.0.1',
    'description': 'A Python game engine for the browser',
    'long_description': '<p align="center">\n  <img src="https://user-images.githubusercontent.com/7717842/173475640-ab6ca0fe-7a92-4369-92c3-3c9b72cdb21f.jpg" alt="enpyre-logo" width="358" />\n</p>\n\n<h1 align="center">\n  Enpyre\n</h1>\n\n<p align="center">\n  <strong>A Python game engine in React.</strong>\n  <br />\n  <sub>Write python games that run in React applications 👌</sub>\n</p>\n\n<br />\n\n<p align="center">\n  <a href="https://github.com/Enpyre/engine/actions/workflows/build_and_deploy.yml" target="_blank"><img src="https://github.com/Enpyre/engine/actions/workflows/build_and_deploy.yml/badge.svg" alt="build status" /></a>\n<!--   <a href="https://www.npmjs.com/package/enpyre/" target="_blank"><img src="https://img.shields.io/npm/v/enpyre/latest" alt="npm version" /></a> -->\n  <a href="https://github.com/Enpyre/engine/blob/main/LICENSE" target="_blank"><img src="https://img.shields.io/badge/License-MPL_2.0-brightgreen.svg" alt="license" /></a>\n</p>\n\n<br />\n\nEnpyre is an open-source library to render 2D games made with Python in React with graphics by <a href="http://www.pixijs.com/">PIXI.js</a> and the power of <a href="https://pyodide.org/en/stable/">Pyodide</a>, <a href="https://webassembly.org/">WASM</a>, and modern web technologies.\n\n## Install and Usage\n\nEnpyre python engine only works inside Pyodide environment.\n\n### With Enpyre npm package\n\nJust start a React project and add [enpyre](https://www.npmjs.com/package/enpyre) package.\n\n### Standalone\n\nStart a [pyodide](https://pyodide.org/en/stable/usage/quickstart.html) environment and install [enpyre]() pip package by micropip:\n```js\nawait pyodide.loadPackage(\'micropip\');\nawait pyodide.runPythonAsync(`\n    import micropip\n    await micropip.install(\'enpyre\')\n    from enpyre import *\n`);\n```\n\n## Example games\n\nSee [examples](https://github.com/Enpyre/engine/tree/main/src/examples) of usage.\n\n## Development\n\n### Install Poetry\n\n- OSX/Linux: `curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -`\n- Windows: `(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python -`\n\n### Install dependencies\n\n`poetry install`\n\n### Pre commit install\n\n`pre-commit install`\n\n### Run server\n\n`./start.sh`\n\n### Local package\n\nSet you web appliction to install enpyre package from `http://localhost:8080/enpyre-0.0.1-py3-none-any.whl`\n',
    'author': 'Lucas Amoedo',
    'author_email': 'lucas.advc@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Enpyre/engine',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
