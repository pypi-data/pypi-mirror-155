from setuptools import setup

name = "types-pycurl"
description = "Typing stubs for pycurl"
long_description = '''
## Typing stubs for pycurl

This is a PEP 561 type stub package for the `pycurl` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `pycurl`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/pycurl. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `411d85feebc96e24a8d0c2c21fba405b1d650ce7`.
'''.lstrip()

setup(name=name,
      version="7.44.9",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/pycurl.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['pycurl-stubs'],
      package_data={'pycurl-stubs': ['__init__.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
