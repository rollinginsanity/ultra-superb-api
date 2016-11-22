from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
import json
from ultraSuperbAPI import api
import urllib

customer_api = Blueprint('customer', __name__, template_folder='templates')

@customer_api.route('/')
def index():

    endpoints = []
    for rule in api.url_map.iter_rules():
        methods = ','.join(rule.methods)
        line = urllib.unquote("{:50s} {:20s} {}".format(rule.endpoint, methods, rule))
        endpoints.append(line)

    endpoints_json = json.dump(endpoints)

    return endpoints_json, 200, {'Content-Type': 'application/json; charset=utf-8'}
