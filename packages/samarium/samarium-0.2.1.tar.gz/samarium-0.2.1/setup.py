# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['samarium']

package_data = \
{'': ['*'], 'samarium': ['modules/*']}

install_requires = \
['termcolor>=1.1.0,<2.0.0']

entry_points = \
{'console_scripts': ['samarium = samarium.__main__:main',
                     'samarium-debug = samarium.__main__:main_debug']}

setup_kwargs = {
    'name': 'samarium',
    'version': '0.2.1',
    'description': 'The Samarium Programming Language',
    'long_description': '# Samarium\n\nSamarium is a dynamic interpreted language transpiled to Python.\nSamarium, in its most basic form, doesn\'t use any digits or letters.\n\nHere\'s a `Hello, World!` program written in Samarium:\n\n<span style="display: inline-block" align="left">\n    <img src="docs/assets/example.png" width="50%">\n</span>\n\nDocumentation on how to program in Samarium can be found [here](https://samarium-lang.github.io/Samarium/).\n\n\n# Installation\n\n## [pip](https://pypi.org/project/pip/)\n\n`pip install samarium`\n\n## [AUR](https://aur.archlinux.org/)\n\n`git clone https://aur.archlinux.org/samarium.git; cd samarium; makepkg -sirc` or use your favorite [AUR helper](https://wiki.archlinux.org/title/AUR_helpers).\n\n## Using Samarium\n\nYou can run Samarium programs with `samarium program.sm`.\n`samarium-debug` may be used instead, which will first print out the intermediary Python code that the Samarium program is transpiled into, before executing it.\n\nShort | Long | Description\n:---: | :---: | :---\n`-c <cmd>` | `--command <cmd>` | Can be used to execute Samarium code from the string `cmd`,<br>directly in the terminal. `cmd` can be one or more statements<br>separated by semicolons as usual. Note that the last statement<br> of `cmd` will be printed if it does not end in a semicolon.\n`-h` | `--help` | Shows the help message\n`-v` | `--version` | Prints Samarium version\n\n\nThere is also a VSCode syntax highlighting extension for Samarium, which can be found here [here](https://marketplace.visualstudio.com/items?itemName=Samarium.samarium-language). The source code can be found [here](https://github.com/samarium-lang/vscode-samarium).\n\n\n# Credits\n\nSamarium was inspired by several languages, including [brainfuck](https://esolangs.org/wiki/Brainfuck), [Rust](https://www.rust-lang.org/), [Java](https://www.java.com/) and [Python](https://www.python.org/).\nThanks to:\n- [tetraxile](https://github.com/tetraxile) for helping with design choices and writing the docs\n- [MithicSpirit](https://github.com/MithicSpirit) for making an AUR package for Samarium\n- [DarviL82](https://github.com/DarviL82) for fixing some issues\n- [Endercheif](https://github.com/Endercheif) for making the documentation look fancy\n\nIf you have any questions, or would like to get in touch, join the [Discord server](https://discord.gg/C8QE5tVQEq)!\n',
    'author': 'trag1c',
    'author_email': 'trag1cdev@yahoo.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9',
}


setup(**setup_kwargs)
