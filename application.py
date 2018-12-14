from flask import Flask, render_template, request
from flask import redirect, jsonify, url_for, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, User, Category, Item
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
from flask_bootstrap import Bootstrap
import requests
from datetime import datetime

app = Flask(__name__)
Bootstrap(app)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Item catalog"

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/category/list/')
def allCategories():
    return 'List all categories'


@app.route('/category/new/')
def newCategory():
    return 'New category view'


@app.route('/category/edit/<int:category_id>/')
def editCategoryByID(category_id):
    return 'Edit category by ID view'


@app.route('/category/delete/<int:category_id>/')
def deleteCategoryByID(category_id):
    return 'Delete category by ID view'


@app.route('/item/new/<int:category_id>/')
def newItem(category_id):
    return 'Create new item under category'


@app.route('/item/edit/<int:item_id>/')
def editItemByID(item_id):
    return 'Edit item by ID'


@app.route('/item/delete/<int:item_id>/')
def deleteItemByID(item_id):
    return 'Delete item by ID'


@app.route('/login')
def login():
    return 'here go login screen'


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
