from local_step_functions.models.db import db


class Activity(db.Model):
    __tablename__ = 'activity'

    name = db.Column(db.String(), primary_key=True)
    uuid = db.Column(db.String(), unique=True)
    creationDate = db.Column(db.BigInteger())
