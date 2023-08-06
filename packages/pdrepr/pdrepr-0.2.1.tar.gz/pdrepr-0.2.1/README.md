# pdrepr

pdrepr takes a pandas DataFrame as input, and *attempts* to output a valid Python expression that will create an identical DataFrame. Supports multiindices for rows and columns, at least for the relatively
simple cases I have tested. DataFrames with datatypes other than strings, ints and floats should work if their 
``_repr__()`` method also returns a string that can be passed to `eval()`, resulting in a similar object.  

![Testing and linting](https://github.com/danhje/pdrepr/workflows/Test%20And%20Lint/badge.svg)
[![codecov](https://codecov.io/gh/danhje/pdrepr/branch/master/graph/badge.svg)](https://codecov.io/gh/danhje/pdrepr)
![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/danhje/pdrepr?include_prereleases)
![PyPI](https://img.shields.io/pypi/v/pdrepr)

## Motivation

I was tired of having to manually construct DataFrames to be used in testing, especially the reference object to be compared with the resulting DF. With this package, such a code snipped can be created from the resulting DF.


## Installation

Using poetry:

```shell
poetry add pdrepr
```

Using pipenv:

```shell
pipenv install pdrepr
```

Using pip:

```shell
pip install pdrepr
```

## Usage

```python
>>> from pdrepr import pdrepr

>>> pdrepr(df)
pd.DataFrame({'character': ['The Nude Organist', 'BBC continuity announcer', 'The Colonel'], 'played by': ['Terry Jones and Terry Gilliam', 'John Cleese', 'Graham Chapman']}).set_index(['character'])

>>> pd.DataFrame({'character': ['The Nude Organist', 'BBC continuity announcer', 'The Colonel'], 'played by': ['Terry Jones and Terry Gilliam', 'John Cleese', 'Graham Chapman']}).set_index(['character'])
                                              played by
character                                              
The Nude Organist         Terry Jones and Terry Gilliam
BBC continuity announcer                    John Cleese
The Colonel                              Graham Chapman

```
