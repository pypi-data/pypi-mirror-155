# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['multivar_horner', 'multivar_horner.classes']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.21,<2.0']

extras_require = \
{'numba': ['numba>=0.55,<0.56']}

setup_kwargs = {
    'name': 'multivar-horner',
    'version': '3.0.3',
    'description': 'python package implementing a multivariate Horner scheme for efficiently evaluating multivariate polynomials',
    'long_description': '===============\nmultivar_horner\n===============\n\n\n.. image:: https://travis-ci.org/jannikmi/multivar_horner.svg?branch=master\n    :alt: CI status\n    :target: https://travis-ci.org/jannikmi/multivar_horner\n\n.. image:: https://readthedocs.org/projects/multivar_horner/badge/?version=latest\n    :alt: documentation status\n    :target: https://multivar_horner.readthedocs.io/en/latest/?badge=latest\n\n.. image:: https://img.shields.io/pypi/wheel/multivar-horner.svg\n    :target: https://pypi.python.org/pypi/multivar-horner\n\n.. image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n   :target: https://github.com/pre-commit/pre-commit\n   :alt: pre-commit\n\n.. image:: https://pepy.tech/badge/multivar-horner\n    :alt: Total PyPI downloads\n    :target: https://pepy.tech/project/multivar-horner\n\n.. image:: https://img.shields.io/pypi/v/multivar_horner.svg\n    :alt: latest version on PyPI\n    :target: https://pypi.python.org/pypi/multivar-horner\n\n.. image:: https://joss.theoj.org/papers/0b514c6894780f3cc81ed88c141631d4/status.svg\n    :alt: JOSS status\n    :target: https://joss.theoj.org/papers/0b514c6894780f3cc81ed88c141631d4\n\n.. image:: https://zenodo.org/badge/155578190.svg\n   :target: https://zenodo.org/badge/latestdoi/155578190\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/psf/black\n\n\n``multivar_horner`` is a python package implementing a multivariate\n`Horner scheme ("Horner\'s method", "Horner\'s rule") <https://en.wikipedia.org/wiki/Horner%27s_method>`__\nfor efficiently evaluating multivariate polynomials.\n\n\nQuick Guide:\n\n::\n\n\n    pip install multivar_horner\n\n\nFor efficiency this package is compiling the instructions required for polynomial evaluation to C by default.\nIf you don\'t have a C compiler (``gcc`` or ``cc``) installed you also need to install numba for using an alternative method:\n\n::\n\n\n    pip install multivar_horner[numba]\n\n\nSimple example:\n\n.. code-block:: python\n\n    import numpy as np\n    from multivar_horner import HornerMultivarPolynomial\n\n    # input parameters defining the polynomial\n    #   p(x) = 5.0 + 1.0 x_1^3 x_2^1 + 2.0 x_1^2 x_3^1 + 3.0 x_1^1 x_2^1 x_3^1\n    coefficients = np.array([[5.0], [1.0], [2.0], [3.0]], dtype=np.float64)\n    exponents = np.array([[0, 0, 0], [3, 1, 0], [2, 0, 1], [1, 1, 1]], dtype=np.uint32)\n\n    # [#ops=7] p(x) = x_1 (x_1 (x_1 (1.0 x_2) + 2.0 x_3) + 3.0 x_2 x_3) + 5.0\n    horner_polynomial = HornerMultivarPolynomial(coefficients, exponents)\n    x = np.array([-2.0, 3.0, 1.0], dtype=np.float64)\n    p_x = horner_polynomial(x)\n\n\nFor more refer to the `documentation <https://multivar_horner.readthedocs.io/en/latest/>`__.\n\n\nAlso see:\n`GitHub <https://github.com/jannikmi/multivar_horner>`__,\n`PyPI <https://pypi.python.org/pypi/multivar_horner/>`__,\n`arXiv paper <https://arxiv.org/abs/2007.13152>`__\n',
    'author': 'jannikmi',
    'author_email': 'github@michelfe.it',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://multivar-horner.readthedocs.io/en/latest/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
