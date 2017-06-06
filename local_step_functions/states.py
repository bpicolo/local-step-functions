import time
from copy import deepcopy

import arrow
from datetime import datetime
from jsonpath_ng import parse

from .util import path_update
from .util import required_single_path_match
from .util import seconds_until

STATE_TYPES = frozenset([
    'Task',
    'Wait',
    'Pass',
    'Succeed',
    'Fail',
    'Choice',
    'Parallel'
])

# Awkward python forward-declare
STATE_TYPE_TO_RUNNER = {}


class StatesError:
    all = 'States.ALL'
    timeout = 'States.Timeout'
    failed = 'States.TaskFailed'
    permissions = 'States.Permissions'
    result_path_match_failure = 'States.ResultPathMatchFailure'
    branch_failed = 'States.BranchFailed'
    no_choice_matched = 'States.NoChoiceMatched'


class StateMachineFailure(Exception):

    def __init__(self, error, cause):
        self.error = error
        self.cause = cause


def _parse_input(schema, input_data):
    if 'InputPath' not in schema:
        return input_data

    if schema['InputPath'] is None:
        return {}

    return required_single_path_match(input_data, schema['InputPath'])


def run_state(schema, input_data):
    if schema['Type'] == 'Fail':
        return run_fail(schema, input_data)

    data = _parse_input(schema, input_data)
    output, next_state = STATE_TYPE_TO_RUNNER[schema['Type']](schema, data)

    if 'OutputPath' in schema:
        if schema['OutputPath'] is None:
            output = {}
        else:
            output = path_update(schema['OutputPath'], deepcopy(input_data), output)

    return output, next_state


def _next_state(schema):
    if schema.get('End', False) is True:
        return None

    return schema['Next']


def run_pass(schema, data):
    if 'Result' in schema:
        # if the result is None, the raw input is treated as the result
        if schema['Result'] is None:
            schema['Result'] = deepcopy(data)

        return path_update(
            schema.get('ResultPath', '$'),
            data,
            schema['Result']
        ), _next_state(schema)

    return data, _next_state(schema)


def run_wait(schema, data):
    seconds_to_wait = None
    if 'Seconds' in schema:
        seconds_to_wait = int(schema['seconds'])
    elif 'SecondsPath' in schema:
        seconds_to_wait = int(required_single_path_match(data, schema['SecondsPath']))
    elif 'Timestamp' in schema:
        seconds_to_wait = seconds_until(arrow.get(schema['Timestamp']).datetime)
    elif 'TimestampPath' in schema:
        seconds_to_wait = seconds_until(required_single_path_match(data, schema['TimestampPath']))
    else:
        raise Exception('One of Seconds, SecondsPath, Timestamp, TimestampPath required for Wait state')

    time.sleep(seconds_to_wait)

    return data, _next_state(schema)


def run_succeed(schema, data):
    return data, None


def run_fail(schema, data):
    raise StateMachineFailure(schema['error'], schema['cause'])


def run_parallel(schema, data):
    raise NotImplementedError()


STATE_TYPE_TO_RUNNER = {
    'Pass': run_pass,
    'Wait': run_wait,
    'Succeed': run_succeed,
    'Fail': run_fail
}
