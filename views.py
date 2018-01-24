from main import app
from flask import Flask, request, render_template

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/profile/<name>')
def profile(name):
	return render_template("profile.html", name=name)

@app.route("/api/v1/users/create", methods=['POST'])
def create_user():

@app.route('/login', methods=['GET', 'POST'])
def login():
	return "poop"