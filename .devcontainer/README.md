# Development container

This directory contains a set of files to set up a reproducible and disposable development environment in Visual Studio Code using the [Remote - Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers).

## Supported features

- Pre-installed tools/packages required for local development
- Pre-configured VSCode settings and extensions

## Prerequisites

- [Visual Studio Code](https://code.visualstudio.com/)
- [Remote - Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
- [Docker](https://www.docker.com/)

## Getting started

1. Open the repository in VSCode
2. Press `Ctrl/Cmd+Shift+P` to launch [the command palette](https://code.visualstudio.com/docs/getstarted/userinterface#_command-palette)
3. Select `Remote-Containers: Reopen in Container`
4. Once the devcontainer is up and running, launch the command palette again
5. Select `Terminal: Create New Terminal`
6. Run the following commands and make sure they run successfully:

```bash
python -V
pip -V
pyenv --version
pytest -V
```
