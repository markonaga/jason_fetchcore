#for debug:
from __future__ import print_function # In python 2.7
import sys

from flask import Flask, request, render_template, url_for, redirect, session
from flask_assets import Bundle, Environment
import requests
import os

# fetchcore imports
from fetchcore import configuration
from fetchcore.resources.maps import Map
from fetchcore.resources.robots import Robot
# from fetchcore.resources.actions import NavigateAction
from fetchcore.resources import Task


app = Flask(__name__)
app.secret_key = os.urandom(24)

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
@app.route('/login/', methods=['POST'])
def login():
	if request.method == 'POST':
		session['username'] = request.form.get('username', None)
		session['password'] = request.form.get('pass', None)
		session['hostIP'] = request.form.get('hostIP', None)

		return redirect(url_for('connectfetch'))

	return render_template('login.html')

		
#Connect to  fetchcore for authorization token
@app.route('/connectfetch/')
def connectfetch():
	port = 443
	ssl = True

    # Connect to Fetchcore using your credentials
	try:
		configuration.initialize_global_client(session['username'], session['password'], session['hostIP'], port, ssl)
		print("Authorized")
		return redirect(url_for('displayrobots'))
	except:
		print("You are not authorized. Check your login credentials and try again.")
		print(url, session['username'], session['password'])
	return redirect(url_for('clearsession'))
	
#Clear session and require new login
@app.route('/clearsession/')
def clearsession():
	session.pop('username', None)
	session.pop('password', None)
	session.pop('hostIP', None)
	session.pop('token', None)
	return redirect(url_for('index'))
	
#Get robot information (IDs, Poses) using SDK
@app.route('/displayrobots/')
def displayrobots():
	# robotlist = {'robot1': ['pose1', 'pose2', 'pose3'],
	#  'robot2': ['pose21', 'pose22', 'pose23'],
	#  'robot3': ['pose31', 'pose32', 'pose33'],
	#  'robot4': ['pose41', 'pose42', 'pose43', 'pose53']}

	#Get a list of every robot
	robots = Robot.list()

	#Create dictionary object to store {"freight1: [pose1,pose2], ..."}
	robot_dict = {}
	for robot in robots:
		#Get each robots map
		robots_map = robot.map

    	#Temporary list to append pose names
		temp = []

    	#Get poses from each map and append to list
		for pose in robots_map.poses:
			temp.append(pose.name)

    	#Store pose list corresponding to robot key
		robot_dict[robot.name] = temp
		print(robot.name)

	return render_template('robots.html', robotlist=robot_dict)

@app.route('/sendpose/<int:number>')
def sendpose(number):
	return "Sending to Pose: " + number


@app.route('/profile/<name>')
def profile(name):
	return render_template("profile.html", name=name)
	

if __name__ == '__main__':
	app.run(debug=True)




