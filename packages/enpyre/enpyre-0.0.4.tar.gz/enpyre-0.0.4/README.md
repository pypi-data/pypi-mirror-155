<p align="center">
  <img src="https://user-images.githubusercontent.com/7717842/173475640-ab6ca0fe-7a92-4369-92c3-3c9b72cdb21f.jpg" alt="enpyre-logo" width="358" />
</p>

<h1 align="center">
  Enpyre
</h1>

<p align="center">
  <strong>A Python game engine in React.</strong>
  <br />
  <sub>Write python games that run in React applications 👌</sub>
</p>

<br />

<p align="center">
  <a href="https://github.com/Enpyre/engine/actions/workflows/build_and_deploy.yml" target="_blank"><img src="https://github.com/Enpyre/engine/actions/workflows/build_and_deploy.yml/badge.svg" alt="build status" /></a>
<!--   <a href="https://www.npmjs.com/package/enpyre/" target="_blank"><img src="https://img.shields.io/npm/v/enpyre/latest" alt="npm version" /></a> -->
  <a href="https://github.com/Enpyre/engine/blob/main/LICENSE" target="_blank"><img src="https://img.shields.io/badge/License-MPL_2.0-brightgreen.svg" alt="license" /></a>
</p>

<br />

Enpyre is an open-source library to render 2D games made with Python in React with graphics by <a href="http://www.pixijs.com/">PIXI.js</a> and the power of <a href="https://pyodide.org/en/stable/">Pyodide</a>, <a href="https://webassembly.org/">WASM</a>, and modern web technologies.

## Install and Usage

Enpyre python engine only works inside Pyodide environment.

### With Enpyre npm package

Just start a React project and add [enpyre](https://www.npmjs.com/package/enpyre) package.

### Standalone

Start a [pyodide](https://pyodide.org/en/stable/usage/quickstart.html) environment and install [enpyre]() pip package by micropip:
```js
await pyodide.loadPackage('micropip');
await pyodide.runPythonAsync(`
    import micropip
    await micropip.install('enpyre')
    from enpyre import *
`);
```

## Example games

See [examples](https://github.com/Enpyre/engine/tree/main/src/examples) of usage.

## Development

### Install Poetry

- OSX/Linux: `curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -`
- Windows: `(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python -`

### Install dependencies

`poetry install`

### Pre commit install

`pre-commit install`

### Run server

`./start.sh`

### Local package

Set you web appliction to install enpyre package from `http://localhost:8080/enpyre-0.0.1-py3-none-any.whl`
