from local_step_functions.models.db import db
from local_step_functions.models.state_machine_execution import ExecutionStatus


class StateMachineStep(db.Model):
    __tablename__ = 'state_machine_step'

    id = db.Column(db.Integer(), primary_key=True)
    state_machine_execution_uuid = db.Column(db.String(), index=True)
    type = db.Column(db.String())
    # activity_id = db.Column(db.Integer(), unique=True)
    input = db.Column(db.String())
    output = db.Column(db.String())
    status = db.Column(db.String())
