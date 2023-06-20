# pyepggrab

Extension / replacement of the original [XMLTV][xmltv].

All grabbers are written following the XMLTV specifications and compatible 
with all XMLTV tools (`tv_find_grabbers`, `tv_validate_*`).

Grabbers found here can be used together with the grabbers found in the
original XMLTV project, and any software uses the original XMLTV project
can use these grabbers without any modification.

To avoid name conflicts, pyepggrab grabbers use the prefix `tv_grab_pyepg_`.

## Installation

Currently, there are no premade packages available, but this expected to change
in the future.

If the functionality of `tv_find_grabbers` is required the one in the
original [XMLTV][xmltv] project can be used until we provide an alternative.
(On the [Roadmap](#roadmap))

To install from source, create a wheel package (this requires `hatch`):

> `hatch build`

and install it with your preferred package manager (`pipx` in the example):

> `pipx install dist/pyepggrab-*.whl`

## Available grabbers:

| Country | Guide source      | Grabber                |
|:-------:|-------------------|------------------------|
| HU      | [port.hu][porthu] | [hu_porthu][hu_porthu] |

[porthu]: https://port.hu
[hu_porthu]: pyepggrab/grabbers/hu_porthu

## Roadmap

In no particular order

- [ ] Upload a package to PyPi
- [ ] Write an example grabber to demonstrate the usage of pyepggrab
- [ ] Write tools to make it standalone (`tv_find_grabbers`, `tv_validate_*`)

[xmltv]: https://github.com/XMLTV/xmltv