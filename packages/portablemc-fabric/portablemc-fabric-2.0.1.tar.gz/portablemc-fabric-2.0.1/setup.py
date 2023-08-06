# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['portablemc_fabric']

package_data = \
{'': ['*']}

install_requires = \
['portablemc>=3,<4']

setup_kwargs = {
    'name': 'portablemc-fabric',
    'version': '2.0.1',
    'description': "Start Minecraft using the Fabric mod loader using '<exec> start fabric:[<mc-version>[:<loader-version>]]'.",
    'long_description': '# Fabric add-on\nThe fabric add-on allows you to install and run Minecraft with fabric mod loader in a single command \nline!\n\n![PyPI - Version](https://img.shields.io/pypi/v/portablemc-fabric?label=PyPI%20version&style=flat-square) &nbsp;![PyPI - Downloads](https://img.shields.io/pypi/dm/portablemc-fabric?label=PyPI%20downloads&style=flat-square)\n\n```console\npip install --user portablemc-fabric\n```\n\n## Usage\nThis add-on extends the syntax accepted by the [start](/README.md#start-the-game) sub-command, by \nprepending the version with `fabric:`. Almost all releases since 1.14 are supported by fabric,\nyou can find more information on [fabric website](https://fabricmc.net/develop/), note the snapshots\nare currently not supported by this addon, but this could be the case in the future because fabric\nprovides support for them. You can also use version aliases like `release` or equivalent empty version \n(just `fabric:`). This addon also provides a way of specifying the loader version, you just have to \nadd `:<loader_version>` after the game version (the game version is still allowed to be aliases \nor empty, the following syntax is valid: `fabric::<loader_version>`).\n\nThis addon requires external HTTP accesses if:\n- the game version is an alias.\n- if the loader version is unspecified.\n- if the specified version is not installed.\n\n## Examples\n```sh\nportablemc start fabric:                # Start latest fabric loader version for latest release\nportablemc start fabric:release         # Same as above\nportablemc start fabric:1.19            # Start latest fabric loader version for 1.19\nportablemc start fabric:1.19:0.14.8     # Start fabric loader 0.14.8 for game version 1.19\nportablemc start fabric::0.14.8         # Start fabric loader 0.14.8 for the latest release\nportablemc start --dry fabric:          # Install (and exit) the latest fabric loader version for latest release\n```\n\n![fabric animation](/doc/assets/fabricmc.gif)\n\n## Credits\n- [Fabric Website](https://fabricmc.net/)\n',
    'author': 'Théo Rozier',
    'author_email': 'contact@theorozier.fr',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
