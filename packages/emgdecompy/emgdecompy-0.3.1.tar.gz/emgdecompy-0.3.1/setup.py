# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['emgdecompy']

package_data = \
{'': ['*']}

install_requires = \
['altair-data-server>=0.4.1,<0.5.0',
 'altair>=4.2.0,<5.0.0',
 'numpy>=1.22.3,<2.0.0',
 'pandas>=1.4.2,<2.0.0',
 'scipy>=1.8.0,<2.0.0',
 'sklearn>=0.0,<0.1']

setup_kwargs = {
    'name': 'emgdecompy',
    'version': '0.3.1',
    'description': 'A package for decomposing raw EMG signals into individual motor unit activity.',
    'long_description': '# EMGdecomPy\n\n[![ci-cd](https://github.com/UBC-SPL-MDS/emg-decomPy/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/UBC-SPL-MDS/emg-decomPy/actions/workflows/ci-cd.yml)\n[![codecov](https://codecov.io/gh/UBC-SPL-MDS/EMGdecomPy/branch/main/graph/badge.svg?token=78ZU40UEOE)](https://codecov.io/gh/UBC-SPL-MDS/EMGdecomPy)\n\nA package for decomposing raw EMG signals into individual motor unit activity.\n\n## Proposal\n\nOur project proposal can be found [here](https://github.com/UBC-SPL-MDS/emg-decomPy/blob/main/docs/proposal/proposal.pdf).\n\nTo generate the proposal locally, run the following command from the root directory:\n\n```Rscript -e "rmarkdown::render(\'docs/proposal/proposal.Rmd\')"```\n\n## Installation\n\n```bash\npip install emgdecompy\n```\n\n## Usage\n\n- TODO\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`emgdecompy` was created by Daniel King, Jasmine Ortega, Rada Rudyak, and Rowan Sivanandam. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`emgdecompy` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n\nThe data used for validation was obtained from [`Hug et al. (2021)`](https://figshare.com/articles/dataset/Analysis_of_motor_unit_spike_trains_estimated_from_high-density_surface_electromyography_is_highly_reliable_across_operators/13695937).\n',
    'author': 'Daniel King',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
