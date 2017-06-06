from local_step_functions.models.db import db


class ExecutionStatus:
    running = 'RUNNING'
    succeeded = 'SUCCEEDED'
    failed = 'FAILED'
    timed_out = 'TIMED_OUT'
    aborted = 'ABORTED'


class StateMachineExecution(db.Model):
    __tablename__ = 'state_machine_execution'

    id = db.Column(db.Integer(), primary_key=True)
    state_machine_name = db.Column(db.String(), index=True)
    # Name can be user input, defaults to a uuid
    name = db.Column(db.String(), unique=True)
    raw_input = db.Column(db.Text())
    # current/final output
    data = db.Column(db.Text())
    startDate = db.Column(db.BigInteger())
    stopDate = db.Column(db.BigInteger())
    status = db.Column(db.String(), index=True)
    waiting_for_task = db.Column(db.Boolean(), default=False, nullable=False)
