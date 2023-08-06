from setuptools import setup

name = "types-zxcvbn"
description = "Typing stubs for zxcvbn"
long_description = '''
## Typing stubs for zxcvbn

This is a PEP 561 type stub package for the `zxcvbn` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `zxcvbn`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/zxcvbn. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `f9e24680c375894bd20f1c3535a6d64c671d6600`.
'''.lstrip()

setup(name=name,
      version="4.4.0",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/zxcvbn.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['zxcvbn-stubs'],
      package_data={'zxcvbn-stubs': ['__init__.pyi', 'adjacency_graphs.pyi', 'feedback.pyi', 'frequency_lists.pyi', 'matching.pyi', 'scoring.pyi', 'time_estimates.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
