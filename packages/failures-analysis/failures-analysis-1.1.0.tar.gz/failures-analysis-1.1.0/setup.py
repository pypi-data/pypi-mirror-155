# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['failure_analysis']

package_data = \
{'': ['*']}

install_requires = \
['lxml>=4.9.0,<5.0.0',
 'numpy>=1.22.4,<2.0.0',
 'pandas>=1.4.2,<2.0.0',
 'sklearn>=0.0,<0.1']

entry_points = \
{'console_scripts': ['failures-analysis = '
                     'failure_analysis.failure_analysis:main']}

setup_kwargs = {
    'name': 'failures-analysis',
    'version': '1.1.0',
    'description': ' failures-analysis package provides fast and reliable way to find and group similar failures in test automation.',
    'long_description': '# Failure analysis\n\n[![Version](https://img.shields.io/pypi/v/failures-analysis.svg)](https://pypi.org/project/failures-analysis/)\n[![Actions Status](https://github.com/F-Secure/failures-analysis/workflows/CICD/badge.svg)](https://github.com/F-Secure/failures-analysis/actions)\n[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nTests failure analysis package provides fast and reliable way to find and group similar failures in your CI/CD\npipeline. When failure grouping and similarity scoring is done automatically by a machine, it will free\nresources from development team member to fix the most important failures in their CI/CD pipeline. It is tedious\nwork for a human to download, open and read all the test failures and analyse which failures belong to the same group.\nThe failure-analysis package solves this problem by processing xunit xml files using cosine similiarity and Levenshtein distance to find similar\nfailures from the test results.\n\nTest failure analysis package supports calculating similiarities with the following algorithms. \n\n- Sequence Matcher from Pythons diff library https://docs.python.org/3/library/difflib.html\n- Jaro-Winkler distance using jellyfish library https://pypi.org/project/jellyfish/\n- Jaccard index using jellyfish library https://pypi.org/project/jellyfish/\n- Levenshtein ratio using jellyfish library https://pypi.org/project/jellyfish/\n- Cosine similiarty using sklearn https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.cosine_similarity.html\n\nWhile it supports five different algorithms, best performing algorithms (cosine similiarity and levenshtein ratio) are only currently calculated.\n\nResults and the reason why only cosine and levenshtein deemed good enough are published here: LINK TO THE FIRST PUBLICATION\n\n# Installation instructions\n\nOnly Python 3.8 or newer is supported.\n\n1. Update pip `pip install -U pip` to ensure latest version is used\n2. Install from the commandline: `pip install failures-analysis`\n\n# Usage\nTo be able to find similar failures, users need to download xunit result(s) in to folder. How and where the download of\nthe xunit files is done, is not part of this project, but example\n[flaky-test CI](https://github.com/F-Secure/flaky-test-ci/blob/main/download_artifacts.py) has an example\nhow download from GitHub can be performed. Tool can be used from command line and it needs only one argument:\npath to folder where xunit xml files are located, example: \n`failures-analysis path/to/xunit/files`\n\n# Supported xunit formats\nPackage has been tested with Pytest and Robot Framework xunit output files. Other format might be supported,\nbut because we do not have visibility on those formats, those are not listed.\n',
    'author': 'Tatu Aalto',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/F-Secure/failures-analysis',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
