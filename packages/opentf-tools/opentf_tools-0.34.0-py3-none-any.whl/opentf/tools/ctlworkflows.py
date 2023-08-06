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

import json
import os
import sys

from time import sleep

import yaml

from opentf.tools.ctlcommons import (
    _is_command,
    _get_value,
    _get_columns,
    _emit_csv,
    _ensure_uuid,
    _error,
    _warning,
    _debug,
)
from opentf.tools.ctlconfig import read_configuration
from opentf.tools.ctlnetworking import (
    _observer,
    _receptionist,
    _killswitch,
    _qualitygate,
    _get,
    _delete,
    _post,
)


########################################################################

# pylint: disable=broad-except

DEFAULT_COLUMNS = (
    'WORKFLOW_ID:.metadata.workflow_id',
    'STATUS:.details.status',
    'NAME:.metadata.name',
)
WIDE_COLUMNS = (
    'WORKFLOW_ID:.metadata.workflow_id',
    'STATUS:.details.status',
    'FIRST_SEEN_TIMESTAMP:.metadata.creationTimestamp',
    'NAME:.metadata.name',
)


WATCHED_EVENTS = (
    'ExecutionCommand',
    'ExecutionResult',
    'ExecutionError',
    'ProviderCommand',
    'GeneratorCommand',
)

AUTOVARIABLES_PREFIX = 'OPENTF_RUN_'

WARMUP_DELAY = 5
REFRESH_DELAY = 10


########################################################################
# Help messages

RUN_WORKFLOW_HELP = '''Start a workflow

Examples:
  # Start the workflow defined in my_workflow.yaml
  opentf-ctl run workflow my_workflow.yaml

  # Start the workflow and wait until it completes
  opentf-ctl run workflow my_workflow.yaml --wait

  # Start the workflow and define an environment variable
  opentf-ctl run workflow my_workflow.yaml -e TARGET=example.com

  # Start a workflow and provide environment variables defined in a file
  opentf-ctl run workflow my_workflow.yaml -e variables

  # Start a workflow and provide a localy-defined environment variable
  export OPENTF_RUN_MYVAR=my_value
  opentf-ctl run workflow my_workflow.yaml  # variable 'MYVAR' will be defined

  # Start the wokflow and provide a local file
  opentf-ctl run workflow my_workflow.yaml -f key=./access_key.pem

Environment variables:
  Environment variables with an 'OPENTF_RUN_' prefix will be defined without the prefix in the workflow and while running commands in execution environment.

Options:
  -e var=value: 'var' will be defined in the workflow and while running commands in execution environment.
  -e path/to/file: variables defined in file will be defined in the workflow and while running commands in execution environment.  'file' must contain one variable definition per line, of the form 'var=value'.
  -f name=path/to/file: the specified local file will be available for use by the workflow.  'name' is the file name specified in the `resources.files` part of the workflow.
  --wait: wait for workflow completion.
  --step_depth=1: show nested steps to the given depth (only used with --wait).
  --job_depth=1: show nested jobs to the given depth (only used with --wait).

Usage:
  opentf-ctl run workflow NAME [-e var=value]... [-e path/to/file] [-f name=path/to/file]... [--wait] [--job_depth=value] [--step_depth=value] [options]

Use "opentf-ctl options" for a list of global command-line options (applies to all commands).
'''

GET_WORKFLOW_HELP = '''Get a workflow status

Examples:
  # Get the current status of a workflow
  opentf-ctl get workflow 9ea3be45-ee90-4135-b47f-e66e4f793383

  # Get the status of a workflow and wait until its completion
  opentf-ctl get workflow 9ea3be45-ee90-4135-b47f-e66e4f793383 --watch

  # Get the status of a workflow, showing first-level nested steps
  opentf-ctl get workflow 9ea3be45-ee90-4135-b47f-e66e4f793383 --step_depth=2

Options:
  --step_depth=1: show nested steps to the given depth.
  --job_depth=1: show nested jobs to the given depth.
  --watch: wait until workflow completion or cancellation, displaying status updates as they occur.
  --output=format or -o format: show information in specified format (json or yaml)

Usage:
  opentf-ctl get workflow WORKFLOW_ID [--step_depth=value] [--job_depth=value] [--watch] [options]

Use "opentf-ctl options" for a list of global command-line options (applies to all commands).
'''

GET_QUALITYGATE_HELP = '''Get qualitygate status for a workflow

Examples:
  # Get the current qualitygate status of a workflow
  opentf-ctl get qualitygate 9ea3be45-ee90-4135-b47f-e66e4f793383

  # Get the qualitygate status of a workflow for a specific mode
  opentf-ctl get qualitygate 9ea3be45-ee90-4135-b47f-e66e4f793383 --mode=strict

Options:
  --mode=strict|passing|...: use the specific qualitygate mode

Usage:
  opentf-ctl get qualitygate WORKFLOW_ID [--mode=mode] [options]

Use "opentf-ctl options" for a list of global command-line options (applies to all commands).
'''

GET_WORKFLOWS_HELP = '''List active and recent workflows

Examples:
  # List the IDs of active and recent workflows
  opentf-ctl get workflows

  # Get the status of active and recent workflows
  opentf-ctl get workflows --output=wide

  # Get just the workflow IDs of active and recent workflows
  opentf-ctl get workflows --output=custom-columns=ID:.metadata.workflow_id

Options:
  --output=wide or -o wide: show additional information.
  --output=custom-columns= or -o custom-columns=: show specified information.

Usage:
  opentf-ctl get workflows [--output=wide] [options]

Use "opentf-ctl options" for a list of global command-line options (applies to all commands).
'''

KILL_WORKFLOW_HELP = '''Kill a running workflow

Example:
  # Kill the specified workflow
  opentf-ctl kill workflow 9ea3be45-ee90-4135-b47f-e66e4f793383

Usage:
  opentf-ctl kill workflow WORKFLOW_ID [options]

Use "opentf-ctl options" for a list of global command-line options (applies to all commands).
'''


########################################################################
# Helpers


def _file_not_found(name, err):
    _error('File not found: %s.', name)
    _debug('Error is: %s.', err)
    sys.exit(2)


def _read_variables_file(file, variables):
    """Read file and add variables.

    Abort with an error code 2 if the file does not exist or contains
    invalid content.
    """
    try:
        with open(file, 'r', encoding='utf-8') as varfile:
            for line in varfile:
                if '=' not in line:
                    _error(
                        'Invalid format in file %s, was expecting var=value.',
                        file,
                    )
                    sys.exit(2)
                var, _, value = line.strip().partition('=')
                variables[var] = value
    except FileNotFoundError as err:
        _file_not_found(file, err)


def _add_files(args, files):
    """Handling -f file command-line options."""
    process = False
    for option in args:
        if option == '-f':
            process = True
            continue
        if process:
            process = False
            name, path = option.split('=')
            try:
                files[name] = open(path, 'rb')
            except FileNotFoundError as err:
                _file_not_found(path, err)


def _add_variables(args, files):
    """Handling -e file and -e var=value command-line options."""
    # OPENTF_CONFIG and OPENTF_TOKEN are explicitly excluded to prevent
    # unexpected leak
    variables = {
        key[len(AUTOVARIABLES_PREFIX) :]: value
        for key, value in os.environ.items()
        if key.startswith(AUTOVARIABLES_PREFIX)
        and key not in ('OPENTF_CONFIG', 'OPENTF_TOKEN')
    }
    process = False
    for option in args:
        if option == '-e':
            process = True
            continue
        if process:
            process = False
            if '=' in option:
                var, _, value = option.partition('=')
                variables[var] = value
            else:
                _read_variables_file(option, variables)
    if variables:
        files['variables'] = '\n'.join(f'{k}={v}' for k, v in variables.items())


def _get_workflow_manifest(what):
    """Return workflow manifest.

    # Required parameters

    - what: a collection of messages.

    # Returned value

    If manifest is not found in `what`, returns `None`.
    """
    for manifest in what:
        if manifest.get('kind') == 'Workflow':
            return manifest
    return None


def _generate_row(workflow_id, response, columns):
    row = []
    for item in columns:
        field = item.split(':')[1]
        if field == '.metadata.workflow_id':
            row.append(workflow_id)
        if field == '.details.status':
            row.append(response['details']['status'])
        if field == '.metadata.name':
            if manifest := _get_workflow_manifest(response['details']['items']):
                row.append(manifest['metadata']['name'])
            else:
                row.append('')
        if field == '.metadata.creationTimestamp':
            what = response['details']['items']
            if what:
                manifest = _get_workflow_manifest(what) or what[0]
                row.append(manifest.get('metadata', {}).get('creationTimestamp', ''))
            else:
                row.append('')
    return row


def _generate_rows(workflows_ids, columns):
    for workflow_id in workflows_ids:
        response = _get_first_page(workflow_id)
        if response.status_code == 200:
            yield _generate_row(workflow_id, response.json(), columns)
        else:
            print(workflow_id, 'got response code', response.status_code)


def _handler_maybe_outdated(response):
    if response.status_code in (404, 405):
        _error('Could not get workflows list.  Maybe an outdated orchestrator version.')
        _debug('(Return code was %d.)', response.status_code)
    else:
        _error(
            'Could not get workflows list.  Return code was %d.',
            response.status_code,
        )
    sys.exit(2)


def list_workflows():
    """List active and recent workflows."""
    try:
        columns = _get_columns(WIDE_COLUMNS, DEFAULT_COLUMNS)
    except ValueError as err:
        _error('Invalid parameters: %s.', err)
        sys.exit(2)
    except Exception as err:
        _error('Could not get columns specification: %s.', err)
        sys.exit(2)

    response = _get(
        _observer(),
        '/workflows',
        'Could not get workflows list',
        handler=_handler_maybe_outdated,
    )
    workflows_ids = response['details']['items']
    _emit_csv(_generate_rows(workflows_ids, columns), columns)


def _handler_maybe_details(response):
    _error(response.json()['message'])
    if response.json().get('details'):
        _error(response.json()['details'].get('error'))
    sys.exit(1)


def run_workflow(workflow_name):
    """Run a workflow.

    # Required parameters

    - workflow_name: a file name

    # Returned value

    Returns the workflow ID if everything was OK.

    # Raised exceptions

    Abort with an error code of 1 if the workflow was not properly
    received by the orchestrator.

    Abort with an error code of 2 if a parameter was invalid (file not
    found or invalid format).
    """
    try:
        files = {'workflow': open(workflow_name, 'r', encoding='utf-8')}
        _add_files(sys.argv[4:], files)
        _add_variables(sys.argv[4:], files)

        result = _post(
            _receptionist(),
            '/workflows',
            files=files,
            statuses=(201,),
            handler=_handler_maybe_details,
        )
        print('Workflow', result['details']['workflow_id'], 'is running.')
    except FileNotFoundError as err:
        _file_not_found(workflow_name, err)
    except Exception as err:
        _error('Could not start workflow: %s.', err)
        sys.exit(2)

    if '--wait' in sys.argv:
        sleep(WARMUP_DELAY)
        get_workflow(result['details']['workflow_id'], watch=True)


def _emit_prefix(event, file=sys.stdout):
    print(
        f'[{event["metadata"].get("creationTimestamp", "")[:-7]}]',
        f'[job {event["metadata"].get("job_id", "ID not available")}] ',
        end='',
        file=file,
    )


def _emit_command(event, silent, file=sys.stdout):
    if event['metadata']['step_sequence_id'] == -1:
        _emit_prefix(event, file)
        print(
            'Requesting execution environment providing',
            event['runs-on'],
            'for job',
            repr(event['metadata']['name']),
            file=file,
        )
    elif event['metadata']['step_sequence_id'] == -2:
        _emit_prefix(event, file)
        print(
            'Releasing execution environment for job',
            repr(event['metadata']['name']),
            file=file,
        )
    elif not silent:
        _emit_prefix(event, file)
        print(' ' * (len(event['metadata'].get('step_origin', []))), end='', file=file)
        print('Running command', event['scripts'], file=file)


def _emit_result(event, silent, file=sys.stdout):
    for item in event.get('logs', []):
        _emit_prefix(event, file)
        print(item, file=file)
    if event['status'] == 0 or silent:
        return
    _emit_prefix(event, file)
    print('Status code was:', event['status'], file=file)


def _emit_executionerror(event, file):
    _emit_prefix(event, file)
    if details := event.get('details'):
        if 'error' in details:
            print('ERROR:', details['error'], flush=True, file=file)
        else:
            print('ERROR: An ExecutionError occurred:', flush=True, file=file)
            for k, v in details.items():
                print(f'{k}: {v}', flush=True, file=file)
    else:
        print(f'An ExecutionError occurred: {event}', flush=True, file=file)


def emit_event(
    kind: str,
    event,
    step_depth: int,
    job_depth: int,
    output_format,
    first: bool,
    file=sys.stdout,
):
    """Emit event.

    # Required parameters

    - kind: a string, the event kind (`Workflow`, ...)
    - event: a dictionary
    - step_depth: an integer (0 = infinite details)
    - job_depth: an integer (0 = infinite details)
    - output_format: a string or None (`json`, `yaml`, or None)
    - first: a boolean

    # Optional parameters

    - file: a stream
    """
    if output_format == 'json':
        if first:
            print('    ', end='', file=file)
        else:
            print(',\n    ', end='', file=file)
        print(
            '    '.join(json.dumps(event, indent=2).splitlines(keepends=True)),
            end='',
            file=file,
        )
        return
    if output_format == 'yaml':
        print('- ', end='', file=file)
        print(
            '  '.join(yaml.safe_dump(event).splitlines(keepends=True)),
            end='',
            file=file,
        )
        return

    if kind == 'Workflow':
        print('Workflow', event['metadata']['name'], flush=True, file=file)
        return
    if kind not in WATCHED_EVENTS:
        return
    if kind == 'ExecutionError':
        _emit_executionerror(event, file)
        return

    silent = False
    if job_depth and len(event['metadata'].get('job_origin', [])) >= job_depth:
        silent = True
    elif step_depth and len(event['metadata'].get('step_origin', [])) >= step_depth:
        silent = True

    if kind == 'ExecutionResult':
        _emit_result(event, silent, file)
    elif kind == 'ExecutionCommand':
        _emit_command(event, silent, file)
    elif not silent:
        _emit_prefix(event, file)
        print(' ' * (len(event['metadata'].get('step_origin', []))), end='', file=file)
        print('Running action', event['metadata']['name'], flush=True, file=file)


def _get_first_page(workflow_id):
    """Return a requests.Response, to get following pages if needed."""

    def _handler_unknown_workflowid(response):
        if response.status_code == 404:
            _error(
                'Could not find workflow %s.  The ID is incorrect or too recent or too old.',
                workflow_id,
            )
            sys.exit(1)
        _error(
            'Could not get workflow %s.  Got status code %d (%s).',
            workflow_id,
            response.status_code,
            response.text,
        )
        sys.exit(1)

    return _get(
        _observer(),
        f'/workflows/{workflow_id}/status',
        handler=_handler_unknown_workflowid,
        raw=True,
    )


def _get_outputformat(allowed):
    output_format = _get_value('--output=') or _get_value('-o=')
    if not output_format and '-o' in sys.argv:
        index = sys.argv.index('-o')
        if index < len(sys.argv) - 1:
            output_format = sys.argv[index + 1]
        else:
            _error(
                'Missing value for option "-o" (was expecting %s).', ', '.join(allowed)
            )
            sys.exit(-2)
    if output_format and output_format not in allowed:
        _error(
            'Unexpected output format specified: %s (was expecting %s).',
            output_format,
            ', '.join(allowed),
        )
        sys.exit(2)
    return output_format


def _get_workflow_events(workflow_id, watch):
    current_item = 0
    response = _get_first_page(workflow_id)
    current_page = _observer() + f'/workflows/{workflow_id}/status?page_size'

    while True:
        status = response.json()
        for event in status['details']['items'][current_item:]:
            yield event

        if 'next' in response.links:
            current_item = 0
            current_page = response.links['next']['url']
            response = _get(current_page, raw=True)
            continue

        if not watch:
            break
        if response.json()['details']['status'] != 'RUNNING':
            break

        current_item = len(status['details']['items'])
        while len(status['details']['items']) <= current_item:
            sleep(REFRESH_DELAY)
            response = _get(current_page, raw=True)
            status = response.json()
            if len(status['details']['items']) != current_item:
                break
            if 'next' in response.links:
                break


def get_workflow(workflow_id, watch=False):
    """Get a workflow.

    # Required parameters

    - workflow_id: a string

    # Optional parameters

    - watch: a boolean (False by default)

    # Returned value

    The current workflow status.

    # Raised exceptions

    Abort with an error code 1 if the workflow could not be found on the
    orchestrator.

    Abort with an error code 2 if another error occurred.
    """
    _ensure_uuid(workflow_id)

    cancelation_event = None
    job_depth = int(_get_value('--job-depth=') or 1)
    step_depth = int(_get_value('--step-depth=') or 1)
    output_format = _get_outputformat(allowed=('yaml', 'json'))
    first = True

    if output_format == 'json':
        print('{\n  "items": [')
    elif output_format == 'yaml':
        print('items:')

    for event in _get_workflow_events(workflow_id, watch):
        kind = event.get('kind')
        if kind == 'WorkflowCanceled':
            cancelation_event = event
        emit_event(
            kind,
            event,
            job_depth=job_depth,
            step_depth=step_depth,
            output_format=output_format,
            first=first,
        )
        first = False

    status = _get_first_page(workflow_id).json()

    if output_format == 'json':
        print('\n  ],\n  "status":', json.dumps(status['details']['status']))
        print('}')
        return
    if output_format == 'yaml':
        yaml.safe_dump({'status': status['details']['status']}, sys.stdout)
        return

    workflow_status = status['details']['status']
    if workflow_status == 'DONE':
        print('Workflow completed successfully.')
    elif workflow_status == 'RUNNING':
        print('Workflow is running.')
    elif workflow_status == 'FAILED':
        if (
            cancelation_event
            and cancelation_event.get('details', {}).get('status') == 'cancelled'
        ):
            print('Workflow cancelled.')
        else:
            print('Workflow failed.')
    else:
        _warning(
            'Unexpected workflow status: %s (was expecting DONE, RUNNING, or FAILED).',
            workflow_status,
        )


def kill_workflow(workflow_id):
    """Kill workflow.

    # Required parameter

    - workflow_id: a non-empty string (an UUID)

    # Raised exceptions

    Abort with an error code 1 if the orchestrator replied with an
    unexpected status code (!= 200).

    Abort with an error code 2 if an error occurred while contacting the
    orchestrator.
    """

    def _notknown(response):
        if response.status_code == 404:
            _error(f'Workflow {workflow_id} is not known.')
        else:
            _error(f'Could not check if workflow {workflow_id} exists.')
        _error('Could not kill workflow.')
        sys.exit(1)

    _ensure_uuid(workflow_id)

    _ = _get(_observer(), f'/workflows/{workflow_id}/status', handler=_notknown)
    _ = _delete(_killswitch(), f'/workflows/{workflow_id}')
    print(f'Killing workflow {workflow_id}.')


def get_qualitygate(workflow_id, mode):
    """Get qualitygate status.

    # Required parameter

    - workflow_id: a non-empty string (an UUID)

    # Raised exceptions

    Abort with an error code of 2 if the specified `workflow_id` is
    invalid or if an error occurred while contacting the orchestrator.

    Abort with an error code of 101 if the workflow is still running.

    Abort with an error code of 102 if the qualitygate failed.
    """
    _ensure_uuid(workflow_id)
    result = _get(
        _qualitygate(),
        f'/workflows/{workflow_id}/qualitygate?mode={mode}',
        statuses=(200, 404, 422),
    )
    if result.get('code') == 404:
        _error(
            'Unknown workflow %s.  It is either too new, too old, or the provided '
            + 'workflow ID is incorrect.  You can use "opentf-ctl get workflows" to list '
            + 'the known workflow IDs.',
            workflow_id,
        )
        sys.exit(2)
    if result.get('code') == 422:
        _error(result.get('message'))
        sys.exit(2)
    if 'details' not in result or 'status' not in result.get('details', {}):
        _error(
            'Unexpected response from qualitygate.  Was expecting a JSON object'
            + ' with a .details.status entry, got: %s',
            str(result),
        )
        sys.exit(2)
    status = result['details']['status']
    if status not in ('SUCCESS', 'NOTEST', 'FAILURE', 'RUNNING'):
        _error(
            'Unexpected status from qualitygate: %s (was expecting SUCCESS, NOTEST,'
            + ' FAILURE, or RUNNING).',
            status,
        )
        sys.exit(2)
    if status == 'RUNNING':
        print(
            f'Workflow {workflow_id} is still running.  Please retry after workflow completion.'
        )
        sys.exit(101)
    if status == 'FAILURE':
        print(f'Workflow {workflow_id} failed the qualitygate using mode {mode}.')
        sys.exit(102)
    if status == 'NOTEST':
        print(f'Workflow {workflow_id} contains no test.')
    else:
        print(
            f'Workflow {workflow_id} successfully passed the qualitygate using mode {mode}.'
        )


########################################################################
# Helpers


def print_workflow_help(args):
    """Display help."""
    if _is_command('run workflow', args):
        print(RUN_WORKFLOW_HELP)
    elif _is_command('get workflows', args):
        print(GET_WORKFLOWS_HELP)
    elif _is_command('get workflow', args):
        print(GET_WORKFLOW_HELP)
    elif _is_command('kill workflow', args):
        print(KILL_WORKFLOW_HELP)
    elif _is_command('get qualitygate', args):
        print(GET_QUALITYGATE_HELP)
    else:
        _error('Unknown command.  Use --help to list known commands.')
        sys.exit(1)


def workflow_cmd():
    """Interact with workflows."""
    if _is_command('get workflows', sys.argv):
        read_configuration()
        list_workflows()
    elif _is_command('run workflow _', sys.argv):
        read_configuration()
        run_workflow(sys.argv[3])
    elif _is_command('get workflow _', sys.argv):
        read_configuration()
        get_workflow(sys.argv[3], '--watch' in sys.argv)
    elif _is_command('kill workflow _', sys.argv):
        read_configuration()
        kill_workflow(sys.argv[3])
    elif _is_command('get qualitygate _', sys.argv):
        read_configuration()
        get_qualitygate(sys.argv[3], _get_value('--mode=') or 'strict')
    else:
        _error('Unknown command.  Use --help to list known commands.')
        sys.exit(1)
