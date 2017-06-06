import json
import time

from local_step_functions.app import create_app
from local_step_functions.logic.runner import run_state_machine
from local_step_functions.models.db import db
from local_step_functions.models.state_machine import StateMachine
from local_step_functions.models.state_machine_execution import ExecutionStatus
from local_step_functions.models.state_machine_execution import StateMachineExecution
from local_step_functions.models.state_machine_step import StateMachineStep


def run_state_executor():
    while True:
        to_run = get_next_machine_to_run()
        if to_run is None:
            time.sleep(2)
            continue

        output = run_state_machine(*to_run)

        print("Output: ")
        print(output)


if __name__ == '__main__':
    app = create_app()
    with app.test_request_context():
        run_state_executor()
