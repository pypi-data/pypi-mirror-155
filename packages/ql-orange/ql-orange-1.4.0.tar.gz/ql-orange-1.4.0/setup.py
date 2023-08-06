# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['black', 'blib2to3', 'blib2to3.pgen2']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.0',
 'mypy_extensions>=0.4.3',
 'pathspec>=0.9.0',
 'platformdirs>=2',
 'tomli>=1.1.0']

extras_require = \
{':python_version < "3.10"': ['typing_extensions>=3.10.0.0'],
 ':python_version < "3.8"': ['typed-ast>=1.4.2'],
 'd': ['aiohttp>=3.7.4'],
 'jupyter': ['ipython>=7.8.0', 'tokenize-rt>=3.2.0']}

entry_points = \
{'console_scripts': ['orange = black:patched_main']}

setup_kwargs = {
    'name': 'ql-orange',
    'version': '1.4.0',
    'description': 'Orange is a fork of Black Python code formatter maintained by Quantlane.',
    'long_description': '# Orange\n\nPython code formatter\n\n[![PyPi version](https://pypip.in/v/ql-orange/badge.png)](https://pypi.org/project/ql-orange/)\n\n\n## What it is\n_Orange_ is fork of [Black](https://github.com/psf/black) maintained by [Quantlane](https://quantlane.com/).\n\n\n## Installation\n\n`pip install ql-orange`\n\n\n## The _Orange_ code style\n_Orange_ mainly follows code style used by _Black_ with few key differences:\n* indentation with tabs,\n* single-quoted strings,\n* default line length is 110,\n\nand some extra rules.\n\n### Spaces around keyword arguments\n```python\n# Black\ndef func(x, y=None):\n    pass\n\n\nfunc(1, y=2)\n```\n\n```python\n# Orange\ndef func(x, y = None):\n\tpass\n\n\nfunc(1, y = 2)\n```\n\n### Multi-line comprehensions\n_Orange_ explodes comprehensions if they don\'t fit on one line.\n```python\n# Black\nlong_list_of_comprehension = [\n    pineapple for pineapple in self.pineapples if getattr(pineapple, "is_still_fresh", False)\n]\nshort = [s for s in l if s]\n```\n\n```python\n# Orange\nlong_list_of_comprehension = [\n\tpineapple\n\tfor pineapple in self.pineapples\n\tif getattr(pineapple, \'is_still_fresh\', False)\n]\nshort = [s for s in l if s]\n```\n\n### Extended _magic trailing comma_\n_Black_ uses [magic trailing comma](https://github.com/psf/black#the-magic-trailing-comma)\nto keep formatting of collections multi-line even if they would fit into one line.\n_Orange_ extends magic trailing comma to work on:\n* function definitions,\n* function calls, and\n* nested collections\n\n```python\n# Black\ndef f(a: int, b: str, c: Optional[float] = None,) -> None:\n    pass\n\n\nf(\n    1, "a", None,\n)\ndata = {\n    "time": datetime.datetime.now(),\n    "id": str(data.id),\n    "key": some_value,\n    "labels": ["Label1", "Label that is quite long",],\n}\n```\n\n```python\n# Orange\ndef f(\n\ta: int,\n\tb: str,\n\tc: Optional[float] = None,\n) -> None:\n\tpass\n\n\nf(\n\t1,\n\t\'a\',\n\tNone,\n)\ndata = {\n\t\'time\': datatime.datetime.now(),\n\t\'id\': str(data.id),\n\t\'key\': some_value,\n\t\'labels\': [\n\t\t\'Label1\',\n\t\t\'Label that is quite long\',\n\t],\n}\n```\n\n## Usage\n\n```\norange {source_file_or_directory}\n```\n\n### Command line options\n\n_Orange_ provides the same options as _black_. You can list them by running `orange --help`:\n\n```text\norange [OPTIONS] [SRC]...\n\nOptions:\n  -c, --code TEXT                 Format the code passed in as a string.\n  -l, --line-length INTEGER       How many characters per line to allow.\n                                  [default: 110]\n  -t, --target-version [py27|py33|py34|py35|py36|py37|py38]\n                                  Python versions that should be supported by\n                                  Black\'s output. [default: per-file auto-\n                                  detection]\n  --py36                          Allow using Python 3.6-only syntax on all\n                                  input files.  This will put trailing commas\n                                  in function signatures and calls also after\n                                  *args and **kwargs. Deprecated; use\n                                  --target-version instead. [default: per-file\n                                  auto-detection]\n  --pyi                           Format all input files like typing stubs\n                                  regardless of file extension (useful when\n                                  piping source on standard input).\n  -S, --skip-string-normalization\n                                  Don\'t normalize string quotes or prefixes.\n  --check                         Don\'t write the files back, just return the\n                                  status.  Return code 0 means nothing would\n                                  change.  Return code 1 means some files\n                                  would be reformatted.  Return code 123 means\n                                  there was an internal error.\n  --diff                          Don\'t write the files back, just output a\n                                  diff for each file on stdout.\n  --fast / --safe                 If --fast given, skip temporary sanity\n                                  checks. [default: --safe]\n  --include TEXT                  A regular expression that matches files and\n                                  directories that should be included on\n                                  recursive searches.  An empty value means\n                                  all files are included regardless of the\n                                  name.  Use forward slashes for directories\n                                  on all platforms (Windows, too).  Exclusions\n                                  are calculated first, inclusions later.\n                                  [default: \\.pyi?$]\n  --exclude TEXT                  A regular expression that matches files and\n                                  directories that should be excluded on\n                                  recursive searches.  An empty value means no\n                                  paths are excluded. Use forward slashes for\n                                  directories on all platforms (Windows, too).\n                                  Exclusions are calculated first, inclusions\n                                  later.  [default: /(\\.eggs|\\.git|\\.hg|\\.mypy\n                                  _cache|\\.nox|\\.tox|\\.venv|_build|buck-\n                                  out|build|dist)/]\n  -q, --quiet                     Don\'t emit non-error messages to stderr.\n                                  Errors are still emitted, silence those with\n                                  2>/dev/null.\n  -v, --verbose                   Also emit messages to stderr about files\n                                  that were not changed or were ignored due to\n                                  --exclude=.\n  --version                       Show the version and exit.\n  --config PATH                   Read configuration from PATH.\n  -h, --help                      Show this message and exit.\n```\n\n',
    'author': 'quantlane.com',
    'author_email': 'info@quantlane.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/quantlane/meta/orange',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
