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

"""Startup script for allinone images.

The following environment variables are used, if defined:

    DEBUG: 'INFO'
    DEBUG_LEVEL: 'INFO'
    OPENTF_CONTEXT: 'allinone'
    OPENTF_AUTHORIZATION_MODE: None
    OPENTF_AUTHORIZATION_POLICY_FILE: None
    OPENTF_TOKEN_AUTH_FILE: None
    OPENTF_TRUSTEDKEYS_AUTH_FILE: None
    OPENTF_DEBUG: 'INFO'
    OPENTF_EVENTBUS_WARMUPDELAY: 2
    OPENTF_EVENTBUS_WARMUPURL: 'http://127.0.0.1:38368/subscriptions'
    OPENTF_EVENTBUSCONFIG: 'conf/eventbus.yaml'
    OPENTF_HEALTHCHECK_DELAY: 60
    OPENTF_LAUNCHERMANIFEST: 'squashtf.yaml'
    OPENTF_PLUGINMANIFEST: 'plugin.yaml'
    OPENTF_SERVICEMANIFEST: 'service.yaml'
    OPENTF_SSHCHANNELCONFIG: 'conf/sshee.yaml'
    OPENTF_TRUSTEDKEYS_PATHS: None
    TRUSTEDKEYS_PATH: '/etc/squashtf'
    TRUSTED_KEYS_FILE: 'trusted_key.pub'
    KEY_SIZE: 4096
    PUBLIC_EXP: 65537
    PUBLIC_KEY: None
    SSH_CHANNEL_HOST: None
    SSH_CHANNEL_PASSWORD: None
    SSH_CHANNEL_POOLS: None
    SSH_CHANNEL_TAGS: None
    SSH_CHANNEL_USER: None
"""

from typing import Any, Dict, List, Optional, Tuple, Union

from importlib.metadata import version

import base64
import hashlib
import json
import logging
import os
import subprocess
import sys
import time

import jwt
import requests
import yaml

import opentf


LOGGING_FORMAT = '[%(asctime)s] %(levelname)s in startup: %(message)s'
if os.environ.get('DEBUG') or os.environ.get('OPENTF_DEBUG'):
    logging.basicConfig(level=logging.DEBUG, format=LOGGING_FORMAT)
else:
    logging.basicConfig(level=logging.INFO, format=LOGGING_FORMAT)


########################################################################

SERVICEFILE_NAME = 'init_services.json'

ENVIRONMENT_VARIABLES = {
    'DEBUG': 'INFO',
    'DEBUG_LEVEL': 'INFO',
    'OPENTF_CONTEXT': 'allinone',
    'OPENTF_AUTHORIZATION_MODE': None,
    'OPENTF_AUTHORIZATION_POLICY_FILE': None,
    'OPENTF_TOKEN_AUTH_FILE': None,
    'OPENTF_TRUSTEDKEYS_AUTH_FILE': None,
    'OPENTF_DEBUG': 'INFO',
    'OPENTF_EVENTBUS_WARMUPDELAY': 2,
    'OPENTF_EVENTBUS_WARMUPURL': 'http://127.0.0.1:38368/subscriptions',
    'OPENTF_EVENTBUSCONFIG': 'conf/eventbus.yaml',
    'OPENTF_HEALTHCHECK_DELAY': 60,
    'OPENTF_LAUNCHERMANIFEST': 'squashtf.yaml',
    'OPENTF_PLUGINMANIFEST': 'plugin.yaml',
    'OPENTF_SERVICEMANIFEST': 'service.yaml',
    'OPENTF_SSHCHANNELCONFIG': 'conf/sshee.yaml',
    'OPENTF_TRUSTEDKEYS_PATHS': None,
    'TRUSTEDKEYS_PATH': '/etc/squashtf',
    'TRUSTED_KEYS_FILE': 'trusted_key.pub',
    'KEY_SIZE': 4096,
    'PUBLIC_EXP': 65537,
    'PUBLIC_KEY': None,
    'SSH_CHANNEL_HOST': None,
    'SSH_CHANNEL_PASSWORD': None,
    'SSH_CHANNEL_POOLS': None,
    'SSH_CHANNEL_TAGS': None,
    'SSH_CHANNEL_USER': None,
}
ENVIRONMENT_SECRETS = {'SSH_CHANNEL_PASSWORD'}


########################################################################
# Environment variables helpers


def _get_env(var: str) -> str:
    """Read var from env, using default if not set."""
    return os.environ.get(var, ENVIRONMENT_VARIABLES[var])


def _get_env_int(var: str) -> int:
    """Read var from env, using default if not set or not int."""
    try:
        return int(_get_env(var))
    except ValueError:
        val = ENVIRONMENT_VARIABLES[var]
        logging.warning(
            'Environment variable %s not an integer, defaulting to %d.',
            var,
            val,
        )
        return val


def dump_environment():
    """Dump environment variables."""
    logging.info('Environment variables:')
    for var, val in ENVIRONMENT_VARIABLES.items():
        if val := os.environ.get(var):
            logging.info(
                '  %s: %s',
                var,
                repr(val) if var not in ENVIRONMENT_SECRETS else '*' * len(val),
            )
        else:
            if val is not None:
                logging.info(
                    '  %s not set. Using default value %s.',
                    var,
                    repr(val),
                )
            else:
                logging.info('  %s not set.  No default value.', var)


OPENTF_MANIFEST = _get_env('OPENTF_LAUNCHERMANIFEST')
PLUGIN_MANIFEST = _get_env('OPENTF_PLUGINMANIFEST')
SERVICE_MANIFEST = _get_env('OPENTF_SERVICEMANIFEST')
SSHCHANNEL_CONFIG = _get_env('OPENTF_SSHCHANNELCONFIG')
EVENTBUS_CONFIG = _get_env('OPENTF_EVENTBUSCONFIG')

HEALTHCHECK_DELAY = _get_env_int('OPENTF_HEALTHCHECK_DELAY')
EVENTBUS_WARMUP_DELAY = _get_env_int('OPENTF_EVENTBUS_WARMUPDELAY')
EVENTBUS_WARMUP_URL = _get_env('OPENTF_EVENTBUS_WARMUPURL')

TRUSTEDKEYS_PATH = _get_env('TRUSTEDKEYS_PATH')
TRUSTED_KEYS_FILE = _get_env('TRUSTED_KEYS_FILE')
KEY_SIZE = _get_env_int('KEY_SIZE')
PUBLIC_EXP = _get_env_int('PUBLIC_EXP')

DEFAULT_CONTEXT = _get_env('OPENTF_CONTEXT')

OPENTF_AUTHORIZATION_MODE = _get_env('OPENTF_AUTHORIZATION_MODE')
OPENTF_AUTHORIZATION_POLICY_FILE = _get_env('OPENTF_AUTHORIZATION_POLICY_FILE')
OPENTF_TOKEN_AUTH_FILE = _get_env('OPENTF_TOKEN_AUTH_FILE')
OPENTF_TRUSTEDKEYS_AUTH_FILE = _get_env('OPENTF_TRUSTEDKEYS_AUTH_FILE')
OPENTF_TRUSTEDKEYS_PATHS = _get_env('OPENTF_TRUSTEDKEYS_PATHS')

########################################################################
# Helpers


CORE = '${{ CORE }}'


def _expand(path: str) -> List[str]:
    """Perform path substitution."""
    if CORE in path:
        return [path.replace(CORE, root) for root in sys.modules['opentf'].__path__]
    return [path]


def _generate_token() -> Tuple[str, str]:
    """Generate temporary key and JWT token."""
    # pylint: disable=import-outside-toplevel
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.hazmat.backends import default_backend

    private_key = rsa.generate_private_key(
        public_exponent=PUBLIC_EXP, key_size=KEY_SIZE, backend=default_backend()
    )
    public_key = private_key.public_key()
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode()
    pub = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    ).decode()
    token = jwt.encode(
        {'iss': 'squash orchestrator', 'sub': 'temp token'}, pem, algorithm='RS512'
    )
    return token, pub


def start_microservice(cmd: Union[str, List[str]]) -> Any:
    """Start cmd in a detached process, returning popen object."""
    if isinstance(cmd, str):
        cmd = cmd.split(' ')
    cmd += ['--context', DEFAULT_CONTEXT]
    if OPENTF_AUTHORIZATION_MODE:
        cmd += ['--authorization-mode', OPENTF_AUTHORIZATION_MODE]
    if OPENTF_AUTHORIZATION_POLICY_FILE:
        cmd += ['--authorization-policy-file', OPENTF_AUTHORIZATION_POLICY_FILE]
    if OPENTF_TOKEN_AUTH_FILE:
        cmd += ['--token-auth-file', OPENTF_TOKEN_AUTH_FILE]
    if OPENTF_TRUSTEDKEYS_AUTH_FILE:
        cmd += ['--trustedkeys-auth-file', OPENTF_TRUSTEDKEYS_AUTH_FILE]
    if OPENTF_TRUSTEDKEYS_PATHS:
        cmd += ['--trusted-authorities', OPENTF_TRUSTEDKEYS_PATHS]
    logging.info('Starting %s...', str(cmd))
    pid = subprocess.Popen(cmd)
    logging.debug('(pid is %d.)', pid.pid)
    return pid


RUNNING = set()
SERVICES = set()


def parse_and_start(
    paths: List[str], item: str, disabled: Optional[List[str]] = None
) -> List[Any]:
    """Lookup item manifests and start them if not disabled."""
    result = []
    for path in paths:
        for entry in os.walk(path):
            logging.debug('Reading path %s.', entry[0])
            if item not in entry[2]:
                logging.debug('(No manifest found in path.)')
                continue
            logging.debug('(Found a %s manifest, parsing.)', item)
            with open(os.path.join(entry[0], item), 'r', encoding='utf-8') as manifests:
                for manifest in yaml.safe_load_all(manifests):
                    if disabled and manifest['metadata']['name'].lower() in disabled:
                        logging.debug(
                            '(Plugin %s explicitly disabled, ignoring.)',
                            manifest['metadata']['name'],
                        )
                        continue
                    if manifest.get('cmd') is None:
                        continue
                    SERVICES.add(manifest['metadata']['name'])
                    if manifest['cmd'] not in RUNNING:
                        RUNNING.add(manifest['cmd'])
                        result.append(start_microservice(manifest['cmd']))
    return result


def write_init_file():
    """Write service json file."""
    init_dictionary: Dict[str, Any] = {'services': list(SERVICES)}
    services = ''.join(SERVICES)
    services_bytes = base64.b64encode(services.encode('utf-8'))
    checksum = hashlib.sha256(services_bytes).hexdigest()
    init_dictionary['checksum'] = checksum
    with open(SERVICEFILE_NAME, 'w', encoding='utf-8') as outfile:
        json.dump(init_dictionary, outfile)


def get_eventbus_endpoint():
    """Get eventbus endpoint."""
    try:
        with open(EVENTBUS_CONFIG, 'r', encoding='utf-8') as conf:
            ebconf = yaml.safe_load(conf)
        for context in ebconf['contexts']:
            if context['name'] == DEFAULT_CONTEXT:
                return EVENTBUS_WARMUP_URL.replace(
                    '38368', str(context['context']['port'])
                )
    except Exception as err:
        logging.warning(
            'Could not find eventbus configuration, assuming default. (%s)', str(err)
        )

    return EVENTBUS_WARMUP_URL


def maybe_start_eventbus(conf: Dict[str, Any]) -> List[Any]:
    """Start eventbus if needed."""
    if 'eventbus' in conf:
        bus = start_microservice(conf['eventbus'])
        time.sleep(EVENTBUS_WARMUP_DELAY)
        start = time.monotonic()
        while True:
            try:
                status = requests.get(get_eventbus_endpoint()).status_code
                if status == 200:
                    break
                logging.debug('Event Bus not ready yet, got %d status code.', status)
            except Exception:
                logging.debug('Event Bus not ready, could not reach yet.')
            if time.monotonic() - start > HEALTHCHECK_DELAY:
                logging.error(
                    'Event Bus not ready for %d seconds, aborting.', HEALTHCHECK_DELAY
                )
                sys.exit(1)
            time.sleep(EVENTBUS_WARMUP_DELAY)
        return [bus]
    return []


def start_services(conf: Dict[str, Any]) -> List[Any]:
    """Lookup core services and start them."""
    services = []
    for entry in conf['services']:
        services += parse_and_start(_expand(entry), SERVICE_MANIFEST)
    return services


def start_plugins(conf: Dict[str, Any]) -> List[Any]:
    """Lookup plugins and start them."""
    if disabled := conf.get('disabled'):
        disabled = [plugin.lower() for plugin in disabled]
    plugins = []
    for entry in conf['plugins']:
        plugins += parse_and_start(_expand(entry), PLUGIN_MANIFEST, disabled)
    return plugins


def configure_sshee(pools: Dict[str, Any]) -> None:
    """Configure pools."""
    try:
        logging.info('Configuring SSH channel plugin.')
        with open(SSHCHANNEL_CONFIG, 'r', encoding='utf-8') as manifest:
            config = yaml.safe_load(manifest)
        config['pools'] = pools
        aio = [ctx for ctx in config['contexts'] if ctx.get('name') == DEFAULT_CONTEXT]
        if len(aio) != 1:
            logging.error(
                'Could not find \'%s\' context for SSH channel plugin.', DEFAULT_CONTEXT
            )
            sys.exit(1)
        aio[0]['context']['targets'] = list(pools)
        with open(SSHCHANNEL_CONFIG, 'w', encoding='utf-8') as manifest:
            yaml.safe_dump(config, manifest)
    except Exception as err:
        logging.error('Error while configuring SSH channel plugin.')
        logging.error(err)
        sys.exit(1)


def configure_pools() -> None:
    """Configure pools."""
    pools_defined = False
    if pools_definition := os.environ.get('SSH_CHANNEL_POOLS'):
        logging.info('Reading pools definition %s...', pools_definition)
        try:
            with open(pools_definition, 'r', encoding='utf-8') as manifest:
                pools = yaml.safe_load(manifest)
                if 'pools' not in pools:
                    logging.error(
                        'Pools definition \'%s\' needs a \'pools\' entry.',
                        pools_definition,
                    )
                pools = pools['pools']
            pools_defined = True
        except Exception as err:
            logging.error(
                'Could not read specified pools definition \'%s\'.', pools_definition
            )
            logging.error(err)
            sys.exit(1)
    else:
        pools = {}

    if (
        os.environ.get('SSH_CHANNEL_HOST')
        and os.environ.get('SSH_CHANNEL_USER')
        and os.environ.get('SSH_CHANNEL_TAGS')
        and os.environ.get('SSH_CHANNEL_PASSWORD')
    ):
        logging.info('Configuring execution environment from SSH_CHANNEL_*...')
        agent = {
            'host': os.environ.get('SSH_CHANNEL_HOST'),
            'port': int(os.environ.get('SSH_CHANNEL_PORT', '22')),
            'username': os.environ.get('SSH_CHANNEL_USER'),
            'password': os.environ.get('SSH_CHANNEL_PASSWORD'),
            'tags': os.environ.get('SSH_CHANNEL_TAGS').split(','),
            'missing_host_key_policy': 'auto-add',
            'script_path': '/tmp',
        }
        pools['agents'] = [agent] + pools.get('agents', [])
        pools_defined = True
    elif (
        os.environ.get('SSH_CHANNEL_HOST')
        or os.environ.get('SSH_CHANNEL_USER')
        or os.environ.get('SSH_CHANNEL_TAGS')
        or os.environ.get('SSH_CHANNEL_PASSWORD')
    ):
        logging.error('Incomplete execution environment specification.')
        if not os.environ.get('SSH_CHANNEL_HOST'):
            logging.error('SSH_CHANNEL_HOST not provided')
        if not os.environ.get('SSH_CHANNEL_USER'):
            logging.error('SSH_CHANNEL_USER not provided')
        if not os.environ.get('SSH_CHANNEL_TAGS'):
            logging.error('SSH_CHANNEL_TAGS not provided')
        if not os.environ.get('SSH_CHANNEL_PASSWORD'):
            logging.error('SSH_CHANNEL_PASSWORD not provided')
        sys.exit(1)

    if pools_defined:
        configure_sshee(pools)


def maybe_generate_token() -> None:
    """Generate token if no trusted keys defined."""
    if not os.path.exists(TRUSTEDKEYS_PATH):
        os.makedirs(TRUSTEDKEYS_PATH)
    if public_key := os.environ.get('PUBLIC_KEY'):
        logging.debug('Using provided PUBLIC_KEY.')
        with open(
            os.path.join(TRUSTEDKEYS_PATH, TRUSTED_KEYS_FILE), 'w', encoding='utf-8'
        ) as key:
            key.write(public_key)
    if not os.listdir(TRUSTEDKEYS_PATH):
        # generate a JWT token
        token, pub = _generate_token()
        logging.info('Creating temporary JWT token')
        logging.info(token)
        with open(
            os.path.join(TRUSTEDKEYS_PATH, TRUSTED_KEYS_FILE), 'w', encoding='utf-8'
        ) as key:
            key.write(pub)


def wait_for_observer():
    """Wait for observer subscription."""
    start = time.monotonic()
    while True:
        try:
            subs = requests.get(get_eventbus_endpoint())
            if subs.status_code == 200:
                for _, manifest in subs.json()['items'].items():
                    if manifest['metadata']['name'] == 'observer':
                        return
            logging.debug('Observer not ready, got %d status code.', subs.status_code)
        except Exception:
            logging.debug('Observer not ready, not subscribed yet.')
        if time.monotonic() - start > HEALTHCHECK_DELAY:
            logging.error(
                'Observer not ready for %d seconds, aborting.', HEALTHCHECK_DELAY
            )
            sys.exit(1)
        time.sleep(EVENTBUS_WARMUP_DELAY)


########################################################################
# Main


def main():
    """Starting all services, as defined in ./squashtf.yaml, waiting."""
    try:
        logging.info(
            'OpenTestFactory orchestrator version: %s', version('opentf-orchestrator')
        )
    except:
        pass
    logging.info(
        'OpenTestFactory python-toolkit version: %s', version('opentf-toolkit')
    )
    dump_environment()
    logging.info(
        'Reading OpenTestFactory Launcher Manifest \'%s\' ...', OPENTF_MANIFEST
    )
    try:
        with open(OPENTF_MANIFEST, 'r', encoding='utf-8') as manifest:
            conf = yaml.safe_load(manifest)
    except Exception as err:
        logging.error('Reading SquashTF manifest failed: %s.', str(err))
        sys.exit(1)

    logging.info('Checking Configuration...')
    maybe_generate_token()
    configure_pools()

    running = []
    logging.info('Preparing EventBus...')
    running += maybe_start_eventbus(conf)

    services_idx = len(running)
    logging.info('Starting Core Services...')
    running += start_services(conf)
    wait_for_observer()
    plugins_idx = len(running)
    logging.info('Starting Plugins...')
    running += start_plugins(conf)

    logging.info('OpenTestFactory Orchestrator Ready.')
    if services_idx:
        logging.info('  Started eventbus.')
    else:
        logging.info('  (Eventbus already exists.)')
    logging.info('  Started %d core services.', plugins_idx - services_idx)
    logging.info('  Started %d plugins.', len(running) - plugins_idx)
    write_init_file()
    try:
        while True:
            time.sleep(HEALTHCHECK_DELAY)
            if any(item.poll() is not None for item in running):
                logging.error('At least one service or plugin failed, aborting:')
                for item in running:
                    if item.poll():
                        logging.error(
                            '  %s failed with return code %s',
                            str(item.args),
                            str(item.returncode),
                        )
                for item in running:
                    item.terminate()
                sys.exit(1)
    except KeyboardInterrupt:
        logging.info('Shutting down core services and plugins.')
        for item in running:
            item.terminate()
        sys.exit(0)


if __name__ == '__main__':
    main()
