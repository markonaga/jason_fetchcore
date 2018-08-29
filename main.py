# for debug:
from __future__ import print_function # In python 2.7
import sys
from datetime import datetime

# Flask imports
from flask import Flask, request, render_template, url_for, redirect, session, flash
import requests
import os
import json
import time

from http_req import get_robots, create_nav_action

app = Flask(__name__)

# Set the APP_SETTINGS environment variable in VENV with terminal 
# export APP_SETTINGS="config.DevelopmentConfig" 
# export APP_SETTINGS="config.ProductionConfig"
app.config.from_object(os.environ['APP_SETTINGS'])


@app.route('/')
def index():
	if session.get('Token'):
		# Login information saved from previous use:
		return redirect(url_for('displayrobots'))

	return render_template("login.html")


# Get user info and saves to the session
@app.route('/login/', methods=['POST'])
def login():
	if request.method == 'POST':
		session['username'] = request.form.get('username', 'default_user')
		session['password'] = request.form.get('pass', 'default_pass')
		session['hostIP'] = request.form.get('hostIP', 'default_ip')
		session['robot_names'] = []
		session['robot_poses'] = {}
		session['pose_dict'] = {}
		session.permanent = True
		
		return redirect(url_for('connectfetch'))

	return render_template('login.html')

		
# Connect to Fetchcore for authorization token
@app.route('/connectfetch/')
def connectfetch():
	error = ''
	port = 443
	ssl = True
	url = 'https://' + session['hostIP'] + '/api/v1/auth/login/'
	payload = {'username' : session['username'], 'password' : session['password']}

	# Connect to Fetchcore using the REST API
	for i in range(5):
		try:
			r = requests.post(url, data = payload, verify = None)
			json_data = json.loads(r.text)
			session['Token'] = 'Token ' + json_data['token']

		except Exception as error:
			# error = "You are not authorized. Check your login credentials and try again."
			time.sleep(1)
			if i == 4:
				return redirect(url_for('clearsession', e = error))
		else:
			# If the try block succeeds, redirect to display robots
			return redirect(url_for('displayrobots'))

	return redirect(url_for('clearsession', e = error))
	

# Clear session and require new login
@app.route('/clearsession/<e>')
def clearsession(e):
	session.clear()
	flash(e)
	return render_template("login.html")
	

# Get robot information (IDs, Poses) using SDK
@app.route('/displayrobots/')
def displayrobots():
	# Get a list of every robot: populates session['robot_names'], session['robot_poses'], session['pose_dict']

	# Check if the user already has robot data cached in their session cookie
	if not session['robot_names']:
		try:
			# Should catch the case where the session token is present but expired
			get_robots()

		except Exception as error:
			return redirect(url_for('clearsession', e = error))

	selected_robot = session['robot_names'][0]

	return render_template('robots.html', robotlist = session['robot_names'], 
						   				  selected_robot = selected_robot,
						   				  robot_poses = session['robot_poses'][selected_robot])

# Creates a navtask to send robot to requested pose
@app.route('/sendpose/<robotdata>')
def sendpose(robotdata):
	# Robotdata is in the form "robot_name+pose_name"
	data = robotdata.split('+')
	robot_n = data[0] 
	pose_n = data[1]

	response = create_nav_action(robot_n, session['pose_dict'][pose_n])	

	if response == 201:
		# Notify the user that their request has been processed

		flash("Sent " + robot_n + " to " + pose_n + " at " + str(datetime.utcnow()))

	else:
		# Notify the user that their request has failed
		flash('Failed to create Nav Action, reason: ' + str(response))
		

	

	return render_template('robots.html', robotlist = session['robot_names'], 
						   				  selected_robot = robot_n,
						   				  robot_poses = session['robot_poses'][robot_n])


@app.route('/displaynext/<selected_robot>')
def displaynext(selected_robot):

	return render_template('robots.html', robotlist = session['robot_names'], 
						   				  selected_robot = selected_robot,
						   				  robot_poses = session['robot_poses'][selected_robot])


# Dummy route for testing
@app.route('/profile/<name>')
def profile(name):
	flash(name)
	return render_template("profile.html", name=name)


# @app.route('/test/')
# def test():
# 	get_robots()
# 	# GetPoses():
# 	return session['robot_names'][0]
	

if __name__ == '__main__':
	app.run()




