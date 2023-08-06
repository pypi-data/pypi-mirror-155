# Orange

Python code formatter

[![PyPi version](https://pypip.in/v/ql-orange/badge.png)](https://pypi.org/project/ql-orange/)


## What it is
_Orange_ is fork of [Black](https://github.com/psf/black) maintained by [Quantlane](https://quantlane.com/).


## Installation

`pip install ql-orange`


## The _Orange_ code style
_Orange_ mainly follows code style used by _Black_ with few key differences:
* indentation with tabs,
* single-quoted strings,
* default line length is 110,

and some extra rules.

### Spaces around keyword arguments
```python
# Black
def func(x, y=None):
    pass


func(1, y=2)
```

```python
# Orange
def func(x, y = None):
	pass


func(1, y = 2)
```

### Multi-line comprehensions
_Orange_ explodes comprehensions if they don't fit on one line.
```python
# Black
long_list_of_comprehension = [
    pineapple for pineapple in self.pineapples if getattr(pineapple, "is_still_fresh", False)
]
short = [s for s in l if s]
```

```python
# Orange
long_list_of_comprehension = [
	pineapple
	for pineapple in self.pineapples
	if getattr(pineapple, 'is_still_fresh', False)
]
short = [s for s in l if s]
```

### Extended _magic trailing comma_
_Black_ uses [magic trailing comma](https://github.com/psf/black#the-magic-trailing-comma)
to keep formatting of collections multi-line even if they would fit into one line.
_Orange_ extends magic trailing comma to work on:
* function definitions,
* function calls, and
* nested collections

```python
# Black
def f(a: int, b: str, c: Optional[float] = None,) -> None:
    pass


f(
    1, "a", None,
)
data = {
    "time": datetime.datetime.now(),
    "id": str(data.id),
    "key": some_value,
    "labels": ["Label1", "Label that is quite long",],
}
```

```python
# Orange
def f(
	a: int,
	b: str,
	c: Optional[float] = None,
) -> None:
	pass


f(
	1,
	'a',
	None,
)
data = {
	'time': datatime.datetime.now(),
	'id': str(data.id),
	'key': some_value,
	'labels': [
		'Label1',
		'Label that is quite long',
	],
}
```

## Usage

```
orange {source_file_or_directory}
```

### Command line options

_Orange_ provides the same options as _black_. You can list them by running `orange --help`:

```text
orange [OPTIONS] [SRC]...

Options:
  -c, --code TEXT                 Format the code passed in as a string.
  -l, --line-length INTEGER       How many characters per line to allow.
                                  [default: 110]
  -t, --target-version [py27|py33|py34|py35|py36|py37|py38]
                                  Python versions that should be supported by
                                  Black's output. [default: per-file auto-
                                  detection]
  --py36                          Allow using Python 3.6-only syntax on all
                                  input files.  This will put trailing commas
                                  in function signatures and calls also after
                                  *args and **kwargs. Deprecated; use
                                  --target-version instead. [default: per-file
                                  auto-detection]
  --pyi                           Format all input files like typing stubs
                                  regardless of file extension (useful when
                                  piping source on standard input).
  -S, --skip-string-normalization
                                  Don't normalize string quotes or prefixes.
  --check                         Don't write the files back, just return the
                                  status.  Return code 0 means nothing would
                                  change.  Return code 1 means some files
                                  would be reformatted.  Return code 123 means
                                  there was an internal error.
  --diff                          Don't write the files back, just output a
                                  diff for each file on stdout.
  --fast / --safe                 If --fast given, skip temporary sanity
                                  checks. [default: --safe]
  --include TEXT                  A regular expression that matches files and
                                  directories that should be included on
                                  recursive searches.  An empty value means
                                  all files are included regardless of the
                                  name.  Use forward slashes for directories
                                  on all platforms (Windows, too).  Exclusions
                                  are calculated first, inclusions later.
                                  [default: \.pyi?$]
  --exclude TEXT                  A regular expression that matches files and
                                  directories that should be excluded on
                                  recursive searches.  An empty value means no
                                  paths are excluded. Use forward slashes for
                                  directories on all platforms (Windows, too).
                                  Exclusions are calculated first, inclusions
                                  later.  [default: /(\.eggs|\.git|\.hg|\.mypy
                                  _cache|\.nox|\.tox|\.venv|_build|buck-
                                  out|build|dist)/]
  -q, --quiet                     Don't emit non-error messages to stderr.
                                  Errors are still emitted, silence those with
                                  2>/dev/null.
  -v, --verbose                   Also emit messages to stderr about files
                                  that were not changed or were ignored due to
                                  --exclude=.
  --version                       Show the version and exit.
  --config PATH                   Read configuration from PATH.
  -h, --help                      Show this message and exit.
```

