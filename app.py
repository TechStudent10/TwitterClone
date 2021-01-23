from flask import Flask, render_template, session, request, redirect, url_for
from models import User, Post, Comment

from userViews import user
from api import api

import randomCode
import requests

app = Flask(__name__)
app.secret_key = "1234"
app.register_blueprint(user)
app.register_blueprint(api, url_prefix="/api")

# Stuff That Should Be Executed Before Rendering
def STSBEBR():
	if 'session_key' not in session:
		session['session_key'] = randomCode.generate()

@app.route("/")
def home():
	STSBEBR()
	return render_template("index.html")

@app.route("/list")
def listUsers():
	STSBEBR()
	return requests.post("http://127.0.0.1:5000/api/getUsers").json()

if __name__ == "__main__":
	app.run(debug=True)