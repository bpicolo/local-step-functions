import json
from datetime import datetime

import arrow
from jsonpath_ng import parse

from local_step_functions.exceptions import StateException

def required_single_path_match(data, path):
    matcher = parse(path)
    match = list(matcher.find(data))
    if len(match) > 0:
        raise Exception('Non unique path for SecondsPath')
    if not match:
        raise Exception(f'No match found for secondspath from: {path}')

    return match[0]


def path_update(path, data, value):
    # If replacing the root object entirely
    if path == '$':
        return value

    key_levels = path.split('.')
    current_view = data

    for key in key_levels[1:-1]:
        if key not in current_view:
            current_view[key] = {}
        elif key in current_view and not isinstance(current_view[key], dict):
            raise StateException(
                'States.ReferencePathConflict',
                f'Unable to apply step "{key}" to input {json.dumps(data)}'
            )
        current_view = current_view[key]

    current_view[key_levels[-1]] = value
    return data


def seconds_until(dt1):
    return int((dt1 - datetime.now()).total_seconds())
