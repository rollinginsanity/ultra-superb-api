from flask import Blueprint, render_template, abort, url_for, request
from jinja2 import TemplateNotFound
import json
import hashlib, binascii
import time
from ultraSuperbAPI.helpers import buildResponseDictionary, validJSON
from ultraSuperbAPI.api import db

from ultraSuperbAPI.models import auth_models

from ultraSuperbAPI.authAPI import helpers as auth_helpers

auth_api = Blueprint('auth', __name__, template_folder='templates')



@auth_api.route('/')
def index():

    URLS = [
        {
            'URL': url_for('auth.index'),
            "methods": ["GET"],
            "description": "This endpoint, lists available endpoints and methods."
        },
        {
            'URL': url_for('auth.oauthAuth'),
            "methods": ["POST", "GET"],
            "description": "Create a new admin user, and get an API key back."
        }
    ]

    endpoints = {
        'name': '',
        'description': 'Auth endpoints for authenticating users.',
        'URLS': URLS
    }

    endpoints_json = json.dumps(endpoints)

    return endpoints_json, 200, {'Content-Type': 'application/json; charset=utf-8'}

@auth_api.route('/auth/oauth/', methods=["POST", "GET"])
def oauthAuth():
    """
    This route either takes a post or a get, both need to provide:
    username
    password
    client_id (in this case, one of the API keys will do.)

    some endpoints may in the future take a token generated just off an API key, so maybe that will be an option as well.
    """

    data = {}
    error = {}
    responseCode = "200"
    requestJSON = ""

    #Get data from GET query params.
    if request.method == "GET":
        username = request.args.get("username")
        password = request.args.get("password")
        client_id = request.args.get("client_id")
        ##If any data is missing error out.
        if not username or not password or not client_id:
            error = {"description": "Missing parameter, make sure username, password and client_id are all set.", "code": "1"}

    #Get data from POST body.
    elif request.method == "POST":
        requestJSON = request.json
        ##If any data is missing error out.
        if not "username" in requestJSON or not "password" in requestJSON or not "client_id" in requestJSON:
            error = {"description": "Missing parameter, make sure username, password and client_id are all set.", "code": "1"} #Code 1, invalid auth request.
        else:
            username = requestJSON["username"]
            password = requestJSON["password"]
            client_id = requestJSON["client_id"]


    #validate credentials
    auth_state = auth_helpers.validateCredentials(username, password, client_id)
    if not auth_state["authenticated"]:
        error = {"description": auth_state["error"], "code": "2"} #Code 2, auth failed, invalid credentials.

    #If there has been an error, don't set data, and return a 500.
    if "code" in error:
        data = {}
        responseCode = "500"
    else:

        #If a user already has tokens, delete them.
        if  auth_models.oAuthAccessToken.query.filter_by(user_id = auth_state["user_id"]).one_or_none():
            access_token = auth_models.oAuthAccessToken.query.filter_by(user_id = auth_state["user_id"]).first()
            db.session.delete(access_token)
            db.session.commit()

        #If a user already has tokens, delete them.
        if auth_models.oAuthRefreshToken.query.filter_by(user_id = auth_state["user_id"]).one_or_none():
            refresh_token = auth_models.oAuthRefreshToken.query.filter_by(user_id = auth_state["user_id"]).first()
            db.session.delete(refresh_token)
            db.session.commit()

        access_token = auth_models.oAuthAccessToken(token_value=auth_helpers.tokenGenerator(32), user_id=auth_state["user_id"])
        refresh_token = auth_models.oAuthRefreshToken(token_value=auth_helpers.tokenGenerator(64), user_id=auth_state["user_id"])
        db.session.add(access_token)
        db.session.add(refresh_token)
        db.session.commit()

        data = {
            "username": username,
            "client_id": client_id,
            "access_token": access_token.token_value,
            "refresh_token": refresh_token.token_value
        }

    return buildResponseDictionary(data, error), responseCode, {'Content-Type': 'application/json; charset=utf-8'}
