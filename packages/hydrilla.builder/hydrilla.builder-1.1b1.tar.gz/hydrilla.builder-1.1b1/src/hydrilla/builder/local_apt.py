# SPDX-License-Identifier: AGPL-3.0-or-later

# Using a local APT.
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

# Enable using with Python 3.7.
from __future__ import annotations

import zipfile
import shutil
import re
import subprocess
CP = subprocess.CompletedProcess
from pathlib import Path, PurePosixPath
from tempfile import TemporaryDirectory, NamedTemporaryFile
from hashlib import sha256
from urllib.parse import unquote
from contextlib import contextmanager
from typing import Optional, Iterable

from .. import util
from .piggybacking import Piggybacked
from .common_errors import *

here = Path(__file__).resolve().parent

_ = util.translation(here / 'locales').gettext

"""
Default cache directory to save APT configurations and downloaded GPG keys in.
"""
default_apt_cache_dir = Path.home() / '.cache' / 'hydrilla' / 'builder' / 'apt'

"""
Default keyserver to use.
"""
default_keyserver = 'hkps://keyserver.ubuntu.com:443'

"""
Default keys to download when using a local APT.
"""
default_keys = [
    # Trisquel
    'E6C27099CA21965B734AEA31B4EFB9F38D8AEBF1',
    '60364C9869F92450421F0C22B138CA450C05112F',
    # Ubuntu
    '630239CC130E1A7FD81A27B140976EAF437D05B5',
    '790BC7277767219C42C86F933B4FE6ACC0B21F32',
    'F6ECB3762474EDA9D21B7022871920D1991BC93C',
    # Debian
    '6D33866EDD8FFA41C0143AEDDCC9EFBF77E11517',
    '80D15823B7FD1561F9F7BCDDDC30D7C23CBBABEE',
    'AC530D520F2F3269F5E98313A48449044AAD5C5D'
]

"""sources.list file contents for known distros."""
default_lists = {
    'nabia': [f'{type} http://archive.trisquel.info/trisquel/ nabia{suf} main'
              for type in ('deb', 'deb-src')
              for suf in ('', '-updates', '-security')]
}

class GpgError(Exception):
    """
    Exception used to report various problems when calling GPG.
    """

class AptError(SubprocessError):
    """
    Exception used to report various problems when calling apt-* and dpkg-*
    commands.
    """

def run(command, **kwargs):
    """A wrapped around subprocess.run that sets some default options."""
    return subprocess.run(command, **kwargs, env={'LANG': 'en_US'},
                          capture_output=True, text=True)

class Apt:
    """
    This class represents an APT instance and can be used to call apt-get
    commands with it.
    """
    def __init__(self, apt_conf: str) -> None:
        """Initialize this Apt object."""
        self.apt_conf = apt_conf

    def get(self, *args: str, **kwargs) -> CP:
        """
        Run apt-get with the specified arguments and raise a meaningful AptError
        when something goes wrong.
        """
        command = ['apt-get', '-c', self.apt_conf, *args]
        try:
            cp = run(command, **kwargs)
        except FileNotFoundError:
            msg = _('couldnt_execute_{}_is_it_installed').format('apt-get')
            raise AptError(msg)

        if cp.returncode != 0:
            msg = _('command_{}_failed').format(' '.join(command))
            raise AptError(msg, cp)

        return cp

def cache_dir() -> Path:
    """
    Return the directory used to cache data (APT configurations, keyrings) to
    speed up repeated operations.

    This function first ensures the directory exists.
    """
    default_apt_cache_dir.mkdir(parents=True, exist_ok=True)
    return default_apt_cache_dir

class SourcesList:
    """Representation of apt's sources.list contents."""
    def __init__(self, list: [str]=[], codename: Optional[str]=None) -> None:
        """Initialize this SourcesList."""
        self.codename = None
        self.list = [*list]
        self.has_extra_entries = bool(self.list)

        if codename is not None:
            if codename not in default_lists:
                raise DistroError(_('distro_{}_unknown').format(codename))

            self.codename = codename
            self.list.extend(default_lists[codename])

    def identity(self) -> str:
        """
        Produce a string that uniquely identifies this sources.list contents.
        """
        if self.codename and not self.has_extra_entries:
            return self.codename

        return sha256('\n'.join(sorted(self.list)).encode()).digest().hex()

def apt_conf(directory: Path) -> str:
    """
    Given local APT's directory, produce a configuration suitable for running
    APT there.

    'directory' must not contain any special characters including quotes and
    spaces.
    """
    return f'''
Architecture "amd64";
Dir "{directory}";
Dir::State "{directory}/var/lib/apt";
Dir::State::status "{directory}/var/lib/dpkg/status";
Dir::Etc::SourceList "{directory}/etc/apt.sources.list";
Dir::Etc::SourceParts "";
Dir::Cache "{directory}/var/cache/apt";
pkgCacheGen::Essential "none";
Dir::Etc::Trusted "{directory}/etc/trusted.gpg";
'''

def apt_keyring(keys: [str]) -> bytes:
    """
    Download the requested keys if necessary and export them as a keyring
    suitable for passing to APT.

    The keyring is returned as a bytes value that should be written to a file.
    """
    try:
        from gnupg import GPG
    except ModuleNotFoundError:
        raise GpgError(_('couldnt_import_{}_is_it_installed').format('gnupg'))

    gpg = GPG(keyring=str(cache_dir() / 'master_keyring.gpg'))
    for key in keys:
        if gpg.list_keys(keys=[key]) != []:
            continue

        if gpg.recv_keys(default_keyserver, key).imported == 0:
            raise GpgError(_('gpg_couldnt_recv_key_{}').format(key))

    return gpg.export_keys(keys, armor=False, minimal=True)

def cache_apt_root(apt_root: Path, destination_zip: Path) -> None:
    """
    Zip an APT root directory for later use and move the zipfile to the
    requested destination.
    """
    temporary_zip_path = None
    try:
        tmpfile = NamedTemporaryFile(suffix='.zip', prefix='tmp_',
                                     dir=cache_dir(), delete=False)
        temporary_zip_path = Path(tmpfile.name)

        to_skip = {Path('etc') / 'apt.conf', Path('etc') / 'trusted.gpg'}

        with zipfile.ZipFile(tmpfile, 'w') as zf:
            for member in apt_root.rglob('*'):
                relative = member.relative_to(apt_root)
                if relative not in to_skip:
                    # This call will also properly add empty folders to zip file
                    zf.write(member, relative, zipfile.ZIP_DEFLATED)

        shutil.move(temporary_zip_path, destination_zip)
    finally:
        if temporary_zip_path is not None and temporary_zip_path.exists():
            temporary_zip_path.unlink()

def setup_local_apt(directory: Path, list: SourcesList, keys: [str]) -> Apt:
    """
    Create files and directories necessary for running APT without root rights
    inside 'directory'.

    'directory' must not contain any special characters including quotes and
    spaces and must be empty.

    Return an Apt object that can be used to call apt-get commands.
    """
    apt_root = directory / 'apt_root'

    conf_text     = apt_conf(apt_root)
    keyring_bytes = apt_keyring(keys)

    apt_zipfile = cache_dir() / f'apt_{list.identity()}.zip'
    if apt_zipfile.exists():
        with zipfile.ZipFile(apt_zipfile) as zf:
            zf.extractall(apt_root)

    for to_create in (
            apt_root / 'var' / 'lib' / 'apt' / 'partial',
            apt_root / 'var' / 'lib' / 'apt' / 'lists',
            apt_root / 'var' / 'cache' / 'apt' / 'archives' / 'partial',
            apt_root / 'etc' / 'apt' / 'preferences.d',
            apt_root / 'var' / 'lib' / 'dpkg',
            apt_root / 'var' / 'log' / 'apt'
    ):
        to_create.mkdir(parents=True, exist_ok=True)

    conf_path    = apt_root / 'etc' / 'apt.conf'
    trusted_path = apt_root / 'etc' / 'trusted.gpg'
    status_path  = apt_root / 'var' / 'lib' / 'dpkg' / 'status'
    list_path    = apt_root / 'etc' / 'apt.sources.list'

    conf_path.write_text(conf_text)
    trusted_path.write_bytes(keyring_bytes)
    status_path.touch()
    list_path.write_text('\n'.join(list.list))

    apt = Apt(str(conf_path))
    apt.get('update')

    cache_apt_root(apt_root, apt_zipfile)

    return apt

@contextmanager
def local_apt(list: SourcesList, keys: [str]) -> Iterable[Apt]:
    """
    Create a temporary directory with proper local APT configuration in it.
    Yield an Apt object that can be used to issue apt-get commands.

    This function returns a context manager that will remove the directory on
    close.
    """
    with TemporaryDirectory() as td:
        td = Path(td)
        yield setup_local_apt(td, list, keys)

def download_apt_packages(list: SourcesList, keys: [str], packages: [str],
                          destination_dir: Path, with_deps: bool) -> [str]:
    """
    Set up a local APT, update it using the specified sources.list configuration
    and use it to download the specified packages.

    This function downloads .deb files of packages matching the amd64
    architecture (which includes packages with architecture 'all') as well as
    all their corresponding source package files and (if requested) the debs
    and source files of all their declared dependencies.

    Return value is a list of names of all downloaded files.
    """
    install_line_regex = re.compile(r'^Inst (?P<name>\S+) \((?P<version>\S+) ')

    with local_apt(list, keys) as apt:
        if with_deps:
            cp = apt.get('install', '--yes', '--just-print', *packages)

            lines = cp.stdout.split('\n')
            matches = [install_line_regex.match(l) for l in lines]
            packages = [f'{m.group("name")}={m.group("version")}'
                        for m in matches if m]

            if not packages:
                raise AptError(_('apt_install_output_not_understood'), cp)

        # Download .debs to indirectly to destination_dir by first placing them
        # in a temporary subdirectory.
        with TemporaryDirectory(dir=destination_dir) as td:
            td = Path(td)
            cp = apt.get('download', *packages, cwd=td)

            deb_name_regex = re.compile(
                r'''
                ^
                (?P<name>[^_]+)
                _
                (?P<ver>[^_]+)
                _
                .+              # architecture (or 'all')
                \.deb
                $
                ''',
                re.VERBOSE)

            names_vers = []
            downloaded = []
            for deb_file in td.iterdir():
                match = deb_name_regex.match(deb_file.name)
                if match is None:
                    msg = _('apt_download_gave_bad_filename_{}')\
                        .format(deb_file.name)
                    raise AptError(msg, cp)

                names_vers.append((
                    unquote(match.group('name')),
                    unquote(match.group('ver'))
                ))
                downloaded.append(deb_file.name)

            apt.get('source', '--download-only',
                    *[f'{n}={v}' for n, v in names_vers], cwd=td)

            for source_file in td.iterdir():
                if source_file.name in downloaded:
                    continue

                downloaded.append(source_file.name)

            for filename in downloaded:
                shutil.move(td / filename, destination_dir / filename)

    return downloaded

@contextmanager
def piggybacked_system(piggyback_def: dict, foreign_packages: Optional[Path]) \
    -> Iterable[Piggybacked]:
    """
    Resolve resources from APT. Optionally, use package files (.deb's, etc.)
    from a specified directory instead of resolving and downloading them.

    The directories and files created for the yielded Piggybacked object shall
    be deleted when this context manager gets closed.
    """
    assert piggyback_def['system'] == 'apt'

    with TemporaryDirectory() as td:
        td       = Path(td)
        root     = td / 'root'
        root.mkdir()

        if foreign_packages is None:
            archives = td / 'archives'
            archives.mkdir()
        else:
            archives = foreign_packages / 'apt'
            archives.mkdir(exist_ok=True)

        if [*archives.glob('*.deb')] == []:
            sources_list = SourcesList(piggyback_def.get('sources_list', []),
                                       piggyback_def.get('distribution'))
            packages = piggyback_def['packages']
            with_deps = piggyback_def['dependencies']
            pgp_keys = [
                *default_keys,
                *piggyback_def.get('trusted_keys', [])
            ]

            download_apt_packages(
                list=sources_list,
                keys=pgp_keys,
                packages=packages,
                destination_dir=archives,
                with_deps=with_deps
            )

        for deb in archives.glob('*.deb'):
            command = ['dpkg-deb', '-x', str(deb), str(root)]
            try:
                cp = run(command)
            except FileNotFoundError:
                msg = _('couldnt_execute_{}_is_it_installed'.format('dpkg-deb'))
                raise AptError(msg)

            if cp.returncode != 0:
                msg = _('command_{}_failed').format(' '.join(command))
                raise AptError(msg, cp)

        docs_dir = root / 'usr' / 'share' / 'doc'
        copyright_paths = [p / 'copyright' for p in docs_dir.iterdir()] \
                    if docs_dir.exists() else []
        copyright_paths = [PurePosixPath('.apt-root') / p.relative_to(root)
                           for p in copyright_paths if p.exists()]

        standard_depends = piggyback_def.get('depend_on_base_packages', True)
        must_depend = [{'identifier': 'apt-common-licenses'}] \
            if standard_depends else []

        yield Piggybacked(
            archives={'apt': archives},
            roots={'.apt-root': root},
            package_license_files=copyright_paths,
            resource_must_depend=must_depend
        )
