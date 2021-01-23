from flask import Blueprint, session, request, redirect, url_for
from models import User
import randomCode

api = Blueprint("API Views", __name__)
users = {}
posts = {}

def generateSessionKey(length=6):
	session_key = randomCode.generate(length)
	session['session_key'] = session_key

	return session_key

@api.route("/signup", methods=['POST'])
def signup():
	username = request.form.get('username')
	password = request.form.get('password')
	
	user = {
		"username": username,
		"password": password,
		"user_id": session['session_key'] if 'session_key' in session else generateSessionKey(),
	}

	users[user['username']] = user
	posts[user['username']] = {}

	return redirect(url_for('User Views.login'))

@api.route("/login", methods=['POST'])
def login():
	form = request.form

	username = form.get('username')
	password = form.get('password')

	if username in users:
		session['current_user'] = users[username]
		users[username]['user_id'] = session['session_key']
		return redirect(url_for('User Views.userPage', user_id=session['current_user']['username'], session_id=username))
	return "User doesn't exist."

@api.route("/createPost", methods=['POST'])
def createPost():
	form = request.form

	name = form.get('name')
	body = form.get('body')
	key = randomCode.generate(length=9)

	posts[session['current_user']['username']][key] = {
		'name': name,
		'author': session['current_user']['username'],
		'body': body,
		'unique_id': key
	}

	return redirect(url_for("User Views.showPost", user_id=session['current_user']['username'], post_id=key)), 201

@api.route("/getUsers", methods=['POST'])
def getUsers():
	return users, 200

@api.route("/getUser", methods=['POST'])
def getUser():
	user_id = request.form.get('user_id')
	if user_id in users:
		return users[user_id]
	return "", 404

@api.route("/getPosts", methods=['POST'])
def getPosts():
	form = request.form

	user_id = form.get('user_id')
	if user_id in users:
		return posts[user_id]
	return "User doesn't exist."

@api.route("/getPost", methods=['POST'])
def getPost():
	form = request.form

	post_id = form.get('post_id')
	user_id = form.get('user_id')

	if post_id in posts[user_id]:
		return posts[user_id][post_id]
	return "", 404