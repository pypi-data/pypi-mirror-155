# SPDX-License-Identifier: AGPL-3.0-or-later

# Repository tests
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

import pytest
import sys
import shutil
import json
import functools as ft

from pathlib import Path
from hashlib import sha256
from tempfile import TemporaryDirectory
from typing import Callable, Optional

from flask.testing import FlaskClient
from markupsafe import escape
from werkzeug import Response

from hydrilla import util as hydrilla_util
from hydrilla.builder import build
from hydrilla.server import config, _version, serve

from .helpers import *

here        = Path(__file__).resolve().parent
config_path = here / 'config.json'
source_path = here / 'source-package-example'

expected_generated_by = {
    'name': 'hydrilla.server',
    'version': _version.version
}

SetupMod = Optional[Callable[['Setup'], None]]

source_files = (
    'index.json', 'hello.js', 'bye.js', 'message.js', 'README.txt',
    'README.txt.license', '.reuse/dep5', 'LICENSES/CC0-1.0.txt'
)

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

@pytest.fixture
def mock_reuse(mock_subprocess_run):
    """
    Mock the REUSE command when executed through subprocess.run() from serve.py.
    """
    mock_subprocess_run(build, run_reuse)

class Setup:
    """
    Facilitate preparing test malcontent directory, Hydrilla config file and the
    actual Flask client. In a customizable way.
    """
    def __init__(self, modify_before_build: SetupMod=None,
                 modify_after_build: SetupMod=None) -> None:
        """Initialize Setup."""
        self._modify_before_build = modify_before_build
        self._modify_after_build = modify_after_build
        self._config = None
        self._client = None

    def _prepare(self) -> None:
        """Perform the build and call the callbacks as appropriate."""
        self.tmpdir = TemporaryDirectory()

        self.containing_dir = Path(self.tmpdir.name)
        self.malcontent_dir = self.containing_dir / 'sample_malcontent'
        self.index_json     = Path('index.json')

        self.source_dir = self.containing_dir / 'sample_source_package'
        for source_file in source_files:
            dst_path = self.source_dir / source_file
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source_path / source_file, dst_path)

        self.config_path = self.containing_dir / 'config.json'
        shutil.copyfile(config_path, self.config_path)

        if self._modify_before_build:
            self._modify_before_build(self)

        build_obj = build.Build(self.source_dir, self.index_json)
        build_obj.write_package_files(self.malcontent_dir)

        if self._modify_after_build:
            self._modify_after_build(self)

    def config(self) -> dict:
        """Provide the contents of JSON config file used."""
        if self._config is None:
            self._prepare()
            self._config = config.load([self.config_path])

        return self._config

    def client(self) -> FlaskClient:
        """
        Provide app client that serves the objects from built sample package.
        """
        if self._client is None:
            app = serve.HydrillaApp(self.config(),
                                    flask_config={'TESTING': True})
            self._client = app.test_client()

        return self._client

def index_json_modification(modify_index_json):
    """Decorator for function that modifies index.json before build."""
    def handle_index_json(setup):
        """Modify index.json before build."""
        index_path = setup.source_dir / 'index.json'
        index_json, _ = hydrilla_util.load_instance_from_file(index_path)

        index_json = modify_index_json(index_json) or index_json

        index_json = f'''
        // SPDX-License-Identifier: CC0-1.0
        // Copyright (C) 2021, 2022 Wojtek Kosior
        {json.dumps(index_json)}
        '''

        index_path.write_text(index_json)

    return handle_index_json

@index_json_modification
def remove_all_uuids(index_json):
    """Modify sample packages to contain no (optional) UUIDs"""
    for definition in index_json['definitions']:
        del definition['uuid']

@index_json_modification
def bump_schema_v2(index_json) -> None:
    """Modify sample packages to use version 2 of Hydrilla JSON schemas."""
    for definition in index_json['definitions']:
        definition['min_haketilo_version'] = [1, 1]

        if definition['identifier'] == 'helloapple' and \
           definition['type'] == 'resource':
            definition['required_mappings'] = {'identifier': 'helloapple'}

default_setup = lambda: Setup()
uuidless_setup = lambda: Setup(modify_before_build=remove_all_uuids)
schema_v2_setup = lambda: Setup(modify_before_build=bump_schema_v2)

setup_makers = [default_setup, uuidless_setup, schema_v2_setup]

@pytest.mark.usefixtures('mock_reuse')
@pytest.mark.parametrize('setup_maker', setup_makers)
@pytest.mark.parametrize('item_type', ['resource', 'mapping'])
def test_get_newest(setup_maker, item_type: str) -> None:
    """
    Verify that
        GET '/{item_type}/{item_identifier}.json'
    returns proper definition that is also served at:
        GET '/{item_type}/{item_identifier}/{item_version}'
    """
    setup = setup_maker()
    response = setup.client().get(f'/{item_type}/helloapple.json')
    assert response.status_code == 200
    definition = json.loads(response.data.decode())
    assert definition['type']        == item_type
    assert definition['identifier']  == 'helloapple'

    response = setup.client().get(f'/{item_type}/helloapple/2021.11.10')
    assert response.status_code == 200
    assert definition == json.loads(response.data.decode())

    assert ('uuid' in definition) == (setup_maker is not uuidless_setup)

    hydrilla_util.validator_for(f'api_{item_type}_description-1.0.1.schema.json')\
                 .validate(definition)

@pytest.fixture
def setup(mock_reuse):
    """Prepare server test environment in the default way."""
    return default_setup()

def test_project_url(setup) -> None:
    """Fetch index.html and verify project URL from config is present there."""
    response = setup.client().get('/')
    assert b'html' in response.data
    project_url = setup.config()['hydrilla_project_url']
    assert escape(project_url).encode() in response.data

@pytest.mark.parametrize('item_type', ['resource', 'mapping'])
def test_get_nonexistent(setup, item_type: str) -> None:
    """
    Verify that attempts to GET a JSON definition of a nonexistent item or item
    version result in 404.
    """
    response = setup.client().get(f'/{item_type}/nonexistentapple.json')
    assert response.status_code == 404
    response = setup.client().get(f'/{item_type}/helloapple/1.2.3.999')
    assert response.status_code == 404

@pytest.mark.parametrize('item_type', ['resource', 'mapping'])
def test_file_refs(setup, item_type: str) -> None:
    """
    Verify that files referenced by definitions are accessible under their
    proper URLs and that their hashes match.
    """
    response = setup.client().get(f'/{item_type}/helloapple/2021.11.10')
    assert response.status_code == 200
    definition = json.loads(response.data.decode())

    for file_ref in [*definition.get('scripts', []),
                     *definition['source_copyright']]:
        hash_sum = file_ref["sha256"]
        response = setup.client().get(f'/file/sha256/{hash_sum}')

        assert response.status_code == 200
        assert sha256(response.data).digest().hex() == hash_sum

def test_empty_query(setup) -> None:
    """
    Verify that querying mappings for URL gives an empty list when there're no
    mathes.
    """
    response = setup.client().get(f'/query?url=https://nonexiste.nt/example')
    assert response.status_code == 200

    response_object = json.loads(response.data.decode())

    assert response_object == {
        '$schema': 'https://hydrilla.koszko.org/schemas/api_query_result-1.schema.json',
        'mappings': [],
        'generated_by': expected_generated_by
    }

    hydrilla_util.validator_for('api_query_result-1.0.1.schema.json')\
                 .validate(response_object)

def test_query(setup) -> None:
    """
    Verify that querying mappings for URL gives a list with reference(s) the the
    matching mapping(s).
    """
    response = setup.client().get(f'/query?url=https://hydrillabugs.koszko.org/')
    assert response.status_code == 200

    response_object = json.loads(response.data.decode())

    assert response_object == {
        '$schema': 'https://hydrilla.koszko.org/schemas/api_query_result-1.schema.json',
        'mappings': [{
            'identifier': 'helloapple',
            'long_name': 'Hello Apple',
            'version': [2021, 11, 10]
        }],
        'generated_by': expected_generated_by
    }

    hydrilla_util.validator_for('api_query_result-1.schema.json')\
                 .validate(response_object)

def test_source(setup) -> None:
    """Verify source descriptions are properly served."""
    response = setup.client().get(f'/source/hello.json')
    assert response.status_code == 200

    description = json.loads(response.data.decode())
    assert description['source_name'] == 'hello'

    assert sorted([d['identifier'] for d in description['definitions']]) == \
        ['hello-message', 'helloapple', 'helloapple']

    zipfile_hash = description['source_archives']['zip']['sha256']
    response = setup.client().get(f'/source/hello.zip')
    assert sha256(response.data).digest().hex() == zipfile_hash

    hydrilla_util.validator_for('api_source_description-1.schema.json')\
                 .validate(description)

def test_missing_source(setup) -> None:
    """Verify requests for nonexistent sources result in 404."""
    response = setup.client().get(f'/source/nonexistent.json')
    assert response.status_code == 404

    response = setup.client().get(f'/source/nonexistent.zip')
    assert response.status_code == 404

def test_normalize_version():
    assert hydrilla_util.normalize_version([4, 5, 3, 0, 0]) == [4, 5, 3]
    assert hydrilla_util.normalize_version([1, 0, 5, 0])    == [1, 0, 5]
    assert hydrilla_util.normalize_version([3, 3])          == [3, 3]
