from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from ultraSuperbAPI.adminAPI import admin_api
from ultraSuperbAPI.metaAPI import meta_api

api = Flask(__name__)

api.register_blueprint(admin_api, url_prefix='/admin/v1')
api.register_blueprint(meta_api, url_prefix='/meta/v1')

db = SQLAlchemy(api)
