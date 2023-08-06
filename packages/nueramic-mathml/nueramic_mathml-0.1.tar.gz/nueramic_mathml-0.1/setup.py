# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['nueramic_mathml', 'nueramic_mathml.ml']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.21.6,<2.0.0', 'torch>=1.11.0,<2.0.0']

setup_kwargs = {
    'name': 'nueramic-mathml',
    'version': '0.1',
    'description': 'Math algorithms in ML on torch',
    'long_description': '.. -*- mode: rst -*-\n   \n|PyPi|_ |Python|_ |Download|_ |License|_ |RTD|_\n\n\n------\n\n.. |PyPi| image:: https://img.shields.io/pypi/v/nueramic-mathml?color=edf2f4&style=flat-square\n.. _PyPi: https://pypi.org/project/nueramic-mathml/\n\n\n.. |Python| image:: https://img.shields.io/pypi/pyversions/p?color=edf2f4&style=flat-square\n.. _Python: https://github.com/nueramic/mathml\n\n.. |Download| image:: https://img.shields.io/pypi/dm/nueramic-mathml?color=edf2f4&label=dowloads&style=flat-square\n.. _Download: https://pypi.org/project/nueramic-mathml/\n\n.. |License| image:: https://img.shields.io/github/license/nueramic/mathml?color=edf2f4&style=flat-square\n.. _License: https://github.com/nueramic/mathml\n\n.. |RTD| image:: https://img.shields.io/readthedocs/nueramic-mathml?color=edf2f4&style=flat-square\n.. _RTD: https://nueramic-mathml.readthedocs.io\n\n.. |Colab_1| image:: https://colab.research.google.com/assets/colab-badge.svg\n.. _Colab_1: https://colab.research.google.com/drive/19moQvDMK8kfTDYOGuRwEl06jdf_KXNMW?usp=sharing\n\n.. image:: docs/_static/nueramic-logo-cropped-black.svg\n    :width: 200\n    :align: center\n\n..\n    .. raw:: html\n\n       <p align="center">\n       <picture align="center">\n         <source width=150px" media="(prefers-color-scheme: dark)" srcset="docs/_static/nueramic-logo-cropped-white.svg">\n         <source width=150px" media="(prefers-color-scheme: light)" srcset="docs/_static/nueramic-logo-cropped-black.svg">\n         <img alt="two logos" src="docs/_static/nueramic-logo-cropped-black.svg">\n       </picture>\n       </p>\n   \nNueramic MathML\n===============\nNueramic-mathml is a library for visualizing and logging the steps of basic optimization algorithms in machine learning. The project uses torch for calculations and plotly for visualization.\n\n.. code-block:: python\n\n  pip install nueramic-mathml\n\n\nQuick tour  |Colab_1|_\n======================\n\nYou can minimize the functions and see a detailed description of each step. After minimizing, you have a history with complete logs.\n\n.. code-block:: python\n   \n   a\n\n\n',
    'author': 'Victor Barbarich',
    'author_email': 'vktrbr@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nueramic/mathml',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
