# pyepggrab example grabber

`cc_example` is an example grabber for demonstration and template purposes.

To make the grabber part of pyepggrab, copy the `cc_example` directory to
`pyepggrab/grabbers/` and add

```
tv_grab_pyepg_cc_example = "pyepggrab.grabbers.cc_example.cc_example:run"
```

to `pyproject.toml` under the `[project.scripts]` section.

Detailed documentation available in the example grabber, in the referenced
classes, and other classes of pyepggrab.

# General guidelines

## Naming

The name of a grabber have at least two parts.

1. `cc` - The country code of the target audience
2. `example` - Some identifier, such as a data source

Note: regardless of the language of the target audience the code must be
written and commented in english.

## Code and Style

Code must be written and commented in english.

Type hints are preferred and recommended.

You can check the conformance by running `hatch run style:check`.
Some can be fixed by running `hatch run style:fmt`.

