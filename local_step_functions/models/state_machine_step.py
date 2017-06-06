from local_step_functions.models.db import db
from local_step_functions.models.state_machine_execution import ExecutionStatus


class StepStatus:
    running = 'RUNNING'
    succeeded = 'SUCCEEDED'
    failed = 'FAILED'
    timed_out = 'TIMED_OUT'
    aborted = 'ABORTED'
    waiting_for_activity = 'WAITING_FOR_ACTIVITY'


class StateMachineStep(db.Model):
    __tablename__ = 'state_machine_step'

    id = db.Column(db.Integer(), primary_key=True)
    state_machine_execution_id = db.Column(db.String(), index=True)
    type = db.Column(db.String())
    name = db.Column(db.String())
    input = db.Column(db.String())
    output = db.Column(db.String())
    status = db.Column(db.String())
    end = db.Column(db.Boolean())
    startDate = db.Column(db.BigInteger())
    stopDate = db.Column(db.BigInteger())
