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
    accounts = db.relationship('Account', backref="owner", cascade="all, delete-orphan" , lazy='dynamic')

    def as_dict(self):
        #Urgh, this totally won't come back to bite me in the arse...
        #In theory, there's an issue serialising datetime objects... not a problem right now...
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __json__(self):
        return ['id', 'user_id', 'email', 'street_address', 'city', 'state', 'country', 'postcode']

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    account_name = db.Column(db.String(128), index=True)
    balance = db.Column(db.Float)
    transactions = db.relationship('Transaction', backref="account", cascade="all, delete-orphan" , lazy='dynamic')
    pending_transactions = db.relationship('PendingTransaction', backref="pt_account", cascade="all, delete-orphan" , lazy='dynamic')

    def as_dict(self):
        #Urgh, this totally won't come back to bite me in the arse...
        #In theory, there's an issue serialising datetime objects... not a problem right now...
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    #Reduce Balance
    def debit(self,amount):
        self.balance = self.balance - amount
        return True

    #Increase Balance
    def credit(self, amount):
        self.balance = self.balance + amount
        return True

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    to_account = db.Column(db.Integer)
    tran_type = db.Column(db.String(128), index=True)
    amount = db.Column(db.Float)

    def as_dict(self):
        #Urgh, this totally won't come back to bite me in the arse...
        #In theory, there's an issue serialising datetime objects... not a problem right now...
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class PendingTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    to_account = db.Column(db.Integer)
    tran_type = db.Column(db.String(128), index=True)
    amount = db.Column(db.Float)

    def as_dict(self):
        #Urgh, this totally won't come back to bite me in the arse...
        #In theory, there's an issue serialising datetime objects... not a problem right now...
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
