# CHIME/FRB API

|   **`Build`**   | **`Coverage`**  |  **`Release`**  |   **`Style`**   |
|-----------------|-----------------|-----------------|-----------------|
|[![Continous Deployment](https://github.com/CHIMEFRB/frb-api/actions/workflows/cd.yml/badge.svg)](https://github.com/CHIMEFRB/frb-api/actions/workflows/cd.yml) | [![codecov](https://codecov.io/gh/CHIMEFRB/frb-api/branch/main/graph/badge.svg?token=ALG4K6S75M)](https://codecov.io/gh/CHIMEFRB/frb-api) | [![PyPI version](https://img.shields.io/pypi/v/chime-frb-api.svg)](https://pypi.org/project/chime-frb-api/) | [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://black.readthedocs.io/en/stable/)

--------

`chime-frb-api` is a python library to access CHIME/FRB backend. This library enables you interact with resources such as databases, event headers, calibration products, cluster jobs etc.

Check out the **[documentation](https://chimefrb.github.io/frb-api/)** for more details.

## Installation

The latest stable version is available on [PyPI](https://pypi.org/project/chime-frb-api/). 
To install `chime-frb-api` simply run,

```bash
pip install --upgrade chime-frb-api
```

To add `chime-frb-api` to your project,

```bash
poetry add chime-frb-api
```

## Usage

```python
from chime_frb_api.backends import frb_master

master = frb_master.FRBMaster()
master.events.get_event(65540476)
{
    "beam_numbers": [185, 1185, 2185, 3185],
    "event_type": "EXTRAGALACTIC",
    "fpga_time": 271532193792,
    "id": 65540476,
}
```

## Documentation

For further reading, please refer to the [documentation](https://chimefrb.github.io/frb-api/).
