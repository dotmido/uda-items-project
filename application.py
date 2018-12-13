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
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Item catalog"

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
def home():
    return 'here goes homepage'


@app.route('/category/list/')
def allCategories():
    return 'List all categories'


@app.route('/category/new/')
def newCategory():
    return 'New category view'


@app.route('/category/edit/<int:category_id>/')
def editCategoryByID():
    return 'Edit category by ID view'


@app.route('/category/delete/<int:category_id>/')
def deleteCategoryByID():
    return 'Delete category by ID view'


@app.route('/item/new/<int:category_id>/')
def newItem():
    return 'Create new item under category'


@app.route('/item/edit/<int:item_id>/')
def editItemByID():
    return 'Edit item by ID'


@app.route('/item/delete/<int:item_id>/')
def deleteItemByID():
    return 'Delete item by ID'


@app.route('/login')
def login():
    return 'here go login screen'


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
