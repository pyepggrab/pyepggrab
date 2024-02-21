# pyepggrab

Extension / replacement of the original [XMLTV][xmltv].

All grabbers are written following the XMLTV specifications and compatible 
with all XMLTV tools (`tv_find_grabbers`, `tv_validate_*`).

Grabbers found here can be used together with the grabbers found in the
original XMLTV project, and any software uses the original XMLTV project
can use these grabbers without any modification.

To avoid name conflicts, pyepggrab grabbers use the prefix `tv_grab_pyepg_`.

## Installation

If the functionality of `tv_find_grabbers` is required the one in the
original [XMLTV][xmltv] project can be used until we provide an alternative.
(On the [Roadmap](#roadmap))

### From package

pyepggrab is available on PyPi: https://pypi.org/project/pyepggrab/

Install it with your preferred package manager.

For example, with `pip`
```
pip install pyepggrab
```

or with `pipx`
```
pipx install pyepggrab
```

### From source

To install from source, create a wheel package (this requires `hatch`):

```
hatch build
```

and install it with your preferred package manager.

For example, with `pip`
```
pip install dist/pyepggrab-*.whl
```

or with `pipx`
```
pipx install dist/pyepggrab-*.whl
```

## Available grabbers:

| Country | Guide source      | Grabber                |
|:-------:|-------------------|------------------------|
| HU      | [port.hu][porthu] | [hu_porthu][hu_porthu] |

[porthu]: https://port.hu
[hu_porthu]: pyepggrab/grabbers/hu_porthu

## Standard XMLTV parameters

### All grabbers

- `--capabilities`: capabilities of the grabber (below)
- `--description`: short description of the grabber
- `--help`: list of all parameters that the grabber supports
- `--version`: display the version of the grabber

### Baseline capability 

- `--quiet`: no logging output (supported by every grabber)
- `--output`: save the output to a file (default is STDOUT)
- `--days`: Download the specified number of days
- `--offset`: Download from the specified offset (0 = today)
- `--config-file`: use the specified config file

### Manualconfig capability 

- `--configure`: run an interactive configuration session

## Pyepggrab specific parameters

### All grabbers

- `--pyepggrabver`: display the version of pyepggrab
- `-q`, `--quiet`: alias for the baseline parameter
- `-l`, `--loglevel`: logging level: FATAL, ERROR, WARNING, INFO, DEBUG
- `-v`, `--verbose`: alias for `--loglevel INFO`
- `-d`, `--debug`: alias for `--loglevel DEBUG`

### Grabber specific parameters

Documented in each grabber's README.

## Roadmap

In no particular order

- [x] Upload a package to PyPi
- [x] Write an example grabber to demonstrate the usage of pyepggrab (see [example](example) directory)
- [ ] Write tools to make it standalone (`tv_find_grabbers`, `tv_validate_*`)

[xmltv]: https://github.com/XMLTV/xmltv