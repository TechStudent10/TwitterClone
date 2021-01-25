from flask import Blueprint, session, request, redirect, url_for
from models import User
import randomCode

api = Blueprint("API Views", __name__)
users = {
	"Post Bot": {
		"username": "Post Bot",
		"password": "admin",
		"user_id": "PostBotAdminLol",
	}
}
posts = {
	"Post Bot": {
		"WelcomeToPostBot": {
			'name': "I am Post Bot.",
			'author': "Post Bot",
			'body': "I am Post Bot! I am basically the TwitterClone admin. Please don't comment on any posts!",
			'comments': {
				"Comment1": {
					"unique_id": "Comment1", 
					"commenter": "Post Bot", 
					"comment": "Don't comment!"
				}
			},
			'unique_id': "WelcomeToPostBot"
		}
	}
}

def generateSessionKey(length=6):
	session_key = randomCode.generate(length)
	session['session_key'] = session_key

	return session_key

@api.route("/signup", methods=['POST'])
def signup():
	username = request.form.get('username')
	password = request.form.get('password')
	
	'''
	user = User(username=username, password=password)
	db.session.add(user)
	db.session.commit()
	'''

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

	'''
	users = User.query.filter_by(username=username, password=password).all()
	if len(users) <= 0:
		return "User doesn't exist".
	else:
		user = User.query.filter_by(username=username, password=password).first()
		session['current_user'] = user
		return redirect(url_for("User Views.userPage", user_id=user.id, session_id=user.id))

	'''
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
		'comments': {},
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
	return {
		'name': "404: Post Not Found",
		'author': "Post Bot",
		'body': "This post was not found. Maybe reload the post. See if it pops up.",
		'comments': {},
		'unique_id': "404PostNotFound"
	}, 404

@api.route("/insertComment", methods=['POST'])
def insertComment():
	form = request.form

	post_id = form.get('post_id')
	username = form.get('username')
	comment = form.get('comment')
	poster = form.get('poster')

	if poster in users:
		if post_id in posts[poster]:
			code = randomCode.generate()
			posts[poster][post_id]['comments'][code] = {"unique_id": code, "commenter": username, "comment": comment}
			return redirect(url_for('User Views.showPost', user_id=username, post_id=post_id, author=poster))
	return '', 404

@api.route("/getComments", methods=['POST'])
def getComments():
	form = request.form

	poster = form.get('poster')
	post_id = form.get('post_id')

	if poster in users:
		if post_id in posts[poster]:
			return posts[poster][post_id]['comments']
	return {"unique_id": "PostNotFound", "commenter": "Post Bot", "comment": "Comment Error"}