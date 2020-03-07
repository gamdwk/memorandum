from flask import Flask, jsonify, make_response, g
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
import flask_restful

db = SQLAlchemy()


def creatapp(c):
    app = Flask(__name__)
    app.config.from_object(c)
    db.init_app(app)
    return app


app = creatapp('config')
auth = HTTPBasicAuth()
from api.errors import api_abort

flask_restful.abort = api_abort

from api import api, models, authentication
