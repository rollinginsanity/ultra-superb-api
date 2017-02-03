#This file will contain models relating to authentication, both for API keys and oAuth tokens

from ultraSuperbAPI.api import db
#Some useful sqlalchemy functions
from sqlalchemy.sql import func

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, index=True, unique=True)
    email = db.Column(db.String(128), index=True)
    street_address = db.Column(db.String(128), index=True)
    city = db.Column(db.String(128), index=True)
    country = db.Column(db.String(128), index=True)
    state = db.Column(db.String(128), index=True)
    postcode = db.Column(db.Integer)

    def as_dict(self):
        #Urgh, this totally won't come back to bite me in the arse...
        #In theory, there's an issue serialising datetime objects... not a problem right now...
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __json__(self):
        return ['id', 'user_id', 'email', 'street_address', 'city', 'state', 'country', 'postcode']
