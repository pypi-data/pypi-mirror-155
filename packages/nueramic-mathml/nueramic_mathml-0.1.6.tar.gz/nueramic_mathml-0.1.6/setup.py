# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['nueramic_mathml', 'nueramic_mathml.ml', 'nueramic_mathml.visualize']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.21.6,<2.0.0',
 'pandas>=1.3,<2.0',
 'plotly>=5.8.2,<6.0.0',
 'torch>=1.11.0,<2.0.0']

setup_kwargs = {
    'name': 'nueramic-mathml',
    'version': '0.1.6',
    'description': 'Math algorithms in ML on torch',
    'long_description': '.. -*- mode: rst -*-\n   \n|PyPi|_ |Python|_ |Download|_ |License|_ |RTD|_\n\n\n------\n\n.. |PyPi| image:: https://img.shields.io/pypi/v/nueramic-mathml?color=edf2f4&style=flat-square\n.. _PyPi: https://pypi.org/project/nueramic-mathml/\n\n\n.. |Python| image:: https://img.shields.io/pypi/pyversions/p?color=edf2f4&style=flat-square\n.. _Python: https://github.com/nueramic/mathml\n\n.. |Download| image:: https://img.shields.io/pypi/dm/nueramic-mathml?color=edf2f4&label=dowloads&style=flat-square\n.. _Download: https://pypi.org/project/nueramic-mathml/\n\n.. |License| image:: https://img.shields.io/github/license/nueramic/mathml?color=edf2f4&style=flat-square\n.. _License: https://github.com/nueramic/mathml\n\n.. |RTD| image:: https://img.shields.io/readthedocs/nueramic-mathml?color=edf2f4&style=flat-square\n.. _RTD: https://nueramic-mathml.readthedocs.io\n\n.. |Colab_1| image:: https://colab.research.google.com/assets/colab-badge.svg\n.. _Colab_1: https://colab.research.google.com/drive/19moQvDMK8kfTDYOGuRwEl06jdf_KXNMW?usp=sharing\n\n..\n    .. raw:: html\n\n       <p align="center">\n       <picture align="center">\n         <source width=150px" media="(prefers-color-scheme: dark)" srcset="docs/_static/nueramic-logo-cropped-white.svg">\n         <source width=150px" media="(prefers-color-scheme: light)" srcset="docs/_static/nueramic-logo-cropped-black.svg">\n         <img alt="two logos" src="docs/_static/nueramic-logo-cropped-black.svg">\n       </picture>\n       </p>\n\n\nNueramic MathML\n===============\nNueramic-mathml is a library for visualizing and logging the steps of optimization algorithms in machine learning. The project uses torch for calculations and plotly for visualization.\n\n.. code-block:: python\n\n    pip install nueramic-mathml\n\n\nQuick tour  |Colab_1|_\n======================\n\nOptimization\n------------------\nYou can minimize the functions and see a detailed description of each step. After minimizing, you have a history with complete logs.\nAlso available multidimensional optimisation.\n\n.. code-block:: python\n\n    def f(x): return x ** 3 - x ** 2 - x  # Minimum at x = 1\n    bounds = (0, 3)\n    one_optimize.golden_section_search(f, bounds, epsilon=0.01, verbose=True)[0]\n\n    Iteration: 0 \t|\t point = 1.500 \t|\t f(point) = -0.375\n    Iteration: 1 \t|\t point = 0.927 \t|\t f(point) = -0.990\n    Iteration: 2 \t|\t point = 1.281 \t|\t f(point) = -0.820\n    Iteration: 3 \t|\t point = 1.062 \t|\t f(point) = -0.992\n    Iteration: 4 \t|\t point = 0.927 \t|\t f(point) = -0.990\n    Iteration: 5 \t|\t point = 1.011 \t|\t f(point) = -1.000\n    Iteration: 6 \t|\t point = 0.959 \t|\t f(point) = -0.997\n    Iteration: 7 \t|\t point = 0.991 \t|\t f(point) = -1.000\n    Iteration: 8 \t|\t point = 1.011 \t|\t f(point) = -1.000\n    Iteration: 9 \t|\t point = 0.998 \t|\t f(point) = -1.000\n    Iteration: 10 \t|\t point = 1.006 \t|\t f(point) = -1.000\n    Searching finished. Successfully. code 0\n    1.0059846881033916\n\nModels\n-------\nYou can use our models for classification and regression\n\n.. code-block:: python\n\n    from nueramic_mathml.ml import LogisticRegressionRBF\n    from sklearn.datasets import make_moons\n\n    x, y = make_moons(10_000, noise=.1, random_state=84)\n    x, y = torch.tensor(x), torch.tensor(y)\n    logistic_model_rbf = LogisticRegressionRBF(x[:1000]).fit(x, y, show_epoch=10)\n\n    Epoch:     1 | CrossEntropyLoss:  0.71496\n    Epoch:    12 | CrossEntropyLoss:  0.35328\n    Epoch:    23 | CrossEntropyLoss:  0.27769\n    Epoch:    34 | CrossEntropyLoss:  0.22395\n    Epoch:    45 | CrossEntropyLoss:  0.19266\n    Epoch:    56 | CrossEntropyLoss:  0.16695\n    Epoch:    67 | CrossEntropyLoss:  0.14686\n    Epoch:    78 | CrossEntropyLoss:  0.13051\n    Epoch:    89 | CrossEntropyLoss:  0.11724\n    Epoch:   100 | CrossEntropyLoss:  0.10629\n\n    logistic_model_rbf.metrics_tab(x, y)\n\n    {\'auc_roc\': 0.9974513817072977,\n     \'f1\': 0.9700730618209839,\n     \'precision\': 0.9709476828575134,\n     \'recall\': 0.9692000150680542}',
    'author': 'Victor Barbarich',
    'author_email': 'vktrbr@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nueramic/mathml',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)
