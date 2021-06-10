import os
from flask import Flask
from flask_restful import Resource, Api
from flask_jwt_extended import JWTManager
from flask_apispec import FlaskApiSpec


class HelloReclass(Resource):
    def get(self):
        return 'Hello, Reclass!'


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    JWTManager(app)

    if test_config is None:
        app.config.from_pyfile('dev_config.py', silent=False)
        app.config['DATABASE'] = os.path.join(app.instance_path, 'toynet.sqlite')
    else:
        app.config.from_pyfile('test_config.py', silent=True)

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
    docs = FlaskApiSpec(app)

    from .user import ToyNetUser, ToyNetUserLogin
    api.add_resource(ToyNetUser, '/api/user')
    api.add_resource(ToyNetUserLogin, '/api/login')
    docs.register(ToyNetUser)
    docs.register(ToyNetUserLogin)

    from .value import ToyNetValueById, ToyNetValueEntryById
    api.add_resource(ToyNetValueById, '/api/value/<int:value_id>/inspirations')
    api.add_resource(ToyNetValueEntryById, '/api/value/<int:value_id>/entry')
    docs.register(ToyNetValueById)
    docs.register(ToyNetValueEntryById)

    from .quiz import ToyNetQuizById
    api.add_resource(ToyNetQuizById, '/api/quiz/<int:quiz_id>')
    docs.register(ToyNetQuizById)

    from .survey import ToyNetSurveyById
    api.add_resource(ToyNetSurveyById, '/api/survey/<string:survey_id>')
    docs.register(ToyNetSurveyById)

    from .session import ToyNetSession
    api.add_resource(ToyNetSession, '/api/toynet/session')
    docs.register(ToyNetSession)

    from .session import ToyNetSessionById
    api.add_resource(ToyNetSessionById, '/api/toynet/session/<int:toynet_session_id>')
    docs.register(ToyNetSessionById)

    return app
