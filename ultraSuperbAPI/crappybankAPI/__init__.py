from flask import Blueprint, render_template, abort, request, url_for, g
from jinja2 import TemplateNotFound
import json
from ultraSuperbAPI import api
from ultraSuperbAPI.api import db
from ultraSuperbAPI.authAPI import helpers as auth_helpers
from ultraSuperbAPI.helpers import buildResponseDictionary, validJSON
from ultraSuperbAPI.models import auth_models, customer_models
from flask.ext.jsontools import jsonapi



crappybank_api = Blueprint('crappybank', __name__, template_folder='templates')

@crappybank_api.before_request
def authenticate():
    if 'Authorization' in request.headers:
        auth_state = auth_helpers.validateAccessToken(request.headers.get('Authorization'))
    else:
        return buildResponseDictionary(error={"error": "Unauthenticated"}), 403, {'Content-Type': 'application/json; charset=utf-8'}


    if auth_state["valid"]:
        g.user_state = {
            "user_id": auth_state["user_id"]
        }
    else:
        #Need this, as @jsonapi doesn't work here... it breaks.
        return buildResponseDictionary(error={"error": "Unauthenticated, please use token: header with the API key."}), 403, {'Content-Type': 'application/json; charset=utf-8'}


@crappybank_api.route('/')
def index():
    print(g.user_state)
    URLS = [
        {
            'URL': url_for('crappybank.index'),
            "methods": ["GET"],
            "description": "This endpoint, lists available endpoints and methods."
        },
        {
            'URL': url_for('crappybank.auth_check'),
            "methods": ["GET"],
            "description": "Validates the user's session token, shows the user's own name."
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
@jsonapi
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

    return {"data": data,"error": error}, responseCode, {'Content-Type': 'application/json; charset=utf-8'}

@crappybank_api.route("/customer/<int:cust_id>", methods=["GET","POST"])
@jsonapi
def customer_view(cust_id):
    """
    View customer data.
    """

    #Set these two to default to blank, so that they are always returned.
    data = {}
    error = {}


    #Look ma, no access control!

    if request.method == "GET":

        customer = customer_models.Customer.query.filter_by(user_id=cust_id).first()

        return {"data": customer.as_dict(),"error": error}

    elif request.method == "POST":



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

            #Assign values
            customer = customer_models.Customer.query.filter_by(user_id=cust_id).first()

            if "city" in requestJSON:
                customer.city = requestJSON["city"]

            if "street_address" in requestJSON:
                customer.street_address = requestJSON["street_address"]

            if "postcode" in requestJSON:
                customer.postcode = requestJSON["postcode"]

            if "state" in requestJSON:
                customer.state = requestJSON["state"]

            if "country" in requestJSON:
                customer.country = requestJSON["country"]

            if "email" in requestJSON:
                customer.email = requestJSON["email"]

            db.session.add(customer)
            db.session.commit()

            customer = customer_models.Customer.query.filter_by(user_id=cust_id).first()

            data = customer.as_dict()

            responseCode = 200


        return {"data": data,"error": error}, responseCode, {'Content-Type': 'application/json; charset=utf-8'}

@crappybank_api.route("/customer/<int:cust_id>/urls")
@jsonapi
def generate_customer_urls(cust_id):
    """
    Generate URLs which can be used in the UI (a shortcut, if you will.)
    """

    urls = {}

    error = {}

    urls["update_url"] = url_for("crappybank.customer_view", cust_id=cust_id)
    urls["accounts_url"] = url_for("crappybank.get_accounts", cust_id=cust_id)

    return {"data": urls, "error": ""}

#Let a customer view accounts they own.
@crappybank_api.route("/customer/<int:cust_id>/accounts")
@jsonapi
def get_accounts(cust_id):
    error = {}
    data = {}

    customer = customer_models.Customer.query.filter_by(id=cust_id).first()

    if customer == None:
        return {"data": {}, "error": {"error": "Invalid customer ID."}}

    accounts = []

    for account in customer.accounts:
        accounts.append(account.as_dict())

    data = {"accounts": accounts}

    return {"data": data, "error": error}

@crappybank_api.route("/transactions/create", methods=["POST"])
@jsonapi
def create_transaction():
    error = {}
    data = {}
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

    tran_type = ""

    from_account = requestJSON["from_account"]
    to_account = requestJSON["to_account"]
    amount = requestJSON["amount"]

    account = customer_models.Account.query.filter_by(id=from_account).first()

    pending_transaction = customer_models.PendingTransaction(account_id=account.id, to_account=to_account, amount=float(amount), tran_type="debit")

    pending_id = pending_transaction.id

    db.session.add(pending_transaction)
    db.session.commit()
    pending_id = pending_transaction.id
    pending_transaction = customer_models.PendingTransaction.query.filter_by(id=pending_id).first()

    return {"data": pending_transaction.as_dict(), "error": {}}

@crappybank_api.route("/transactions/pending/<int:acct_id>")
@jsonapi
def get_pending_transactions(acct_id):

    account = customer_models.Account.query.filter_by(id=acct_id).first()

    pending_transactions = []

    for pend_tran in account.pending_transactions:
        pending_transactions.append(pend_tran.as_dict())

    return {"data": pending_transactions, "error": {}}

@crappybank_api.route("/transactions/<int:acct_id>")
@jsonapi
def get_transactions(acct_id):

    account = customer_models.Account.query.filter_by(id=acct_id).first()

    transactions = []

    for tran in account.transactions:
        transactions.append(pend_tran.as_dict())

    return {"data": transactions, "error": {}}
