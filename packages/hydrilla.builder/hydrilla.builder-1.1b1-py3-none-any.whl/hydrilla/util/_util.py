# SPDX-License-Identifier: AGPL-3.0-or-later

# Building Hydrilla packages.
#
# This file is part of Hydrilla
#
# Copyright (C) 2021, 2022 Wojtek Kosior
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

import re
import json
import locale
import gettext

from pathlib import Path
from typing import Optional, Union

from jsonschema import RefResolver, Draft7Validator

here = Path(__file__).resolve().parent

class UnknownSchemaError(Exception):
    """
    Exception used to record problems with JSON documents for which not even
    the appropriate validation schema could be determined.
    """
    pass

_strip_comment_re = re.compile(r'''
^ # match from the beginning of each line
( # catch the part before '//' comment
  (?: # this group matches either a string or a single out-of-string character
    [^"/] |
    "
    (?: # this group matches any in-a-string character
      [^"\\] |          # match any normal character
      \\[^u] |          # match any escaped character like '\f' or '\n'
      \\u[a-fA-F0-9]{4} # match an escape
    )*
    "
  )*
)
# expect either end-of-line or a comment:
# * unterminated strings will cause matching to fail
# * bad comment (with '/' instead of '//') will be indicated by second group
#   having length 1 instead of 2 or 0
(//?|$)
''', re.VERBOSE)

def strip_json_comments(text: str) -> str:
    """
    Accept JSON text with optional C++-style ('//') comments and return the text
    with comments removed. Consecutive slashes inside strings are handled
    properly. A spurious single slash ('/') shall generate an error. Errors in
    JSON itself shall be ignored.
    """
    processed = 0
    stripped_text = []
    for line in text.split('\n'):
        match = _strip_comment_re.match(line)

        if match is None: # unterminated string
            # ignore this error, let json module report it
            stripped = line
        elif len(match[2]) == 1:
            raise json.JSONDecodeError(_('bad_comment'), text,
                                       processed + len(match[1]))
        else:
            stripped = match[1]

        stripped_text.append(stripped)
        processed += len(line) + 1

    return '\n'.join(stripped_text)

def normalize_version(ver: list[int]) -> list[int]:
    """Strip right-most zeroes from 'ver'. The original list is not modified."""
    new_len = 0
    for i, num in enumerate(ver):
        if num != 0:
            new_len = i + 1

    return ver[:new_len]

def parse_version(ver_str: str) -> list[int]:
    """
    Convert 'ver_str' into an array representation, e.g. for ver_str="4.6.13.0"
    return [4, 6, 13, 0].
    """
    return [int(num) for num in ver_str.split('.')]

def version_string(ver: list[int], rev: Optional[int]=None) -> str:
    """
    Produce version's string representation (optionally with revision), like:
        1.2.3-5
    No version normalization is performed.
    """
    return '.'.join([str(n) for n in ver]) + ('' if rev is None else f'-{rev}')

_schema_name_re = re.compile(r'''
(?P<name_base>[^/]*)
-
(?P<ver>
  (?P<major>[1-9][0-9]*)
  (?: # this repeated group matches the remaining version numbers
    \.
    (?:[1-9][0-9]*|0)
  )*
)
\.schema\.json
$
''', re.VERBOSE)

schema_paths = {}
for path in (here.parent / 'schemas').rglob('*.schema.json'):
    match = _schema_name_re.search(path.name)
    schema_name_base = match.group('name_base')
    schema_ver_list = match.group('ver').split('.')

    for i in range(len(schema_ver_list)):
        schema_ver = '.'.join(schema_ver_list[:i+1])
        schema_paths[f'{schema_name_base}-{schema_ver}.schema.json'] = path

for name, path in [*schema_paths.items()]:
    schema_paths[f'https://hydrilla.koszko.org/schemas/{name}'] = path

schemas = {}

def _get_schema(schema_name: str) -> dict:
    """Return loaded JSON of the requested schema. Cache results."""
    path = schema_paths[schema_name]

    if path not in schemas:
        schemas[path] = json.loads(path.read_text())

    return schemas[path]

def validator_for(schema: Union[str, dict]) -> Draft7Validator:
    """
    Prepare a validator for the provided schema.

    Other schemas under '../schemas' can be referenced.
    """
    if isinstance(schema, str):
        schema = _get_schema(schema)

    resolver = RefResolver(
        base_uri=schema['$id'],
        referrer=schema,
        handlers={'https': _get_schema}
    )

    return Draft7Validator(schema, resolver=resolver)

def load_instance_from_file(path: Path) -> tuple[dict, Optional[int]]:
    """
    Open a file and load its contents as a JSON document (with additional
    '//' comments support). Then parse its "$schema" property (if present)
    and return a tuple of the document instance and the major number of
    schema version.

    If no schema version number can be extracted, None is used instead.
    """
    instance = json.loads(strip_json_comments(path.read_text()))
    major = None

    if type(instance) is dict and type(instance.get('$schema')) is str:
        match = _schema_name_re.search(instance.get('$schema'))
        major = match and int(match.group('major'))

    return instance, major

def translation(localedir: Union[Path, str], lang: Optional[str]=None) \
    -> gettext.GNUTranslations:
    """
    Configure translations for domain 'hydrilla-messages' and return the object
    that represents them.

    If `lang` is set, look for translations for `lang`. Otherwise, try to
    determine system's default language and use that.
    """
    # https://stackoverflow.com/questions/3425294/how-to-detect-the-os-default-language-in-python
    # But I am not going to surrender to Microbugs' nonfree, crappy OS to test
    # it, to the lines inside try: may fail.
    if lang is None:
        try:
            from ctypes.windll import kernel32 as windll
            lang = locale.windows_locale[windll.GetUserDefaultUILanguage()]
        except:
            lang = locale.getdefaultlocale()[0] or 'en_US'

    localedir = Path(localedir)
    if not (localedir / lang).is_dir():
        lang = 'en_US'

    return gettext.translation('hydrilla-messages', localedir=localedir,
                               languages=[lang])

_ = translation(here.parent / 'builder' / 'locales').gettext
