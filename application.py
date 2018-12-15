#!/usr/bin/env python

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
    if 'username' in login_session:
        user_id = getUserID(login_session['email'])
        user = session.query(User).filter_by(id=user_id).one()
        return render_template('items.html', items=items,
                               category=category, user=user)
    else:
        return render_template('items.html', items=items,
                               category=category)


@app.route('/category/list/')
def allCategories():
    categories = session.query(Category).all()
    if 'username' in login_session:
        user_id = getUserID(login_session['email'])
        user = session.query(User).filter_by(id=user_id).one()
        return render_template('categories.html',
                               categories=categories, user=user)
    else:
        return render_template('categories.html', categories=categories)


@app.route('/category/new/', methods=['GET', 'POST'])
def newCategory():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newCategory = Category(
            name=request.form['name'], user_id=login_session['user_id'])
        session.add(newCategory)
        flash('New Category %s added successfully' % newCategory.name)
        session.commit()
        return redirect(url_for('allCategories'))
    else:
        return render_template('Category/new.html')


@app.route('/category/edit/<int:category_id>/', methods=['POST', 'GET'])
def editCategoryByID(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if category.user_id != login_session['user_id']:
        return """<script>
        function myFunction() {
        alert('You are not authorized to edit this category!.
        Please create your own category in order to edit.');
        }</script><body onload='myFunction()'>"""
    if request.method == 'POST':
        if request.form['name']:
            category.name = request.form['name']
            flash('Category %s updated successfully!' % category.name)
            return redirect(url_for('allCategories'))
    return render_template('Category/edit.html', category=category)


@app.route('/category/delete/<int:category_id>/', methods=['POST', 'GET'])
def deleteCategoryByID(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if category.user_id != login_session['user_id']:
        return """<script>
        function myFunction() {
        alert('You are not authorized to delete this category!);
        }</script><body onload='myFunction()'>"""
    if request.method == 'POST':
        session.delete(category)
        flash('%s deleted successfully!' % category.name)
        session.commit()
        return redirect(url_for('allCategories'))
    else:
        return render_template('Category/delete.html', category=category)


@app.route('/item/new/<int:category_id>/', methods=['POST', 'GET'])
def newItem(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        item = Item(name=request.form['name'],
                    description=request.form['description'],
                    price=request.form['price'],
                    category_id=category.id, user_id=login_session['user_id'])
        session.add(item)
        flash('%s Added successfully!' % item.name)
        session.commit()
        return redirect(url_for('listItems', category_id=category.id))
    return render_template('Item/new.html', category=category)


@app.route('/item/edit/<int:item_id>/', methods=['POST', 'GET'])
def editItemByID(item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    category = session.query(Category).filter_by(id=item.category_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if item.user_id != login_session['user_id']:
        return """<script>
        function myFunction() {
        alert('You are not authorized to edit this item!.
        Please create your own item in order to edit.');
        }</script><body onload='myFunction()'>"""
    if request.method == 'POST':
        item.name = request.form['name']
        item.description = request.form['description']
        item.price = request.form['price']
        session.add(item)
        session.commit()
        flash('Item updated successfully')
        return redirect(url_for('listItems', category_id=category.id))
    else:
        return render_template('/Item/edit.html', item=item, category=category)


@app.route('/item/delete/<int:item_id>/', methods=['POST', 'GET'])
def deleteItemByID(item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    category = session.query(Category).filter_by(id=item.category_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if item.user_id != login_session['user_id']:
        return """<script>
        function myFunction() {
        alert('You are not authorized to edit this item!.');
        }</script><body onload='myFunction()'>"""
    if request.method == 'POST':
        session.delete(item)
        flash('%s deleted successfully' % item.name)
        session.commit()
        return redirect(url_for('listItems', category_id=category.id))
    else:
        return render_template('/Item/delete.html',
                               item=item, category=category)


@app.route('/category/JSON/')
@app.route('/category/json/')
def categoriesJson():
    categories = session.query(Category).all()
    return jsonify(categories=[r.serialize for r in categories])


@app.route('/category/<int:category_id>/items/json/')
def itemsListJson(category_id):
    items = session.query(Item).filter_by(category_id=category_id).all()
    return jsonify(items=[i.serialize for i in items])


# @app.route('/users/json')
# def users():
#    users = session.query(User).all()
#    return jsonify(users=[u.serialize for u in users])


@app.route('/login')
def login():
    state = ''.join(
        random.choice(string.ascii_uppercase +
                      string.digits) for x in range(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code, now compatible with Python3
    request.get_data()
    code = request.data.decode('utf-8')

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    # Submit request, parse response - Python3 compatible
    h = httplib2.Http()
    response = h.request(url, 'GET')[1]
    str_response = response.decode('utf-8')
    result = json.loads(str_response)

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += """ style = "width: 300px; height: 300px;
    border-radius: 150px;-webkit-border-radius: 150px;
    -moz-border-radius: 150px;"> """
    flash("you are now logged in as %s" % login_session['username'])
    return output

# User Helper Functions


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except Exception:
        return None

# DISCONNECT - Revoke a current user's token and reset their login_session


@app.route('/gdisconnect')
def gdisconnect():
        # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        # Reset the user's sesson.
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return redirect(url_for('home'))
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
