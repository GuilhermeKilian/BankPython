from app import app
from flask import render_template 
@app.route('/')
@app.route('/account')
@app.route('/bankinterest')
@app.route('/customer')
@app.route('/withdraw')
@app.route('/deposit')
@app.route('/account')

def index():
    return render_template('index.html')
def account():
    return render_template('account.html')
def bankinterest():
    return render_template('bankinterest.html')
def customer():
    return render_template('customer.html')
def withdraw():
    return render_template('withdraw.html')
def deposit():
    return render_template('deposit.html')
