from setuptools import setup

name = "types-gdb"
description = "Typing stubs for gdb"
long_description = '''
## Typing stubs for gdb

This is a PEP 561 type stub package for the `gdb` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `gdb`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/gdb. All fixes for
types and metadata should be contributed there.

Type hints for GDB's [Python API](https://sourceware.org/gdb/onlinedocs/gdb/Python-API.html). Note that this API is available only when running Python scripts under GDB: is is not possible to install the `gdb` package separately, for instance using `pip`.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `640053e8e3bcc2b4d8d9bbecdac573ecc4500cbf`.
'''.lstrip()

setup(name=name,
      version="12.1.0",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/gdb.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['gdb-stubs'],
      package_data={'gdb-stubs': ['__init__.pyi', 'events.pyi', 'printing.pyi', 'prompt.pyi', 'types.pyi', 'unwinder.pyi', 'xmethod.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
