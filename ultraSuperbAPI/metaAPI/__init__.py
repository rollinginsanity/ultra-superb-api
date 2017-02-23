from flask import Blueprint, render_template, abort, url_for, request
from jinja2 import TemplateNotFound
import json
import hashlib, binascii
import time
from ultraSuperbAPI.helpers import buildResponseDictionary, validJSON
from ultraSuperbAPI.api import db
from ultraSuperbAPI.models import auth_models, customer_models
from ultraSuperbAPI.authAPI import helpers as auth_helpers
from flask_jsontools import jsonapi

meta_api = Blueprint('meta', __name__, template_folder='templates')

@meta_api.route('/')
@jsonapi
def index():

    endpoints = {
        'name': '',
        'description': 'Yep, there is an API here. This API is for the management of everything else, and probably the only place where vulnerabilities are accidental.'
    }

    return endpoints, 200, {'Content-Type': 'application/json; charset=utf-8'}

#Gets the user at a specific user ID.
@meta_api.route("/user/<int:userid>", methods=["GET", "POST"])
def users(userid):
    data = {}
    error = {}
    responseCode = 200
    if request.method == "GET":
        user = auth_models.User.query.filter_by(id=userid).first()
        if user:
            data = {
                "user_id": user.id,
                "username": user.username
            }
        else:
            error = {"description": "No user exists with that ID."}

    if request.method == "POST":
        user = auth_models.User.query.filter_by(id=userid).first()
        if user:
            data = {
                "user_id": user.id,
                "username": user.username
            }
        else:
            error = {"description": "No user exists with that ID."}

    return buildResponseDictionary(data, error), responseCode, {'Content-Type': 'application/json; charset=utf-8'}

#Create a new user for the other APIs.
@meta_api.route("/user/create", methods=["POST"])
@jsonapi
def create_user():
    responseCode = 200

    if validJSON(request.data.decode('UTF-8')):
        requestJSON = request.json
        if "username" in requestJSON and "password" in requestJSON:
            username = requestJSON["username"]
            password = requestJSON["password"]

            if not auth_models.User.query.filter_by(username=username).first():

                password_hash = auth_helpers.hashPassword(password)

                user = auth_models.User(username=username, password=password_hash)

                db.session.add(user)

                db.session.commit()

                user = auth_models.User.query.filter_by(username=username).first()

                #Create a customer record.
                customer = customer_models.Customer(user_id=user.id)

                db.session.add(customer)

                db.session.commit()

                customer = customer_models.Customer.query.filter_by(user_id=user.id).first()

                cust_id = str(customer.id)

                customer.customer_number = "CST"+"099"+cust_id.zfill(14)

                db.session.add(customer)

                db.session.commit()

                response_body = {
                    "username": user.username,
                    "user_id": user.id,
                    "customer_number": customer.customer_number
                }
            else:
                response_body = {"error": "Duplicate username detected."}
                responseCode = 400
        else:
            response_body = {"error": "Missing username or password in JSON body."}
            responseCode = 400

    else:
        response_body = {"error": "Invalid JSON"}
        responseCode = 400

    return response_body, responseCode

#list all users.
@meta_api.route("/users")
def all_users():
    data = {}
    error = {}
    responseCode = 200

    users_list = []

    users = auth_models.User.query.all()
    for user in users:
        users_list.append({"user_id": user.id, "username": user.username})

    data = {"users": users_list}

    return buildResponseDictionary(data, error), responseCode, {'Content-Type': 'application/json; charset=utf-8'}

@meta_api.route("/user/account", methods=["POST","GET"])
@jsonapi
def accounts():
    data = {}
    error = {}
    if request.method == "GET":
        return {"Todo": "Implement This Functionality"}, 200, {'Content-Type': 'application/json; charset=utf-8'}
    elif request.method == "POST":
        if validJSON(request.data.decode('UTF-8')):
            requestJSON = request.json
            account_name = requestJSON["account_name"]
            account_owner = requestJSON["owner"]
            balance = requestJSON["balance"]

            customer = customer_models.Customer.query.filter_by(id=account_owner).first()

            account = customer_models.Account(owner=customer, account_name=account_name, balance=float(balance))

            account_id = account.id

            db.session.add(account)
            db.session.commit()

            account = customer_models.Account.query.filter_by(id=account.id).first()

            acct_id = str(account.id)

            account.account_number = "ACCT"+"-"+"TRAN"+acct_id.zfill(9)

            db.session.add(account)

            db.session.commit()

            data = account.as_dict()

        else:
            error = {"error": "invalid JSON. :("}
            return {data, error}, 500, {'Content-Type': 'application/json; charset=utf-8'}

    return {"data": data, "error": error}

@meta_api.route("/users/all")
@jsonapi
def list_all():
    data = {"customers": []}
    error = {}
    customers = customer_models.Customer.query.all()
    for customer in customers:
        accounts = []
        for account in customer.accounts:
            accounts.append(account.as_dict())
        data["customers"].append({"customer_id": customer.id, "user_id": customer.user_id, "accounts": accounts})

    return data, 200, {'Content-Type': 'application/json; charset=utf-8'}
