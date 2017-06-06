from flask import Blueprint
from flask import Flask
from flask import jsonify
from flask import request

from datetime import datetime

from local_step_functions.models.db import db
from local_step_functions.routes import ROUTE_RULES

routes = Blueprint('routes', __name__)


@routes.route('/', methods=['GET', 'POST'])
def index():
    (api, method) = request.headers['x-amz-target'].split('.')
    return jsonify(ROUTE_RULES[method]())


def create_app():
    app = Flask(__name__)
    app.register_blueprint(routes, url_prefix='')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
    db.init_app(app)

    app.before_first_request(lambda: db.create_all())

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
