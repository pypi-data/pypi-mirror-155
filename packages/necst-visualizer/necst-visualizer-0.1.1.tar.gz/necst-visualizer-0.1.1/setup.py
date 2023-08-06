# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['necst_visualizer']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.4.3,<4.0.0',
 'n-const>=1.0.4,<2.0.0',
 'neclib>=0.7.0,<0.8.0',
 'necstdb>=0.2.5,<0.3.0',
 'xarray>=0.20.0,<0.21.0']

extras_require = \
{':python_version < "3.8"': ['astropy>=3.0,<4.0'],
 ':python_version >= "3.8"': ['astropy>=5.0.4,<6.0.0']}

setup_kwargs = {
    'name': 'necst-visualizer',
    'version': '0.1.1',
    'description': '',
    'long_description': '# necst-visualizer\n\n[![PyPI](https://img.shields.io/pypi/v/necst-visualizer.svg?label=PyPI&style=flat-square)](https://pypi.org/pypi/necst-visualizer/)\n[![Python](https://img.shields.io/pypi/pyversions/necst-visualizer.svg?label=Python&color=yellow&style=flat-square)](https://pypi.org/pypi/necst-visualizer/)\n[![Test](https://img.shields.io/github/workflow/status/nanten2/necst-visualizer/Test?logo=github&label=Test&style=flat-square)](https://github.com/nanten2/necst-visualizer/actions)\n[![License](https://img.shields.io/badge/license-MIT-blue.svg?label=License&style=flat-square)](LICENSE)\n\nSimulate necst system\n\n## Features\nThis package provides:\n- Check scanning path\n\n## Installation\n```\npip install necst-visualizer\n```\n\n## Usage\n\nSee the [API reference](https://nanten2.github.io/necst-visualizer/_source/necst_visualizer.html).',
    'author': 'FumikaDemachi',
    'author_email': 'f.demachi@a.phys.nagoya-u.ac.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nanten2/necst-visualizer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)
