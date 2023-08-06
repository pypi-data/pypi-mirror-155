#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0

# Copyright (C) 2022 Wojtek Kosior <koszko@koszko.org>
#
# Available under the terms of Creative Commons Zero v1.0 Universal.

import setuptools

from setuptools.command.build_py import build_py
from setuptools.command.sdist import sdist

from pathlib import Path

here = Path(__file__).resolve().parent

class CustomBuildCommand(build_py):
    """The build command but runs babel before build."""
    def run(self, *args, **kwargs):
        """Wrapper around build_py's original run() method."""
        self.run_command('compile_catalog')

        super().run(*args, **kwargs)

class CustomSdistCommand(sdist):
    """
    The sdist command but prevents compiled message catalogs from being included
    in the archive.
    """
    def run(self, *args, **kwargs):
        """Wrapper around sdist's original run() method."""
        locales_dir = here / 'src/hydrilla/builder/locales'
        locale_files = {}

        for path in locales_dir.rglob('*.mo'):
            locale_files[path] = path.read_bytes()

        for path in locale_files:
            path.unlink()

        super().run(*args, **kwargs)

        for path, contents in locale_files.items():
            path.write_bytes(contents)

setuptools.setup(cmdclass = {
    'build_py': CustomBuildCommand,
    'sdist': CustomSdistCommand
})
