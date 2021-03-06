from local_step_functions.models.db import db


class StateMachine(db.Model):
    __tablename__ = 'state_machine'

    name = db.Column(db.String(), primary_key=True)
    definition = db.Column(db.Text())
    roleArn = db.Column(db.String())
    creationDate = db.Column(db.BigInteger())
