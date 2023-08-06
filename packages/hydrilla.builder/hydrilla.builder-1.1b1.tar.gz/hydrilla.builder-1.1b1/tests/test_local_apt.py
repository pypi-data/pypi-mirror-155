# SPDX-License-Identifier: CC0-1.0

# Copyright (C) 2022 Wojtek Kosior <koszko@koszko.org>
#
# Available under the terms of Creative Commons Zero v1.0 Universal.

import pytest
import tempfile
import re
import json
from pathlib import Path, PurePosixPath
from zipfile import ZipFile
from tempfile import TemporaryDirectory

from hydrilla.builder import local_apt
from hydrilla.builder.common_errors import *

here = Path(__file__).resolve().parent

from .helpers import *

@pytest.fixture
def mock_cache_dir(monkeypatch):
    """Make local_apt.py cache files to a temporary directory."""
    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        monkeypatch.setattr(local_apt, 'default_apt_cache_dir', td_path)
        yield td_path

@pytest.fixture
def mock_gnupg_import(monkeypatch, mock_cache_dir):
    """Mock gnupg library when imported dynamically."""

    gnupg_mock_dir = mock_cache_dir / 'gnupg_mock'
    gnupg_mock_dir.mkdir()
    (gnupg_mock_dir / 'gnupg.py').write_text('GPG = None\n')

    monkeypatch.syspath_prepend(str(gnupg_mock_dir))

    import gnupg

    keyring_path = mock_cache_dir / 'master_keyring.gpg'

    class MockedImportResult:
        """gnupg.ImportResult replacement"""
        def __init__(self):
            """Initialize MockedImportResult object."""
            self.imported = 1

    class MockedGPG:
        """GPG replacement that does not really invoke GPG."""
        def __init__(self, keyring):
            """Verify the keyring path and initialize MockedGPG."""
            assert keyring == str(keyring_path)

            self.known_keys = {*keyring_path.read_text().split('\n')} \
                if keyring_path.exists() else set()

        def recv_keys(self, keyserver, key):
            """Mock key receiving - record requested key as received."""
            assert keyserver == local_apt.default_keyserver
            assert key not in self.known_keys

            self.known_keys.add(key)
            keyring_path.write_text('\n'.join(self.known_keys))

            return MockedImportResult()

        def list_keys(self, keys=None):
            """Mock key listing - return a list with dummy items."""
            if keys is None:
                return ['dummy'] * len(self.known_keys)
            else:
                return ['dummy' for k in keys if k in self.known_keys]

        def export_keys(self, keys, **kwargs):
            """
            Mock key export - check that the call has the expected arguments and
            return a dummy bytes array.
            """
            assert kwargs['armor']   == False
            assert kwargs['minimal'] == True
            assert {*keys} == self.known_keys

            return b'<dummy keys export>'

    monkeypatch.setattr(gnupg, 'GPG', MockedGPG)

def process_run_args(command, kwargs, expected_command):
    """
    Perform assertions common to all mocked subprocess.run() invocations and
    extract variable parts of the command line (if any).
    """
    assert kwargs['env'] == {'LANG': 'en_US'}
    assert kwargs['capture_output'] == True

    return process_command(command, expected_command)

def run_apt_get_update(command, returncode=0, **kwargs):
    """
    Instead of running an 'apt-get update' command just touch some file in apt
    root to indicate that the call was made.
    """
    expected = ['apt-get', '-c', '<conf_path>', 'update']
    conf_path = Path(process_run_args(command, kwargs, expected)['conf_path'])

    (conf_path.parent / 'update_called').touch()

    return MockedCompletedProcess(command, returncode,
                                  text_output=kwargs.get('text'))

"""
Output of 'apt-get install --yes --just-print libjs-mathjax' on some APT-based
system.
"""
sample_install_stdout = '''\
NOTE: This is only a simulation!
      apt-get needs root privileges for real execution.
      Keep also in mind that locking is deactivated,
      so don't depend on the relevance to the real current situation!
Reading package lists...
Building dependency tree...
Reading state information...
The following additional packages will be installed:
  fonts-mathjax
Suggested packages:
  fonts-mathjax-extras fonts-stix libjs-mathjax-doc
The following NEW packages will be installed:
  fonts-mathjax libjs-mathjax
0 upgraded, 2 newly installed, 0 to remove and 0 not upgraded.
Inst fonts-mathjax (0:2.7.9+dfsg-1 Devuan:4.0/stable, Devuan:1.0.0/unstable [all])
Inst libjs-mathjax (0:2.7.9+dfsg-1 Devuan:4.0/stable, Devuan:1.0.0/unstable [all])
Conf fonts-mathjax (0:2.7.9+dfsg-1 Devuan:4.0/stable, Devuan:1.0.0/unstable [all])
Conf libjs-mathjax (0:2.7.9+dfsg-1 Devuan:4.0/stable, Devuan:1.0.0/unstable [all])
'''

def run_apt_get_install(command, returncode=0, **kwargs):
    """
    Instead of running an 'apt-get install' command just print a possible
    output of one.
    """
    expected = ['apt-get', '-c', '<conf_path>', 'install',
                '--yes', '--just-print', 'libjs-mathjax']

    conf_path = Path(process_run_args(command, kwargs, expected)['conf_path'])

    return MockedCompletedProcess(command, returncode,
                                  stdout=sample_install_stdout,
                                  text_output=kwargs.get('text'))

def run_apt_get_download(command, returncode=0, **kwargs):
    """
    Instead of running an 'apt-get download' command just write some dummy
    .deb to the appropriate directory.
    """
    expected = ['apt-get', '-c', '<conf_path>', 'download']
    if 'libjs-mathjax' in command:
        expected.append('libjs-mathjax')
    else:
        expected.append('fonts-mathjax=0:2.7.9+dfsg-1')
        expected.append('libjs-mathjax=0:2.7.9+dfsg-1')

    conf_path = Path(process_run_args(command, kwargs, expected)['conf_path'])

    destination = Path(kwargs.get('cwd') or Path.cwd())

    package_name_regex = re.compile(r'^[^=]+-mathjax')

    for word in expected:
        match = package_name_regex.match(word)
        if match:
            filename = f'{match.group(0)}_0%3a2.7.9+dfsg-1_all.deb'
            deb_path = destination / filename
            deb_path.write_text(f'dummy {deb_path.name}')

    return MockedCompletedProcess(command, returncode,
                                  text_output=kwargs.get('text'))

def run_apt_get_source(command, returncode=0, **kwargs):
    """
    Instead of running an 'apt-get source' command just write some dummy
    "tarballs" to the appropriate directory.
    """
    expected = ['apt-get', '-c', '<conf_path>', 'source',
                '--download-only', 'libjs-mathjax=0:2.7.9+dfsg-1']
    if 'fonts-mathjax=0:2.7.9+dfsg-1' in command:
        if command[-1] == 'fonts-mathjax=0:2.7.9+dfsg-1':
            expected.append('fonts-mathjax=0:2.7.9+dfsg-1')
        else:
            expected.insert(-1, 'fonts-mathjax=0:2.7.9+dfsg-1')

    destination = Path(kwargs.get('cwd') or Path.cwd())
    for filename in [
        'mathjax_2.7.9+dfsg-1.debian.tar.xz',
        'mathjax_2.7.9+dfsg-1.dsc',
        'mathjax_2.7.9+dfsg.orig.tar.xz'
    ]:
        (destination / filename).write_text(f'dummy {filename}')

    return MockedCompletedProcess(command, returncode,
                                  text_output=kwargs.get('text'))

def make_run_apt_get(**returncodes):
    """
    Produce a function that chooses and runs the appropriate one of
    subprocess_run_apt_get_*() mock functions.
    """
    def mock_run(command, **kwargs):
        """
        Chooses and runs the appropriate one of subprocess_run_apt_get_*() mock
        functions.
        """
        for subcommand, run in [
            ('update',   run_apt_get_update),
            ('install',  run_apt_get_install),
            ('download', run_apt_get_download),
            ('source',   run_apt_get_source)
        ]:
            if subcommand in command:
                returncode = returncodes.get(f'{subcommand}_code', 0)
                return run(command, returncode, **kwargs)

        raise Exception('Unknown command: {}'.format(' '.join(command)))

    return mock_run

@pytest.mark.subprocess_run(local_apt, make_run_apt_get())
@pytest.mark.usefixtures('mock_subprocess_run', 'mock_gnupg_import')
def test_local_apt_contextmanager(mock_cache_dir):
    """
    Verify that the local_apt() function creates a proper apt environment and
    that it also properly restores it from cache.
    """
    sources_list = local_apt.SourcesList(['deb-src sth', 'deb sth'])

    with local_apt.local_apt(sources_list, local_apt.default_keys) as apt:
        apt_root = Path(apt.apt_conf).parent.parent

        assert (apt_root / 'etc' / 'trusted.gpg').read_bytes() == \
            b'<dummy keys export>'

        assert (apt_root / 'etc' / 'update_called').exists()

        assert (apt_root / 'etc' / 'apt.sources.list').read_text() == \
            'deb-src sth\ndeb sth'

        conf_lines = (apt_root / 'etc' / 'apt.conf').read_text().split('\n')

        # check mocked keyring
        assert {*local_apt.default_keys} == \
            {*(mock_cache_dir / 'master_keyring.gpg').read_text().split('\n')}

    assert not apt_root.exists()

    expected_conf = {
        'Architecture':           'amd64',
        'Dir':                    str(apt_root),
        'Dir::State':             f'{apt_root}/var/lib/apt',
        'Dir::State::status':     f'{apt_root}/var/lib/dpkg/status',
        'Dir::Etc::SourceList':   f'{apt_root}/etc/apt.sources.list',
        'Dir::Etc::SourceParts':  '',
        'Dir::Cache':             f'{apt_root}/var/cache/apt',
        'pkgCacheGen::Essential': 'none',
        'Dir::Etc::Trusted':      f'{apt_root}/etc/trusted.gpg',
    }

    conf_regex = re.compile(r'^(?P<key>\S+)\s"(?P<val>\S*)";$')
    assert dict([(m.group('key'), m.group('val'))
                 for l in conf_lines if l for m in [conf_regex.match(l)]]) == \
        expected_conf

    with ZipFile(mock_cache_dir / f'apt_{sources_list.identity()}.zip') as zf:
        # reuse the same APT, its cached zip file should exist now
        with local_apt.local_apt(sources_list, local_apt.default_keys) as apt:
            apt_root = Path(apt.apt_conf).parent.parent

            expected_members = {*apt_root.rglob('*')}
            expected_members.remove(apt_root / 'etc' / 'apt.conf')
            expected_members.remove(apt_root / 'etc' / 'trusted.gpg')

            names = zf.namelist()
            assert len(names) == len(expected_members)

            for name in names:
                path = apt_root / name
                assert path in expected_members
                assert zf.read(name) == \
                    (b'' if path.is_dir() else path.read_bytes())

    assert not apt_root.exists()

@pytest.mark.subprocess_run(local_apt, run_missing_executable)
@pytest.mark.usefixtures('mock_subprocess_run', 'mock_gnupg_import')
def test_local_apt_missing(mock_cache_dir):
    """
    Verify that the local_apt() function raises a proper error when 'apt-get'
    command is missing.
    """
    sources_list = local_apt.SourcesList(['deb-src sth', 'deb sth'])

    with pytest.raises(local_apt.AptError,
                       match='^couldnt_execute_apt-get_is_it_installed$'):
        with local_apt.local_apt(sources_list, local_apt.default_keys) as apt:
            pass

@pytest.mark.subprocess_run(local_apt, make_run_apt_get(update_code=1))
@pytest.mark.usefixtures('mock_subprocess_run', 'mock_gnupg_import')
def test_local_apt_update_fail(mock_cache_dir):
    """
    Verify that the local_apt() function raises a proper error when
    'apt-get update' command returns non-0.
    """
    sources_list = local_apt.SourcesList(['deb-src sth', 'deb sth'])

    error_regex = """^\
command_apt-get -c \\S+ update_failed

STDOUT_OUTPUT_heading

some output

STDERR_OUTPUT_heading

some error output\
$\
"""

    with pytest.raises(local_apt.AptError, match=error_regex):
        with local_apt.local_apt(sources_list, local_apt.default_keys) as apt:
            pass

@pytest.mark.subprocess_run(local_apt, make_run_apt_get())
@pytest.mark.usefixtures('mock_subprocess_run', 'mock_gnupg_import')
def test_local_apt_download(mock_cache_dir):
    """
    Verify that download_apt_packages() function properly performs the download
    of .debs and sources.
    """
    sources_list = local_apt.SourcesList(['deb-src sth', 'deb sth'])
    destination = mock_cache_dir / 'destination'
    destination.mkdir()

    local_apt.download_apt_packages(sources_list, local_apt.default_keys,
                                    ['libjs-mathjax'], destination, False)

    libjs_mathjax_path = destination / 'libjs-mathjax_0%3a2.7.9+dfsg-1_all.deb'
    fonts_mathjax_path = destination / 'fonts-mathjax_0%3a2.7.9+dfsg-1_all.deb'

    source_paths = [
        destination / 'mathjax_2.7.9+dfsg-1.debian.tar.xz',
        destination / 'mathjax_2.7.9+dfsg-1.dsc',
        destination / 'mathjax_2.7.9+dfsg.orig.tar.xz'
    ]

    assert {*destination.iterdir()} == {libjs_mathjax_path, *source_paths}

    local_apt.download_apt_packages(sources_list, local_apt.default_keys,
                                    ['libjs-mathjax'], destination,
                                    with_deps=True)

    assert {*destination.iterdir()} == \
        {libjs_mathjax_path, fonts_mathjax_path, *source_paths}

@pytest.mark.subprocess_run(local_apt, make_run_apt_get(install_code=1))
@pytest.mark.usefixtures('mock_subprocess_run', 'mock_gnupg_import')
def test_local_apt_install_fail(mock_cache_dir):
    """
    Verify that the download_apt_packages() function raises a proper error when
    'apt-get install' command returns non-0.
    """
    sources_list = local_apt.SourcesList(['deb-src sth', 'deb sth'])
    destination = mock_cache_dir / 'destination'
    destination.mkdir()

    error_regex = f"""^\
command_apt-get -c \\S+ install --yes --just-print libjs-mathjax_failed

STDOUT_OUTPUT_heading

{re.escape(sample_install_stdout)}

STDERR_OUTPUT_heading

some error output\
$\
"""

    with pytest.raises(local_apt.AptError, match=error_regex):
        local_apt.download_apt_packages(sources_list, local_apt.default_keys,
                                        ['libjs-mathjax'], destination,
                                        with_deps=True)

    assert [*destination.iterdir()] == []

@pytest.mark.subprocess_run(local_apt, make_run_apt_get(download_code=1))
@pytest.mark.usefixtures('mock_subprocess_run', 'mock_gnupg_import')
def test_local_apt_download_fail(mock_cache_dir):
    """
    Verify that the download_apt_packages() function raises a proper error when
    'apt-get download' command returns non-0.
    """
    sources_list = local_apt.SourcesList(['deb-src sth', 'deb sth'])
    destination = mock_cache_dir / 'destination'
    destination.mkdir()

    error_regex = """^\
command_apt-get -c \\S+ download libjs-mathjax_failed

STDOUT_OUTPUT_heading

some output

STDERR_OUTPUT_heading

some error output\
$\
"""

    with pytest.raises(local_apt.AptError, match=error_regex):
        local_apt.download_apt_packages(sources_list, local_apt.default_keys,
                                        ['libjs-mathjax'], destination, False)

    assert [*destination.iterdir()] == []

@pytest.fixture
def mock_bad_deb_file(monkeypatch, mock_subprocess_run):
    """
    Make mocked 'apt-get download' command produce an incorrectly-named file.
    """
    old_run = local_apt.subprocess.run

    def twice_mocked_run(command, **kwargs):
        """
        Create an evil file if needed; then act just like the run() function
        that got replaced by this one.
        """
        if 'download' in command:
            destination = Path(kwargs.get('cwd') or Path.cwd())
            (destination / 'arbitrary-name').write_text('anything')

        return old_run(command, **kwargs)

    monkeypatch.setattr(local_apt.subprocess, 'run', twice_mocked_run)

@pytest.mark.subprocess_run(local_apt, make_run_apt_get())
@pytest.mark.usefixtures('mock_subprocess_run', 'mock_gnupg_import',
                         'mock_bad_deb_file')
def test_local_apt_download_bad_filename(mock_cache_dir):
    """
    Verify that the download_apt_packages() function raises a proper error when
    'apt-get download' command produces an incorrectly-named file.
    """
    sources_list = local_apt.SourcesList([], 'nabia')
    destination = mock_cache_dir / 'destination'
    destination.mkdir()

    error_regex = """^\
apt_download_gave_bad_filename_arbitrary-name

STDOUT_OUTPUT_heading

some output

STDERR_OUTPUT_heading

some error output\
$\
"""

    with pytest.raises(local_apt.AptError, match=error_regex):
        local_apt.download_apt_packages(sources_list, local_apt.default_keys,
                                        ['libjs-mathjax'], destination, False)

    assert [*destination.iterdir()] == []

@pytest.mark.subprocess_run(local_apt, make_run_apt_get(source_code=1))
@pytest.mark.usefixtures('mock_subprocess_run', 'mock_gnupg_import')
def test_local_apt_source_fail(mock_cache_dir):
    """
    Verify that the download_apt_packages() function raises a proper error when
    'apt-get source' command returns non-0.
    """
    sources_list = local_apt.SourcesList(['deb-src sth', 'deb sth'])
    destination = mock_cache_dir / 'destination'
    destination.mkdir()

    error_regex = """^\
command_apt-get -c \\S* source --download-only \\S+_failed

STDOUT_OUTPUT_heading

some output

STDERR_OUTPUT_heading

some error output\
$\
"""

    with pytest.raises(local_apt.AptError, match=error_regex):
        local_apt.download_apt_packages(sources_list, local_apt.default_keys,
                                        ['libjs-mathjax'], destination, False)

    assert [*destination.iterdir()] == []

def test_sources_list():
    """Verify that the SourcesList class works properly."""
    list = local_apt.SourcesList([], 'nabia')
    assert list.identity() == 'nabia'

    with pytest.raises(local_apt.DistroError, match='^distro_nabiał_unknown$'):
        local_apt.SourcesList([], 'nabiał')

    list = local_apt.SourcesList(['deb sth', 'deb-src sth'], 'nabia')
    assert list.identity() == \
        'ef28d408b96046eae45c8ab3094ce69b2ac0c02a887e796b1d3d1a4f06fb49f1'

def run_dpkg_deb(command, returncode=0, **kwargs):
    """
    Insted of running an 'dpkg-deb -x' command just create some dummy file
    in the destination directory.
    """
    expected = ['dpkg-deb', '-x', '<deb_path>', '<dst_path>']

    variables = process_run_args(command, kwargs, expected)
    deb_path = Path(variables['deb_path'])
    dst_path = Path(variables['dst_path'])

    package_name = re.match('^([^_]+)_.*', deb_path.name).group(1)
    for path in [
            dst_path / 'etc' / f'dummy_{package_name}_config',
            dst_path / 'usr/share/doc' / package_name / 'copyright'
    ]:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f'dummy {path.name}')

    return MockedCompletedProcess(command, returncode,
                                  text_output=kwargs.get('text'))

def download_apt_packages(list, keys, packages, destination_dir,
                          with_deps=False):
    """
    Replacement for download_apt_packages() function in local_apt.py, for
    unit-testing the piggybacked_system() function.
    """
    for path in [
            destination_dir / 'some-bin-package_1.1-2_all.deb',
            destination_dir / 'another-package_1.1-2_all.deb',
            destination_dir / 'some-source-package_1.1.orig.tar.gz',
            destination_dir / 'some-source-package_1.1-1.dsc'
    ]:
        path.write_text(f'dummy {path.name}')

    with open(destination_dir / 'test_data.json', 'w') as out:
        json.dump({
            'list_identity': list.identity(),
            'keys': keys,
            'packages': packages,
            'with_deps': with_deps
        }, out)

@pytest.fixture
def mock_download_packages(monkeypatch):
    """Mock the download_apt_packages() function in local_apt.py."""
    monkeypatch.setattr(local_apt, 'download_apt_packages',
                        download_apt_packages)

@pytest.mark.subprocess_run(local_apt, run_dpkg_deb)
@pytest.mark.parametrize('params', [
    {
        'with_deps': False,
        'base_depends': True,
        'identity': 'nabia',
        'props': {'distribution': 'nabia', 'dependencies': False},
        'all_keys': local_apt.default_keys,
        'prepared_directory': False
    },
    {
        'with_deps': True,
        'base_depends': False,
        'identity': '38db0b4fa2f6610cd1398b66a2c05d9abb1285f9a055a96eb96dee0f6b72aca8',
        'props': {
            'sources_list': [f'deb{suf} http://example.com/ stable main'
                             for suf in ('', '-src')],
            'trusted_keys': ['AB' * 20],
            'dependencies': True,
            'depend_on_base_packages': False
        },
        'all_keys': [*local_apt.default_keys, 'AB' * 20],
        'prepared_directory': True
    }
])
@pytest.mark.usefixtures('mock_download_packages', 'mock_subprocess_run')
def test_piggybacked_system_download(params, tmpdir):
    """
    Verify that the piggybacked_system() function properly downloads and unpacks
    APT packages.
    """
    foreign_packages_dir = tmpdir if params['prepared_directory'] else None

    with local_apt.piggybacked_system({
            'system': 'apt',
            **params['props'],
            'packages': ['some-bin-package', 'another-package=1.1-2']
    }, foreign_packages_dir) as piggybacked:
        expected_depends = [{'identifier': 'apt-common-licenses'}] \
            if params['base_depends'] else []
        assert piggybacked.resource_must_depend == expected_depends

        archive_files = dict(piggybacked.archive_files())

        archive_names = [
            'some-bin-package_1.1-2_all.deb',
            'another-package_1.1-2_all.deb',
            'some-source-package_1.1.orig.tar.gz',
            'some-source-package_1.1-1.dsc',
            'test_data.json'
        ]
        assert {*archive_files.keys()} == \
            {PurePosixPath('apt') / n for n in archive_names}

        for path in archive_files.values():
            if path.name == 'test_data.json':
                assert json.loads(path.read_text()) == {
                    'list_identity': params['identity'],
                    'keys': params['all_keys'],
                    'packages': ['some-bin-package', 'another-package=1.1-2'],
                    'with_deps': params['with_deps']
                }
            else:
                assert path.read_text() == f'dummy {path.name}'

            if foreign_packages_dir is not None:
                assert path.parent == foreign_packages_dir / 'apt'

        license_files = {*piggybacked.package_license_files}

        assert license_files == {
            PurePosixPath('.apt-root/usr/share/doc/another-package/copyright'),
            PurePosixPath('.apt-root/usr/share/doc/some-bin-package/copyright')
        }

        assert ['dummy copyright'] * 2 == \
            [piggybacked.resolve_file(p).read_text() for p in license_files]

        for name in ['some-bin-package', 'another-package']:
            path = PurePosixPath(f'.apt-root/etc/dummy_{name}_config')
            assert piggybacked.resolve_file(path).read_text() == \
                f'dummy {path.name}'

        assert piggybacked.resolve_file(PurePosixPath('a/b/c')) == None
        assert piggybacked.resolve_file(PurePosixPath('')) == None

        output_text = 'loading_.apt-root/a/../../../b_outside_piggybacked_dir'
        with pytest.raises(FileReferenceError,
                           match=f'^{re.escape(output_text)}$'):
            piggybacked.resolve_file(PurePosixPath('.apt-root/a/../../../b'))

        root = piggybacked.resolve_file(PurePosixPath('.apt-root/dummy')).parent
        assert root.is_dir()

    assert not root.exists()

    if foreign_packages_dir:
        assert [*tmpdir.iterdir()] == [tmpdir / 'apt']

@pytest.mark.subprocess_run(local_apt, run_dpkg_deb)
@pytest.mark.usefixtures('mock_subprocess_run')
def test_piggybacked_system_no_download():
    """
    Verify that the piggybacked_system() function is able to use pre-downloaded
    APT packages.
    """
    archive_names = {
        f'{package}{rest}'
        for package in ('some-lib_1:2.3', 'other-lib_4.45.2')
        for rest in ('-1_all.deb', '.orig.tar.gz', '-1.debian.tar.xz', '-1.dsc')
    }

    with TemporaryDirectory() as td:
        td = Path(td)
        (td / 'apt').mkdir()
        for name in archive_names:
            (td / 'apt' / name).write_text(f'dummy {name}')

        with local_apt.piggybacked_system({
                'system': 'apt',
                'distribution': 'nabia',
                'dependencies': True,
                'packages': ['whatever', 'whatever2']
        }, td) as piggybacked:
            archive_files = dict(piggybacked.archive_files())

            assert {*archive_files.keys()} == \
                {PurePosixPath('apt') / name for name in archive_names}

            for path in archive_files.values():
                assert path.read_text() == f'dummy {path.name}'

            assert {*piggybacked.package_license_files} == {
                PurePosixPath('.apt-root/usr/share/doc/some-lib/copyright'),
                PurePosixPath('.apt-root/usr/share/doc/other-lib/copyright')
            }

            for name in ['some-lib', 'other-lib']:
                path = PurePosixPath(f'.apt-root/etc/dummy_{name}_config')
                assert piggybacked.resolve_file(path).read_text() == \
                    f'dummy {path.name}'

@pytest.mark.subprocess_run(local_apt, run_missing_executable)
@pytest.mark.usefixtures('mock_download_packages', 'mock_subprocess_run')
def test_piggybacked_system_missing():
    """
    Verify that the piggybacked_system() function raises a proper error when
    'dpkg-deb' is missing.
    """
    with pytest.raises(local_apt.AptError,
                       match='^couldnt_execute_dpkg-deb_is_it_installed$'):
        with local_apt.piggybacked_system({
                'system': 'apt',
                'distribution': 'nabia',
                'packages': ['some-package'],
                'dependencies': False
        }, None) as piggybacked:
            pass

@pytest.mark.subprocess_run(local_apt, lambda c, **kw: run_dpkg_deb(c, 1, **kw))
@pytest.mark.usefixtures('mock_download_packages', 'mock_subprocess_run')
def test_piggybacked_system_fail():
    """
    Verify that the piggybacked_system() function raises a proper error when
    'dpkg-deb -x' command returns non-0.
    """
    error_regex = """^\
command_dpkg-deb -x \\S+\\.deb \\S+_failed

STDOUT_OUTPUT_heading

some output

STDERR_OUTPUT_heading

some error output\
$\
"""

    with pytest.raises(local_apt.AptError, match=error_regex):
        with local_apt.piggybacked_system({
                'system': 'apt',
                'distribution': 'nabia',
                'packages': ['some-package'],
                'dependencies': False
        }, None) as piggybacked:
            pass
