# for debug:
from __future__ import print_function # In python 2.7
import sys
from datetime import datetime

# Flask imports
from flask import Flask, request, render_template, url_for, redirect, session, flash
from flask_assets import Bundle, Environment
import requests
import os

# Fetchcore imports
from fetchcore import configuration
from fetchcore.resources.maps import Map
from fetchcore.resources.robots import Robot
from fetchcore.resources.tasks.actions.definitions import NavigateAction
from fetchcore.resources import Task


app = Flask(__name__)
app.secret_key = os.urandom(24)

# Bundle my js files
js = Bundle('login.js', 'jquery-3.2.1.min.js', 'js/bootstrap.min.js',  output='gen/main.js')
assets = Environment(app)

# Register bundle name to be used in template
assets.register('main_js', js)

# Global robot dictionary for optimization purposes
robot_dict = {}

@app.route('/')
def index():
	if session.get('logged_in'):
		# Login information saved from previous use:
		return redirect(url_for('connectfetch'))

	return render_template("login.html")


# Get user info and saves to the session
@app.route('/login/', methods=['POST'])
def login():
	if request.method == 'POST':
		session['username'] = request.form.get('username', None)
		session['password'] = request.form.get('pass', None)
		session['hostIP'] = request.form.get('hostIP', None)

		return redirect(url_for('connectfetch'))

	return render_template('login.html')

		
# Connect to Fetchcore for authorization token
@app.route('/connectfetch/')
def connectfetch():
	error = ''
	port = 443
	ssl = True

    # Connect to Fetchcore using your credentials
	try:
		configuration.initialize_global_client(session['username'], session['password'], session['hostIP'], port, ssl)
		session['logged_in'] = True
		return redirect(url_for('displayrobots'))

	except:
		error = "You are not authorized. Check your login credentials and try again."

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

	#Get a list of every robot
	robots = Robot.list()

	for robot in robots:
		# Get each robots map
		robots_map = robot.map

    	# Temporary list to append pose names
		temp = []

    	# Get poses from each map and append to list
		for pose in robots_map.poses:
			temp.append(pose)

    	# Store pose list corresponding to robot key in global dictionary
		robot_dict[robot.name] = temp

	return render_template('robots.html', robotlist=robot_dict)


# Creates a navtask to send robot to requested pose
@app.route('/sendpose/<robotdata>')
def sendpose(robotdata):
	# Robotdata is in the form "robot_name+pose_name"
	data = robotdata.split('+')
	robot_n = data[0] 
	pose_n = data[1]

	# Get the entire pose object from our saved dictionary
	pose = [elem for elem in robot_dict[robot_n] if elem.name == pose_n]

	goal_pose = {
		"x": pose[0].x,
		"y": pose[0].y,
		"theta": pose[0].theta
		}

	# Create nav action
	nav_action = NavigateAction(goal_pose=goal_pose)

    # Create nav task
	nav_task = Task(name="Nav to Poses", type="NAVIGATE",
                    actions=[nav_action], robot=robot_n)

    # Save task to update remote server
	nav_task.save()

	# Notify the user that their request has been processed
	flash("Sent " + robot_n + " to " + pose_n + " at " + str(datetime.utcnow()))

	return render_template('robots.html', robotlist=robot_dict)


# Dummy route for testing
@app.route('/profile/<name>')
def profile(name):
	flash(name)
	return render_template("profile.html", name=name)
	

if __name__ == '__main__':
	app.run(debug=True)




