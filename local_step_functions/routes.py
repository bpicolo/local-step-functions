import json
from datetime import datetime
from uuid import uuid4

from flask import request

from local_step_functions.models.db import db
from local_step_functions.models.state_machine_execution import ExecutionStatus
from local_step_functions.models.state_machine import StateMachine
from local_step_functions.models.state_machine_execution import StateMachineExecution


def state_machine_arn(resource, uuid):
    return f'arn:aws:states:us-west-2:123456789:stateMachine:{resource}:{uuid}'


def execution_arn(resource, uuid):
    return f'arn:aws:states:us-west-2:123456789:execution:{resource}:{uuid}'


def serialize_state_machine(state_machine):
    return {
        'creationDate': state_machine.creationDate,
        'name': state_machine.name,
        'stateMachineArn': state_machine_arn(state_machine.name, state_machine.uuid)
    }


def load_state_machine(arn):
    uuid = arn.split(':')[-1]
    return StateMachine.query.filter_by(uuid=uuid).first()


def list_state_machines():
    data = json.loads(request.data)
    max_results = data.get('MaxResults', 100) or 100

    query = db.session.query(StateMachine).order_by(
        StateMachine.uuid.desc()
    )

    # TODO dont think this bit works atm
    if data.get('nextToken', False) is not False:
        query = query.filter(StateMachine.uuid < data['nextToken'])

    results = query.limit(max_results + 1).all()

    next_result = None
    if len(results) > max_results:
        next_result = results[-1]
        results = results[:-1]

    out = {
        'stateMachines': [
            serialize_state_machine(machine)
            for machine in results
        ]
    }
    if next_result is not None:
        out['nextToken'] = next_result.uuid

    return out


def create_state_machine():
    data = json.loads(request.data)

    state_machine = StateMachine(
        name=data['name'],
        definition=data['definition'],
        roleArn=data['roleArn'],
        uuid=str(uuid4()),
        creationDate=int(datetime.now().timestamp()),
    )
    db.session.add(state_machine)
    db.session.commit()

    return {
        'creationDate': state_machine.creationDate,
        'stateMachineArn': state_machine_arn(state_machine.name, state_machine.uuid)
    }


def start_execution():
    data = json.loads(request.data)
    machine = load_state_machine(data['stateMachineArn'])
    execution = StateMachineExecution(
        state_machine_uuid=machine.uuid,
        name=data.get('name', str(uuid4())),
        data=data['input'],
        startDate=int(datetime.now().timestamp()),
        status=ExecutionStatus.running,
    )

    db.session.add(execution)
    db.session.commit()

    return {
        'executionArn': execution_arn(machine.name, execution.name),
        'startDate': execution.startDate
    }


ROUTE_RULES = {
    'CreateStateMachine': create_state_machine,
    'ListStateMachines': list_state_machines,
    'StartExecution': start_execution
}
