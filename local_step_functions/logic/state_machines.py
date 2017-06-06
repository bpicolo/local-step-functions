from sqlalchemy.sql import func

from uuid import uuid4
from local_step_functions.models.db import db
from local_step_functions.models.state_machine import StateMachine
from local_step_functions.models.state_machine_execution import ExecutionStatus
from local_step_functions.models.state_machine_execution import StateMachineExecution


def load_execution_by_arn(arn):
    return load_execution(arn.split(':')[-1])


def load_execution(name):
    return StateMachineExecution.query.filter(
        StateMachineExecution.name == name
    ).first()


def get_next_machine_to_run():
    return db.session.query(
        StateMachine,
        StateMachineExecution
    ).filter(
        StateMachine.name == StateMachineExecution.state_machine_name,
        StateMachineExecution.status == ExecutionStatus.running,
        StateMachineExecution.waiting_for_task.is_(False)
    ).first()
