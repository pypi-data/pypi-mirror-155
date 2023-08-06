from setuptools import setup

name = "types-ujson"
description = "Typing stubs for ujson"
long_description = '''
## Typing stubs for ujson

This is a PEP 561 type stub package for the `ujson` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `ujson`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/ujson. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `8cac5284ae8414ac57abe3758d462c5f4e78cd5e`.
'''.lstrip()

setup(name=name,
      version="5.3.0",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/ujson.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['ujson-stubs'],
      package_data={'ujson-stubs': ['__init__.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
