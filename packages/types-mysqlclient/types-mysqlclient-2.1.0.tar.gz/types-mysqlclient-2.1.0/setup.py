from setuptools import setup

name = "types-mysqlclient"
description = "Typing stubs for mysqlclient"
long_description = '''
## Typing stubs for mysqlclient

This is a PEP 561 type stub package for the `mysqlclient` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `mysqlclient`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/mysqlclient. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `b36c7705a79a07736aa9cf2607b29e789d0b004d`.
'''.lstrip()

setup(name=name,
      version="2.1.0",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/mysqlclient.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['MySQLdb-stubs'],
      package_data={'MySQLdb-stubs': ['__init__.pyi', '_exceptions.pyi', '_mysql.pyi', 'connections.pyi', 'constants/CLIENT.pyi', 'constants/CR.pyi', 'constants/ER.pyi', 'constants/FIELD_TYPE.pyi', 'constants/FLAG.pyi', 'constants/__init__.pyi', 'converters.pyi', 'cursors.pyi', 'release.pyi', 'times.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
