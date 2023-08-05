# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scbs']

package_data = \
{'': ['*']}

install_requires = \
['click-help-colors>=0.9,<1',
 'click>=7.1.2,<8.1',
 'colorama>=0.3.9,<1',
 'numba>=0.53.0,<1',
 'numpy>=1.20.1,<2',
 'pandas>=1.2.3,<2',
 'scipy>=1.6.1,<2',
 'statsmodels>=0.12.2,<1']

entry_points = \
{'console_scripts': ['scbs = scbs.cli:cli']}

setup_kwargs = {
    'name': 'scbs',
    'version': '0.3.4',
    'description': 'command line utility to work with single cell methylation data',
    'long_description': '# Command line utility for downstream analysis of single cell methylation data\n\n## Installation\n1. clone the repo\n```\ngit clone https://github.com/LKremer/scbs.git\n```\n2. install the package with Python3 pip\n```\npython3 -m pip install --upgrade pip  # you need a recent pip version\npython3 -m pip install scbs/dist/scbs-[choose-version].tar.gz\n```\nThe command line interface should now be available when typing the command `scbs` in a terminal. If this is the case, the installation is finished. If not, try these steps:  \nFirst, restart the terminal or use `source ~/.bashrc`. If that doesn\'t help, carefully check the output log of pip. Look for a message like `WARNING: The script scbs is installed in \'/home/ubuntu/.local/bin\' which is not on PATH.`, which would indicate that you need to add `/home/ubuntu/.local/bin` to your path. Alternatively, you can copy `/home/ubuntu/.local/bin/scbs` to e.g. `/usr/local/bin`.\n\n\n## Updating to the latest version\nJust use `--upgrade` when installing the package, otherwise it\'s the same process as installing:\n```\npython3 -m pip install --upgrade scbs/dist/scbs-[choose-version].tar.gz\n```\nAfterwards, make sure that the latest version is correctly installed:\n```\nscbs --version\n```\n\n## [Tutorial](docs/tutorial.md) of a typical `scbs` run\nA tutorial can be found [here](docs/tutorial.md).\n\nAlso make sure to read the help by typing `scbs --help`.\n\n\n## Troubleshooting\nIf you encounter a "too many open files" error during `scbs prepare` (`OSError: [Errno 24] Too many open files`), you need to increase the maximum number of files that can be opened. In Unix systems, try `ulimit -n 9999`.  \nIf you encounter problems during installation, make sure you have Python3.8 or higher. If the problem persists, consider installing scbs in a clean Python environment (for example using [venv](https://docs.python.org/3/library/venv.html)).\n\n\n## Contributors\n- [Lukas PM Kremer](https://github.com/LKremer)\n- [Leonie Küchenhoff](https://github.com/LeonieKuechenhoff)\n- [Alexey Uvarovskii](https://github.com/alexey0308)\n- [Simon Anders](https://github.com/simon-anders)\n',
    'author': 'Lukas PM Kremer',
    'author_email': 'L-Kremer@web.de',
    'maintainer': 'Lukas PM Kremer',
    'maintainer_email': 'L-Kremer@web.de',
    'url': 'https://github.com/LKremer/scbs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
