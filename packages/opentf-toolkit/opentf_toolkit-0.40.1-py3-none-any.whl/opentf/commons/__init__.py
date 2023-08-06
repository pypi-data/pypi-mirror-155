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

"""Helpers for the OpenTestFactory orchestrator"""

from typing import Any, Dict, Iterable, List, Optional, Tuple, Union

import argparse
import csv
import itertools
import logging
import json
import os
import sys

from datetime import datetime
from functools import wraps
from logging.config import dictConfig
from uuid import uuid4

import jwt
import yaml

from flask import Flask, current_app, make_response, request, g
from jsonschema import validate, ValidationError

import requests

from toposort import toposort, CircularDependencyError

import opentf.schemas


########################################################################
# Constants

NOTIFICATION_LOGGER_EXCLUSIONS = 'eventbus'

DEFAULT_NAMESPACE = 'default'

SERVICECONFIG = 'opentestfactory.org/v1alpha1/ServiceConfig'
SSHSERVICECONFIG = 'opentestfactory.org/v1alpha2/SSHServiceConfig'
EVENTBUSCONFIG = 'opentestfactory.org/v1alpha1/EventBusConfig'
PROVIDERCONFIG = 'opentestfactory.org/v1alpha1/ProviderConfig'

SUBSCRIPTION = 'opentestfactory.org/v1alpha1/Subscription'

WORKFLOW = 'opentestfactory.org/v1alpha1/Workflow'
WORKFLOWCOMPLETED = 'opentestfactory.org/v1alpha1/WorkflowCompleted'
WORKFLOWCANCELED = 'opentestfactory.org/v1alpha1/WorkflowCanceled'
WORKFLOWRESULT = 'opentestfactory.org/v1alpha1/WorkflowResult'

GENERATORCOMMAND = 'opentestfactory.org/v1alpha1/GeneratorCommand'
GENERATORRESULT = 'opentestfactory.org/v1alpha1/GeneratorResult'

PROVIDERCOMMAND = 'opentestfactory.org/v1alpha1/ProviderCommand'
PROVIDERRESULT = 'opentestfactory.org/v1alpha1/ProviderResult'

EXECUTIONCOMMAND = 'opentestfactory.org/v1alpha1/ExecutionCommand'
EXECUTIONRESULT = 'opentestfactory.org/v1alpha1/ExecutionResult'
EXECUTIONERROR = 'opentestfactory.org/v1alpha1/ExecutionError'

AGENTREGISTRATION = 'opentestfactory.org/v1alpha1/AgentRegistration'

NOTIFICATION = 'opentestfactory.org/v1alpha1/Notification'

ALLURE_COLLECTOR_OUTPUT = 'opentestfactory.org/v1alpha1/AllureCollectorOutput'

DEFAULT_HEADERS = {
    'Content-Type': 'application/json',
    'Strict-Transport-Security': 'max-age=31536000; includeSubdomains',
    'X-Frame-Options': 'SAMEORIGIN',
    'X-Content-Type-Options': 'nosniff',
    'Referrer-Policy': 'no-referrer',
    'Content-Security-Policy': 'default-src \'none\'',
}

DEFAULT_CONTEXT = {
    'host': '127.0.0.1',
    'port': 443,
    'ssl_context': 'adhoc',
    'eventbus': {'endpoint': 'https://127.0.0.1:38368', 'token': 'invalid-token'},
}

REASON_STATUS = {
    'OK': 200,
    'Created': 201,
    'NoContent': 204,
    'BadRequest': 400,
    'Unauthorized': 401,
    'PaymentRequired': 402,
    'Forbidden': 403,
    'NotFound': 404,
    'AlreadyExists': 409,
    'Conflict': 409,
    'Invalid': 422,
    'InternalError': 500,
}

ALLOWED_ALGORITHMS = [
    'ES256',  # ECDSA signature algorithm using SHA-256 hash algorithm
    'ES384',  # ECDSA signature algorithm using SHA-384 hash algorithm
    'ES512',  # ECDSA signature algorithm using SHA-512 hash algorithm
    'RS256',  # RSASSA-PKCS1-v1_5 signature algorithm using SHA-256 hash algorithm
    'RS384',  # RSASSA-PKCS1-v1_5 signature algorithm using SHA-384 hash algorithm
    'RS512',  # RSASSA-PKCS1-v1_5 signature algorithm using SHA-512 hash algorithm
    'PS256',  # RSASSA-PSS signature using SHA-256 and MGF1 padding with SHA-256
    'PS384',  # RSASSA-PSS signature using SHA-384 and MGF1 padding with SHA-384
    'PS512',  # RSASSA-PSS signature using SHA-512 and MGF1 padding with SHA-512
]

READONLY_VERBS = ('get', 'watch', 'list')
READWRITE_VERBS = ('create', 'delete', 'update', 'patch')


########################################################################
# Config Helpers


class ConfigError(Exception):
    """Invalid configuration file."""


def _add_securityheaders(resp):
    """Add DEFAULT_HEADERS to response."""
    for header, value in DEFAULT_HEADERS.items():
        resp.headers[header] = value
    return resp


def _is_authorizer_required() -> bool:
    """Check if ABAC or RBAC is enabled for service."""
    return current_app and (
        'RBAC' in current_app.config['CONTEXT'].get('authorization_mode', [])
        or 'ABAC' in current_app.config['CONTEXT'].get('authorization_mode', [])
    )


def _read_authorization_policy_file(file: str, context: Dict[str, Any]) -> None:
    """Read ABAC authorization policy file.

    Policy file is a JSONL file, of form:

    ```json
    {"apiVersion": "abac.opentestfactory.org/v1alpha1", "kind": "Policy", "spec": {"user": "alice", "namespace": "*", "resource": "*", "apiGroup": "*"}}
    ...
    ```

    # Required parameters

    - file: a string
    - context: a dictionary

    # Returned value

    None

    # Raised exceptions

    Raises _ConfigError_ if the specified file is not a JSONL file.
    """
    if not os.path.exists(file):
        raise ConfigError(f'Authorization policy file "{file}" does not exist.')
    try:
        with open(file, 'r', encoding='utf-8') as f:
            context['authorization_policies'] = [
                json.loads(l) for l in f.read().splitlines() if l
            ]
    except Exception as err:
        raise ConfigError(f'Could not read policy file "{file}": {err}.')


def _read_trustedkeys_auth_file(file: str, context: Dict[str, Any]) -> None:
    """Read trustedkeys file.

    Trusted keys auth file is of form:

    ```text
    key,name,"group1,group2,group3","namespace_1,namespace_2"
    ```

    The first 2 columns are required, the remaining columns are
    optional.

    # Raised exceptions

    Raises _ConfigError_ if the specified token file is invalid.
    """
    if not os.path.exists(file):
        raise ConfigError(f'Trusted keys authorization file "{file}" does not exist.')
    try:
        with open(file, 'r', encoding='utf-8') as f:
            context['authorization_trustedkeys'] = list(csv.reader(f, delimiter=','))
        for entry in context['authorization_trustedkeys']:
            if len(entry) < 2:
                raise ConfigError(
                    f'Entries in trusted keys authorization file "{file}" must have at least 2 elements: {entry}.'
                )
        if len(context['authorization_trustedkeys']) != len(
            set(x[0] for x in context['authorization_trustedkeys'])
        ):
            raise ConfigError(
                f'Duplicated entries in trusted keys authorization file "{file}".'
            )
    except Exception as err:
        raise ConfigError(
            f'Could not read trusted keys authorization file "{file}": {err}.'
        )


def _read_token_auth_file(file: str, context: Dict[str, Any]) -> None:
    """Read token file.

    Static token file is of form:

    ```text
    token,user,uid,"group1,group2,group3"
    ```

    The first 3 columns are required, the remaining columns are
    optional.

    # Raised exceptions

    Raises _ConfigError_ if the specified token file is invalid.
    """
    if not os.path.exists(file):
        raise ConfigError(f'Token authorization file "{file}" does not exist.')
    try:
        with open(file, 'r', encoding='utf-8') as f:
            context['authorization_tokens'] = list(csv.reader(f, delimiter=','))
        for entry in context['authorization_tokens']:
            if len(entry) < 3:
                raise ConfigError(
                    f'Entries in token authorization file "{file}" must have at least 3 elements: {entry}'
                )
    except Exception as err:
        raise ConfigError(f'Could not read token authorization file "{file}": {err}.')


def _initialize_authn_authz(args, context: Dict[str, Any]) -> None:
    """Initialize authn & authz

    Handles the following service parameters:

    - `--trusted-authorities`
    - `--enable-insecure-login`
    - `--insecure-bind-address`
    - `--authorization-mode` (ABAC, RBAC)

    # Required parameters

    - args: an argparse result
    - context: a dictionary
    """
    abac = rbac = False
    if args.trusted_authorities:
        context['trusted_authorities'] = args.trusted_authorities.split(',')
    if args.authorization_mode:
        context['authorization_mode'] = args.authorization_mode.split(',')
        abac = 'ABAC' in context['authorization_mode']
        rbac = 'RBAC' in context['authorization_mode']
        if abac and rbac:
            raise ConfigError(
                'Cannot specify both ABAC and RBAC as authorization mode.'
            )
        if abac:
            if not args.authorization_policy_file:
                raise ConfigError('ABAC requires an authorization policy file.')
            if not args.token_auth_file:
                raise ConfigError('ABAC requires a token authentication file.')
            _read_authorization_policy_file(args.authorization_policy_file, context)
            _read_token_auth_file(args.token_auth_file, context)

        if rbac:
            raise ConfigError('RBAC not supported yet.')

    if args.enable_insecure_login:
        context['enable_insecure_login'] = True
    if 'enable_insecure_login' not in context:
        context['enable_insecure_login'] = False
    if 'insecure_bind_address' not in context:
        context['insecure_bind_address'] = args.insecure_bind_address
    if args.trustedkeys_auth_file:
        _read_trustedkeys_auth_file(args.trustedkeys_auth_file, context)
    context['trusted_keys'] = _read_key_files(
        context.get('trusted_authorities', []), context
    )


USERIDS_RULES_CACHE = {}
USERIDS_NAMESPACES_CACHE = {}


def _in_group(user_id, group):
    tokens = current_app.config['CONTEXT'].get('authorization_tokens')
    if group is not None and tokens is not None:
        for entry in tokens:
            if entry[2] == user_id and len(entry) > 3:
                return group in entry[3].split(',')
    return False


def _cache_userid_rules(user_id: str) -> None:
    USERIDS_RULES_CACHE[user_id] = [
        policy['spec']
        for policy in current_app.config['CONTEXT']['authorization_policies']
        if policy['spec'].get('user') == user_id
        or _in_group(user_id, policy['spec'].get('group'))
    ]


def _cache_userid_namespaces(user_id: str) -> None:
    nss = USERIDS_NAMESPACES_CACHE[user_id] = set()
    for rule in USERIDS_RULES_CACHE[user_id]:
        if rule.get('namespace'):
            nss.add(rule['namespace'])


def _is_authorized(payload, resource: str, verb: str) -> bool:
    """Check if resource access is authorized, disregarding namespace."""
    if 'namespaces' in g:
        return True
    user_id = payload['sub']
    if user_id not in USERIDS_RULES_CACHE:
        _cache_userid_rules(user_id)
    authorized = False
    for rule in USERIDS_RULES_CACHE[user_id]:
        if rule['resource'] in (resource, '*'):
            authorized |= verb in READONLY_VERBS if rule.get('readonly') else True
    return authorized


def can_use_namespace(
    namespace: str, resource: Optional[str] = None, verb: Optional[str] = None
) -> bool:
    """Check if namespace is accessible for current request.

    If called outside of a request context, returns True.

    # Required parameters

    - namespace: a string

    # Optional parameters

    - resource: a string or None (None by default)
    - verb: a string or None (None by default)
    """
    if not g or g.get('insecure_login'):
        return True
    if g and 'namespaces' in g:
        return namespace in g.namespaces or '*' in g.namespaces
    if g and 'payload' in g:
        user = g.payload['sub']
        if user not in USERIDS_RULES_CACHE:
            _cache_userid_rules(user)
        if user not in USERIDS_NAMESPACES_CACHE:
            _cache_userid_namespaces(user)
        if resource and verb:
            authorized = False
            for rule in USERIDS_RULES_CACHE[user]:
                if rule['namespace'] in ('*', namespace) and rule['resource'] in (
                    resource,
                    '*',
                ):
                    authorized |= (
                        verb in READONLY_VERBS if rule.get('readonly') else True
                    )
            return authorized
        namespaces = USERIDS_NAMESPACES_CACHE[user]
        return namespace in namespaces or '*' in namespaces
    return False


def authorizer(resource: str, verb: str):
    """Decorate a function by adding an access control verifier.

    # Required parameters

    - resource: a string
    - verb: a string

    # Returned value

    The decorated function, unchanged if no authorizer required.

    The decorated function, which is expected to be a endpoint, will
    reject incoming requests if access control is enabled and the
    requester does not have the necessary rights.
    """

    def inner(function):
        """Ensure the incoming request has the required authorization"""

        @wraps(function)
        def wrapper(*args, **kwargs):
            if not _is_authorizer_required() or not g or g.get('insecure_login'):
                return function(*args, **kwargs)
            payload = g.get('payload')
            if not payload:
                return make_status_response('Unauthorized', 'No JWT payload.')
            if not _is_authorized(payload, resource, verb):
                return make_status_response(
                    'Forbidden',
                    f'User {payload["sub"]} is not authorized to {verb} {resource}.',
                )
            return function(*args, **kwargs)

        return wrapper

    return inner


def _check_token(authz: str, context: Dict[str, Any]):
    """Check token validity.

    Token is checked against known trusted authorities and then against
    `token_auth_file`, if any.

    # Required parameters

    - authz: a string ('bearer xxxxxx')
    - context: a dictionary

    # Returned value

    None if the the bearer token is valid.  A status response if the
    token is invalid.
    """
    parts = authz.split()
    if not parts or parts[0].lower() != 'bearer' or len(parts) != 2:
        logging.error(authz)
        return make_status_response('Unauthorized', 'Invalid Authorization header.')
    for mode in context.get('authorization_mode', []) + ['JWT']:
        if mode == 'JWT':
            for i, pubkey in enumerate(context['trusted_keys']):
                try:
                    payload = jwt.decode(
                        parts[1], pubkey[0], algorithms=ALLOWED_ALGORITHMS
                    )
                    logging.debug('Token signed by trusted key #%d', i)
                    g.payload = payload
                    g.namespaces = pubkey[1]
                    return None
                except ValueError as err:
                    logging.error('Invalid trusted key #%d:', i)
                    logging.error(err)
                except jwt.InvalidAlgorithmError as err:
                    logging.error(
                        'Invalid algorithm while verifying token by trusted key #%d:', i
                    )
                    logging.error(err)
                except jwt.InvalidTokenError as err:
                    logging.debug('Token could not be verified by trusted key #%d:', i)
                    logging.debug(err)
        elif mode == 'ABAC':
            for user in context.get('authorization_tokens', []):
                if user[0] == parts[1]:
                    g.payload = {'sub': user[2]}
                    return None
    return make_status_response('Unauthorized', 'Invalid JWT token.')


def _make_authenticator(context: Dict[str, Any]):
    """Make an authenticator function tied to context."""

    def inner():
        """Ensure the incoming request is authenticated.

        If from localhost, allow.

        If from somewhere else, ensure there is a valid token attached.
        """
        if context.get('enable_insecure_login') and request.remote_addr == context.get(
            'insecure_bind_address'
        ):
            g.insecure_login = True
            return None
        authz = request.headers.get('Authorization')
        if authz is None:
            return make_status_response('Unauthorized', 'No Bearer token')
        return _check_token(authz, context)

    return inner


def get_actor() -> Optional[str]:
    """Get actor.

    # Returned value

    The subject (user), if authenticated.  None otherwise.
    """
    if g and 'payload' in g:
        return g.payload.get('sub')
    return None


def run_app(app):
    """Start the app."""
    context = app.config['CONTEXT']
    ssl_enabled = context.get('ssl_context') != 'disabled'

    app.run(
        host=context['host'],
        port=context['port'],
        ssl_context=context['ssl_context'] if ssl_enabled else None,
    )


class EventbusLogger(logging.Handler):
    """A Notification logger.

    A logging handler that posts Notifications if the workflow is
    known.

    Does nothing if the log event is not patched to a workflow.

    If `silent` is set to False, will print on stdout whenever it fails
    to send notifications.
    """

    def __init__(self, silent: bool = True):
        self.silent = silent
        super().__init__()

    def emit(self, record):
        if request and 'workflow_id' in g:
            try:
                publish(
                    {
                        'apiVersion': 'opentestfactory.org/v1alpha1',
                        'kind': 'Notification',
                        'metadata': {
                            'name': 'log notification',
                            'workflow_id': g.workflow_id,
                        },
                        'spec': {'logs': [self.format(record)]},
                    },
                    current_app.config['CONTEXT'],
                )
            except Exception:
                if not self.silent:
                    print(
                        f'{record.name}: Could not send notification to workflow {g.workflow_id}.'
                    )


def _make_argparser(description: str, configfile: str):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        '--config', help=f'alternate config file (default to {configfile})'
    )
    parser.add_argument('--context', help='alternative context')
    parser.add_argument('--host', help='alternative host')
    parser.add_argument('--port', help='alternative port')
    parser.add_argument(
        '--ssl_context', '--ssl-context', help='alternative ssl context'
    )
    parser.add_argument(
        '--trusted_authorities',
        '--trusted-authorities',
        help='alternative trusted authorities',
    )
    parser.add_argument(
        '--enable_insecure_login',
        '--enable-insecure-login',
        action='store_true',
        help='enable insecure login (disabled by default)',
    )
    parser.add_argument(
        '--insecure_bind_address',
        '--insecure-bind-address',
        help='insecure bind address (127.0.0.1 by default)',
        default='127.0.0.1',
    )
    parser.add_argument(
        '--authorization_mode',
        '--authorization-mode',
        help='authorization mode, JWT without RBAC if unspecified',
    )
    parser.add_argument(
        '--authorization_policy_file',
        '--authorization-policy-file',
        help='authorization policies for ABAC',
    )
    parser.add_argument(
        '--token_auth_file',
        '--token-auth-file',
        help='authenticated users for ABAC and RBAC',
    )
    parser.add_argument(
        '--trustedkeys_auth_file',
        '--trustedkeys-auth-file',
        help='authenticated trusted keys for ABAC and RBAC',
    )
    return parser


def make_app(
    name: str,
    description: str,
    configfile: str,
    schema: Optional[str] = None,
    defaultcontext: Optional[Dict[str, Any]] = None,
):
    """Create a new app.

    # Required parameters:

    - name: a string
    - description: a string
    - configfile: a string

    # Optional parameters:

    - schema: a string or None (None by default)
    - defaultcontext: a dictionary or None (None by default)

    # Returned value

    A new flask app.  Two entries are added to `app.config`: `CONTEXT`
    and `CONFIG`.

    `CONFIG` is a dictionary, the complete config file.  `CONTEXT` is a
    subset of `CONFIG`, the current entry in `CONFIG['context']`.  It is
    also a dictionary.

    # Raised Exception

    A _ConfigError_ exception is raised if the context is not found or
    if the config file is invalid.
    """
    parser = _make_argparser(description, configfile)
    args = parser.parse_args()

    logging_conf = {
        'version': 1,
        'formatters': {
            'default': {
                'format': f'[%(asctime)s] %(levelname)s in {name}: %(message)s',
            }
        },
        'handlers': {
            'wsgi': {
                'class': 'logging.StreamHandler',
                'stream': 'ext://flask.logging.wsgi_errors_stream',
                'formatter': 'default',
            },
        },
        'root': {
            'level': os.environ.get('DEBUG_LEVEL', 'INFO'),
            'handlers': ['wsgi'],
        },
    }
    if name not in NOTIFICATION_LOGGER_EXCLUSIONS:
        logging_conf['handlers']['eventbus'] = {
            'class': 'opentf.commons.EventbusLogger',
            'formatter': 'default',
        }
        logging_conf['root']['handlers'] += ['eventbus']
    dictConfig(logging_conf)

    app = Flask(name)
    try:
        if args.config is None and not os.path.isfile(configfile):
            if args.context:
                raise ConfigError(
                    'Cannot specify a context with default configuration.'
                )
            context = defaultcontext or DEFAULT_CONTEXT
            config = {}
        else:
            with open(args.config or configfile, 'r', encoding='utf-8') as cnf:
                config = yaml.safe_load(cnf)

            valid, extra = validate_schema(schema or SERVICECONFIG, config)
            if not valid:
                raise ConfigError(f'Not a valid config file: {extra}.')

            context_name = args.context or config['current-context']
            contexts = [
                ctx for ctx in config['contexts'] if ctx['name'] == context_name
            ]

            if len(contexts) != 1:
                raise ConfigError(
                    f'Could not find context "{context_name}" in config file "{args.config}".'
                )
            context = contexts[0]['context']
    except ConfigError as err:
        app.logger.error(err)
        sys.exit(2)

    if args.host:
        context['host'] = args.host
    if args.port:
        context['port'] = args.port
    if args.ssl_context:
        context['ssl_context'] = args.ssl_context

    try:
        _initialize_authn_authz(args, context)
    except ConfigError as err:
        app.logger.error(err)
        sys.exit(2)

    app.config['CONTEXT'] = context
    app.config['CONFIG'] = config
    app.config['DEBUG_LEVEL'] = os.environ.get('DEBUG_LEVEL', 'INFO')
    app.before_request(_make_authenticator(context))
    app.after_request(_add_securityheaders)
    return app


########################################################################
## Misc. internal helpers


def _read_key_files(items: Iterable[str], context) -> List[str]:
    """Read a series of files.

    # Required parameters

    - items: an iterable of strings
    - auth_file: a string or None

    Items are either fully-qualified file names or fully-qualified
    directory name ending with '/*'.  They may have a secondary part,
    following a ',', which is either a '*' or a list of comma-separated
    namespaces, in double quotes.

    For example:

    - /etc/opentf/a_public_key
    - /etc/opentf/dept_a/*
    - /etc/opentf/another_public_key
    - /etc/opentf/dept_b/*

    If no namespace is specified, 'default' is assumed.

    # Returned value

    A list of pairs.  The pair's first element is a fully-qualified file
    name, the second element is a list of namespaces.
    """
    files = []
    for item in items:
        if item.endswith('/*'):
            files += [
                f'{item[:-1]}{file}'
                for file in os.listdir(item[:-2])
                if not file.startswith('.')
            ]
        else:
            files.append(item)
    keys = []
    auths = {}
    for auth in context.get('authorization_trustedkeys', []):
        if len(auth) >= 4:
            auths[auth[0]] = auth[3].split(',')
    for i, keyfile in enumerate(files):
        try:
            with open(keyfile, 'r', encoding='utf-8') as key:
                logging.debug('Reading trusted key #%d (%s)', i, keyfile)
                keys.append((key.read(), auths.get(keyfile, ['default'])))
        except Exception as err:
            logging.error(
                'Error while reading trusted key #%d (%s), skipping:', i, keyfile
            )
            logging.error(err)
    logging.debug('Trusted keys/namespaces mapping: %s', keys)
    return keys


########################################################################
## Misc. helpers


def make_uuid():
    """Generate a new uuid as a string."""
    return str(uuid4())


########################################################################
# JSON Schema Helpers

_schemas = {}

SCHEMAS_ROOT_DIRECTORY = list(opentf.schemas.__path__)[0]


def get_schema(name: str) -> Dict[str, Any]:
    """Get specified schema.

    # Required parameters

    - name: a string, the schema name (its kind)

    # Returned value

    A _schema_.  A schema is a dictionary.

    # Raised exceptions

    If an error occurs while reading the schema, the initial exception
    is logged and raised again.
    """
    if name not in _schemas:
        try:
            with open(
                os.path.join(SCHEMAS_ROOT_DIRECTORY, f'{name}.json'),
                'r',
                encoding='utf-8',
            ) as schema:
                _schemas[name] = json.loads(schema.read())
        except Exception as err:
            logging.error('Could not read schema %s: %s', name, err)
            raise
    return _schemas[name]


def validate_schema(schema, instance) -> Tuple[bool, Any]:
    """Return True if instance validates schema.

    # Required parameters

    - name: a string, the schema name (its kind)
    - instance: a dictionary

    # Returned value

    A (bool, Optional[str]) pair.  If `instance` is a valid instance of
    `schema`, returns `(True, None)`.  If not, returns `(False, error)`.

    # Raised exceptions

    If an error occurs while reading the schema, the initial exception
    is logged and raised again.
    """
    try:
        validate(schema=get_schema(schema), instance=instance)
    except ValidationError as err:
        return False, err
    return True, None


########################################################################
# API Server Helpers


def make_event(schema: str, **kwargs) -> Dict[str, Any]:
    """Return a new event dictionary.

    # Required parameters

    - schema: a string

    # Optional parameters

    A series of key=values

    # Returned value

    A dictionary.
    """
    apiversion, kind = schema.rsplit('/', 1)
    return {'apiVersion': apiversion, 'kind': kind, **kwargs}


def make_status_response(
    reason: str, message: str, details: Optional[Dict[str, Any]] = None
):
    """Return a new status response object.

    # Required parameters

    - reason: a non-empty string (must exist in `REASON_STATUS`)
    - message: a string

    # Optional parameters:

    - details: a dictionary or None (None by default)

    # Returned value

    A _status_.  A status is a dictionary with the following entries:

    - kind: a string (`'Status'`)
    - apiVersion: a string (`'v1'`)
    - metadata: an empty dictionary
    - status: a string (either `'Success'` or `'Failure'`)
    - message: a string (`message`)
    - reason: a string (`reason`)
    - details: a dictionary or None (`details`)
    - code: an integer (derived from `reason`)
    """
    code = REASON_STATUS[reason]
    if code // 100 == 4:
        logging.warning(message)
    elif code // 100 == 5:
        logging.error(message)
    return make_response(
        {
            'kind': 'Status',
            'apiVersion': 'v1',
            'metadata': {},
            'status': 'Success' if code // 100 == 2 else 'Failure',
            'message': message,
            'reason': reason,
            'details': details,
            'code': code,
        },
        code,
    )


########################################################################
# Pipelines Helpers


def validate_pipeline(
    workflow: Dict[str, Any]
) -> Tuple[bool, Union[str, List[List[str]]]]:
    """Validate workflow jobs, looking for circular dependencies.

    # Required parameters

    - workflow: a dictionary

    # Returned value

    A (`bool`, extra) pair.

    If there is a dependency on an non-existing job, returns
    `(False, description (a string))`.

    If there are circular dependencies in the workflow jobs, returns
    `(False, description (a string))`.

    If there are no circular dependencies, returns `(True, jobs)` where
    `jobs` is an ordered list of job names lists.  Each item in the
    returned list is a set of jobs that can run in parallel.
    """
    try:
        jobs = {}
        for job in workflow['jobs']:
            needs = workflow['jobs'][job].get('needs')
            if needs:
                if isinstance(needs, list):
                    jobs[job] = set(needs)
                else:
                    jobs[job] = {needs}
            else:
                jobs[job] = set()
        for src, dependencies in jobs.items():
            for dep in dependencies:
                if dep not in jobs:
                    return (
                        False,
                        f"Job '{src}' has a dependency on job '{dep}' which does not exist.",
                    )

        return True, [list(items) for items in toposort(jobs)]
    except CircularDependencyError as err:
        return False, str(err)


def get_execution_sequence(workflow: Dict[str, Any]) -> Optional[List[str]]:
    """Return an execution sequence for jobs.

    # Required parameters

    - workflow: a dictionary

    # Returned value

    `None` or a list of jobs names.
    """
    try:
        jobs = {}
        for job in workflow['jobs']:
            needs = workflow['jobs'][job].get('needs')
            if needs:
                if isinstance(needs, list):
                    jobs[job] = set(needs)
                else:
                    jobs[job] = {needs}
            else:
                jobs[job] = set()
        return list(itertools.chain.from_iterable(toposort(jobs)))
    except CircularDependencyError:
        return None


########################################################################
# Publishers & Subscribers Helpers


def make_subscription(
    name: str, selector: Dict[str, Any], target: str, context: Dict[str, Any]
) -> Dict[str, Any]:
    """Generate a subscription manifest.

    # Required parameter

    - name: a string
    - selector: a dictionary
    - target: a string
    - context: a dictionary

    # Returned value

    A _subscription manifest_.  A subscription manifest is a dictionary
    with the following entries:

    - apiVersion: a string
    - kind: a string
    - metadata: a dictionary
    - spec: a dictionary

    `metadata` has two entries: `name` and `timestamp`.

    `spec` has two entries: `selector` and `subscriber`.
    """
    protocol = 'https' if context.get('ssl_context') != 'disabled' else 'http'
    hostname = context['eventbus'].get('hostname', context['host'])
    subscriber = {'endpoint': f'{protocol}://{hostname}:{context["port"]}/{target}'}
    return {
        'apiVersion': 'opentestfactory.org/v1alpha1',
        'kind': 'Subscription',
        'metadata': {'name': name, 'creationTimestamp': datetime.now().isoformat()},
        'spec': {'selector': selector, 'subscriber': subscriber},
    }


def subscribe(
    kind: str,
    target: str,
    app,
    labels: Optional[Dict[str, Any]] = None,
    fields: Optional[Dict[str, Any]] = None,
) -> str:
    """Subscribe on specified endpoint.

    `kind` is of form `[apiVersion/]kind`.

    # Required parameters

    - kind: a string
    - target: a string
    - app: a flask app

    # Optional parameters

    - labels: a dictionary
    - fields: a dictionary

    # Returned value

    A _uuid_ (a string).

    # Raised exceptions

    An exception is raised if the subscription failed.
    """
    if '/' in kind:
        apiversion, kind = kind.rsplit('/', 1)
        if fields is None:
            fields = {}
        fields['apiVersion'] = apiversion
    selector: Dict[str, Any] = {'matchKind': kind}
    if labels:
        selector['matchLabels'] = labels
    if fields:
        selector['matchFields'] = fields
    context = app.config['CONTEXT']
    return requests.post(
        context['eventbus']['endpoint'] + '/subscriptions',
        json=make_subscription(
            app.name, selector=selector, target=target, context=context
        ),
        headers={'Authorization': f'Bearer {context["eventbus"]["token"]}'},
        verify=not context['eventbus'].get('insecure-skip-tls-verify', False),
    ).json()['details']['uuid']


def unsubscribe(subscription_id: str, app) -> requests.Response:
    """Cancel specified subscription

    #  Required parameters

    - subscription_id: a string (an uuid)
    - app: a flask app

    # Returned value

    A `requests.Response` object.
    """
    context = app.config['CONTEXT']
    return requests.delete(
        context['eventbus']['endpoint'] + '/subscriptions/' + subscription_id,
        headers={'Authorization': f'Bearer {context["eventbus"]["token"]}'},
        verify=not context['eventbus'].get('insecure-skip-tls-verify', False),
    )


def publish(publication: Any, context: Dict[str, Any]) -> requests.Response:
    """Publish publication on specified endpoint.

    If `publication` is a dictionary, and if it has a `metadata` entry,
    a `creationTimestamp` sub-entry will be created (or overwritten if
    it already exists).

    # Required parameters

    - publication: an object
    - context: a dictionary

    # Returned value

    A `requests.Response` object.
    """
    if isinstance(publication, dict) and 'metadata' in publication:
        publication['metadata']['creationTimestamp'] = datetime.now().isoformat()
    return requests.post(
        context['eventbus']['endpoint'] + '/publications',
        json=publication,
        headers={'Authorization': f'Bearer {context["eventbus"]["token"]}'},
        verify=not context['eventbus'].get('insecure-skip-tls-verify', False),
    )
