# This file is part of Toynet-Flask.
#
# Toynet-Flask is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Toynet-Flask is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Toynet-Flask.  If not, see <https://www.gnu.org/licenses/>.

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

    # Change default API specification paths
    app.config.update({
        'APISPEC_SWAGGER_URL': '/swagger',
        'APISPEC_SWAGGER_UI_URL': '/swagger-ui',
    })

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

    from .quiz import ToyNetQuizById, ToyNetQuizScore, ToyNetQuizScoresByUser
    api.add_resource(ToyNetQuizById, '/api/quiz/<int:quiz_id>')
    api.add_resource(ToyNetQuizScore, '/api/quizscore')
    api.add_resource(ToyNetQuizScoresByUser, '/api/quizscores')
    docs.register(ToyNetQuizById)
    docs.register(ToyNetQuizScore)
    docs.register(ToyNetQuizScoresByUser)

    from .survey import ToyNetSurveyById
    api.add_resource(ToyNetSurveyById, '/api/survey/<string:survey_id>')
    docs.register(ToyNetSurveyById)

    from .session import ToyNetSession, ToyNetSessionById, \
        ToyNetSessionByIdTerminate, ToyNetSessionByIdCreateHost, \
        ToyNetSessionByIdCreateSwitch, ToyNetSessionByIdCreateRouter, \
        ToyNetSessionByIdCreateRouterInterface, ToyNetSessionByIdCreateLink, \
        ToyNetSessionByIdDeleteDevice, ToyNetSessionByIdDeleteLink, \
        ToyNetSessionByIdDeleteRouterInterface
    api.add_resource(ToyNetSession, '/api/toynet/session')
    api.add_resource(ToyNetSessionById, '/api/toynet/session/<int:toynet_session_id>')
    api.add_resource(ToyNetSessionByIdTerminate,
                     '/api/toynet/session/<int:toynet_session_id>/terminate')
    api.add_resource(ToyNetSessionByIdCreateHost,
                     '/api/toynet/session/<int:toynet_session_id>/create/host')
    api.add_resource(ToyNetSessionByIdCreateSwitch,
                     '/api/toynet/session/<int:toynet_session_id>/create/switch')
    api.add_resource(ToyNetSessionByIdCreateRouter,
                     '/api/toynet/session/<int:toynet_session_id>/create/router')
    api.add_resource(ToyNetSessionByIdCreateRouterInterface,
                     '/api/toynet/session/<int:toynet_session_id>/create/router/interface')
    api.add_resource(ToyNetSessionByIdCreateLink,
                     '/api/toynet/session/<int:toynet_session_id>/create/link')
    api.add_resource(ToyNetSessionByIdDeleteDevice,
                     '/api/toynet/session/<int:toynet_session_id>/delete/<string:device_type>')
    api.add_resource(ToyNetSessionByIdDeleteRouterInterface,
                     '/api/toynet/session/<int:toynet_session_id>/delete/router/interface')
    api.add_resource(ToyNetSessionByIdDeleteLink,
                     '/api/toynet/session/<int:toynet_session_id>/delete/link')
    docs.register(ToyNetSession)
    docs.register(ToyNetSessionById)
    docs.register(ToyNetSessionByIdTerminate)
    docs.register(ToyNetSessionByIdCreateHost)
    docs.register(ToyNetSessionByIdCreateSwitch)
    docs.register(ToyNetSessionByIdCreateRouter)
    docs.register(ToyNetSessionByIdCreateRouterInterface)
    docs.register(ToyNetSessionByIdCreateLink)
    docs.register(ToyNetSessionByIdDeleteDevice)
    docs.register(ToyNetSessionByIdDeleteRouterInterface)
    docs.register(ToyNetSessionByIdDeleteLink)

    return app
