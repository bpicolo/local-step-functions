import json
import os

import pytest

from local_step_functions.runner import run_state_machine

DEFINITIONS_ROOT = os.path.dirname(os.path.realpath(__file__)) + '/definitions'


def get_definition(name):
    return json.loads(
        open(os.path.join(DEFINITIONS_ROOT, name + '.json')).read()
    )

def test_hello_world():
    assert run_state_machine(
        get_definition('hello_world'),
        1,
        {}
    ) == 'Hello World!'


def test_result_path():
    assert run_state_machine(
        get_definition('hello_world_rp'),
        1,
        {}
    ) == {'hello': 'World'}
