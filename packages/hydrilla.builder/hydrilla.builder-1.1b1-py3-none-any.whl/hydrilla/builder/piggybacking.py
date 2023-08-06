# SPDX-License-Identifier: AGPL-3.0-or-later

# Handling of software packaged for other distribution systems.
#
# This file is part of Hydrilla
#
# Copyright (C) 2022 Wojtek Kosior
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#
# I, Wojtek Kosior, thereby promise not to sue for violation of this
# file's license. Although I request that you do not make use this code
# in a proprietary program, I am not going to enforce this in court.

"""
This module contains definitions that may be reused by multiple piggybacked
software system backends.
"""

# Enable using with Python 3.7.
from __future__ import annotations

from pathlib import Path, PurePosixPath
from typing import Optional, Iterable

from .. import util
from .common_errors import *

here = Path(__file__).resolve().parent

_ = util.translation(here / 'locales').gettext

class Piggybacked:
    """
    Store information about foreign resources in use.

    Public attributes:
        'resource_must_depend' (read-only)
        'package_license_files' (read-only)
    """
    def __init__(self, archives: dict[str, Path]={}, roots: dict[str, Path]={},
                 package_license_files: list[PurePosixPath]=[],
                 resource_must_depend: list[dict]=[]):
        """
        Initialize this Piggybacked object.

        'archives' maps piggybacked system names to directories that contain
        package(s)' archive files. An 'archives' object may look like
        {'apt': PosixPath('/path/to/dir/with/debs/and/tarballs')}.

        'roots' associates directory names to be virtually inserted under
        Hydrilla source package directory with paths to real filesystem
        directories that hold their desired contents, i.e. unpacked foreign
        packages.

        'package_license_files' lists paths to license files that should be
        included with the Haketilo package that will be produced. The paths are
        to be resolved using 'roots' dictionary.

        'resource_must_depend' lists names of Haketilo packages that the
        produced resources will additionally depend on. This is meant to help
        distribute common licenses with a separate Haketilo package.
        """
        self.archives              = archives
        self.roots                 = roots
        self.package_license_files = package_license_files
        self.resource_must_depend  = resource_must_depend

    def resolve_file(self, file_ref_name: PurePosixPath) -> Optional[Path]:
        """
        'file_ref_name' is a path as may appear in an index.json file. Check if
        the file belongs to one of the roots we have and return either a path
        to the relevant file under this root or None.

        It is not being checked whether the file actually exists in the
        filesystem.
        """
        parts = file_ref_name.parts
        root_path = self.roots.get(parts and parts[0])
        path = root_path
        if path is None:
            return None

        for part in parts[1:]:
            path = path / part

        path = path.resolve()

        try:
            path.relative_to(root_path)
        except ValueError:
            raise FileReferenceError(_('loading_{}_outside_piggybacked_dir')
                                     .format(file_ref_name))

        return path

    def archive_files(self) -> Iterable[tuple[PurePosixPath, Path]]:
        """
        Yield all archive files in use. Each yielded tuple holds file's desired
        path relative to the piggybacked archives directory to be created and
        its current real path.
        """
        for system, real_dir in self.archives.items():
            for path in real_dir.rglob('*'):
                yield PurePosixPath(system) / path.relative_to(real_dir), path
