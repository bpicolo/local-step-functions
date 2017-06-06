import json
from datetime import datetime
from uuid import uuid4

from flask import request

from local_step_functions.logic.state_machines import load_execution_by_arn
from local_step_functions.models.db import db
from local_step_functions.models.state_machine_execution import ExecutionStatus
from local_step_functions.models.state_machine import StateMachine
from local_step_functions.models.state_machine_execution import StateMachineExecution


def state_machine_arn(machine):
    return f'arn:aws:states:us-west-2:123456789:stateMachine:{machine.name}'


def execution_arn(machine_name, execution_name):
    return f'arn:aws:states:us-west-2:123456789:execution:{machine_name}:{execution_name}'


def serialize_state_machine(state_machine):
    return {
        'creationDate': state_machine.creationDate,
        'name': state_machine.name,
        'stateMachineArn': state_machine_arn(state_machine)
    }


def load_state_machine_by_arn(arn):
    return load_state_machine(arn.split(':')[-1])


def load_state_machine(name):
    return StateMachine.query.filter_by(name=name).first()


def describe_execution():
    data = json.loads(request.data)
    arn = data['executionArn']
    execution = load_execution_by_arn(arn)
    machine = load_state_machine(execution.state_machine_name)

    return {
        'executionArn': execution_arn(machine.name, execution.name),
        'input': execution.raw_input,
        'output': execution.data,
        'startDate': execution.startDate,
        'stopDate': execution.stopDate,
        'status': execution.status,
        'stateMachineArn': state_machine_arn(machine),
    }


def list_state_machines():
    data = json.loads(request.data)
    max_results = data.get('MaxResults', 100) or 100

    query = db.session.query(StateMachine).order_by(
        StateMachine.name.desc()
    )

    # TODO dont think this bit works atm
    if data.get('nextToken', False) is not False:
        query = query.filter(StateMachine.name < data['nextToken'])

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
        out['nextToken'] = next_result.name

    return out


def create_state_machine():
    data = json.loads(request.data)

    state_machine = StateMachine(
        name=data['name'],
        definition=data['definition'],
        roleArn=data['roleArn'],
        creationDate=int(datetime.now().timestamp()),
    )
    db.session.add(state_machine)
    db.session.commit()

    return {
        'creationDate': state_machine.creationDate,
        'stateMachineArn': state_machine_arn(state_machine)
    }


def start_execution():
    data = json.loads(request.data)
    machine = load_state_machine_by_arn(data['stateMachineArn'])
    execution = StateMachineExecution(
        state_machine_name=machine.name,
        name=data.get('name', str(uuid4())),
        raw_input=data['input'],
        data=data['input'],
        startDate=int(datetime.now().timestamp()),
        status=ExecutionStatus.running,
        waiting_for_task=False,
    )

    db.session.add(execution)
    db.session.commit()

    return {
        'executionArn': execution_arn(machine.name, execution.name),
        'startDate': execution.startDate
    }


STATE_MACHINE_ROUTES = {
    'CreateStateMachine': create_state_machine,
    'ListStateMachines': list_state_machines,
    'StartExecution': start_execution,
    'DescribeExecution': describe_execution,
}
