from flask import Flask
from flask import jsonify
from flask import request

from datetime import datetime

from local_step_functions.models.db import db
from local_step_functions.routes import ROUTE_RULES

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    (api, method) = request.headers['x-amz-target'].split('.')
    return jsonify(ROUTE_RULES[method]())

@app.before_first_request
def make_db():
  db.create_all()

if __name__ == '__main__':
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
    db.init_app(app)
    app.run()
