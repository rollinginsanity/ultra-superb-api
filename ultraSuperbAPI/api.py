#import the basics
from flask import Flask
#SQLAlchemy, the ORM of champions.
from flask_sqlalchemy import SQLAlchemy



from ultraSuperbAPI import models

#Our Flask Object is called 'api', remember that.
api = Flask(__name__)

#load the config for the api DB.
api.config.from_object('ultraSuperbAPI.config')

#Yay, the Database!
db = SQLAlchemy(api)


#These imports need to happen here, below db, as they need to use db... circular references SUCK!
from ultraSuperbAPI.adminAPI import admin_api
from ultraSuperbAPI.metaAPI import meta_api
from ultraSuperbAPI.authAPI import auth_api

#Register the endpoints, make sure the apis are mounted on paths thatmake sense. Haven't figured out versioning yet.
api.register_blueprint(admin_api, url_prefix='/admin/v1')
api.register_blueprint(meta_api, url_prefix='/meta/v1')
api.register_blueprint(auth_api, url_prefix='/auth/v1')
