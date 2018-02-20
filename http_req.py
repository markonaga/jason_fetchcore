from flask import session
import requests
import json
import time


# header = {'AUTHORIZATION' : 'Token 5fef8810c6692d339a472def4814d2d7fc7db110', 
		# 'content-type' : 'application/json',
		# 'Accept-Language' : 'jp'} 

# robot_names = []
# robot_poses = {}
# pose_dict = {}

# Get a list of all available robots and poses on a specified Fetchcore instance
def get_robots():

	# Configure the URL endpoint
	url = 'https://' + session['hostIP']+ '/api/v1/robots'
	# url = 'https://softbank.fetchcore-cloud.com/api/v1/robots'

	# Make the request (multiple times in case where there is a 500 error)
	for i in range(5):
		try:
			robot_req = requests.get(url, headers={'AUTHORIZATION' : session['Token']}, timeout = 10)
			# robot_req = requests.get(url, headers=header, timeout = 10)

		except Exception as error:
			time.sleep(.5)
			if i == 5:
				return error

		else:
			# Break out of the loop and parse response
			break

	
	# Convert response data to JSON object
	data = json.loads(robot_req.text)

	# Pull out the results key from the JSON object
	results = data['results']

	# Parse through JSON object and extract out robot_names
	for index, robo_dict in enumerate(results):

		# Get the relevant data from each Robot in the Robots endpoint
		name = robo_dict['name']
		map_id = robo_dict['map']

		# Append the names to our robot list for use in Jinja Template
		session['robot_names'].append(robo_dict['name'])
		# robot_names.append(name)

		# Pass in the map ID and get the list of poses corresponding to that robot's map
		session['robot_poses'][name] = get_poses(map_id)
		# robot_poses[name] = get_poses(map_id)

	# print(robot_names)
	# print(robot_poses)


# Returns a list of poses from specified map 
def get_poses(map_id):

	# Temporary list for storing the pose names
	pose_names = []

	# Configure the URL endpoint
	url = 'https://' + session['hostIP'] + '/api/v1/maps/' + str(map_id) + '/annotations'
	# url = 'https://softbank.fetchcore-cloud.com/api/v1/maps/' + str(map_id) + '/annotations'
	
	# Make the request (multiple times in case where there is a 500 error)
	for i in range(5):
		try:
			map_req = requests.get(url, headers={'AUTHORIZATION' : session['Token']}, timeout = 10)
			# map_req = requests.get(url, headers=header, timeout = 10)

		except Exception as error:
			time.sleep(.5)
			if i == 4:
				return error

		else:
			# Break out of the loop and parse response
			break

	# Convert response data to JSON object
	raw_json = json.loads(map_req.text)

	# Pull 'poses' dictionary from body 
	data = raw_json[5]

	# Pull out list from the dictionary
	pose_list = data['poses']

	# Get each of the pose names and append to a list
	for index, pose in enumerate(pose_list):
		pose_name = pose['name']
		pose_names.append(pose_name)
		session['pose_dict'][pose_name] = pose['id']

	return pose_names


def create_nav_action(robot_name, pose_id):
	# username ='jvranek@innovation-matrix.com'
	# Configure the URL endpoint
	# url = 'https://softbank.fetchcore-cloud.com/api/v1/tasks/'
	url = 'https://' + session['hostIP']+ '/api/v1/tasks/'

	# Configure the body of the request 
	nav_template = {
		'actions' : 
			[{
				'action_definition' : 'NAVIGATE',
	    		'inputs' : {
				    'limit_velocity' : True,
				    'max_angular_velocity' : 2.5,
				    'max_velocity' : 1.5,
			    	'pose_id' : pose_id,
	    			},
	    		'preemptable' : 'HARD',
			    'status' : 'NEW'
			}],
	    'requester' : session['username'],
	    'robot': robot_name,
	    'status': 'NEW',
	    'type' : 'SEND'
    }

    # Convert to string before sending (because of this 'content-type' : 'application/json')

	nav_str = json.dumps(nav_template)

	# Make the request (multiple times in case where there is a 500 error)
	for i in range(5):
		try:
			nav_req = requests.post(url, headers={'AUTHORIZATION' : session['Token'], 
										'content-type' : 'application/json',
										'Accept-Language' : 'jp'}, 
										timeout = 10, 
										data = nav_str)

		except Exception as error:
			# Wait a second before retrying
			time.sleep(1)
			if i == 4:
				return nav_req.status_code
		else:
			# Check if the response was bad
			if nav_req.status_code == 500 or 400:
				# Bad response, so retry
				continue

			# Good response,
			return status_code

	return nav_req.status_code
	
	# nav_req = requests.post(url, headers=header, data=nav_str, timeout = 10)
	# print(nav_req.text)


# if __name__ == '__main__':
# 	# get_robots()
# 	get_poses(14)
	# create_nav_action('freight27', pose_dict['Pose 002'])	






