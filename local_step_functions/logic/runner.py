import json
import logging
from pprint import pformat

from local_step_functions.exceptions import StateMachinePausedForTask
from local_step_functions.models.db import db
from local_step_functions.models.state_machine_step import StepStatus
from local_step_functions.models.state_machine_step import StateMachineStep
from local_step_functions.models.state_machine_execution import ExecutionStatus
from local_step_functions.states import run_state
from local_step_functions.states import StateMachineFailure
from local_step_functions.util import now_timestamp

log = logging.getLogger('local_step_functions.state_machine')


def create_step(execution, state_name, definition, input):
    step = StateMachineStep(
        state_machine_execution_id=execution.id,
        type=definition['Type'],
        input=json.dumps(input),
        output=None,
        name=state_name,
        status=StepStatus.running,
        end=definition.get('End', False),
        startDate=now_timestamp()
    )

    db.session.add(step)
    db.session.commit()

    return step


def finish_step(step, output):
    step.output = json.dumps(output)
    step.status = StepStatus.succeeded
    step.stopDate = now_timestamp()
    db.session.commit()


def run_state_machine(state_machine, state_machine_execution, last_step):
    machine_definition = json.loads(state_machine.definition)

    states = machine_definition['States']
    data = json.loads(state_machine_execution.data)

    log.info('ExecutionStarted')
    log.info({
        'input': state_machine_execution.data,
        'roleArn': state_machine.roleArn
    })

    state_name = machine_definition['StartAt']
    if last_step is not None:
        # means we had paused to do an activity
        state_name = machine_definition[last_step_name]['Next']

    while state_name:
        definition = states[state_name]
        try:
            step = create_step(
                state_machine_execution,
                state_name,
                definition,
                data
            )
            data, state_name = run_state(definition, data)
            finish_step(step, data)
        except StateMachineFailure:
            # Handle failure
            pass
        except StateMachinePausedForTask:
            state_machine_execution.waiting_for_task = True
            state_machine_execution.data = data
            db.session.commit()
            return

    state_machine_execution.data = json.dumps(data)
    state_machine_execution.status = ExecutionStatus.succeeded
    state_machine_execution.stopDate = now_timestamp()
    db.session.commit()

    print(f'ExecutionSucceeded: {state_machine_execution.name}')
    print(json.dumps({'output': data}))
