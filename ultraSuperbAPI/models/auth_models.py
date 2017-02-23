#This file will contain models relating to authentication, both for API keys and oAuth tokens
import datetime
from ultraSuperbAPI.api import db
#Some useful sqlalchemy functions
from sqlalchemy.sql import func

class APIKey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key_name = db.Column(db.String(64), index=True, unique=True)
    key_value = db.Column(db.String(128), index=True, unique=True)
    creation_date = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return '<Token %r>' % (self.key_name)

class oAuthAccessToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, index=True)
    token_value = db.Column(db.String(64), index=True, unique=True)
    grant = db.Column(db.String(128), index=True)
    creation_date = db.Column(db.DateTime(), server_default=db.func.current_timestamp())

class oAuthRefreshToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, index=True)
    token_value = db.Column(db.String(64), index=True, unique=True)
    grant = db.Column(db.String(128), index=True)
    creation_date = db.Column(db.DateTime(), server_default=db.func.current_timestamp())

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128), index=True)
    creation_date = db.Column(db.DateTime(timezone=True), server_default=func.now())
