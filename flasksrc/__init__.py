import os

from flask import Flask
from flask_restful import Resource, Api


class HelloReclass(Resource):
    def get(self):
        # return {'hello': 'reclass'}
        return 'Hello, Reclass!'


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'toynet.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # initialize DB
    from . import db
    db.init_app(app)

    # make RESTful
    api = Api(app)
    api.add_resource(HelloReclass, '/')

    from .value import ToyNetValueById
    api.add_resource(ToyNetValueById, '/api/value/<string:value_id>')

    return app
