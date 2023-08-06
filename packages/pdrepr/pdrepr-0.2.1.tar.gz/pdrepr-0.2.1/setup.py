# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pdrepr']

package_data = \
{'': ['*']}

install_requires = \
['pandas']

setup_kwargs = {
    'name': 'pdrepr',
    'version': '0.2.1',
    'description': 'eval-able string representation of pandas objects',
    'long_description': "# pdrepr\n\npdrepr takes a pandas DataFrame as input, and *attempts* to output a valid Python expression that will create an identical DataFrame. Supports multiindices for rows and columns, at least for the relatively\nsimple cases I have tested. DataFrames with datatypes other than strings, ints and floats should work if their \n``_repr__()`` method also returns a string that can be passed to `eval()`, resulting in a similar object.  \n\n![Testing and linting](https://github.com/danhje/pdrepr/workflows/Test%20And%20Lint/badge.svg)\n[![codecov](https://codecov.io/gh/danhje/pdrepr/branch/master/graph/badge.svg)](https://codecov.io/gh/danhje/pdrepr)\n![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/danhje/pdrepr?include_prereleases)\n![PyPI](https://img.shields.io/pypi/v/pdrepr)\n\n## Motivation\n\nI was tired of having to manually construct DataFrames to be used in testing, especially the reference object to be compared with the resulting DF. With this package, such a code snipped can be created from the resulting DF.\n\n\n## Installation\n\nUsing poetry:\n\n```shell\npoetry add pdrepr\n```\n\nUsing pipenv:\n\n```shell\npipenv install pdrepr\n```\n\nUsing pip:\n\n```shell\npip install pdrepr\n```\n\n## Usage\n\n```python\n>>> from pdrepr import pdrepr\n\n>>> pdrepr(df)\npd.DataFrame({'character': ['The Nude Organist', 'BBC continuity announcer', 'The Colonel'], 'played by': ['Terry Jones and Terry Gilliam', 'John Cleese', 'Graham Chapman']}).set_index(['character'])\n\n>>> pd.DataFrame({'character': ['The Nude Organist', 'BBC continuity announcer', 'The Colonel'], 'played by': ['Terry Jones and Terry Gilliam', 'John Cleese', 'Graham Chapman']}).set_index(['character'])\n                                              played by\ncharacter                                              \nThe Nude Organist         Terry Jones and Terry Gilliam\nBBC continuity announcer                    John Cleese\nThe Colonel                              Graham Chapman\n\n```\n",
    'author': 'Daniel Hjertholm',
    'author_email': 'daniel.hjertholm@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/danhje/pdrepr',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
