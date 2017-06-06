import logging
from pprint import pformat

from local_step_functions.states import run_state
from local_step_functions.states import StateMachineFailure

log = logging.getLogger('local_step_functions.state_machine')

def run_state_machine(machine_definition, run_id, input_data):
    states = machine_definition['States']
    data = input_data

    log.info(f'Starting run: {run_id}')
    log.info('Data:')
    log.info(pformat(input_data, width=100))

    state = machine_definition['StartAt']
    while state:
        try:
            definition = states[state]
            data, state = run_state(definition, data)
        except StateMachineFailure:
            pass

    return data
