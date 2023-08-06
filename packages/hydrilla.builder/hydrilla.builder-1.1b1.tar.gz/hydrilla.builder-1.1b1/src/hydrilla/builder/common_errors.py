# SPDX-License-Identifier: AGPL-3.0-or-later

# Error classes.
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
This module defines error types for use in other parts of Hydrilla builder.
"""

# Enable using with Python 3.7.
from __future__ import annotations

from pathlib import Path

from .. import util

here = Path(__file__).resolve().parent

_ = util.translation(here / 'locales').gettext

class DistroError(Exception):
    """
    Exception used to report problems when resolving an OS distribution.
    """

class FileReferenceError(Exception):
    """
    Exception used to report various problems concerning files referenced from
    source package.
    """

class SubprocessError(Exception):
    """
    Exception used to report problems related to execution of external
    processes, includes. various problems when calling apt-* and dpkg-*
    commands.
    """
    def __init__(self, msg: str, cp: Optional[CP]=None) -> None:
        """Initialize this SubprocessError"""
        if cp and cp.stdout:
            msg = '\n\n'.join([msg, _('STDOUT_OUTPUT_heading'), cp.stdout])

        if cp and cp.stderr:
            msg = '\n\n'.join([msg, _('STDERR_OUTPUT_heading'), cp.stderr])

        super().__init__(msg)
