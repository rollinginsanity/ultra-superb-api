from flask import Blueprint, render_template, abort, url_for, request
from jinja2 import TemplateNotFound
import json
from ultraSuperbAPI.loggy import crappyLog
from flask.ext.jsontools import jsonapi

admin_api = Blueprint('admin', __name__, template_folder='templates')


@admin_api.route('/logs', methods=["POST"])
@jsonapi
def logsey():
    #What the? Look at this. It takes user input for the logfile display back to the user. Whyyy?
    requestJSON = request.json
    #What? So adding .log to the command should stop injection? Nope, use one of #theseones '#' to escape.
    last_20_logs = crappyLog.view_logs(requestJSON["logfile"]+".log").splitlines()

    logs = []

    for log in last_20_logs:
        logs.append(log)


    return {"logs": logs}, 200, {'Content-Type': 'application/json; charset=utf-8'}
