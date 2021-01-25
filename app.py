from flask import Flask, render_template, session, request, redirect, url_for
from models import User, Post, Comment
from flask_sqlalchemy import SQLAlchemy

from userViews import user
from api import api

import randomCode
import requests
import datetime

app = Flask(__name__)
app.secret_key = "1234"
app.register_blueprint(user)
app.register_blueprint(api, url_prefix="/api")

'''
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

db = SQLAlchemy(app)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(50))
	password = db.Column(db.String(50))
	date_created = db.Column(db.DateTime, default=datetime.datetime.now)
'''

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