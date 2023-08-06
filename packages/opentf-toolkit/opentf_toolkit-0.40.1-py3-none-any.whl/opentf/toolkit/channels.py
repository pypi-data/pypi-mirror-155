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

"""Toolkit helpers for channels plugins."""


import re

from opentf.commons import make_uuid
from opentf.toolkit import core

## workflow commands

SETOUTPUT_COMMAND = r'^::set-output\s+name=(\w+)::(.*)$'
ATTACH_COMMAND = r'^::attach(\s+.*?)?::(.*?)\s*$'
DEBUG_COMMAND = r'^::debug::(.*)$'
WARNING_COMMAND = r'^::warning(\s+(.*)+)?::(.*)$'
ERROR_COMMAND = r'^::error(\s+(.*)+)?::(.*)$'
STOPCOMMANDS_COMMAND = r'^::stop-commands::(\w+)$'
ADDMASK_COMMAND = r'^::add-mask::(.*)$'
PUT_FILE_COMMAND = r'^::put file=(.*?)\s*::(.*?)\s*$'


## step sequence IDs

SETUP_JOB = -1
TEARDOWN_JOB = -2
NOTIFY_JOB = -3

DEFAULT_CHANNEL_LEASE = 60  # how long to keep the offer, in seconds

## shells

# For cmd:
#
# - /D: ignore registry autorun commands
# - /E:ON: enable command extensions
# - /V:OFF: disable delayed environment expansion
# - /S: strip " quote characters from command
# - /C: run command then terminate
#
# For bash:
#
# - --noprofile: ignore /etc/profile & al.
# - --norc: ignore /etc/bash.bashrc & al.
# - -e: exit at first error
# - -o pipefail: exit if one of the commands in the pipe fails

SHELL_DEFAULT = {'linux': 'bash', 'macos': 'bash', 'windows': 'cmd'}
SHELL_TEMPLATE = {
    'bash': 'bash --noprofile --norc -eo pipefail {0}',
    'cmd': '%ComSpec% /D /E:ON /V:OFF /S /C "CALL "{0}""',
    'python': 'python {0}',
}

SCRIPTPATH_DEFAULT = {'linux': '/tmp', 'macos': '/tmp', 'windows': '%TEMP%'}
SCRIPTFILE_DEFAULT = {
    'linux': '{root}/{job_id}_{step_sequence_id}.sh',
    'macos': '{root}/{job_id}_{step_sequence_id}.sh',
    'windows': '{root}\\{job_id}_{step_sequence_id}.cmd',
}

LINESEP = {'linux': '\n', 'macos': '\n', 'windows': '\r\n'}
RUNNER_OS = {'windows', 'macos', 'linux'}

OPENTF_WORKSPACE_TEMPLATE = {
    'linux': '`pwd`/{job_id}',
    'macos': '`pwd`/{job_id}',
    'windows': '%CD%\\{job_id}',
}
OPENTF_VARIABLES_TEMPLATE = {
    'linux': '{root}/{job_id}_dynamic_env.sh',
    'macos': '{root}/{job_id}_dynamic_env.sh',
    'windows': '{root}\\{job_id}_dynamic_env.cmd',
}

## os helpers


def make_variable_linux(name, value):
    """Prepare variable declaration for linux runners."""
    if ' ' in value:
        value = f'"{value}"'
    return f'export {name}={value}'


def make_variable_windows(name, value):
    """Prepare variable declaration for windows runners."""
    return f'@set "{name}={value}"'


def add_default_variables(script, job_id, runner_os, root):
    """Prepare default variables."""
    script.append(
        VARIABLE_MAKER[runner_os](
            'OPENTF_WORKSPACE',
            OPENTF_WORKSPACE_TEMPLATE[runner_os].format(job_id=job_id),
        )
    )
    script.append(
        VARIABLE_MAKER[runner_os](
            'OPENTF_VARIABLES',
            OPENTF_VARIABLES_TEMPLATE[runner_os].format(job_id=job_id, root=root),
        )
    )
    script.append(VARIABLE_MAKER[runner_os]('OPENTF_ACTOR', 'dummy'))
    script.append(VARIABLE_MAKER[runner_os]('CI', 'true'))


def prepare_exec(command, job_id, runner_os, root):
    """..."""
    script_file = SCRIPTFILE_DEFAULT[runner_os].format(
        root=root,
        job_id=job_id,
        step_sequence_id=command['metadata']['step_sequence_id'],
    )
    shell = command.get('shell', SHELL_DEFAULT[runner_os])
    if '{0}' not in shell:
        shell = SHELL_TEMPLATE.get(shell)
    if '{0}' not in shell:
        core.error()
    return shell.format(script_file), script_file


def process_output(stdout, copy):
    """Process output, filling structures.

    # Required parameters

    - stdout: a list of strings
    - copy: a function copying a remote file to a local path

    # Returned value

    A (dictionary, list, list, dictionary) tuple.
    """

    def _sanitize(text):
        for item in masks:
            text = text.replace(item, '*' * len(item))
        return text

    attachments = []
    attachments_metadata = {}
    outputs = {}
    logs = []
    stop_command = None
    masks = set()

    for line in stdout:
        # Parsing stdout for workflow commands
        core.debug('[stdout] %s', line)
        if stop_command:
            if line == stop_command:
                stop_command = None
            continue

        if wcmd := re.match(ATTACH_COMMAND, line):
            remote = wcmd.group(2)
            try:
                rhs = remote.split('/')[-1].split('\\')[-1]
                local_uuid = make_uuid()
                local_path = f'/tmp/{local_uuid}_{rhs}'
                copy(remote, local_path)
                attachments.append(local_path)
                attachments_metadata[local_path] = {'uuid': local_uuid}
            except Exception as err:
                core.warning(f'Could not read {remote}: {err}.')
        elif wcmd := re.match(SETOUTPUT_COMMAND, line):
            outputs[wcmd.group(1)] = wcmd.group(2)
        elif wcmd := re.match(DEBUG_COMMAND, line):
            logs.append(f'DEBUG,{_sanitize(wcmd.group(1))}')
        elif wcmd := re.match(WARNING_COMMAND, line):
            logs.append(f'WARNING,{_sanitize(wcmd.group(3))}')
        elif wcmd := re.match(ERROR_COMMAND, line):
            logs.append(f'ERROR,{_sanitize(wcmd.group(3))}')
        elif wcmd := re.match(STOPCOMMANDS_COMMAND, line):
            stop_command = wcmd.group(1)
        elif wcmd := re.match(ADDMASK_COMMAND, line):
            masks.add(wcmd.group(1))

    return outputs, logs, attachments, attachments_metadata


def make_script(command, job_id, runner_os, root):
    """Prepare script."""
    script = []
    if runner_os == 'windows':
        script.append('@echo off')
        prefix = '@'
    else:
        script.append('#!/usr/bin/env bash')
        prefix = ''

    add_default_variables(script, job_id, runner_os, root)
    for name, value in command.get('variables', {}).items():
        script.append(VARIABLE_MAKER[runner_os](name, value))

    step_sequence_id = command['metadata']['step_sequence_id']
    if step_sequence_id == 0:
        script.append(f'{prefix}mkdir {job_id}')
        if runner_os != 'windows':
            script.append('touch "$OPENTF_VARIABLES"')
        else:
            script.append('@type nul >>"%OPENTF_VARIABLES%"')

    if step_sequence_id == TEARDOWN_JOB:
        script.append(
            f'rm -rf {job_id}' if runner_os != 'windows' else f'@rmdir /s/q {job_id}'
        )
        script.append(
            f'rm "{root}/{job_id}"_*.sh'
            if runner_os != 'windows'
            else f'@del /q "{root}\\{job_id}_*.cmd"'
        )
    else:
        script.append(f'{prefix}cd {job_id}')
        if runner_os == 'windows':
            script.append('call "%OPENTF_VARIABLES%"')
        else:
            script.append('. "$OPENTF_VARIABLES"')

    if 'working-directory' in command:
        path = command['working-directory']
        if runner_os == 'windows':
            path = path.replace('/', '\\')
        if ' ' in path:
            path = '"' + path.strip('"') + '"'
        script.append(f'{prefix}cd {path}')
    script += command['scripts']
    return LINESEP[runner_os].join(script)


VARIABLE_MAKER = {
    'linux': make_variable_linux,
    'macos': make_variable_linux,
    'windows': make_variable_windows,
}
