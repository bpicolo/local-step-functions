import json
import os

import pytest

from tests.cases.states import pass_state_cases
from local_step_functions.states import run_pass


@pytest.mark.parametrize(
    "state,input,output",
    [
        (case['state'], case['input'], case['output'])
        for case in pass_state_cases
    ]
)
def test_pass_state(state, input, output):
    assert run_pass(state, input) == (output, None)
