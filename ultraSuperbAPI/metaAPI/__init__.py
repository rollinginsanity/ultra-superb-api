from flask import Blueprint, render_template, abort, url_for, request
from jinja2 import TemplateNotFound
import json
import hashlib, binascii
import time
from ultraSuperbAPI.helpers import buildResponseDictionary, validJSON
from ultraSuperbAPI.api import db

from ultraSuperbAPI.models import auth_models

meta_api = Blueprint('meta', __name__, template_folder='templates')

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
