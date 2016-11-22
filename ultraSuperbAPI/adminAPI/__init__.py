from flask import Blueprint, render_template, abort, url_for
from jinja2 import TemplateNotFound
import json

admin_api = Blueprint('admin', __name__, template_folder='templates')

@admin_api.route('/')
def index():

    URLS = [
        {
            'URL': url_for('admin.index'),
            "methods": ["GET"],
            "description": "This endpoint, lists available endpoints and methods."
        },
        {
            'URL': url_for('admin.authenticate'),
            "methods": ["POST"],
            "description": "Lets an admin application or user authenticate."
        }
    ]

    endpoints = {
        'name': 'Admin APIs',
        'description': 'Administration APIs. Create banking users, check activity, all that fun stuff.',
        'URLS': URLS
    }

    endpoints_json = json.dumps(endpoints)

    return endpoints_json, 200, {'Content-Type': 'application/json; charset=utf-8'}

@admin_api.route('/authenticate')
def authenticate():
    return '{"huh": "?"}', 200, {'Content-Type': 'application/json; charset=utf-8'}
