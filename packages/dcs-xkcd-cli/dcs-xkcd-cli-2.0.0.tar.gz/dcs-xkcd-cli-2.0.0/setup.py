# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xkcd_cli']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.1.1,<10.0.0',
 'beautifulsoup4>=4.11,<5.0',
 'requests>=2.27,<3.0',
 'typer>=0.4,<0.5']

entry_points = \
{'console_scripts': ['xkcd = xkcd_cli.xkcd:main']}

setup_kwargs = {
    'name': 'dcs-xkcd-cli',
    'version': '2.0.0',
    'description': 'Get your daily dose of xkcd directly from the terminal! 🤩',
    'long_description': '# xkcd cli tool\n\n<p align="center">\n<img alt="Lint and static code analysis on develop branch" src="https://github.com/dotcs/xkcd-cli/actions/workflows/lint-sca.yaml/badge.svg?branch=develop"/>\n<a href="https://github.com/dotcs/xkcd-cli/blob/main/LICENSE"><img alt="License: MIT" src="https://black.readthedocs.io/en/stable/_static/license.svg"/></a>\n<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"/></a>\n</p>\n\nGet your daily dose of [xkcd] directly from the terminal! 🤩\n\nhttps://user-images.githubusercontent.com/3976183/163873282-f586f312-2643-4b77-af79-89e344091b2f.mp4\n\n[xkcd] is a webcomic created by [Randall Munroe][munroe]. \nIt is a comic of Language, Math, Romance and Sarcasm and a [couple of other categories][explain-xkcd-categories].\n\nIf [kitty], [iterm] or any terminal that has support for the [sixel] file format is used as the terminal, the xkcd comic will be rendered directly in the terminal, otherwise the default viewer for PNG images is used.\nThis tool requires [fzf] to be installed on the machine to filter available comics by their title. \n\n## Installation\n\n### With pip\n\nInstall this package directly from the [Python Package Index (PyPI)][pypi-repo].\nThe CLI tool requires Python >= 3.8 to be installed.\n\n```console\n$ pip install dcs-xkcd-cli\n```\n\nThis will install a CLI tool named `xkcd` which can be used as described below.\n\n### With pipx\n\nInstallation with [pipx] is similar to the pip variant above, but uses `pipx` instead of `pip`.\n\n```console\n$ pipx install dcs-xkcd-cli\n```\n\nNote that with pipx, this package can be tried out without the need to install it permanently.\n\n```console\n$ pipx run dcs-xkcd-cli <args>\n```\n\n\n## Usage\n\n### Search by title\n\n```console\n$ xkcd show\n```\n\nThis functionality requires [fzf] to be installed.\n\n### Show latest xkcd comic\n\n```console\n$ xkcd show --latest\n```\n\n### Show random xkcd comic\n\n```console\n$ xkcd show --random\n```\n\n### Show xkcd comic by its ID\n\n```console\n$ xkcd show --comic-id 207\n```\n\n### Upscaling / width of comics\n\nBy default images are upscaled to match the terminal dimensions.\nThis behavior can be controlled with the `--terminal-scale-up / --no-terminal-scale-up` options.\nImages can be also rendered with an explicit width by using the `--width` CLI option.\n\n```console\n$ xkcd show --comic-id 207 --no-terminal-scale-up    # disable scaling\n$ xkcd show --comic-id 207 --width 1200              # set explicit width\n```\n\n\n### Disable rendering in terminals\n\n```console\n$ xkcd show --no-terminal-graphics\n```\n\nThis command will disable the automatic image protocol detection and directly open the image with the help of `xdg-open` in the default image viewer.\n\n### Disable or update cache\n\nUnder the hood this tool uses a cache which is updated once per day transparently.\nThe cache is used to remember the list of xkcd comics from the [archive].\n\nTo disable the cache, use the following command\n\n```console\n$ xkcd show --no-cache\n```\n\nTo update the cache manually, use the following command\n```console\n$ xkcd update-cache\n```\n\n## Development\n\nThis repository manages Python dependencies with [poetry].\nTo install the package and its dependencies run:\n\n```console\n$ poetry install\n```\n\nThe code is formatted with [black] and type checked with [pyright].\n\nThen run the the following commands to lint and test the code:\n\n```console\n$ poetry run python -m black --check --diff .   # tests for any lint issues\n$ poetry run python -m black .                  # auto-formats the code\n\n$ poetry run python -m pyright                  # runs static code analysis\n\n$ poetry run python -m pytest --cov="xkcd_cli/" --cov-report term --cov-report html   # run tests with code coverage report\n```\n\n\n[fzf]: https://github.com/junegunn/fzf\n[kitty]: https://sw.kovidgoyal.net/kitty/\n[archive]: https://xkcd.com/archive/\n[xkcd]: https://xkcd.com\n[munroe]: https://en.wikipedia.org/wiki/Randall_Munroe\n[explain-xkcd-categories]: https://www.explainxkcd.com/wiki/index.php/Category:Comics_by_topic\n[pypi-repo]: https://pypi.org/project/dcs-xkcd-cli/\n[pipx]: https://pypa.github.io/pipx/\n[iterm]: https://iterm2.com/\n[sixel]: https://en.wikipedia.org/wiki/Sixel\n[poetry]: https://python-poetry.org/\n[black]: https://black.readthedocs.io/en/stable/\n[pyright]: https://github.com/Microsoft/pyright\n',
    'author': 'dotcs',
    'author_email': 'repositories@dotcs.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dotcs/xkcd-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
