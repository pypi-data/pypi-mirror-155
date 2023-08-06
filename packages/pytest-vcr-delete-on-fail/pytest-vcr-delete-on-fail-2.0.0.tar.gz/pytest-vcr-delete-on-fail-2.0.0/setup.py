# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_vcr_delete_on_fail']

package_data = \
{'': ['*']}

install_requires = \
['pytest>=6.2.2']

entry_points = \
{'pytest11': ['vcr_delete_on_fail = pytest_vcr_delete_on_fail.main']}

setup_kwargs = {
    'name': 'pytest-vcr-delete-on-fail',
    'version': '2.0.0',
    'description': 'A pytest plugin that automates vcrpy cassettes deletion on test failure.',
    'long_description': '*************************\npytest-vcr-delete-on-fail\n*************************\n\n.. image:: https://img.shields.io/pypi/v/pytest-vcr-delete-on-fail\n    :target: https://pypi.org/project/pytest-vcr-delete-on-fail/\n    :alt: PyPI\n.. image:: https://img.shields.io/pypi/pyversions/pytest-vcr-delete-on-fail\n    :target: https://pypi.org/project/pytest-vcr-delete-on-fail/\n    :alt: PyPI - Python Version\n.. image:: https://img.shields.io/github/workflow/status/CarloDePieri/pytest-vcr-delete-on-fail/prod?logo=github\n    :target: https://github.com/CarloDePieri/pytest-vcr-delete-on-fail/actions/workflows/prod.yml\n    :alt: CI Status\n.. image:: https://coveralls.io/repos/github/CarloDePieri/pytest-vcr-delete-on-fail/badge.svg?branch=main\n    :target: https://coveralls.io/github/CarloDePieri/pytest-vcr-delete-on-fail?branch=main\n    :alt: Coverage status\n.. image:: https://img.shields.io/badge/sonarqube%20ratings-A-success\n    :alt: Sonarqube ratings: A\n.. image:: https://img.shields.io/github/license/CarloDePieri/pytest-vcr-delete-on-fail\n    :target: https://github.com/CarloDePieri/pytest-vcr-delete-on-fail/blob/main/LICENSE\n    :alt: License: GPL-3.0\n.. image:: https://img.shields.io/maintenance/yes/2022\n    :target: https://github.com/CarloDePieri/pytest-vcr-delete-on-fail/\n    :alt: Maintained!\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/psf/black\n    :alt: Code style: black\n\nA pytest plugin that automates vcrpy cassettes deletion on test failure.\n\n.. code-block:: console\n\n    $ pip install pytest-vcr-delete-on-fail\n\nThen, in your test:\n\n.. code-block:: python\n\n    import pytest\n    import requests\n    import vcr\n\n    my_vcr = vcr.VCR(record_mode="once")\n\n    cassette_path = "tests/cassettes/this.yaml"\n\n    @pytest.mark.vcr_delete_on_fail(cassette_path)\n    def test_this():\n        with my_vcr.use_cassette(cassette_path):\n            requests.get("https://github.com")\n        assert False\n\nIn this example a cassette will be saved on disk when exiting the ``use_cassette`` context manager, but since the test\neventually fails, the cassette will be deleted after the test teardown.\n\nRationale\n^^^^^^^^^\n\nSometimes when testing a function containing multiple http requests a failure will occur halfway through (this happens\nall the time when doing TDD). When using `vcrpy`_ to cache http requests, this could\nresult in a test cache that only cover a fraction of the function under test, which in turn could prevent the function\nto ever succeed or the test to pass in subsequent run if the http requests that didn\'t get cached depended on a\nfresh context (maybe they are time sensitive or there\'s randomness involved).\n\nThis possibility leads to doubt and lack of trust towards the test suite, which is wrong on too many level.\n\nThis plugin provides tools to solve this uncertainty, by deleting a test http requests cache if it fails, so that it\ncan start fresh on the next run.\n\n.. _vcrpy: https://github.com/kevin1024/vcrpy\n\n.. The documentation index page include only up to this point. The rest appears only on github / pypi.\n\nDocs\n----\n\nMore information and examples can be found in the in-depth `documentation`_.\n\n.. _documentation: https://carlodepieri.github.io/pytest-vcr-delete-on-fail\n\nDevelopment\n-----------\n\nInstall `invoke`_ and `poetry`_:\n\n.. _invoke: http://pyinvoke.org/\n.. _poetry: https://python-poetry.org/\n\n.. code-block:: console\n\n    $ pip install invoke poetry\n\nNow clone the git repo:\n\n.. code-block:: console\n\n    $ git clone https://github.com/CarloDePieri/pytest-vcr-delete-on-fail.git\n    $ cd pytest-vcr-delete-on-fail\n    $ inv install\n\nThis will try to create a virtualenv based on ``python3.7`` and install there all\nproject\'s dependencies. If a different python version is preferred, it can be\nselected by specifying  the ``--python`` (``-p``) flag like this:\n\n.. code-block:: console\n\n    $ inv install -p python3.8\n\nThe test suite can be run with commands:\n\n.. code-block:: console\n\n    $ inv test         # run the test suite\n    $ inv test-cov     # run the tests suite and produce a coverage report\n\nTo run the test suite against all supported python version (they must be in path!) run:\n\n.. code-block:: console\n\n    $ inv test-all-python-version\n\nTo test the GitHub workflow with `act`_:\n\n.. _act: https://github.com/nektos/act\n\n.. code-block:: console\n\n    $ inv act-dev               # test the dev workflow\n    $ inv act-dev -c shell      # open a shell in the act container (the above must fail first!)\n    $ inv act-dev -c clean      # stop and delete a failed act container\n\nTo write the documentation with autobuild and livereload launch:\n\n.. code-block:: console\n\n    $ inv docs-serve',
    'author': 'Carlo De Pieri',
    'author_email': 'depieri.carlo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/CarloDePieri/pytest-vcr-delete-on-fail',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
