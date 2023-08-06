# SPDX-License-Identifier: AGPL-3.0-or-later

# Building Hydrilla packages.
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

import json
import re
import zipfile
import subprocess
from pathlib import Path, PurePosixPath
from hashlib import sha256
from sys import stderr
from contextlib import contextmanager
from tempfile import TemporaryDirectory, TemporaryFile
from typing import Optional, Iterable, Union

import jsonschema
import click

from .. import util
from . import _version
from . import local_apt
from .piggybacking import Piggybacked
from .common_errors import *

here = Path(__file__).resolve().parent

_ = util.translation(here / 'locales').gettext

schemas_root = 'https://hydrilla.koszko.org/schemas'

generated_by = {
    'name': 'hydrilla.builder',
    'version': _version.version
}

class ReuseError(SubprocessError):
    """
    Exception used to report various problems when calling the REUSE tool.
    """

def generate_spdx_report(root: Path) -> bytes:
    """
    Use REUSE tool to generate an SPDX report for sources under 'root' and
    return the report's contents as 'bytes'.

    In case the directory tree under 'root' does not constitute a
    REUSE-compliant package, as exception is raised with linting report
    included in it.

    In case the reuse tool is not installed, an exception is also raised.
    """
    for command in [
            ['reuse', '--root', str(root), 'lint'],
            ['reuse', '--root', str(root), 'spdx']
    ]:
        try:
            cp = subprocess.run(command, capture_output=True, text=True)
        except FileNotFoundError:
            msg = _('couldnt_execute_{}_is_it_installed').format('reuse')
            raise ReuseError(msg)

        if cp.returncode != 0:
            msg = _('command_{}_failed').format(' '.join(command))
            raise ReuseError(msg, cp)

    return cp.stdout.encode()

class FileRef:
    """Represent reference to a file in the package."""
    def __init__(self, path: PurePosixPath, contents: bytes) -> None:
        """Initialize FileRef."""
        self.include_in_distribution   = False
        self.include_in_source_archive = True
        self.path                      = path
        self.contents                  = contents

        self.contents_hash = sha256(contents).digest().hex()

    def make_ref_dict(self) -> dict[str, str]:
        """
        Represent the file reference through a dict that can be included in JSON
        defintions.
        """
        return {
            'file':   str(self.path),
            'sha256': self.contents_hash
        }

@contextmanager
def piggybacked_system(piggyback_def: Optional[dict],
                       piggyback_files: Optional[Path]) \
                       -> Iterable[Piggybacked]:
    """
    Resolve resources from a foreign software packaging system. Optionally, use
    package files (.deb's, etc.) from a specified directory instead of resolving
    and downloading them.
    """
    if piggyback_def is None:
        yield Piggybacked()
    else:
        # apt is the only supported system right now
        assert piggyback_def['system'] == 'apt'

        with local_apt.piggybacked_system(piggyback_def, piggyback_files) \
             as piggybacked:
            yield piggybacked

class Build:
    """
    Build a Hydrilla package.
    """
    def __init__(self, srcdir: Path, index_json_path: Path,
                 piggyback_files: Optional[Path]=None):
        """
        Initialize a build. All files to be included in a distribution package
        are loaded into memory, all data gets validated and all necessary
        computations (e.g. preparing of hashes) are performed.
        """
        self.srcdir          = srcdir.resolve()
        self.piggyback_files = piggyback_files
        if piggyback_files is None:
            piggyback_default_path = \
                srcdir.parent / f'{srcdir.name}.foreign-packages'
            if piggyback_default_path.exists():
                self.piggyback_files = piggyback_default_path
        self.files_by_path   = {}
        self.resource_list   = []
        self.mapping_list    = []

        if not index_json_path.is_absolute():
            index_json_path = (self.srcdir / index_json_path)

        index_obj, major = util.load_instance_from_file(index_json_path)

        if major not in (1, 2):
            msg = _('unknown_schema_package_source_{}')\
                .format(index_json_path)
            raise util.UnknownSchemaError(msg)

        index_desired_path = PurePosixPath('index.json')
        self.files_by_path[index_desired_path] = \
            FileRef(index_desired_path, index_json_path.read_bytes())

        self._process_index_json(index_obj, major)

    def _process_file(self, filename: Union[str, PurePosixPath],
                      piggybacked: Piggybacked,
                      include_in_distribution: bool=True):
        """
        Resolve 'filename' relative to srcdir, load it to memory (if not loaded
        before), compute its hash and store its information in
        'self.files_by_path'.

        'filename' shall represent a relative path withing package directory.

        if 'include_in_distribution' is True it shall cause the file to not only
        be included in the source package's zipfile, but also written as one of
        built package's files.

        For each file an attempt is made to resolve it using 'piggybacked'
        object. If a file is found and pulled from foreign software packaging
        system this way, it gets automatically excluded from inclusion in
        Hydrilla source package's zipfile.

        Return file's reference object that can be included in JSON defintions
        of various kinds.
        """
        include_in_source_archive = True

        desired_path = PurePosixPath(filename)
        if '..' in desired_path.parts:
            msg = _('path_contains_double_dot_{}').format(filename)
            raise FileReferenceError(msg)

        path = piggybacked.resolve_file(desired_path)
        if path is None:
            path = (self.srcdir / desired_path).resolve()
            try:
                rel_path = path.relative_to(self.srcdir)
            except ValueError:
                raise FileReferenceError(_('loading_{}_outside_package_dir')
                                         .format(filename))

            if str(rel_path) == 'index.json':
                raise FileReferenceError(_('loading_reserved_index_json'))
        else:
            include_in_source_archive = False

        file_ref = self.files_by_path.get(desired_path)
        if file_ref is None:
            if not path.is_file():
                msg = _('referenced_file_{}_missing').format(desired_path)
                raise FileReferenceError(msg)

            file_ref = FileRef(desired_path, path.read_bytes())
            self.files_by_path[desired_path] = file_ref

        if include_in_distribution:
            file_ref.include_in_distribution = True

        if not include_in_source_archive:
            file_ref.include_in_source_archive = False

        return file_ref.make_ref_dict()

    def _prepare_source_package_zip(self, source_name: str,
                                    piggybacked: Piggybacked) -> str:
        """
        Create and store in memory a .zip archive containing files needed to
        build this source package.

        'src_dir_name' shall not contain any slashes ('/').

        Return zipfile's sha256 sum's hexstring.
        """
        tf = TemporaryFile()
        source_dir_path      = PurePosixPath(source_name)
        piggybacked_dir_path = PurePosixPath(f'{source_name}.foreign-packages')

        with zipfile.ZipFile(tf, 'w') as zf:
            for file_ref in self.files_by_path.values():
                if file_ref.include_in_source_archive:
                    zf.writestr(str(source_dir_path / file_ref.path),
                                file_ref.contents)

            for desired_path, real_path in piggybacked.archive_files():
                zf.writestr(str(piggybacked_dir_path / desired_path),
                            real_path.read_bytes())

        tf.seek(0)
        self.source_zip_contents = tf.read()

        return sha256(self.source_zip_contents).digest().hex()

    def _process_item(self, as_what: str, item_def: dict,
                      piggybacked: Piggybacked):
        """
        Process 'item_def' as definition of a resource or mapping (determined by
        'as_what' param) and store in memory its processed form and files used
        by it.

        Return a minimal item reference suitable for using in source
        description.
        """
        resulting_schema_version = [1]

        copy_props = ['identifier', 'long_name', 'description',
                      *filter(lambda p: p in item_def, ('comment', 'uuid'))]

        if as_what == 'resource':
            item_list = self.resource_list

            copy_props.append('revision')

            script_file_refs = [self._process_file(f['file'], piggybacked)
                                for f in item_def.get('scripts', [])]

            deps = [{'identifier': res_ref['identifier']}
                    for res_ref in item_def.get('dependencies', [])]

            new_item_obj = {
                'dependencies': [*piggybacked.resource_must_depend, *deps],
                'scripts':      script_file_refs
            }
        else:
            item_list = self.mapping_list

            payloads = {}
            for pat, res_ref in item_def.get('payloads', {}).items():
                payloads[pat] = {'identifier': res_ref['identifier']}

            new_item_obj = {
                'payloads': payloads
            }

        new_item_obj['version'] = util.normalize_version(item_def['version'])

        if as_what == 'mapping' and item_def['type'] == "mapping_and_resource":
            new_item_obj['version'].append(item_def['revision'])

        if self.source_schema_ver >= [2]:
            # handle 'required_mappings' field
            required = [{'identifier': map_ref['identifier']}
                        for map_ref in item_def.get('required_mappings', [])]
            if required:
                resulting_schema_version = max(resulting_schema_version, [2])
                new_item_obj['required_mappings'] = required

            # handle 'permissions' field
            permissions = item_def.get('permissions', {})
            processed_permissions = {}

            if permissions.get('cors_bypass'):
                processed_permissions['cors_bypass'] = True
            if permissions.get('eval'):
                processed_permissions['eval'] = True

            if processed_permissions:
                new_item_obj['permissions'] = processed_permissions
                resulting_schema_version = max(resulting_schema_version, [2])

            # handle '{min,max}_haketilo_version' fields
            for minmax, default in ('min', [1]), ('max', [65536]):
                constraint = item_def.get(f'{minmax}_haketilo_version')
                if constraint in (None, default):
                    continue

                copy_props.append(f'{minmax}_haketilo_version')
                resulting_schema_version = max(resulting_schema_version, [2])

        new_item_obj.update((p, item_def[p]) for p in copy_props)

        new_item_obj['$schema'] = ''.join([
            schemas_root,
            f'/api_{as_what}_description',
            '-',
            util.version_string(resulting_schema_version),
            '.schema.json'
        ])
        new_item_obj['type']             = as_what
        new_item_obj['source_copyright'] = self.copyright_file_refs
        new_item_obj['source_name']      = self.source_name
        new_item_obj['generated_by']     = generated_by

        item_list.append(new_item_obj)

        props_in_ref = ('type', 'identifier', 'version', 'long_name')
        return dict([(prop, new_item_obj[prop]) for prop in props_in_ref])

    def _process_index_json(self, index_obj: dict,
                            major_schema_version: int) -> None:
        """
        Process 'index_obj' as contents of source package's index.json and store
        in memory this source package's zipfile as well as package's individual
        files and computed definitions of the source package and items defined
        in it.
        """
        schema_name = f'package_source-{major_schema_version}.schema.json';

        util.validator_for(schema_name).validate(index_obj)

        match = re.match(r'.*-((([1-9][0-9]*|0)\.)+)schema\.json$',
                         index_obj['$schema'])
        self.source_schema_ver = \
            [int(n) for n in filter(None, match.group(1).split('.'))]

        out_schema = f'{schemas_root}/api_source_description-1.schema.json'

        self.source_name = index_obj['source_name']

        generate_spdx = index_obj.get('reuse_generate_spdx_report', False)
        if generate_spdx:
            contents  = generate_spdx_report(self.srcdir)
            spdx_path = PurePosixPath('report.spdx')
            spdx_ref  = FileRef(spdx_path, contents)

            spdx_ref.include_in_source_archive = False
            self.files_by_path[spdx_path] = spdx_ref

        piggyback_def = None
        if self.source_schema_ver >= [1, 1] and 'piggyback_on' in index_obj:
            piggyback_def = index_obj['piggyback_on']

        with piggybacked_system(piggyback_def, self.piggyback_files) \
             as piggybacked:
            copyright_to_process = [
                *(file_ref['file'] for file_ref in index_obj['copyright']),
                *piggybacked.package_license_files
            ]
            self.copyright_file_refs = [self._process_file(f, piggybacked)
                                        for f in copyright_to_process]

            if generate_spdx and not spdx_ref.include_in_distribution:
                raise FileReferenceError(_('report_spdx_not_in_copyright_list'))

            item_refs = []
            for item_def in index_obj['definitions']:
                if 'mapping' in item_def['type']:
                    ref = self._process_item('mapping', item_def, piggybacked)
                    item_refs.append(ref)
                if 'resource' in item_def['type']:
                    ref = self._process_item('resource', item_def, piggybacked)
                    item_refs.append(ref)

            for file_ref in index_obj.get('additional_files', []):
                self._process_file(file_ref['file'], piggybacked,
                                   include_in_distribution=False)

            zipfile_sha256 = self._prepare_source_package_zip\
                (self.source_name, piggybacked)

            source_archives_obj = {'zip' : {'sha256': zipfile_sha256}}

        self.source_description = {
            '$schema':            out_schema,
            'source_name':        self.source_name,
            'source_copyright':   self.copyright_file_refs,
            'upstream_url':       index_obj['upstream_url'],
            'definitions':        item_refs,
            'source_archives':    source_archives_obj,
            'generated_by':       generated_by
        }

        if 'comment' in index_obj:
            self.source_description['comment'] = index_obj['comment']

    def write_source_package_zip(self, dstpath: Path):
        """
        Create a .zip archive containing files needed to build this source
        package and write it at 'dstpath'.
        """
        with open(dstpath, 'wb') as output:
            output.write(self.source_zip_contents)

    def write_package_files(self, dstpath: Path):
        """Write package files under 'dstpath' for distribution."""
        file_dir_path = (dstpath / 'file' / 'sha256').resolve()
        file_dir_path.mkdir(parents=True, exist_ok=True)

        for file_ref in self.files_by_path.values():
            if file_ref.include_in_distribution:
                file_path = file_dir_path / file_ref.contents_hash
                file_path.write_bytes(file_ref.contents)

        source_dir_path = (dstpath / 'source').resolve()
        source_dir_path.mkdir(parents=True, exist_ok=True)
        source_name = self.source_description["source_name"]

        with open(source_dir_path / f'{source_name}.json', 'wt') as output:
            json.dump(self.source_description, output)

        with open(source_dir_path / f'{source_name}.zip', 'wb') as output:
            output.write(self.source_zip_contents)

        for item_type, item_list in [
                ('resource', self.resource_list),
                ('mapping', self.mapping_list)
        ]:
            item_type_dir_path = (dstpath / item_type).resolve()

            for item_def in item_list:
                item_dir_path = item_type_dir_path / item_def['identifier']
                item_dir_path.mkdir(parents=True, exist_ok=True)

                version = '.'.join([str(n) for n in item_def['version']])
                with open(item_dir_path / version, 'wt') as output:
                    json.dump(item_def, output)

dir_type = click.Path(exists=True, file_okay=False, resolve_path=True)

@click.command(help=_('build_package_from_srcdir_to_dstdir'))
@click.option('-s', '--srcdir', default='./', type=dir_type, show_default=True,
              help=_('source_directory_to_build_from'))
@click.option('-i', '--index-json', default='index.json', type=click.Path(),
              help=_('path_instead_of_index_json'))
@click.option('-p', '--piggyback-files', type=click.Path(),
              help=_('path_instead_for_piggyback_files'))
@click.option('-d', '--dstdir', type=dir_type, required=True,
              help=_('built_package_files_destination'))
@click.version_option(version=_version.version, prog_name='Hydrilla builder',
                      message=_('%(prog)s_%(version)s_license'),
                      help=_('version_printing'))
def perform(srcdir, index_json, piggyback_files, dstdir):
    """
    Execute Hydrilla builder to turn source package into a distributable one.

    This command is meant to be the entry point of hydrilla-builder command
    exported by this package.
    """
    build = Build(Path(srcdir), Path(index_json),
                  piggyback_files and Path(piggyback_files))
    build.write_package_files(Path(dstdir))
