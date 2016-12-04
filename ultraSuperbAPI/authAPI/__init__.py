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

    if request.method == "GET":
        username = request.args.get("username")
        password = request.args.get("password")
        client_id = request.args.get("client_id")

        data = {
            "username": username,
            "client_id": client_id,
            "access_token": auth_helpers.tokenGenerator(32),
            "refresh_token": auth_helpers.tokenGenerator(64)
        }

    elif request.method == "POST":
        requestJSON = request.json
        username = requestJSON["username"]
        password = requestJSON["password"]
        client_id = requestJSON["client_id"]

        data = {
            "username": username,
            "client_id": client_id,
            "access_token": auth_helpers.tokenGenerator(32),
            "refresh_token": auth_helpers.tokenGenerator(64)
        }
    else:
        return "EFF YOU!"

    return buildResponseDictionary(data, error), responseCode, {'Content-Type': 'application/json; charset=utf-8'}
