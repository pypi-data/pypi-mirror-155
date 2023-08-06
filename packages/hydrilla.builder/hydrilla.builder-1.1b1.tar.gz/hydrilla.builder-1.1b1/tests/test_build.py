# SPDX-License-Identifier: CC0-1.0

# Copyright (C) 2022 Wojtek Kosior <koszko@koszko.org>
#
# Available under the terms of Creative Commons Zero v1.0 Universal.

# Enable using with Python 3.7.
from __future__ import annotations

import pytest
import json
import shutil
import functools as ft

from tempfile import TemporaryDirectory
from pathlib import Path, PurePosixPath
from hashlib import sha256
from zipfile import ZipFile
from contextlib import contextmanager

from jsonschema import ValidationError

from hydrilla import util as hydrilla_util
from hydrilla.util._util import _schema_name_re
from hydrilla.builder import build, _version, local_apt
from hydrilla.builder.common_errors import *

from .helpers import *

here = Path(__file__).resolve().parent

expected_generated_by = {
    'name': 'hydrilla.builder',
    'version': _version.version
}

orig_srcdir = here / 'source-package-example'

index_obj, _ = hydrilla_util.load_instance_from_file(orig_srcdir / 'index.json')

def read_files(*file_list):
    """
    Take names of files under srcdir and return a dict that maps them to their
    contents (as bytes).
    """
    return dict((name, (orig_srcdir / name).read_bytes()) for name in file_list)

dist_files = {
    **read_files('LICENSES/CC0-1.0.txt', 'bye.js', 'hello.js', 'message.js'),
    'report.spdx': b'dummy spdx output'
}
src_files = {
    **dist_files,
    **read_files('README.txt', 'README.txt.license', '.reuse/dep5',
                 'index.json')
}
extra_archive_files = {
}

sha256_hashes = dict((name, sha256(contents).digest().hex())
                     for name, contents in src_files.items())

del src_files['report.spdx']

expected_source_copyright = [{
    'file': 'report.spdx',
    'sha256': sha256_hashes['report.spdx']
}, {
    'file': 'LICENSES/CC0-1.0.txt',
    'sha256': sha256_hashes['LICENSES/CC0-1.0.txt']
}]

expected_resources = [{
    '$schema': 'https://hydrilla.koszko.org/schemas/api_resource_description-1.schema.json',
    'source_name': 'hello',
    'source_copyright': expected_source_copyright,
    'type': 'resource',
    'identifier': 'helloapple',
    'long_name': 'Hello Apple',
    'uuid': 'a6754dcb-58d8-4b7a-a245-24fd7ad4cd68',
    'version': [2021, 11, 10],
    'revision': 1,
    'description': 'greets an apple',
    'dependencies': [{'identifier': 'hello-message'}],
    'scripts': [{
        'file': 'hello.js',
        'sha256': sha256_hashes['hello.js']
    }, {
        'file': 'bye.js',
        'sha256': sha256_hashes['bye.js']
    }],
    'generated_by': expected_generated_by
}, {
    '$schema': 'https://hydrilla.koszko.org/schemas/api_resource_description-1.schema.json',
    'source_name': 'hello',
    'source_copyright': expected_source_copyright,
    'type': 'resource',
    'identifier': 'hello-message',
    'long_name': 'Hello Message',
    'uuid': '1ec36229-298c-4b35-8105-c4f2e1b9811e',
    'version': [2021, 11, 10],
    'revision': 2,
    'description': 'define messages for saying hello and bye',
    'dependencies': [],
    'scripts': [{
        'file': 'message.js',
        'sha256': sha256_hashes['message.js']
    }],
    'generated_by': expected_generated_by
}]

expected_mapping = {
    '$schema': 'https://hydrilla.koszko.org/schemas/api_mapping_description-1.schema.json',
    'source_name': 'hello',
    'source_copyright': expected_source_copyright,
    'type': 'mapping',
    'identifier': 'helloapple',
    'long_name': 'Hello Apple',
    'uuid': '54d23bba-472e-42f5-9194-eaa24c0e3ee7',
    'version': [2021, 11, 10],
    'description': 'causes apple to get greeted on Hydrillabugs issue tracker',
    'payloads': {
	'https://hydrillabugs.koszko.org/***': {
	    'identifier': 'helloapple'
	},
	'https://hachettebugs.koszko.org/***': {
	    'identifier': 'helloapple'
        }
    },
    'generated_by': expected_generated_by
}

expected_source_description = {
    '$schema': 'https://hydrilla.koszko.org/schemas/api_source_description-1.schema.json',
    'source_name': 'hello',
    'source_copyright': expected_source_copyright,
    'source_archives': {
        'zip': {
            'sha256': '!!!!value to fill during test!!!!',
        }
    },
    'upstream_url': 'https://git.koszko.org/hydrilla-source-package-example',
    'definitions': [{
        'type': 'mapping',
        'identifier': 'helloapple',
	'long_name': 'Hello Apple',
        'version': [2021, 11, 10],
    }, {
        'type': 'resource',
        'identifier': 'helloapple',
        'long_name': 'Hello Apple',
        'version': [2021, 11, 10],
    }, {
        'type':       'resource',
        'identifier': 'hello-message',
        'long_name': 'Hello Message',
        'version':     [2021, 11, 10],
    }],
    'generated_by': expected_generated_by
}

expected = [expected_mapping, *expected_resources, expected_source_description]
expected_items = expected[:3]

def run_reuse(command, **kwargs):
    """
    Instead of running a 'reuse' command, check if 'mock_reuse_missing' file
    exists under root directory. If yes, raise FileNotFoundError as if 'reuse'
    command was missing. If not, check if 'README.txt.license' file exists
    in the requested directory and return zero if it does.
    """
    expected = ['reuse', '--root', '<root>',
                'lint' if 'lint' in command else 'spdx']

    root_path = Path(process_command(command, expected)['root'])

    if (root_path / 'mock_reuse_missing').exists():
        raise FileNotFoundError('dummy')

    is_reuse_compliant = (root_path / 'README.txt.license').exists()

    return MockedCompletedProcess(command, 1 - is_reuse_compliant,
                                  stdout=f'dummy {expected[-1]} output',
                                  text_output=kwargs.get('text'))

mocked_piggybacked_archives = [
    PurePosixPath('apt/something.deb'),
    PurePosixPath('apt/something.orig.tar.gz'),
    PurePosixPath('apt/something.debian.tar.xz'),
    PurePosixPath('othersystem/other-something.tar.gz')
]

@pytest.fixture
def mock_piggybacked_apt_system(monkeypatch):
    """Make local_apt.piggybacked_system() return a mocked result."""
    # We set 'td' to a temporary dir path further below.
    td = None

    class MockedPiggybacked:
        """Minimal mock of Piggybacked object."""
        package_license_files = [PurePosixPath('.apt-root/.../copyright')]
        resource_must_depend = [{'identifier': 'apt-common-licenses'}]

        def resolve_file(path):
            """
            For each path that starts with '.apt-root' return a valid dummy file
            path.
            """
            if path.parts[0] != '.apt-root':
                return None

            (td / path.name).write_text(f'dummy {path.name}')

            return (td / path.name)

        def archive_files():
            """Yield some valid dummy file path tuples."""
            for desired_path in mocked_piggybacked_archives:
                real_path = td / desired_path.name
                real_path.write_text(f'dummy {desired_path.name}')

                yield desired_path, real_path

    @contextmanager
    def mocked_piggybacked_system(piggyback_def, piggyback_files):
        """Mock the execution of local_apt.piggybacked_system()."""
        assert piggyback_def == {
	    'system': 'apt',
	    'distribution': 'nabia',
	    'packages': ['somelib=1.0'],
	    'dependencies': False
        }
        if piggyback_files is not None:
            assert {str(path) for path in mocked_piggybacked_archives} == \
                {path.relative_to(piggyback_files).as_posix()
                 for path in piggyback_files.rglob('*') if path.is_file()}

        yield MockedPiggybacked

    monkeypatch.setattr(local_apt, 'piggybacked_system',
                        mocked_piggybacked_system)

    with TemporaryDirectory() as td:
        td = Path(td)
        yield

@pytest.fixture
def sample_source():
    """Prepare a directory with sample Haketilo source package."""
    with TemporaryDirectory() as td:
        sample_source = Path(td) / 'hello'
        for name, contents in src_files.items():
            path = sample_source / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(contents)

        yield sample_source

def collect(list):
    """Decorate function by appending it to the specified list."""
    def decorator(function):
        """The actual decorator that will be applied."""
        list.append(function)
        return function

    return decorator

variant_makers = []

@collect(variant_makers)
def sample_source_change_index_json(monkeypatch, sample_source):
    """
    Return a non-standard path for index.json. Ensure parent directories exist.
    """
    # Use a path under sample_source so that it gets auto-deleted after the
    # test. Use a file under .git because .git is ignored by REUSE.
    path = sample_source / '.git' / 'replacement.json'
    path.parent.mkdir()
    return path

@collect(variant_makers)
def sample_source_add_comments(monkeypatch, sample_source):
    """Add index.json comments that should be preserved."""
    for dictionary in (index_obj, *index_obj['definitions'], *expected):
        monkeypatch.setitem(dictionary, 'comment', 'index.json comment')

@collect(variant_makers)
def sample_source_remove_spdx(monkeypatch, sample_source):
    """Remove spdx report generation."""
    monkeypatch.delitem(index_obj, 'reuse_generate_spdx_report')

    pred = lambda ref: ref['file'] != 'report.spdx'
    copy_refs_in = list(filter(pred, index_obj['copyright']))
    monkeypatch.setitem(index_obj, 'copyright', copy_refs_in)

    copy_refs_out = list(filter(pred, expected_source_copyright))
    for obj in expected:
        monkeypatch.setitem(obj, 'source_copyright', copy_refs_out)

    monkeypatch.delitem(dist_files, 'report.spdx')

    # To verify that reuse does not get called now, make mocked subprocess.run()
    # raise an error if called.
    (sample_source / 'mock_reuse_missing').touch()

@collect(variant_makers)
def sample_source_remove_additional_files(monkeypatch, sample_source):
    """Use default value ([]) for 'additionall_files' property."""
    monkeypatch.delitem(index_obj, 'additional_files')

    for name in 'README.txt', 'README.txt.license', '.reuse/dep5':
        monkeypatch.delitem(src_files, name)

@collect(variant_makers)
def sample_source_remove_script(monkeypatch, sample_source):
    """Use default value ([]) for 'scripts' property in one of the resources."""
    monkeypatch.delitem(index_obj['definitions'][2], 'scripts')

    monkeypatch.setitem(expected_resources[1], 'scripts', [])

    for files in dist_files, src_files:
        monkeypatch.delitem(files, 'message.js')

@collect(variant_makers)
def sample_source_remove_payloads(monkeypatch, sample_source):
    """Use default value ({}) for 'payloads' property in mapping."""
    monkeypatch.delitem(index_obj['definitions'][0], 'payloads')

    monkeypatch.setitem(expected_mapping, 'payloads', {})

@collect(variant_makers)
def sample_source_remove_uuids(monkeypatch, sample_source):
    """Don't use UUIDs (they are optional)."""
    for definition in index_obj['definitions']:
        monkeypatch.delitem(definition, 'uuid')

    for description in expected:
        if 'uuid' in description:
            monkeypatch.delitem(description, 'uuid')

@collect(variant_makers)
def sample_source_add_extra_props(monkeypatch, sample_source):
    """Add some unrecognized properties that should be stripped."""
    to_process = [index_obj]
    while to_process:
        processed = to_process.pop()

        if type(processed) is list:
            to_process.extend(processed)
        elif type(processed) is dict and 'spurious_property' not in processed:
            to_process.extend(v for k, v in processed.items()
                              if k != 'payloads')
            monkeypatch.setitem(processed, 'spurious_property', 'some_value')

@collect(variant_makers)
def sample_source_make_version_2(monkeypatch, sample_source,
                                 expected_documents_to_modify=[]):
    """Increase sources' schema version from 1 to 2."""
    for obj in (index_obj, *expected_documents_to_modify):
        monkeypatch.setitem(obj, '$schema', obj['$schema'].replace('1', '2'))

permission_variant_makers = []

@collect(permission_variant_makers)
def sample_source_bool_perm_ignored(permission, monkeypatch, sample_source,
                                    value=True):
    """
    Specify a boolean permissions in sources, but keep sources' schema version
    at 1.
    """
    for definition in index_obj['definitions']:
        monkeypatch.setitem(definition, 'permissions', {permission: value})

@collect(permission_variant_makers)
def sample_source_bool_perm(permission, monkeypatch, sample_source):
    """Specify a boolean permission in sources."""
    sample_source_bool_perm_ignored(permission, monkeypatch, sample_source)
    sample_source_make_version_2(monkeypatch, sample_source, expected_items)

    for obj in expected_items:
        monkeypatch.setitem(obj, 'permissions', {permission: True})

@collect(permission_variant_makers)
def sample_source_bool_perm_defaults(permission, monkeypatch, sample_source):
    """
    Specify a boolean permission in sources but use the default value ("False").
    """
    sample_source_bool_perm_ignored(permission, monkeypatch, sample_source,
                                    value=False)
    sample_source_make_version_2(monkeypatch, sample_source)

for permission in 'cors_bypass', 'eval':
    for variant_maker in permission_variant_makers:
        variant_makers.append(ft.partial(variant_maker, permission))

@collect(variant_makers)
def sample_source_req_mappings_ignored(monkeypatch, sample_source,
                                       value=[{'identifier': 'mapping-dep'}]):
    """
    Specify dependencies on mappings, but keep sources' schema version at 1.
    """
    for definition in index_obj['definitions']:
        monkeypatch.setitem(definition, 'required_mappings', value);

@collect(variant_makers)
def sample_source_req_mappings(monkeypatch, sample_source):
    """Specify dependencies on mappings."""
    sample_source_req_mappings_ignored(monkeypatch, sample_source)
    sample_source_make_version_2(monkeypatch, sample_source, expected_items)

    for obj in expected_items:
        monkeypatch.setitem(obj, 'required_mappings',
                            [{'identifier': 'mapping-dep'}])

@collect(variant_makers)
def sample_source_req_mappings_defaults(monkeypatch, sample_source):
    """Specify dependencies of a mapping, but use the default value ("[]")."""
    sample_source_req_mappings_ignored(monkeypatch, sample_source, value=[])
    sample_source_make_version_2(monkeypatch, sample_source)

@collect(variant_makers)
def sample_source_combined_def(monkeypatch, sample_source):
    """Define mapping and resource together."""
    sample_source_make_version_2(monkeypatch, sample_source)

    mapping_def   = index_obj['definitions'][0]
    resource_defs = index_obj['definitions'][1:3]

    item_defs_shortened = [mapping_def, resource_defs[1]]
    monkeypatch.setitem(index_obj, 'definitions', item_defs_shortened)

    monkeypatch.setitem(mapping_def, 'type', 'mapping_and_resource')

    new_mapping_ver = [*expected_mapping['version'], 1]
    monkeypatch.setitem(mapping_def, 'revision', 1)
    monkeypatch.setitem(expected_mapping, 'version', new_mapping_ver)

    for prop in 'scripts', 'dependencies':
        monkeypatch.setitem(mapping_def, prop, resource_defs[0][prop])

    monkeypatch.setitem(expected_resources[0], 'uuid', mapping_def['uuid'])
    monkeypatch.setitem(expected_resources[0], 'description',
                        mapping_def['description'])

    monkeypatch.setitem(expected_source_description['definitions'][0],
                        'version', new_mapping_ver)

@collect(variant_makers)
def sample_source_minmax_haketilo_ver_ignored(monkeypatch, sample_source,
                                              min_ver=[1, 2], max_ver=[1, 2]):
    """
    Specify version constraints on Haketilo, but keep sources' schema version at
    1.
    """
    mapping_def = index_obj['definitions'][0]
    monkeypatch.setitem(mapping_def, 'min_haketilo_version', min_ver)
    monkeypatch.setitem(mapping_def, 'max_haketilo_version', max_ver)

@collect(variant_makers)
def sample_source_minmax_haketilo_ver(monkeypatch, sample_source):
    """Specify version constraints on Haketilo."""
    sample_source_minmax_haketilo_ver_ignored(monkeypatch, sample_source)
    sample_source_make_version_2(monkeypatch, sample_source, [expected_mapping])

    monkeypatch.setitem(expected_mapping, 'min_haketilo_version', [1, 2])
    monkeypatch.setitem(expected_mapping, 'max_haketilo_version', [1, 2])

@collect(variant_makers)
def sample_source_minmax_haketilo_ver_default(monkeypatch, sample_source):
    """Specify version constraints on Haketilo, but use default values."""
    sample_source_minmax_haketilo_ver_ignored(monkeypatch, sample_source,
                                              min_ver=[1], max_ver=[65536])
    sample_source_make_version_2(monkeypatch, sample_source)

piggyback_archive_names = [
    'apt/something.deb',
    'apt/something.orig.tar.gz',
    'apt/something.debian.tar.xz',
    'othersystem/other-something.tar.gz'
]

@collect(variant_makers)
def sample_source_add_piggyback_ignored(monkeypatch, sample_source,
                                        extra_build_args={}):
    """
    Add piggybacked foreign system packages, but keep sources' schema version at
    1.
    """
    old_build = build.Build
    new_build = lambda *a, **kwa: old_build(*a, **kwa, **extra_build_args)
    monkeypatch.setattr(build, 'Build', new_build)

    monkeypatch.setitem(index_obj, 'piggyback_on', {
	'system': 'apt',
	'distribution': 'nabia',
	'packages': ['somelib=1.0'],
	'dependencies': False
    })

@collect(variant_makers)
def sample_source_add_piggyback(monkeypatch, sample_source,
                                extra_build_args={}):
    """Add piggybacked foreign system packages."""
    sample_source_add_piggyback_ignored\
        (monkeypatch, sample_source, extra_build_args)

    sample_source_make_version_2(monkeypatch, sample_source)

    new_refs = {}
    for name in '.apt-root/.../copyright', '.apt-root/.../script.js':
        contents = f'dummy {PurePosixPath(name).name}'.encode()
        digest = sha256(contents).digest().hex()
        monkeypatch.setitem(dist_files, name, contents)
        monkeypatch.setitem(sha256_hashes, name, digest)
        new_refs[PurePosixPath(name).name] = {'file': name, 'sha256': digest}

    new_list = [*expected_source_copyright, new_refs['copyright']]
    for obj in expected:
        monkeypatch.setitem(obj, 'source_copyright', new_list)

    for obj in expected_resources:
        new_list = [{'identifier': 'apt-common-licenses'}, *obj['dependencies']]
        monkeypatch.setitem(obj, 'dependencies', new_list)

    for obj in index_obj['definitions'][1], expected_resources[0]:
        new_list = [new_refs['script.js'], *obj['scripts']]
        monkeypatch.setitem(obj, 'scripts', new_list)

    for name in piggyback_archive_names:
        path = PurePosixPath('hello.foreign-packages') / name
        monkeypatch.setitem(extra_archive_files, str(path),
                            f'dummy {path.name}'.encode())

def prepare_foreign_packages_dir(path):
    """
    Put some dummy archive in the directory so that it can be passed to
    piggybacked_system().
    """
    for name in piggyback_archive_names:
        archive_path = path / name
        archive_path.parent.mkdir(parents=True, exist_ok=True)
        archive_path.write_text(f'dummy {archive_path.name}')

@collect(variant_makers)
def sample_source_add_piggyback_pass_archives(monkeypatch, sample_source):
    """
    Add piggybacked foreign system packages, use pre-downloaded foreign package
    archives (have Build() find them in their default directory).
    """
    # Dir next to 'sample_source' will also be gc'd by sample_source() fixture.
    foreign_packages_dir = sample_source.parent / 'arbitrary-name'

    prepare_foreign_packages_dir(foreign_packages_dir)

    sample_source_add_piggyback(monkeypatch, sample_source,
                                {'piggyback_files': foreign_packages_dir})

@collect(variant_makers)
def sample_source_add_piggyback_find_archives(monkeypatch, sample_source):
    """
    Add piggybacked foreign system packages, use pre-downloaded foreign package
    archives (specify their directory as argument to Build()).
    """
    # Dir next to 'sample_source' will also be gc'd by sample_source() fixture.
    foreign_packages_dir = sample_source.parent / 'hello.foreign-packages'

    prepare_foreign_packages_dir(foreign_packages_dir)

    sample_source_add_piggyback(monkeypatch, sample_source)

@collect(variant_makers)
def sample_source_add_piggyback_no_download(monkeypatch, sample_source,
                                            pass_directory_to_build=False):
    """
    Add piggybacked foreign system packages, use pre-downloaded foreign package
    archives.
    """
    # Use a dir next to 'sample_source'; have it gc'd by sample_source fixture.
    if pass_directory_to_build:
        foreign_packages_dir = sample_source.parent / 'arbitrary-name'
    else:
        foreign_packages_dir = sample_source.parent / 'hello.foreign-packages'

    prepare_foreign_packages_dir(foreign_packages_dir)

    sample_source_add_piggyback(monkeypatch, sample_source)

@pytest.fixture(params=[lambda m, s: None, *variant_makers])
def sample_source_make_variants(request, monkeypatch, sample_source,
                                mock_piggybacked_apt_system):
    """
    Prepare a directory with sample Haketilo source package in multiple slightly
    different versions (all correct). Return an index.json path that should be
    used when performing test build.
    """
    index_path = request.param(monkeypatch, sample_source) or Path('index.json')

    index_text = json.dumps(index_obj)

    (sample_source / index_path).write_text(index_text)

    monkeypatch.setitem(src_files, 'index.json', index_text.encode())

    return index_path

def try_validate(as_what, instance):
    """
    Select the right JSON schema. Return without errors only if the instance
    validates against it.
    """
    major = _schema_name_re.search(instance['$schema']).group('major')
    exact_schema_version = {'1': '1.0.1', '2': '2'}[major]
    schema_filename = f'{as_what}-{exact_schema_version}.schema.json'
    hydrilla_util.validator_for(schema_filename).validate(instance)

@pytest.mark.subprocess_run(build, run_reuse)
@pytest.mark.usefixtures('mock_subprocess_run')
def test_build(sample_source, sample_source_make_variants, tmpdir):
    """Build the sample source package and verify the produced files."""
    index_json_path = sample_source_make_variants

    # First, build the package
    build.Build(sample_source, index_json_path).write_package_files(tmpdir)

    # Verify directories under destination directory
    assert {'file', 'resource', 'mapping', 'source'} == \
        set([path.name for path in tmpdir.iterdir()])

    # Verify files under 'file/'
    file_dir = tmpdir / 'file' / 'sha256'

    for name, contents in dist_files.items():
        dist_file_path = file_dir / sha256_hashes[name]
        assert dist_file_path.is_file()
        assert dist_file_path.read_bytes() == contents

    assert {p.name for p in file_dir.iterdir()} == \
        {sha256_hashes[name] for name in dist_files.keys()}

    # Verify files under 'resource/'
    resource_dir = tmpdir / 'resource'

    assert {rj['identifier'] for rj in expected_resources} == \
        {path.name for path in resource_dir.iterdir()}

    for resource_json in expected_resources:
        subdir = resource_dir / resource_json['identifier']
        ver_str = hydrilla_util.version_string(resource_json['version'])
        assert [ver_str] == [path.name for path in subdir.iterdir()]

        assert json.loads((subdir / ver_str).read_text()) == resource_json

        try_validate('api_resource_description', resource_json)

    # Verify files under 'mapping/'
    mapping_dir = tmpdir / 'mapping'
    assert ['helloapple'] == [path.name for path in mapping_dir.iterdir()]

    subdir = mapping_dir / 'helloapple'

    ver_str = hydrilla_util.version_string(expected_mapping['version'])
    assert [ver_str] == [path.name for path in subdir.iterdir()]

    assert json.loads((subdir / ver_str).read_text()) == expected_mapping

    try_validate('api_mapping_description', expected_mapping)

    # Verify files under 'source/'
    source_dir = tmpdir / 'source'
    assert {'hello.json', 'hello.zip'} == \
        {path.name for path in source_dir.iterdir()}

    archive_files = {**dict((f'hello/{name}', contents)
                            for name, contents in src_files.items()),
                     **extra_archive_files}

    with ZipFile(source_dir / 'hello.zip', 'r') as archive:
        print(archive.namelist())
        assert len(archive.namelist()) == len(archive_files)

        for name, contents in archive_files.items():
            assert archive.read(name) == contents

    zip_ref = expected_source_description['source_archives']['zip']
    zip_contents = (source_dir / 'hello.zip').read_bytes()
    zip_ref['sha256'] = sha256(zip_contents).digest().hex()

    assert json.loads((source_dir / 'hello.json').read_text()) == \
        expected_source_description

    try_validate('api_source_description', expected_source_description)

error_makers = []

@collect(error_makers)
def sample_source_error_missing_file(monkeypatch, sample_source):
    """
    Modify index.json to expect missing report.spdx file and cause an error.
    """
    monkeypatch.delitem(index_obj, 'reuse_generate_spdx_report')
    return FileReferenceError, '^referenced_file_report.spdx_missing$'

@collect(error_makers)
def sample_source_error_index_schema(monkeypatch, sample_source):
    """Modify index.json to be incompliant with the schema."""
    monkeypatch.delitem(index_obj, 'definitions')
    return ValidationError,

@collect(error_makers)
def sample_source_error_unknown_index_schema(monkeypatch, sample_source):
    """Modify index.json to be use a not-yet-released schema."""
    schema_id = \
        'https://hydrilla.koszko.org/schemas/package_source-65536.schema.json'
    monkeypatch.setitem(index_obj, "$schema", schema_id)
    return hydrilla_util.UnknownSchemaError, \
        r'^unknown_schema_package_source_.*/hello/index\.json$'

@collect(error_makers)
def sample_source_error_bad_comment(monkeypatch, sample_source):
    """Modify index.json to have an invalid '/' in it."""
    return json.JSONDecodeError, '^bad_comment: .*', \
        json.dumps(index_obj) + '/something\n'

@collect(error_makers)
def sample_source_error_bad_json(monkeypatch, sample_source):
    """Modify index.json to not be valid json even after comment stripping."""
    return json.JSONDecodeError, '', json.dumps(index_obj) + '???\n'

@collect(error_makers)
def sample_source_error_missing_reuse(monkeypatch, sample_source):
    """Cause mocked reuse process invocation to fail with FileNotFoundError."""
    (sample_source / 'mock_reuse_missing').touch()
    return build.ReuseError, '^couldnt_execute_reuse_is_it_installed$'

@collect(error_makers)
def sample_source_error_missing_license(monkeypatch, sample_source):
    """Remove a file to make package REUSE-incompliant."""
    (sample_source / 'README.txt.license').unlink()

    error_regex = """^\
command_reuse --root \\S+ lint_failed

STDOUT_OUTPUT_heading

dummy lint output

STDERR_OUTPUT_heading

some error output\
$\
"""

    return build.ReuseError, error_regex

@collect(error_makers)
def sample_source_error_file_outside(monkeypatch, sample_source):
    """Make index.json illegally reference a file outside srcdir."""
    new_list = [*index_obj['copyright'], {'file': '../abc'}]
    monkeypatch.setitem(index_obj, 'copyright', new_list)
    return FileReferenceError, '^path_contains_double_dot_\\.\\./abc$'

@collect(error_makers)
def sample_source_error_reference_itself(monkeypatch, sample_source):
    """Make index.json illegally reference index.json."""
    new_list = [*index_obj['copyright'], {'file': 'index.json'}]
    monkeypatch.setitem(index_obj, 'copyright', new_list)
    return FileReferenceError, '^loading_reserved_index_json$'

@collect(error_makers)
def sample_source_error_report_excluded(monkeypatch, sample_source):
    """
    Make index.json require generation of report.spdx but don't include it among
    copyright files.
    """
    new_list = [file_ref for file_ref in index_obj['copyright']
                if file_ref['file'] != 'report.spdx']
    monkeypatch.setitem(index_obj, 'copyright', new_list)
    return FileReferenceError, '^report_spdx_not_in_copyright_list$'

@collect(error_makers)
def sample_source_error_combined_unsupported(monkeypatch, sample_source):
    """
    Define mapping and resource together but leave source schema version at 1.x
    where this is unsupported.
    """
    mapping_def = index_obj['definitions'][0]
    monkeypatch.setitem(mapping_def, 'type', 'mapping_and_resource')

    return ValidationError,

@pytest.fixture(params=error_makers)
def sample_source_make_errors(request, monkeypatch, sample_source):
    """
    Prepare a directory with sample Haketilo source package in multiple slightly
    broken versions. Return an error type that should be raised when running
    test build.
    """
    error_type, error_regex, index_text = \
        [*request.param(monkeypatch, sample_source), '', ''][0:3]

    index_text = index_text or json.dumps(index_obj)

    (sample_source / 'index.json').write_text(index_text)

    monkeypatch.setitem(src_files, 'index.json', index_text.encode())

    return error_type, error_regex

@pytest.mark.subprocess_run(build, run_reuse)
@pytest.mark.usefixtures('mock_subprocess_run')
def test_build_error(tmpdir, sample_source, sample_source_make_errors):
    """Try building the sample source package and verify generated errors."""
    error_type, error_regex = sample_source_make_errors

    dstdir = Path(tmpdir) / 'dstdir'
    dstdir.mkdir(exist_ok=True)

    with pytest.raises(error_type, match=error_regex):
        build.Build(sample_source, Path('index.json'))\
             .write_package_files(dstdir)
