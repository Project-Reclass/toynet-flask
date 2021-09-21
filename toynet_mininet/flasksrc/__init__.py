import os
from flask import Flask
from flask_restful import Resource, Api
from flask_apispec import FlaskApiSpec

class HelloReclass(Resource):
    def get(self):
        return 'Hello, Reclass!'


def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # make RESTful
    api = Api(app)
    api.add_resource(HelloReclass, '/')
    docs = FlaskApiSpec(app)
    
    from .topo import MiniFlaskTopo
    api.add_resource(MiniFlaskTopo, '/api/topo')
    docs.register(MiniFlaskTopo)

    from .terminate import MiniFlaskTerminate
    api.add_resource(MiniFlaskTerminate, '/api/terminate')
    docs.register(MiniFlaskTerminate)

    from .command import MiniFlaskCommand
    api.add_resource(MiniFlaskCommand, '/api/command')
    docs.register(MiniFlaskCommand)

    return app
