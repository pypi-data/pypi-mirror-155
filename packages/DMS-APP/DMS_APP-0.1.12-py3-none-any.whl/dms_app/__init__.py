from flask import Flask
from dms_app.config import Config
from flask_cors import CORS
from dms_app.router import register_routes
from .namespace import api, ns
import datetime
from flask_jwt_extended import JWTManager, create_access_token


class App:
    config = Config()

    def create_app(self):
        flask_app = Flask(__name__)
        JWTManager(flask_app)
        flask_app.config.from_object(self.config)
        CORS(flask_app, resources={r"*": {"origins": ["*"]}})
        flask_app.config["CORS_HEADERS"] = "Content-Type"
        flask_app.config["CORS_ORIGINS"] = "*"
        flask_app.config["SECRET_KEY"] = "cc6e455f0b76439d99cc8e1669232518"
        flask_app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=30)
        api.init_app(flask_app)
        register_routes(ns)
        return flask_app
