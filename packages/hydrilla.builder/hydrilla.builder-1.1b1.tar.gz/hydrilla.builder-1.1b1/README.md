# Hydrilla builder

This is the repository of the builder part of [Hydrilla](https://hydrillabugs.koszko.org/projects/hydrilla/wiki). You can find the repository of its server part [here](https://git.koszko.org/pydrilla/).

Hydrilla builder is a tool to create Haketilo packages in serveable form. The information below is meant to help hack on the codebase. If you're instead looking for some noob-friendly documentation, see the [user manual](https://hydrillabugs.koszko.org/projects/hydrilla/wiki/User_manual).

## Dependencies

### Runtime

* Python3 (>= 3.7)
* click
* jsonschema (>= 3.0)
* reuse [optional]

### Build

* build (a PEP517 package builder)
* setuptools
* wheel
* setuptools_scm
* babel (Python library)

### Test

* pytest

## Building & testing & installation from wheel

Build, test and installation processes are analogous to those described in the [README of Hydrilla server part](https://git.koszko.org/pydrilla/about).

## Running

This package provides a hydrilla-builder command. You can use it to build the supplied example with something along the lines of:

```
mkdir /tmp/bananowarzez/
hydrilla-builder -s src/test/source-package-example/ -d /tmp/bananowarzez/
# Now, list the serveable package files we just produced.
find /tmp/bananowarzez/
```

You might as well like to run from sources, without installation:

``` shell
mkdir /tmp/bananowarzez/
./setup.py compile_catalog # generate the necessary .po files
PYTHONPATH=src python3 -m hydrilla.builder -s src/test/source-package-example/ \
	       -d /tmp/bananowarzez/
```

You can also consult the included manpage (`man` tool required):
``` shell
man ./doc/man/man1/hydrilla-builder.1
```

## Copying

Hydrilla is Copyright (C) 2021-2022 Wojtek Kosior and contributors, entirely available under the GNU Affero General Public License version 3 or later. Some files might also give you broader permissions, see comments inside them.

*I, Wojtek Kosior, thereby promise not to sue for violation of this project's license. Although I request that you do not make use this code in a proprietary program, I am not going to enforce this in court.*

## Contributing

Please visit our Redmine instance at https://hydrillabugs.koszko.org.

You can also write an email to koszko@koszko.org.
