import json
import logging
from pprint import pformat

from local_step_functions.states import run_state
from local_step_functions.states import StateMachineFailure

log = logging.getLogger('local_step_functions.state_machine')


# TODO interstitial step state (to allow for 'activities' to be executed)
def run_state_machine(state_machine, state_machine_execution, startAt):
    machine_definition = json.loads(state_machine.definition)

    states = machine_definition['States']
    data = json.loads(state_machine_execution.data)

    log.info('ExecutionStarted')
    log.info({
        'input': state_machine_execution.data,
        'roleArn': state_machine.roleArn
    })
    state = machine_definition['StartAt']

    while state:
        try:
            definition = states[state]
            data, state = run_state(definition, data)
        except StateMachineFailure:
            # Handle failure
            pass

    return data
