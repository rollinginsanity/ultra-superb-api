from flask import Blueprint, render_template, abort, request, url_for, g
from jinja2 import TemplateNotFound
import json
from ultraSuperbAPI import api
from ultraSuperbAPI.api import db
from ultraSuperbAPI.authAPI import helpers as auth_helpers
from ultraSuperbAPI.helpers import buildResponseDictionary, validJSON
from ultraSuperbAPI.models import auth_models
crappybank_api = Blueprint('crappybank', __name__, template_folder='templates')



@crappybank_api.before_request
def authenticate():
    auth_state = auth_helpers.validateAccessToken(request.headers.get('Authorization'))
    print(request.headers.get('Authorization'))
    print(auth_state)
    if auth_state["valid"]:
        g.user_state = {
            "user_id": auth_state["user_id"]
        }
    else:
        g.user_state = {
            "unauthenticated": True
        }


@crappybank_api.route('/')
def index():
    print(user_state)
    URLS = [
        {
            'URL': url_for('crappybank.index'),
            "methods": ["GET"],
            "description": "This endpoint, lists available endpoints and methods."
        }
    ]

    endpoints = {
        'name': '',
        'description': 'Business logic based around a fictional bank.',
        'URLS': URLS
    }

    endpoints_json = json.dumps(endpoints)

    return endpoints_json, 200, {'Content-Type': 'application/json; charset=utf-8'}


@crappybank_api.route("/auth-check")
def auth_check():
    print(g.user_state)
    data = {}
    error = {}
    responseCode = 200
    if "unauthenticated" in g.user_state:
        return {"error": "Unauthenticated"}, 403, {'Content-Type': 'application/json; charset=utf-8'}

    user = auth_models.User.query.filter_by(id=g.user_state["user_id"]).first()

    data = {
        "username": user.username
    }

    return buildResponseDictionary(data, error), responseCode, {'Content-Type': 'application/json; charset=utf-8'}
