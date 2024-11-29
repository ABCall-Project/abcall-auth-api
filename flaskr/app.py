from flask_restful import Resource, Api
from flask import Flask, request, json
from .utils.json_custom_encoder import JSONCustomEncoder
import requests
from flaskr import create_app
from config import Config
from .endpoint import HealthCheck,AuthUser
import signal
import logging
from flask_cors import CORS
from .infrastructure.databases.postgres.db import Session
from flaskr.endpoint.User.User import User
import newrelic.agent
newrelic.agent.initialize('newrelic.ini')

config = Config()


app = create_app('default')
CORS(app)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('default')
logger.info('starting application ...')
app.json_encoder = JSONCustomEncoder

def before_server_stop(*args, **kwargs):
    logger.info('Closing application ...')

signal.signal(signal.SIGTERM, before_server_stop)

app_context = app.app_context()
app_context.push()



api = Api(app)

api.add_resource(HealthCheck, '/health')
api.add_resource(AuthUser, '/users/<string:action>')
user_view = User.as_view('user')
app.add_url_rule('/user', view_func=user_view, methods=['POST'])

@app.teardown_appcontext
def shutdown_session(exception=None):
    Session.remove()