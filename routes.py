from app import app
from flask import render_template, request, make_response
from logic import *
import json

logic = Logic()

@app.route('/')
@app.route('/index', methods=['GET'])

def index():
    logic.init()
    return render_template('index.html')

@app.route('/customer', methods=['GET'])
def customer():
    return render_template('customer.html')

@app.route('/customer', methods=['POST'])
def customer_post():
    name = request.form['name']
    document = request.form['document']
    gender = request.form['gender']
    birthday = request.form['birthday']
    newCustomer = logic.create_user(name, document, gender, birthday)
    return render_template('customer.html', newCustomer=newCustomer)

@app.route('/account', methods=['GET'])
def account():
    return render_template('account.html')

@app.route('/account', methods=['POST'])
def account_post():
    document = request.form['document']
    accountType = request.form['bankAccountType']
    initialBalance = float(request.form['initial_balance'])
    logic.open_account(document, accountType, initialBalance)
    return render_template('account.html')

@app.route('/bankinterest', methods=['GET'])
def bankinterest():
    return render_template('bankinterest.html')

@app.route('/withdraw', methods=['GET'])
def withdraw():
    return render_template('withdraw.html')

@app.route('/deposit', methods=['GET'])
def deposit():
    return render_template('deposit.html')

@app.route('/deposit', methods=['POST'])
def deposit_post():
    document = request.form['document']
    value = float(request.form['value'])
    bankAccount = logic.deposit(document, value)    
    return render_template('deposit.html', bankAccount=bankAccount)

@app.route('/bankstatement', methods=['GET'])
def bankstatement():
    return render_template('bankstatement.html')

@app.route('/bankAccount/<document>', methods=['GET'])
def getBankAccountByDocument(document):
    bankAccount = logic.get_bankaccount_by_document_or_error(document=document)
    return make_response(json.dumps({ 'balance': bankAccount.balance, 'name': bankAccount.customer.name}), 200, default_headers())

def default_headers():
    return {"Content-Type": "application/json"}