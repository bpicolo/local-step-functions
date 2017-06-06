from local_step_functions.models.db import db


class ActivityTask(db.Model):
    __tablename__ = 'activity_task'

    token = db.Column(db.String(), primary_key=True, autoincrement=False)
    activity_id = db.Column(db.Integer())
    state_machine_step_id = db.Column(db.Integer(), unique=True)
    worker_name = db.Column(db.String())
