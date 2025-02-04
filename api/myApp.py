import os

from flask import Flask, render_template
from flask.json.provider import DefaultJSONProvider
from flask_cors import CORS
##from flask_bcrypt import Bcrypt
##from flask_jwt_extended import JWTManager

from bson import json_util, ObjectId
from datetime import datetime, timedelta
from flask import Blueprint
import api.db as db
from api.paths import food_api_v1

#from mflix.api.movies import movies_api_v1



class MongoJsonEncoder(DefaultJSONProvider):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(obj, ObjectId):
            return str(obj)
        return DefaultJSONProvider.default(obj)


def create_app():
    
    APP_DIR = os.path.abspath(os.path.dirname(__file__))
    STATIC_FOLDER = os.path.join(APP_DIR, '../static')
    TEMPLATE_FOLDER = os.path.join(APP_DIR, '../templates')

    app = Flask(__name__, static_folder=STATIC_FOLDER,
                template_folder=TEMPLATE_FOLDER,
                )
    CORS(app)
    app.json_encoder = MongoJsonEncoder
    app.register_blueprint(food_api_v1)

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        return render_template('/index.html')

    #db.add_restuarant("NONE" , "NONE", "NONE", "NONE")

    return app