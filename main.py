#for debug:
from __future__ import print_function # In python 2.7
import sys

from flask import Flask, request, render_template, url_for, redirect, session
from flask_cors import CORS, cross_origin
from flask_assets import Bundle, Environment
import requests
import os


app = Flask(__name__)
app.secret_key = os.urandom(24)
CORS(app)

#Bundle my js files
js = Bundle('login.js', 'jquery-3.2.1.min.js', 'js/bootstrap.min.js',  output='gen/main.js')
assets = Environment(app)

#register bundle name to be used in template
assets.register('main_js', js)

@app.route('/')
def index():
	if 'username' in session:
		#Login succeeded
		return redirect(url_for('displayrobots'))

	return render_template("login.html")


#Get user info and saves to the session
@app.route('/login', methods=['POST'])
def login():
	if request.method == 'POST':
		session['username'] = request.form.get('username', None)
		session['password'] = request.form.get('password', None)
		session['hostIP'] = request.form.get('hostIP', None)

		return redirect(url_for('connectfetch'))

	return render_template('login.html')

		
#Connect to  fetchcore for authorization token
@cross_origin
@app.route('/connectfetch')
def connectfetch():
	#Connect to fetchcore
	url = "https://" + session['hostIP'] + "/api/v1/auth/login/"
	response = requests.post(url, data={'username': session['username'], 
		'password': session['password'], "Content-Type": "application/json"}, allow_redirects=False)
	
	if response.status_code != 200:							#CHANGE THIS BACK WHEN AUTHORIZATION IS FIXED!!!!!!
		#Got authorization token
		print(response.status_code, response.reason, response.text)
		return redirect(url_for('displayrobots'))

	#Authorization failed due to incorrect credentials
	return redirect(url_for('clearsession'))


#Clear session and require new login
@app.route('/clearsession')
def clearsession():
	session.pop('username', None)
	session.pop('password', None)
	session.pop('hostIP', None)
	session.pop('token', None)
	return redirect(url_for('index'))
	

@app.route('/displayrobots')
def displayrobots():
	#Get robot information (IDs, Poses) using SDK
	robotlist = ["domo", "arigatou", "mister", "roboto"]
	return render_template('robots.html', robotlist=robotlist)


@app.route('/profile/<name>')
def profile(name):
	return render_template("profile.html", name=name)

@app.route("/api/v1/users/create/", methods=['POST'])
def create_user():
	return "poop"

	

if __name__ == '__main__':
	app.run(debug=True)




