# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nemo_bo',
 'nemo_bo.acquisition_functions',
 'nemo_bo.acquisition_functions.expected_improvement',
 'nemo_bo.acquisition_functions.nsga_improvement',
 'nemo_bo.models',
 'nemo_bo.models.base',
 'nemo_bo.opt',
 'nemo_bo.utils']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=21.4.0,<22.0.0',
 'botorch>=0.6.4,<0.7.0',
 'cython>=0.29.30,<0.30.0',
 'forestci>=0.5.1,<0.6.0',
 'gpytorch>=1.6.0,<2.0.0',
 'hyperopt>=0.2.7,<0.3.0',
 'matplotlib>=3.5.2,<4.0.0',
 'ngboost>=0.3.12,<0.4.0',
 'numba>=0.55.1,<0.56.0',
 'numpy>=1.22.4,<2.0.0',
 'openpyxl>=3.0.9,<4.0.0',
 'pandas>=1.4.2,<2.0.0',
 'pymoo>=0.5.0,<0.6.0',
 'scikit-learn>=1.1.1,<2.0.0',
 'scipy>=1.8.1,<2.0.0',
 'six>=1.16.0,<2.0.0',
 'smt>=1.2.0,<2.0.0',
 'tensorflow-probability>=0.17.0,<0.18.0',
 'tensorflow>=2.9.1,<3.0.0',
 'torch>=1.11.0,<2.0.0',
 'xgboost-distribution>=0.2.4,<0.3.0']

setup_kwargs = {
    'name': 'nemo-bo',
    'version': '0.1.6',
    'description': 'Multi-objective optimization of chemical processes with automated machine learning workflows',
    'long_description': '#nemo\n\nMulti-objective optimization of chemical processes with automated machine learning model selection',
    'author': 'Simon Sung',
    'author_email': 'simon.sung06@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sustainable-processes/NEMO',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.0,<=3.9.13',
}


setup(**setup_kwargs)
