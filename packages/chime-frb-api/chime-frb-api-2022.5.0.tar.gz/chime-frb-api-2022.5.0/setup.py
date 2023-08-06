# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chime_frb_api',
 'chime_frb_api.backends',
 'chime_frb_api.core',
 'chime_frb_api.modules',
 'chime_frb_api.stations',
 'chime_frb_api.tests',
 'chime_frb_api.workflow',
 'chime_frb_api.workflow.daemons']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=21.2,<22.0',
 'pyjwt>=2.4',
 'python-dateutil>=2.8,<3.0',
 'requests>=2.22,<3.0']

extras_require = \
{'docs': ['mkdocstrings>=0.16',
          'pytkdocs[numpy-style]>=0.10',
          'mkdocs-material>=8']}

setup_kwargs = {
    'name': 'chime-frb-api',
    'version': '2022.5.0',
    'description': 'CHIME/FRB API',
    'long_description': '# CHIME/FRB API\n\n|   **`Build`**   | **`Coverage`**  |  **`Release`**  |   **`Style`**   |\n|-----------------|-----------------|-----------------|-----------------|\n|[![Continous Deployment](https://github.com/CHIMEFRB/frb-api/actions/workflows/cd.yml/badge.svg)](https://github.com/CHIMEFRB/frb-api/actions/workflows/cd.yml) | [![codecov](https://codecov.io/gh/CHIMEFRB/frb-api/branch/main/graph/badge.svg?token=ALG4K6S75M)](https://codecov.io/gh/CHIMEFRB/frb-api) | [![PyPI version](https://img.shields.io/pypi/v/chime-frb-api.svg)](https://pypi.org/project/chime-frb-api/) | [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://black.readthedocs.io/en/stable/)\n\n--------\n\n`chime-frb-api` is a python library to access CHIME/FRB backend. This library enables you interact with resources such as databases, event headers, calibration products, cluster jobs etc.\n\nCheck out the **[documentation](https://chimefrb.github.io/frb-api/)** for more details.\n\n## Installation\n\nThe latest stable version is available on [PyPI](https://pypi.org/project/chime-frb-api/). \nTo install `chime-frb-api` simply run,\n\n```bash\npip install --upgrade chime-frb-api\n```\n\nTo add `chime-frb-api` to your project,\n\n```bash\npoetry add chime-frb-api\n```\n\n## Usage\n\n```python\nfrom chime_frb_api.backends import frb_master\n\nmaster = frb_master.FRBMaster()\nmaster.events.get_event(65540476)\n{\n    "beam_numbers": [185, 1185, 2185, 3185],\n    "event_type": "EXTRAGALACTIC",\n    "fpga_time": 271532193792,\n    "id": 65540476,\n}\n```\n\n## Documentation\n\nFor further reading, please refer to the [documentation](https://chimefrb.github.io/frb-api/).\n',
    'author': 'Shiny Brar',
    'author_email': 'charanjotbrar@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/CHIMEFRB/frb-api',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
