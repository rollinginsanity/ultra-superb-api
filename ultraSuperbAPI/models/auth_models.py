#This file will contain models relating to authentication, both for API keys and oAuth tokens

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
