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

@meta_api.before_request
def authenticate():

    data = {}

    if 'admin-register' not in request.path:
        if 'token' in request.headers:
            pass
        else:
            #return "Meh"
            return buildResponseDictionary(data, {"error": "Unauthenticated, please use token: header with the API key."}), 403, {'Content-Type': 'application/json; charset=utf-8'}

    return


@meta_api.route('/')
def index():

    URLS = [
        {
            'URL': url_for('meta.index'),
            "methods": ["GET"],
            "description": "This endpoint, lists available endpoints and methods."
        },
        {
            'URL': url_for('meta.admin_register'),
            "methods": ["POST"],
            "description": "Create a new admin user, and get an API key back."
        },
        {
            'URL': url_for('meta.users', userid="0"),
            "methods": ["GET", "POST"],
            "description": "View users by ID."
        },
        {
            'URL': url_for('meta.all_users'),
            "methods": ["GET"],
            "description": "View all users"
        }
    ]

    endpoints = {
        'name': '',
        'description': 'Meta APIs, a lazy way of making the rest of the endpoints work.<br />Create new Admin users, etc...',
        'URLS': URLS
    }

    endpoints_json = json.dumps(endpoints)

    return endpoints_json, 200, {'Content-Type': 'application/json; charset=utf-8'}

@meta_api.route('/admin-register', methods=["POST"])
def admin_register():
    """
    Generates an API key to be used to get short lived tokens.
    Actually at the moment it doesn't store it anywhere, just generates a key.
    Still need to pull all fo the request validation logic out and dump it somewhere else.
    """

    #Set these two to default to blank, so that they are always returned.
    data = {}
    error = {}

    #Var to store the request JSON.
    requestJSON = ""

    #Check if the request has data.
    if not request.data:
        responseCode = 400
        error = {"desc": "No data sent to server."}

    #Check the request content type is set correctly.
    if not request.headers['Content-Type'] == 'application/json':
        responseCode = 400
        data = {}
        error = {"desc": "Set content-type to 'application/json'."}

    #Check that the request contains valid JSON.
    if not validJSON(request.data.decode('UTF-8')):
        responseCode = 400
        error = {"desc": "Invalid JSON."}
    else:
        requestJSON = request.json

    #Check the required params are in the JSON.
    if not "name" in requestJSON:
        responseCode = 400
        error = {"desc": "No 'name' argument set."}
    else:
        #Set the response code.
        responseCode = 200

        #Get the value we care about.
        name = requestJSON['name']

        #No security implied. I'm lazy.

        #Generate a token based off a pbkdf2 HMAC of the current UNIX time.
        timestamp = str(time.time())
        api_key_hash = hashlib.pbkdf2_hmac('sha512', timestamp.encode(), b'This is a salt', 100000)

        #Convert output to a string.
        api_key_hex = binascii.hexlify(api_key_hash)
        api_key_string = api_key_hex.decode('utf-8')

        #Need to check if the key name already exists.
        check_key_name = auth_models.APIKey.query.filter_by(key_name=name).first()

        print(check_key_name)
        if check_key_name:
            error = {"desc": "API key already exists with that name."}
            responseCode = 500
        else:
            #Set the API key in the API Key object
            APIKey = auth_models.APIKey(key_name=name, key_value=api_key_string)
            #Add the key.
            db.session.add(APIKey)
            #Commit the changes. Win.
            db.session.commit()

            #Build data dictionary
            data = {
                "name": name,
                "key": api_key_string
            }

    #Send back to user.
    return buildResponseDictionary(data, error), responseCode, {'Content-Type': 'application/json; charset=utf-8'}

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
def create_user():
    data = {}
    error = {}
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

                data = {
                    "username": user.username,
                    "user_id": user.id
                }
            else:
                error = {"description": "Duplicate username detected."}
                responseCode = 400
        else:
            error = {"description": "Missing username or password in JSON body."}
            responseCode = 400

    else:
        error = {"description": "Invalid JSON"}
        responseCode = 400

    return buildResponseDictionary(data, error), responseCode, {'Content-Type': 'application/json; charset=utf-8'}

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
