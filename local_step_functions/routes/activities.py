import json
from datetime import datetime
from uuid import uuid4

from flask import request

from local_step_functions.logic.state_machines import load_execution
from local_step_functions.models.db import db
from local_step_functions.models.activity import Activity
from local_step_functions.models.activity_task import ActivityTask
from local_step_functions.models.state_machine_step import StateMachineStep
from local_step_functions.models.state_machine_step import StepStatus
from local_step_functions.util import now_timestamp


# "activity" might not be the actual resource type
def activity_arn(resource, uuid):
    return f'arn:aws:states:us-west-2:123456789:activity:{resource}:{uuid}'


def create_activity():
    data = json.loads(request.data)
    activity = Activity(
        name=data['name'],
        uuid=str(uuid4()),
        creationDate=now_timestamp()
    )

    db.session.add(activity)
    db.session.commit()

    return {
        'activityArn': activity_arn(activity.name, activity.uuid),
        'creationDate': activity.creationDate
    }


def delete_activity():
    data = json.loads(request.data)
    uuid = data['activtyArn'].split(':')[-1]

    result = Activity.query.filter(uuid=uuid).first()
    if not result:
        # Throw errors the way amazon would guys
        pass

    return {}


def send_task_success():
    data = json.loads(request.data)
    token = data['taskToken']
    task = ActivityTask.query.filter(token=token).first()
    if not task:
        # raise TaskDoesNotExists
        return {}

    step = StateMachineStep.query.filter(id=task.state_machine_step_id).first()
    step.status = StepStatus.succeeded
    step.output = data['output']
    execution = load_execution(step.state_machine_execution_id)
    execution.waiting_for_task = False

    if step.end:
        execution.status = StepStatus.succeeded

    db.session.delete(task)
    db.session.commit()

    return {}


ACTIVITY_ROUTES = {
    'CreateActivity': create_activity,
    'DeleteActivity': delete_activity,
    'SendTaskSuccess': send_task_success,
}
