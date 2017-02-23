from flask import Blueprint, render_template, abort, url_for, request
from jinja2 import TemplateNotFound
import json
import hashlib, binascii
import time
from ultraSuperbAPI.helpers import buildResponseDictionary, validJSON
from ultraSuperbAPI.api import db

from ultraSuperbAPI.models import auth_models
from flask.ext.jsontools import jsonapi
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
@jsonapi
def oauthAuth():
    """
    This route either takes a post or a get, both need to provide:
    username
    password
    client_id (in this case, one of the API keys will do.)

    some endpoints may in the future take a token generated just off an API key, so maybe that will be an option as well.
    """

    response_body = {}
    responseCode = "200"
    requestJSON = ""

    #Get data from GET query params.
    if request.method == "GET":
        username = request.args.get("username")
        password = request.args.get("password")
        client_id = request.args.get("client_id")
        ##If any data is missing error out.
        if not username or not password or not client_id:
            response_body = {"error": "Missing parameter, make sure username, password and client_id are all set.", "code": "1"}
            responseCode = 403

    #Get data from POST body.
    elif request.method == "POST":
        requestJSON = request.json
        ##If any data is missing error out.
        if not "username" in requestJSON or not "password" in requestJSON or not "client_id" in requestJSON:
            response_body = {"error": "Missing parameter, make sure username, password and client_id are all set.", "code": "1"} #Code 1, invalid auth request.
            responseCode = 403
        else:
            username = requestJSON["username"]
            password = requestJSON["password"]
            client_id = requestJSON["client_id"]


    #validate credentials
    auth_state = auth_helpers.validateCredentials(username, password, client_id)
    if not auth_state["authenticated"]:
        response_body = {"error": auth_state["error"], "code": "2"} #Code 2, auth failed, invalid credentials.

    #If there has been an error, don't set data, and return a 500.
    if "error" in response_body:
        return response_body, responseCode
    else:

        access_token = auth_models.oAuthAccessToken(token_value=auth_helpers.tokenGenerator(32), user_id=auth_state["user_id"])
        refresh_token = auth_models.oAuthRefreshToken(token_value=auth_helpers.tokenGenerator(64), user_id=auth_state["user_id"])
        db.session.add(access_token)
        db.session.add(refresh_token)
        db.session.commit()
        print("Did I make it here?")
        response_body = {
            "username": username,
            "access_token": access_token.token_value,
            "refresh_token": refresh_token.token_value
        }

        return response_body, responseCode

#Using an oAuth refresh token, pass out a new access token.
#In the real world you might also want to use additional auth material, such as a PIN, to allow this flow.
@auth_api.route('/auth/oauth/refresh', methods=["POST", "GET"])
@jsonapi
def oauthAuthRefresh():
    #Get JSON body from request.
    requestJSON = request.json
    #Get DB object for Refresh Token
    refresh_token = auth_models.oAuthRefreshToken.query.filter_by(token_value=requestJSON["refresh_token"]).first()
    #Validate we got a result for a refresh token.
    if refresh_token != None:
        #Get user associated with Refresh Token
        user_id = refresh_token.user_id
        #Delete the refresh token we just used.
        db.session.delete(refresh_token)

        #Generate a new access token.
        access_token = auth_models.oAuthAccessToken(token_value=auth_helpers.tokenGenerator(32), user_id=user_id)
        #Generate a new refresh token.
        refresh_token = auth_models.oAuthRefreshToken(token_value=auth_helpers.tokenGenerator(64), user_id=user_id)
        #Add new tokens to the DB session
        db.session.add(access_token)
        db.session.add(refresh_token)
        #Commit to the DB.
        db.session.commit()
        #Return new tokens:
        user = auth_models.User.query.filter_by(id=user_id).first()
        response_body = {
            "username": user.username,
            "access_token": access_token.token_value,
            "refresh_token": refresh_token.token_value
        }
        return response_body, 200
    else:
        return {"error": "Invalid refresh token."}, 403
