# Copyright 2021, 2022 Henix, henix.fr
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

"""opentf-ctl"""

import sys

import jwt

from opentf.tools.ctlcommons import (
    _is_command,
    _error,
    _warning,
    _get_columns,
    _emit_csv,
)
from opentf.tools.ctlconfig import (
    read_configuration,
    config_cmd,
    print_config_help,
)
from opentf.tools.ctlnetworking import (
    _eventbus,
    _agentchannel,
    _observer,
    _get,
    _delete,
)
from opentf.tools.ctlworkflows import print_workflow_help, workflow_cmd


########################################################################

# pylint: disable=broad-except


########################################################################
# Help messages

GENERAL_HELP = '''opentf-ctl controls the OpenTestFactory orchestrators.

Basic Commands:
  get workflows                    List active and recent workflows
  run workflow {filename}          Start a workflow
  get workflow {workflow_id}       Get a workflow status
  kill workflow {workflow_id}      Cancel a running workflow

Agent Commands:
  get agents                       List registered agents
  delete agent {agent_id}          De-register an agent

Channel commands:
  get channels                     List known channels

Qualitygate Commands:
  get qualitygate {workflow_id}    Get qualitygate status for a workflow

Token Commands:
  generate token using {key}       Interactively generate a signed token
  check token {token} using {key}  Check if token signature matches public key
  view token {token}               Show token payload

Advanced Commands:
  get subscriptions                List active subscriptions

Other Commands:
  config                           Modify current opentf-tools configuration
  version                          List the tools version

Usage:
  opentf-ctl <command> [options]

Use "opentf-ctl <command> --help" for more information about a given command.
Use "opentf-ctl options" for a list of global command-line options (applies to all commands).
'''

OPTIONS_HELP = '''
The following environment variables override the defaults, if not overridden by options:

  OPENTF_CONFIG: Path to the opentfconfig file to use for CLI requests
  OPENTF_TOKEN: Bearer token for authentication to the orchestrator

The following options can be passed to any command:

  --token='': Bearer token for authentication to the orchestrator
  --user='': The name of the opentfconfig user to use
  --orchestrator='': The name of the opentfconfig orchestrator to use
  --context='': The name of the opentfconfig context to use
  --insecure-skip-tls-verify=false: If true, the server's certificate will not be checked for validity.  This will make your HTTPS connections insecure
  --opentfconfig='': Path to the opentfconfig file to use for CLI requests
'''

VERSION_HELP = '''
List the tools version

Example:
  # Display the version of the tools
  opentf-ctl version

Usage:
  opentf-ctl version [options]

Use "opentf-ctl options" for a list of global command-line options (applies to all commands).
'''

GET_SUBSCRIPTIONS_HELP = '''List active subscriptions on the eventbus

Example:
  # List the subscriptions
  opentf-ctl get subscriptions

  # List the subscriptions with more details
  opentf-ctl get subscriptions --output=wide

  # Get just the subscription names and IDs
  opentf-ctl get subscriptions --output=custom-columns=NAME:.metadata.name,ID:.metadata.subscription_id

Options:
  --output=wide or -o wide: show additional information.
  --output=custom-columns= or -o custom-columns=: show specified information.

Usage:
  opentf-ctl get subscriptions [options]

Use "opentf-ctl options" for a list of global command-line options (applies to all commands).
'''

GET_CHANNELS_HELP = '''List known channels

Example:
  # List the channels
  opentf-ctl get channels

  # List the channels with more details
  opentf-ctl get channels --output=wide

Options:
  --output=wide or -o wide: show additional information.
  --output=custom-columns= or -o custom-columns=: show specified information.

Usage:
  opentf-ctl get channels [options]

Use "opentf-ctl options" for a list of global command-line options (applies to all commands).
'''

GET_AGENTS_HELP = '''List registered agents

Example:
  # List the agents
  opentf-ctl get agents

  # List the agents with more details
  opentf-ctl get agents --output=wide

  # Get just the agent IDs
  opentf-ctl get agents --output=custom-columns=ID:.metadata.agent_id

Options:
  --output=wide or -o wide: show additional information.
  --output=custom-columns= or -o custom-columns=: show specified information.

Usage:
  opentf-ctl get agents [options]

Use "opentf-ctl options" for a list of global command-line options (applies to all commands).
'''

DELETE_AGENT_HELP = '''De-register an active agent

Example:
  # De-register the specified agent
  opentf-ctl delete agent 9ea3be45-ee90-4135-b47f-e66e4f793383

Usage:
  opentf-ctl delete agent AGENT_ID [options]

Use "opentf-ctl options" for a list of global command-line options (applies to all commands).
'''

GENERATE_TOKEN_HELP = '''Generate a signed token

Example:
  # Generate token interactively
  opentf-ctl generate token using path/to/private.pem

Usage:
  opentf-ctl generate token using NAME [options]

Use "opentf-ctl options" for a list of global command-line options (applies to all commands).
'''

VIEW_TOKEN_HELP = '''View token payload

Example:
  # Display token payload
  opentf-ctl view token $TOKEN

Usage:
  opentf-ctl view token TOKEN [options]

Use "opentf-ctl options" for a list of global command-line options (applies to all commands).
'''

VALIDATE_TOKEN_HELP = '''Validate token signature

Example:
  # Validate token
  opentf-ctl check token $TOKEN using path/to/public.pum

Usage:
  opentf-ctl check token TOKEN using NAME [options]

Use "opentf-ctl options" for a list of global command-line options (applies to all commands).
'''


########################################################################
# Eventbus


SUBSCRIPTION_COLUMNS = (
    'NAME:.metadata.name',
    'ENDPOINT:.spec.subscriber.endpoint',
    'CREATION:.metadata.creationTimestamp',
    'COUNT:.status.publicationCount',
    'SUBSCRIPTIONS:.metadata.annotations',
)

WIDE_SUBSCRIPTION_COLUMNS = (
    'ID:.metadata.subscription_id',
    'NAME:.metadata.name',
    'ENDPOINT:.spec.subscriber.endpoint',
    'CREATION:.metadata.creationTimestamp',
    'COUNT:.status.publicationCount',
    'SUBSCRIPTIONS:.metadata.annotations',
)


def _generate_subscription_row(manifest, columns):
    row = []
    for item in columns:
        field = item.split(':')[1]
        if field == '.metadata.subscription_id':
            row.append(manifest['metadata'].get('subscription_id', ''))
        if field == '.metadata.name':
            row.append(manifest['metadata']['name'])
        if field == '.metadata.creationTimestamp':
            row.append(manifest['metadata'].get('creationTimestamp', ''))
        if field == '.spec.subscriber.endpoint':
            row.append(manifest['spec']['subscriber']['endpoint'])
        if field == '.status.publicationCount':
            row.append(manifest['status']['publicationCount'])
        if field == '.metadata.annotations':
            row.append(':'.join(manifest['metadata']['annotations'].values()))
    return row


def _generate_subscriptions_rows(data, columns):
    for _, manifest in data.items():
        yield _generate_subscription_row(manifest, columns)


def list_subscriptions():
    """List all active subscriptions.

    Outputs information in CSV format (using ',' as a column delimiter).

    # Raised exceptions

    Abort with an error code 1 if the orchestrator replied with a non-ok
    code.

    Abort with an error code 2 if another error occurred.
    """
    what = _get(_eventbus(), '/subscriptions', 'Could not get subscriptions list')

    columns = _get_columns(WIDE_SUBSCRIPTION_COLUMNS, SUBSCRIPTION_COLUMNS)
    _emit_csv(_generate_subscriptions_rows(what['items'], columns), columns)


# Channels

CHANNEL_COLUMNS = (
    'NAME:.metadata.name',
    'NAMESPACES:.metadata.namespaces',
    'TAGS:.spec.tags',
    'LAST_REFRESH_TIMESTAMP:.status.lastCommunicationTimestamp',
    'STATUS:.status.phase',
)

WIDE_CHANNEL_COLUMNS = (
    'HANDLER_ID:.metadata.channelhandler_id',
    'NAME:.metadata.name',
    'NAMESPACES:.metadata.namespaces',
    'TAGS:.spec.tags',
    'LAST_REFRESH_TIMESTAMP:.status.lastCommunicationTimestamp',
    'STATUS:.status.phase',
)


def _generate_channel_row(manifest, columns):
    row = []
    for item in columns:
        field = item.split(':')[1]
        if field == '.metadata.name':
            row.append(manifest['metadata']['name'])
        if field == '.metadata.namespaces':
            row.append(':'.join(manifest['metadata']['namespaces'].split(',')))
        if field == '.spec.tags':
            row.append(':'.join(manifest['spec']['tags']))
        if field == '.status.lastCommunicationTimestamp':
            row.append(manifest['status']['lastCommunicationTimestamp'][:22])
        if field == '.status.phase':
            row.append(manifest['status']['phase'])
        if field == '.status.currentJobID':
            row.append(manifest['status']['currentJobID'])
        if field == '.metadata.channelhandler_id':
            row.append(manifest['metadata']['channelhandler_id'])
    return row


def _generate_channels_rows(data, columns):
    for manifest in data:
        yield _generate_channel_row(manifest, columns)


def list_channels():
    """List all active agents.

    Outputs information in CSV format (using ',' as a column delimiter).

    # Raised exceptions

    Abort with an error code 1 if the orchestrator replied with a non-ok
    code.

    Abort with an error code 2 if another error occurred.
    """
    what = _get(_observer(), '/channels', 'Could not get channels list')

    columns = _get_columns(WIDE_CHANNEL_COLUMNS, CHANNEL_COLUMNS)
    _emit_csv(_generate_channels_rows(what['details']['items'], columns), columns)


# Agents

AGENT_COLUMNS = (
    'AGENT_ID:.metadata.agent_id',
    'NAME:.metadata.name',
    'NAMESPACES:.metadata.namespaces',
    'TAGS:.spec.tags',
    'REGISTRATION_TIMESTAMP:.metadata.creationTimestamp',
    'LAST_SEEN_TIMESTAMP:.status.lastCommunicationTimestamp',
    'RUNNING_JOB:.status.currentJobID',
)


def _generate_agent_row(manifest, columns):
    # apiVersion: opentestfactory.org/v1alpha1
    # kind: AgentRegistration
    # metadata:
    #   creationTimestamp': 2021-12-03T17:52:36.335360
    #   name: test agent
    #   namespaces: a,b
    #   agent_id: id
    # spec:
    #   encoding: utf-8
    #   script_path': '/where/to/put/scripts'
    #   tags: ['windows', 'robotframework']
    # status:
    #   communicationCount: 0
    #   communicationStatusSummary: {}
    #   lastCommunicationTimestamp: '2021-12-03T17:53:41.560939'
    #   currentJobID: currently running job ID or None if idle
    row = []
    for item in columns:
        field = item.split(':')[1]
        if field == '.metadata.name':
            row.append(manifest['metadata']['name'])
        if field == '.metadata.agent_id':
            row.append(manifest['metadata']['agent_id'])
        if field == '.metadata.namespaces':
            row.append(':'.join(manifest['metadata']['namespaces'].split(',')))
        if field == '.metadata.creationTimestamp':
            row.append(manifest['metadata']['creationTimestamp'])
        if field == '.spec.tags':
            row.append(':'.join(manifest['spec']['tags']))
        if field == '.status.lastCommunicationTimestamp':
            row.append(manifest['status']['lastCommunicationTimestamp'][:22])
        if field == '.status.currentJobID':
            row.append(manifest['status'].get('currentJobID', ''))
    return row


def _generate_agents_rows(data, columns):
    # pre-2022-05 orchestrators where returning a dictionary, not a list
    # of manifests.
    if isinstance(data, dict):
        for agent_id, manifest in data.items():
            manifest['metadata']['agent_id'] = agent_id
            yield _generate_agent_row(manifest, columns)
    else:
        for manifest in data:
            yield _generate_agent_row(manifest, columns)


def list_agents():
    """List all active agents.

    Outputs information in CSV format (using ',' as a column delimiter).

    # Raised exceptions

    Abort with an error code 1 if the orchestrator replied with a non-ok
    code.

    Abort with an error code 2 if another error occurred.
    """
    what = _get(_agentchannel(), '/agents', 'Could not get agents list')

    columns = _get_columns(AGENT_COLUMNS, AGENT_COLUMNS)
    _emit_csv(_generate_agents_rows(what['items'], columns), columns)


def delete_agent(agent_id):
    """Deregister agent."""
    what = _delete(
        _agentchannel(), f'/agents/{agent_id}', f'Could not delete agent {agent_id}'
    )
    print(what['message'])


## JWT tokens

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


def generate_token(privatekey):
    """Generate JWT token.

    # Required parameters

    - privatekey: a non-empty string (a file name)

    # Raised exceptions

    Abort with an error code 2 if something went wrong.
    """
    try:
        with open(privatekey, 'r', encoding='utf-8') as keyfile:
            pem = keyfile.read()
    except FileNotFoundError:
        _error('The specified private key could not be found: %s.', privatekey)
        sys.exit(2)

    algorithm = (
        input('Please specify an algorithm (RS512 if unspecified): ').strip() or 'RS512'
    )
    print('The specified algorithm is:', algorithm)
    while not (
        issuer := input(
            'Please enter the issuer (your company or department): '
        ).strip()
    ):
        _warning('The issuer cannot be empty.')
    while not (
        subject := input(
            'Please enter the subject (you or the person you are making this token for): '
        )
    ):
        _warning('The subject cannot be empty.')

    try:
        token = jwt.encode({'iss': issuer, 'sub': subject}, pem, algorithm=algorithm)
    except NotImplementedError:
        _error('Algorithm not supported: %s.', algorithm)
        sys.exit(2)
    except Exception as err:
        _error('Could not generate token: %s.', err)
        sys.exit(2)

    print('The signed token is:')
    print(token)


def view_token(token):
    """View JWT token payload.

    # Required parameters

    - token: a non-empty string (a JWT token)

    # Raised exceptions

    Abort with an error code 2 if something went wrong.
    """
    try:
        payload = jwt.decode(token, options={"verify_signature": False})
        print('The token payload is:')
        print(payload)
    except Exception as err:
        _error('The specified token is invalid: %s', err)
        print(token)
        sys.exit(2)


def check_token(token, keyname):
    """Check JWT token signature.

    # Required parameters

    - token: a non-empty string (a JWT token)
    - keyname: a non-empty string (a file name)

    # Raised exceptions

    Abort with an error code 2 if something went wrong.
    """
    try:
        with open(keyname, 'r', encoding='utf-8') as keyfile:
            key = keyfile.read()
    except FileNotFoundError:
        _error('The specified public key could not be found: %s.', keyname)
        sys.exit(2)

    try:
        payload = jwt.decode(token, key, algorithms=ALLOWED_ALGORITHMS)
        print(
            f'The token is signed by the {keyname} public key.  The token payload is:'
        )
        print(payload)
    except jwt.exceptions.InvalidSignatureError:
        _error('The token is not signed by %s.', keyname)
        sys.exit(102)
    except AttributeError as err:
        _error(
            'The specified key does not looks like a public key.'
            + '  Got "%s" while reading the provided key.',
            err,
        )
        sys.exit(2)
    except ValueError as err:
        _error(err.args[0])
        sys.exit(2)
    except Exception as err:
        _error('Could not validate token signature: %s.', err)
        sys.exit(2)


def get_tools_version():
    """
    Prints in the console the current version details.
    """

    from importlib.metadata import version
    from pkg_resources import parse_version

    fullversion = parse_version(version('opentf-tools'))
    major = fullversion.base_version.split('.')[0]
    minor = fullversion.base_version.split('.')[1]
    print(
        f'Tools Version: version.Info{{Major:"{major}", Minor: "{minor}", FullVersion: "{fullversion}"}}'
    )


########################################################################
# Helpers


def print_help(args):
    """Display help."""
    if _is_command('options', args):
        print(OPTIONS_HELP)
    if _is_command('version', args):
        print(VERSION_HELP)
    elif _is_command('get subscriptions', args):
        print(GET_SUBSCRIPTIONS_HELP)
    elif _is_command('generate token', args):
        print(GENERATE_TOKEN_HELP)
    elif _is_command('view token', args):
        print(VIEW_TOKEN_HELP)
    elif _is_command('check token', args):
        print(VALIDATE_TOKEN_HELP)
    elif _is_command('get agents', args):
        print(GET_AGENTS_HELP)
    elif _is_command('get channels', args):
        print(GET_CHANNELS_HELP)
    elif _is_command('delete agent', args):
        print(DELETE_AGENT_HELP)
    elif _is_command('config', args):
        print_config_help(args)
    elif (
        _is_command('_ workflow', args)
        or _is_command('_ workflows', args)
        or _is_command('get qualitygate', args)
    ):
        print_workflow_help(args)
    elif len(args) == 2:
        print(GENERAL_HELP)
    else:
        _error('Unknown command.  Use --help to list known commands.')
        sys.exit(1)


########################################################################
# Main


def main():
    """Process command."""
    if len(sys.argv) == 1:
        print(GENERAL_HELP)
        sys.exit(1)
    if sys.argv[-1] == '--help':
        print_help(sys.argv)
        sys.exit(0)

    if _is_command('options', sys.argv):
        print(OPTIONS_HELP)
        sys.exit(0)

    if _is_command('version', sys.argv):
        get_tools_version()
        sys.exit(0)

    if _is_command('generate token using _', sys.argv):
        generate_token(sys.argv[4])
        sys.exit(0)
    if _is_command('view token _', sys.argv):
        view_token(sys.argv[3])
        sys.exit(0)
    if _is_command('check token _ using _', sys.argv):
        check_token(sys.argv[3], sys.argv[5])
        sys.exit(0)

    if _is_command('get subscriptions', sys.argv):
        read_configuration()
        list_subscriptions()
    elif _is_command('get agents', sys.argv):
        read_configuration()
        list_agents()
    elif _is_command('get channels', sys.argv):
        read_configuration()
        list_channels()
    elif _is_command('delete agent _', sys.argv):
        read_configuration()
        delete_agent(sys.argv[3])
    elif (
        _is_command('_ workflow', sys.argv)
        or _is_command('_ workflows', sys.argv)
        or _is_command('get qualitygate', sys.argv)
    ):
        workflow_cmd()
    elif _is_command('config', sys.argv):
        config_cmd()
    else:
        _error('Unknown command.  Use --help to list known commands.')
        sys.exit(1)


if __name__ == '__main__':
    main()
