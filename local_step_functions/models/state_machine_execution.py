from local_step_functions.models.db import db

class StateMachineExecution(db.Model):
    __tablename__ = 'state_machine_execution'

    id = db.Column(db.Integer(), primary_key=True)
    state_machine_uuid = db.Column(db.String(), index=True)
    # Name can be user input, defaults to a uuid
    name = db.Column(db.String(), unique=True)
    data = db.Column(db.Text())
    startDate = db.Column(db.BigInteger())
    stopDate = db.Column(db.BigInteger())
