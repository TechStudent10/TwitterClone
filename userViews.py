from flask import Blueprint, render_template, session, redirect, url_for
import requests
import importlib

user = Blueprint("User Views", __name__)

@user.route("/signup")
def signup():
	return render_template("signup.html")

@user.route("/login")
def login():
	if 'current_user' in session:
		apiModule = importlib.import_module('api')
		if frozenset(session['current_user']) in apiModule.users:
			return redirect(url_for('userPage', user_id=session['current_user']['username']))
		else:
			pass

	return render_template("login.html")

@user.route("/user/<user_id>")
def userPage(user_id):
	try:
		user = requests.post('http://127.0.0.1:5000/api/getUser', {'user_id': user_id}).json()
		del user['password']
		return render_template("user.html", user=user, session_id=session['session_key'])
	except Exception as e:
		print(e)
		return "User doesn't exist."

@user.route("/createNewPost")
def createNewPost():
	return render_template("createNewPost.html")

@user.route("/user/<user_id>/posts")
def listUserPosts(user_id):
	'''
	try:
		return render_template("posts.html", posts=requests.post('http://127.0.0.1:5000/api/getPosts', {'user_id': user_id}).json())
	except Exception as e:
		print(e)
		return "This user has no posts."
	'''
	return render_template("posts.html", posts=requests.post('http://127.0.0.1:5000/api/getPosts', {'user_id': user_id}).json())

@user.route("/user/<user_id>/post/<post_id>")
def showPost(user_id, post_id):
	try:
		try:
			comments = requests.post("http://127.0.0.1:5000/api/getComments", {'poster': user_id, 'post_id': post_id}).json()
		except Exception as e:
			comments = {'RandomCode':{'unique_id': 'RandomCode', 'commenter': 'Post Bot', 'comment': "No Comments"}}
		return render_template("post.html", post=requests.post('http://127.0.0.1:5000/api/getPost', {'post_id': post_id, 'user_id': user_id}).json(), user_id=session['current_user']['username'], comments=comments)
	except Exception as e:
		print(e)
	return "Post doesn't exist."

@user.route("/listUsers")
def listUsers():
	try:
		users = requests.post('http://127.0.0.1:5000/api/getUsers').json()
		for user in users:
			del users[user]['password']
			del users[user]['user_id']
			users[user]['user_url'] = "/user/" + users[user]['username']
		return users
	except Exception as e:
		print(e)
		return "No Users found."