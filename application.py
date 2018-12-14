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

engine = create_engine('sqlite:///catalog.db?check_same_thread=False')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.context_processor
def inject_now():
    return {'now': datetime.now()}


@app.route('/')
def home():
    categories = session.query(Category).order_by(
        Category.date_added.desc())
    items = session.query(Item).order_by(Item.date_added.desc()).limit(9)
    return render_template('index.html', categories=categories, items=items)


def latestCategories():
    return render_template('sidemenu.html', categories=categories)


@app.route('/category/<int:category_id>/items/')
def listItems(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category_id).all()
    return render_template('items.html', items=items, category=category)


@app.route('/category/list/')
def allCategories():
    categories = session.query(Category).all()
    return render_template('categories.html', categories=categories)


@app.route('/category/new/')
def newCategory():
    return render_template('Category/new.html')


@app.route('/category/edit/<int:category_id>/')
def editCategoryByID(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    return render_template('Category/edit.html', category=category)


@app.route('/category/delete/<int:category_id>/')
def deleteCategoryByID(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    return render_template('Category/delete.html', category=category)


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
