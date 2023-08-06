# Copyright (c) 2021 Henix, Henix.fr
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""A toolkit for creating OpenTestFactory plugins."""


import inspect
import os
import sys

from flask import request, g

import yaml

from opentf.commons import (
    make_app,
    run_app,
    subscribe,
    unsubscribe,
    EXECUTIONCOMMAND,
    PROVIDERCOMMAND,
    PROVIDERCONFIG,
    GENERATORCOMMAND,
    SERVICECONFIG,
    validate_schema,
    make_status_response,
)
from opentf.toolkit import core


########################################################################

SUBSCRIPTION_KEY = '__subscription uuid__'
MANIFEST_KEY = '__manifest key__'
KIND_KEY = '__kind key__'

KEEP_WORKSPACE = False

########################################################################


def run_plugin(plugin):
    """Start and run plugin.

    Subscribe to the relevant events before startup and tries to
    unsbuscribe in case of errors.

    Spurious subscriptions may remain in case of brutal termination.
    """
    try:
        kind = plugin.config['CONTEXT'][KIND_KEY]
        plugin.config['CONTEXT'][SUBSCRIPTION_KEY] = []
        for entry in plugin.config['CONTEXT'][MANIFEST_KEY]:
            if not 'action' in entry.get('metadata', {}):
                continue
            for event in entry.get('events', []):
                cat = event.get('category')
                cat_prefix = event.get('categoryPrefix')
                cat_version = event.get('categoryVersion')
                labels = {}
                if cat is not None:
                    labels['opentestfactory.org/category'] = cat
                if cat_prefix is not None:
                    labels['opentestfactory.org/categoryPrefix'] = cat_prefix
                if cat_version is not None:
                    labels['opentestfactory.org/categoryVersion'] = cat_version
                if cat or cat_prefix:
                    plugin.config['CONTEXT'][SUBSCRIPTION_KEY].append(
                        subscribe(
                            kind=kind,
                            labels=labels if labels else None,
                            target='inbox',
                            app=plugin,
                        )
                    )
                else:
                    plugin.logger.warning(
                        'At least one of category, categoryPrefix required, ignoring.'
                    )

        run_app(plugin)
    finally:
        for subscription_id in plugin.config['CONTEXT'][SUBSCRIPTION_KEY]:
            unsubscribe(subscription_id, app=plugin)


def _dispatch_providercommand(plugin, handler, body):
    """Provider plugin dispatcher.

    `handler` is expected to return either a list of steps or raise a
    _core.ExecutionError_ exception.
    """
    try:
        plugin.logger.debug('Identified as the %s action.', handler.__name__)
        core.publish_providerresult(handler(body['step'].get('with', {})))
    except core.ExecutionError as err:
        core.publish_error(str(err))
    except Exception as err:
        core.publish_error(f'Unexpected execution error: {err}.')


def _dispatch_executioncommand(plugin, handler, body):
    """Channel plugin dispatcher."""
    try:
        handler(body)
    except Exception as err:
        core.publish_error(f'Unexpected execution error: {err}.')


def _get_target(labels, providers):
    """Find target for labels.

    Finds the most specific provider.  Returns None if no provider
    matches.
    """
    category = labels['opentestfactory.org/category']
    prefix = labels['opentestfactory.org/categoryPrefix']

    action = f'{prefix}/{category}'
    if action in providers:
        return providers[action]
    action = category
    if action in providers:
        return providers[action]
    return None


def make_plugin(
    name,
    description,
    channel=None,
    generator=None,
    provider=None,
    providers=None,
    publisher=None,
    manifest=None,
    schema=None,
):
    """Create and return a new plugin service.

    One and only one of `channel`, `generator`, `provider`, `providers`,
    or `publisher` must be specified.

    If no `manifest` is specified, there must be `plugin.yaml` file in
    the same directory as the caller source file.  If none is found the
    execution stops.

    - Create default config
    - Subscribe to eventbus
    - Add publication handler
    - Create service (not started)

    # Required parameters

    - name: a string
    - description: a string
    - `channel`, `generator` or `provider`: a function
    - providers: a dictionary

    # Optional parameters

    - manifest: a dictionary or a list of dictionaries or None
    - schema: a string or None

    # Raised exceptions

    A _ValueError_ exception is raised if the provided parameters are
    invalid.
    """

    def process_inbox():
        try:
            body = request.get_json() or {}
        except Exception as err:
            return make_status_response('BadRequest', f'Could not parse body: {err}.')

        valid, extra = validate_schema(kind, body)
        if not valid:
            return make_status_response(
                'BadRequest', f'Not a valid {kind} request: {extra}'
            )

        if workflow_id := body.get('metadata', {}).get('workflow_id'):
            g.workflow_id = workflow_id

        if providers:
            labels = body['metadata']['labels']

            if target := _get_target(labels=labels, providers=providers):
                _dispatch_providercommand(plugin, target, body)
            else:
                plugin.logger.warning(f'Labels {labels} not handled by {name}.')
        elif provider:
            _dispatch_providercommand(plugin, provider, body)
        elif channel:
            _dispatch_executioncommand(plugin, channel, body)
        else:
            return make_status_response('BadRequest', 'Not implemented yet')

        return make_status_response('OK', '')

    if len([_ for _ in (channel, generator, provider, providers, publisher) if _]) != 1:
        raise ValueError(
            'One and only one of channel, generator, provider, providers, or publisher is required.'
        )
    if manifest is None:
        try:
            filename = os.path.join(
                os.path.dirname(inspect.stack()[1].filename), 'plugin.yaml'
            )
            with open(filename, 'r') as definition:
                manifest = list(yaml.safe_load_all(definition))
        except:
            plugin.logger.error('Oops, could not get plugin.yaml manifest, aborting.')
            sys.exit(2)
    elif not isinstance(manifest, dict) and not isinstance(manifest, list):
        raise ValueError(
            'Manifest, if specified, must be a dictionary or a list of dictionaries.'
        )

    kind = (
        EXECUTIONCOMMAND
        if channel
        else GENERATORCOMMAND
        if generator
        else PROVIDERCOMMAND
    )
    if not schema:
        schema = SERVICECONFIG if generator else PROVIDERCONFIG
    configfile = f'conf/{name}.yaml'
    plugin = make_app(name, description, configfile=configfile, schema=schema)
    plugin.route('/inbox', methods=['POST'])(process_inbox)

    plugin.config['CONTEXT'][MANIFEST_KEY] = manifest
    plugin.config['CONTEXT'][KIND_KEY] = kind

    core.register_defaultplugin(plugin)

    return plugin
