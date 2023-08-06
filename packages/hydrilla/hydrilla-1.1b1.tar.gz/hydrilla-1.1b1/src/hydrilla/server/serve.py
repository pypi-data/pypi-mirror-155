# SPDX-License-Identifier: AGPL-3.0-or-later

# Main repository logic.
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
import os
import pathlib
import json
import logging

from pathlib import Path
from hashlib import sha256
from abc import ABC, abstractmethod
from typing import Optional, Union, Iterable

import click
import flask

from werkzeug import Response

from .. import util
from . import config
from . import _version

here = Path(__file__).resolve().parent

generated_by = {
    'name': 'hydrilla.server',
    'version': _version.version
}

class ItemInfo(ABC):
    """Shortened data of a resource/mapping."""
    def __init__(self, item_obj: dict, major_schema_version: int):
        """Initialize ItemInfo using item definition read from JSON."""
        self.version    = util.normalize_version(item_obj['version'])
        self.identifier = item_obj['identifier']
        self.uuid       = item_obj.get('uuid')
        self.long_name  = item_obj['long_name']

        self.required_mappings = []
        if major_schema_version >= 2:
            self.required_mappings = [map_ref['identifier'] for map_ref in
                                      item_obj.get('required_mappings', [])]

    def path(self) -> str:
        """
        Get a relative path to this item's JSON definition with respect to
        directory containing items of this type.
        """
        return f'{self.identifier}/{util.version_string(self.version)}'

class ResourceInfo(ItemInfo):
    """Shortened data of a resource."""
    def __init__(self, resource_obj: dict, major_schema_version: int):
        """Initialize ResourceInfo using resource definition read from JSON."""
        super().__init__(resource_obj, major_schema_version)

        dependencies = resource_obj.get('dependencies', [])
        self.dependencies = [res_ref['identifier'] for res_ref in dependencies]

class MappingInfo(ItemInfo):
    """Shortened data of a mapping."""
    def __init__(self, mapping_obj: dict, major_schema_version: int):
        """Initialize MappingInfo using mapping definition read from JSON."""
        super().__init__(mapping_obj, major_schema_version)

        self.payloads = {}
        for pattern, res_ref in mapping_obj.get('payloads', {}).items():
            self.payloads[pattern] = res_ref['identifier']

    def as_query_result(self) -> str:
        """
        Produce a json.dump()-able object describing this mapping as one of a
        collection of query results.
        """
        return {
            'version':    self.version,
            'identifier': self.identifier,
            'long_name':  self.long_name
        }

class VersionedItemInfo:
    """Stores data of multiple versions of given resource/mapping."""
    def __init__(self):
        self.uuid = None
        self.identifier = None
        self.by_version = {}
        self.known_versions = []

    def register(self, item_info: ItemInfo) -> None:
        """
        Make item info queryable by version. Perform sanity checks for uuid.
        """
        if self.identifier is None:
            self.identifier = item_info.identifier

        if self.uuid is None:
            self.uuid = item_info.uuid

        if self.uuid is not None and self.uuid != item_info.uuid:
            raise ValueError(f_('uuid_mismatch_{identifier}')
                             .format(identifier=self.identifier))

        ver = item_info.version
        ver_str = util.version_string(ver)

        if ver_str in self.by_version:
            raise ValueError(f_('version_clash_{identifier}_{version}')
                             .format(identifier=self.identifier,
                                     version=ver_str))

        self.by_version[ver_str] = item_info
        self.known_versions.append(ver)

    def get_by_ver(self, ver: Optional[list[int]]=None) -> Optional[ItemInfo]:
        """
        Find and return info of the newest version of item.

        If ver is specified, instead find and return info of that version of the
        item (or None if absent).
        """
        ver = util.version_string(ver or self.known_versions[-1])

        return self.by_version.get(ver)

    def get_all(self) -> list[ItemInfo]:
        """
        Return a list of item info for all its versions, from oldest ot newest.
        """
        return [self.by_version[util.version_string(ver)]
                for ver in self.known_versions]

class PatternTreeNode:
    """
    "Pattern Tree" is how we refer to the data structure used for querying
    Haketilo patterns. Those look like 'https://*.example.com/ab/***'. The goal
    is to make it possible for given URL to quickly retrieve all known patterns
    that match it.
    """
    def __init__(self):
        self.wildcard_matches = [None, None, None]
        self.literal_match    = None
        self.children         = {}

    def search(self, segments):
        """
        Yields all matches of this segments sequence against the tree that
        starts at this node. Results are produces in order from greatest to
        lowest pattern specificity.
        """
        nodes = [self]

        for segment in segments:
            next_node = nodes[-1].children.get(segment)
            if next_node is None:
                break

            nodes.append(next_node)

        nsegments = len(segments)
        cond_literal = lambda: len(nodes)     == nsegments
        cond_wildcard = [
            lambda: len(nodes) + 1 == nsegments and segments[-1] != '*',
            lambda: len(nodes) + 1 <  nsegments,
            lambda: len(nodes) + 1 != nsegments or  segments[-1] != '***'
        ]

        while nodes:
            node = nodes.pop()

            for item, condition in [(node.literal_match, cond_literal),
                                    *zip(node.wildcard_matches, cond_wildcard)]:
                if item is not None and condition():
                    yield item

    def add(self, segments, item_instantiator):
        """
        Make item queryable through (this branch of) the Pattern Tree. If there
        was not yet any item associated with the tree path designated by
        segments, create a new one using item_instantiator() function. Return
        all items matching this path (both the ones that existed and the ones
        just created).
        """
        node = self
        segment = None

        for segment in segments:
            wildcards = node.wildcard_matches

            child = node.children.get(segment) or PatternTreeNode()
            node.children[segment] = child
            node = child

        if node.literal_match is None:
            node.literal_match = item_instantiator()

        if segment not in ('*', '**', '***'):
            return [node.literal_match]

        if wildcards[len(segment) - 1] is None:
            wildcards[len(segment) - 1] = item_instantiator()

        return [node.literal_match, wildcards[len(segment) - 1]]

proto_regex  = re.compile(r'^(?P<proto>\w+)://(?P<rest>.*)$')
user_re      = r'[^/?#@]+@' # r'(?P<user>[^/?#@]+)@' # discarded for now
query_re     = r'\??[^#]*'  # r'\??(?P<query>[^#]*)' # discarded for now
domain_re    = r'(?P<domain>[^/?#]+)'
path_re      = r'(?P<path>[^?#]*)'
http_regex   = re.compile(f'{domain_re}{path_re}{query_re}.*')
ftp_regex    = re.compile(f'(?:{user_re})?{domain_re}{path_re}.*')

class UrlError(ValueError):
    """Used to report a URL or URL pattern that is invalid or unsupported."""
    pass

class DeconstructedUrl:
    """Represents a deconstructed URL or URL pattern"""
    def __init__(self, url):
        self.url = url

        match = proto_regex.match(url)
        if not match:
            raise UrlError(f_('invalid_URL_{}').format(url))

        self.proto = match.group('proto')
        if self.proto not in ('http', 'https', 'ftp'):
            raise UrlError(f_('disallowed_protocol_{}').format(proto))

        if self.proto == 'ftp':
            match = ftp_regex.match(match.group('rest'))
        elif self.proto in ('http', 'https'):
            match = http_regex.match(match.group('rest'))

        if not match:
            raise UrlError(f_('invalid_URL_{}').format(url))

        self.domain = match.group('domain').split('.')
        self.domain.reverse()
        self.path = [*filter(None, match.group('path').split('/'))]

class PatternMapping:
    """
    A mapping info, together with one of its patterns, as stored in Pattern
    Tree.
    """
    def __init__(self, pattern: str, mapping_info: MappingInfo):
        self.pattern = pattern
        self.mapping_info = mapping_info

    def register(self, pattern_tree: dict):
        """
        Make self queryable through the Pattern Tree passed in the argument.
        """
        deco = DeconstructedUrl(self.pattern)

        domain_tree = pattern_tree.get(deco.proto) or PatternTreeNode()
        pattern_tree[deco.proto] = domain_tree

        for path_tree in domain_tree.add(deco.domain, PatternTreeNode):
            for match_list in path_tree.add(deco.path, list):
                match_list.append(self)

class Malcontent:
    """
    Instance of this class represents a directory with files that can be loaded
    and served by Hydrilla.
    """
    def __init__(self, malcontent_dir_path: Path):
        """
        When an instance of Malcontent is constructed, it searches
        malcontent_dir_path for serveable site-modifying packages and loads
        them into its data structures.
        """
        self.infos = {'resource': {}, 'mapping': {}}
        self.pattern_tree = {}

        self.malcontent_dir_path = malcontent_dir_path

        if not self.malcontent_dir_path.is_dir():
            raise ValueError(f_('malcontent_dir_path_not_dir_{}')
                             .format(malcontent_dir_path))

        for item_type in ('mapping', 'resource'):
            type_path = self.malcontent_dir_path / item_type
            if not type_path.is_dir():
                continue

            for subpath in type_path.iterdir():
                if not subpath.is_dir():
                    continue

                for ver_file in subpath.iterdir():
                    try:
                        self._load_item(item_type, ver_file)
                    except Exception as e:
                        if flask.current_app._hydrilla_werror:
                            raise e from None

                        msg = f_('couldnt_load_item_from_{}').format(ver_file)
                        logging.error(msg, exc_info=True)

        self._report_missing()
        self._finalize()

    def _load_item(self, item_type: str, ver_file: Path) -> None:
        """
        Reads, validates and autocompletes serveable mapping/resource
        definition, then registers information from it in data structures.
        """
        version    = util.parse_version(ver_file.name)
        identifier = ver_file.parent.name

        item_json, major = util.load_instance_from_file(ver_file)

        util.validator_for(f'api_{item_type}_description-{major}.schema.json')\
            .validate(item_json)

        if item_type == 'resource':
            item_info = ResourceInfo(item_json, major)
        else:
            item_info = MappingInfo(item_json, major)

        if item_info.identifier != identifier:
            msg = f_('item_{item}_in_file_{file}')\
                .format({'item': item_info.identifier, 'file': ver_file})
            raise ValueError(msg)

        if item_info.version != version:
            ver_str = util.version_string(item_info.version)
            msg = f_('item_version_{ver}_in_file_{file}')\
                .format({'ver': ver_str, 'file': ver_file})
            raise ValueError(msg)

        versioned_info = self.infos[item_type].get(identifier)
        if versioned_info is None:
            versioned_info = VersionedItemInfo()
            self.infos[item_type][identifier] = versioned_info

        versioned_info.register(item_info)

    def _all_of_type(self, item_type: str) -> Iterable[ItemInfo]:
        """Iterator over all registered versions of all mappings/resources."""
        for versioned_info in self.infos[item_type].values():
            for item_info in versioned_info.by_version.values():
                yield item_info

    def _report_missing(self) -> None:
        """
        Use logger to print information about items that are referenced but
        were not loaded.
        """
        def report_missing_dependency(info: ResourceInfo, dep: str) -> None:
            msg = f_('no_dep_{resource}_{ver}_{dep}')\
                .format(dep=dep, resource=info.identifier,
                        ver=util.version_string(info.version))
            logging.error(msg)

        for resource_info in self._all_of_type('resource'):
            for dep in resource_info.dependencies:
                if dep not in self.infos['resource']:
                    report_missing_dependency(resource_info, dep)

        def report_missing_payload(info: MappingInfo, payload: str) -> None:
            msg = f_('no_payload_{mapping}_{ver}_{payload}')\
                .format(mapping=info.identifier, payload=payload,
                        ver=util.version_string(info.version))
            logging.error(msg)

        for mapping_info in self._all_of_type('mapping'):
            for payload in mapping_info.payloads.values():
                if payload not in self.infos['resource']:
                    report_missing_payload(mapping_info, payload)

        def report_missing_mapping(info: Union[MappingInfo, ResourceInfo],
                                   required_mapping: str) -> None:
            msg = _('no_mapping_{required_by}_{ver}_{required}')\
                .format(required_by=info.identifier, required=required_mapping,
                        ver=util.version_string(info.version))
            logging.error(msg)

        for item_info in (*self._all_of_type('mapping'),
                          *self._all_of_type('resource')):
            for required in item_info.required_mappings:
                if required not in self.infos['mapping']:
                    report_missing_mapping(item_info, required)

    def _finalize(self):
        """
        Initialize structures needed to serve queries. Called once after all
        data gets loaded.
        """
        for infos_dict in self.infos.values():
            for versioned_info in infos_dict.values():
                versioned_info.known_versions.sort()

        for info in self._all_of_type('mapping'):
            for pattern in info.payloads:
                try:
                    PatternMapping(pattern, info).register(self.pattern_tree)
                except Exception as e:
                    if flask.current_app._hydrilla_werror:
                        raise e from None
                    msg = f_('couldnt_register_{mapping}_{ver}_{pattern}')\
                        .format(mapping=info.identifier, pattern=pattern,
                                ver=util.version_string(info.version))
                    logging.error(msg)

    def query(self, url: str) -> list[MappingInfo]:
        """
        Return a list of registered mappings that match url.

        If multiple versions of a mapping are applicable, only the most recent
        is included in the result.
        """
        deco = DeconstructedUrl(url)

        collected = {}

        domain_tree = self.pattern_tree.get(deco.proto) or PatternTreeNode()

        def process_mapping(pattern_mapping: PatternMapping) -> None:
            if url[-1] != '/' and pattern_mapping.pattern[-1] == '/':
                return

            info = pattern_mapping.mapping_info

            if info.identifier not in collected or \
               info.version > collected[info.identifier].version:
                collected[info.identifier] = info

        for path_tree in domain_tree.search(deco.domain):
            for matches_list in path_tree.search(deco.path):
                for pattern_mapping in matches_list:
                    process_mapping(pattern_mapping)

        return list(collected.values())

bp = flask.Blueprint('bp', __package__)

class HydrillaApp(flask.Flask):
    """Flask app that implements a Hydrilla server."""
    def __init__(self, hydrilla_config: dict, flask_config: dict={}):
        """Create the Flask instance according to the configuration"""
        super().__init__(__package__, static_url_path='/',
                         static_folder=hydrilla_config['malcontent_dir'])
        self.config.update(flask_config)

        # https://stackoverflow.com/questions/9449101/how-to-stop-flask-from-initialising-twice-in-debug-mode
        if self.debug and os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
            return

        self.jinja_options = {
            **self.jinja_options,
            'extensions': [
                *self.jinja_options.get('extensions', []),
                'jinja2.ext.i18n'
            ]
        }

        self._hydrilla_translation = \
            util.translation(here / 'locales', hydrilla_config['language'])
        self._hydrilla_project_url = hydrilla_config['hydrilla_project_url']
        self._hydrilla_port = hydrilla_config['port']
        self._hydrilla_werror = hydrilla_config.get('werror', False)

        if 'hydrilla_parent' in hydrilla_config:
            raise ValueError("Option 'hydrilla_parent' is not implemented.")

        malcontent_dir = Path(hydrilla_config['malcontent_dir']).resolve()
        with self.app_context():
            self._hydrilla_malcontent = Malcontent(malcontent_dir)

        self.register_blueprint(bp)

    def create_jinja_environment(self, *args, **kwargs) \
        -> flask.templating.Environment:
        """
        Flask's create_jinja_environment(), but tweaked to always include the
        'hydrilla_project_url' global variable and to install proper
        translations.
        """
        env = super().create_jinja_environment(*args, **kwargs)
        env.install_gettext_translations(self._hydrilla_translation)
        env.globals['hydrilla_project_url'] = self._hydrilla_project_url

        return env

    def run(self, *args, **kwargs):
        """
        Flask's run(), but tweaked to use the port from hydrilla configuration
        by default.
        """
        return super().run(*args, port=self._hydrilla_port, **kwargs)

def f_(text_key):
    return flask.current_app._hydrilla_translation.gettext(text_key)

def malcontent():
    return flask.current_app._hydrilla_malcontent

@bp.route('/')
def index():
    return flask.render_template('index.html')

identifier_json_re = re.compile(r'^([-0-9a-z.]+)\.json$')

def get_resource_or_mapping(item_type: str, identifier: str) -> Response:
    """
    Strip '.json' from 'identifier', look the item up and send its JSON
    description.
    """
    match = identifier_json_re.match(identifier)
    if not match:
        flask.abort(404)

    identifier = match.group(1)

    versioned_info = malcontent().infos[item_type].get(identifier)

    info = versioned_info and versioned_info.get_by_ver()
    if info is None:
        flask.abort(404)

    # no need for send_from_directory(); path is safe, constructed by us
    file_path = malcontent().malcontent_dir_path / item_type / info.path()
    return flask.send_file(open(file_path, 'rb'), mimetype='application/json')

@bp.route('/mapping/<string:identifier_dot_json>')
def get_newest_mapping(identifier_dot_json: str) -> Response:
    return get_resource_or_mapping('mapping', identifier_dot_json)

@bp.route('/resource/<string:identifier_dot_json>')
def get_newest_resource(identifier_dot_json: str) -> Response:
    return get_resource_or_mapping('resource', identifier_dot_json)

@bp.route('/query')
def query():
    url = flask.request.args['url']

    mapping_refs = [i.as_query_result() for i in malcontent().query(url)]
    result = {
        '$schema': 'https://hydrilla.koszko.org/schemas/api_query_result-1.schema.json',
        'mappings': mapping_refs,
        'generated_by': generated_by
    }

    return Response(json.dumps(result), mimetype='application/json')

@bp.route('/--help')
def mm_help():
    return start.get_help(click.Context(start_wsgi)) + '\n'

@bp.route('/--version')
def mm_version():
    prog_info = {'prog': 'Hydrilla', 'version': _version.version}
    return _('%(prog)s_%(version)s_license') % prog_info + '\n'

default_config_path = Path('/etc/hydrilla/config.json')
default_malcontent_dir = '/var/lib/hydrilla/malcontent'
default_project_url = 'https://hydrillabugs.koszko.org/projects/hydrilla/wiki'

console_gettext = util.translation(here / 'locales').gettext
_ = console_gettext

@click.command(help=_('serve_hydrilla_packages_explain_wsgi_considerations'))
@click.option('-m', '--malcontent-dir',
              type=click.Path(exists=True, file_okay=False),
              help=_('directory_to_serve_from_overrides_config'))
@click.option('-h', '--hydrilla-project-url', type=click.STRING,
              help=_('project_url_to_display_overrides_config'))
@click.option('-p', '--port', type=click.INT,
              help=_('tcp_port_to_listen_on_overrides_config'))
@click.option('-c', '--config', 'config_path',
              type=click.Path(exists=True, dir_okay=False, resolve_path=True),
              help=_('path_to_config_file_explain_default'))
@click.option('-l', '--language', type=click.STRING,
              help=_('language_to_use_overrides_config'))
@click.version_option(version=_version.version, prog_name='Hydrilla',
                      message=_('%(prog)s_%(version)s_license'),
                      help=_('version_printing'))
def start(malcontent_dir: Optional[str], hydrilla_project_url: Optional[str],
          port: Optional[int], config_path: Optional[str],
          language: Optional[str]) -> None:
    """
    Run a development Hydrilla server.

    This command is meant to be the entry point of hydrilla command exported by
    this package.
    """
    config_load_opts = {} if config_path is None \
        else {'config_path': [Path(config_path)]}

    hydrilla_config = config.load(**config_load_opts)

    if malcontent_dir is not None:
        hydrilla_config['malcontent_dir'] = str(Path(malcontent_dir).resolve())

    if hydrilla_project_url is not None:
        hydrilla_config['hydrilla_project_url'] = hydrilla_project_url

    if port is not None:
        hydrilla_config['port'] = port

    if language is not None:
        hydrilla_config['language'] = language

    lang = hydrilla_config.get('language')
    _ = console_gettext if lang is None else \
        util.translation(here / 'locales', lang).gettext

    for opt in ('malcontent_dir', 'hydrilla_project_url', 'port', 'language'):
        if opt not in hydrilla_config:
            raise ValueError(_('config_option_{}_not_supplied').format(opt))

    HydrillaApp(hydrilla_config).run()

@click.command(help=_('serve_hydrilla_packages_wsgi_help'),
               context_settings={
                   'ignore_unknown_options': True,
                   'allow_extra_args': True
               })
@click.version_option(version=_version.version, prog_name='Hydrilla',
                      message=_('%(prog)s_%(version)s_license'),
                      help=_('version_printing'))
def start_wsgi() -> None:
    """
    Create application object for use in WSGI deployment.

    This command Also handles --help and --version options in case it gets
    called outside WSGI environment.
    """
    return HydrillaApp(click.get_current_context().obj or config.load())
