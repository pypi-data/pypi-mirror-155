# SPDX-License-Identifier: AGPL-3.0-or-later

# Loading Hydrilla server configuration file.
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

from pathlib import Path

import jsonschema

from .. import util

config_schema = {
    '$schema': 'http://json-schema.org/draft-07/schema#',
    'type': 'object',
    'properties': {
        'malcontent_dir': {
            'type': 'string'
        },
        'malcontent_dir': {
            'type': 'string'
        },
        'hydrilla_project_url': {
            'type': 'string'
        },
        'try_configs': {
            'type': 'array',
            'items': {
                'type': 'string'
            }
        },
        'use_configs': {
            'type': 'array',
            'items': {
                'type': 'string'
            }
        },
        'port': {
            'type': 'integer',
            'minimum': 0,
            'maximum': 65535
        },
        'werror': {
            'type': 'boolean'
        }
    }
}

here = Path(__file__).resolve().parent

def load(config_paths: list[Path]=[here / 'config.json'],
         can_fail: list[bool]=[]) -> dict:
    config = {}

    bools_missing = max(0, len(config_paths) - len(can_fail))
    config_paths = [*config_paths]
    can_fail = [*can_fail[:len(config_paths)], *([False] * bools_missing)]

    while config_paths:
        path = config_paths.pop()
        fail_ok = can_fail.pop()

        try:
            json_text = path.read_text()
        except Exception as e:
            if fail_ok:
                continue
            raise e from None

        new_config = json.loads(util.strip_json_comments(json_text))
        jsonschema.validate(new_config, config_schema)

        config.update(new_config)

        if 'malcontent_dir' in config:
            malcontent_dir = Path(config['malcontent_dir'])
            if not malcontent_dir.is_absolute():
                malcontent_dir = path.parent / malcontent_dir

        config['malcontent_dir'] = str(malcontent_dir.resolve())

        for key, failure_ok in [('try_configs', True), ('use_configs', False)]:
            paths = new_config.get(key, [])
            paths.reverse()
            config_paths.extend(paths)
            can_fail.extend([failure_ok] * len(paths))

    for key in ('try_configs', 'use_configs'):
        if key in config:
            config.pop(key)

    return config
