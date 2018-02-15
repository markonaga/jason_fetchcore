from flask import session
import requests
import json

# final String jsonB = "{\"actions\":[{\"action_definition\":\"NAVIGATE\",\"inputs\":{\"limit_velocity\":true,\"max_angular_velocity\":2.5,\"max_velocity\":1.5,\"pose_id\":TargetPlaceID},\"pose_name\":null,\"preemptable\":\"HARD\",\"status\":\"NEW\"}],\"requester\":\"UserName\",\"robot\":\"RobotName\",\"status\":\"NEW\",\"type\":\"SEND\"}";



robot_names = []
robot_poses = {}
pose_dict = {}

def get_robots():
	# Configure the URL endpoint
	# url = 'https://' + session['hostIP']+ '/api/v1/robots'
	url = 'https://softbank.fetchcore-cloud.com/api/v1/robots'

	# Make the request
	# robot_req = requests.get(url, headers={'AUTHORIZATION' : session['Token']}, timeout = 10)
	robot_req = requests.get(url, headers=header, timeout = 10)
	
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
		# session['robot_names'].append(robo_dict['name'])
		robot_names.append(name)

		# Pass in the map ID and get the list of poses corresponding to that robot's map
		# session['robot_poses'][name] = get_poses(map_id)
		robot_poses[name] = get_poses(map_id)

	print(robot_names)
	print(robot_poses)


# Returns a list of pose from specified map 
def get_poses(map_id):
	# Temporary list for storing the pose names
	pose_names = []

	# Configure the URL endpoint
	# url = 'https://' + session['hostIP'] + /api/v1/maps/' + str(map_id) + '/annotations'
	url = 'https://softbank.fetchcore-cloud.com/api/v1/maps/' + str(map_id) + '/annotations'
	
	# Make the request
	# robot_req = requests.get(url, headers={'AUTHORIZATION' : session['Token']}, timeout = 10)
	map_req = requests.get(url, headers=header, timeout = 10)

	# Convert response data to JSON object
	raw_json = json.loads(map_req.text)

	# Pull 'poses' dictionary from body 
	data = raw_json[5]

	# Pull out list from the dictionary
	pose_list = data['poses']

	# Get each of the pose names
	for index, pose in enumerate(pose_list):
		pose_names.append(pose['name'])
		pose_dict[pose['name']] = pose['id']


	# Convert from Unicode to JSON
	pretty_list = json.dumps(pose_names)

	# print(pretty_list)
	# print(pose_dict)

	return pretty_list


# int pose_id
# string pose_name
def create_nav_action(robot_name, pose_name, pose_id):
	username ='jvranek@innovation-matrix.com'
	task_template = 'HMI Button Test'
	# Configure the URL endpoint
	url = 'https://softbank.fetchcore-cloud.com/api/v1/tasks/'
	# url = 'https://' + session['hostIP']+ '/api/v1/tasks/'


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
				    # 'goal_pose' : {
				    # 	'theta': -1.58812530744,
        #         		'y': -11.20763476566,
        #         		'x': 127.31641013818,
				    # },
				    # 'pose_name' : pose_name,
	    			},
	    		'preemptable' : 'HARD',
			    'status' : 'NEW'
			}],
	    'requester' : username,
	    'robot': robot_name,
	    'status': 'NEW',
	    'type' : 'SEND'
    }

    # Convert to string before sending (because of this 'content-type' : 'application/json')

	nav_str = json.dumps(nav_template)

	nav_req = requests.post(url, headers=header, data=nav_str, timeout = 10)
	print(nav_req.text)


if __name__ == '__main__':
	# get_robots()
	get_poses(14)
	create_nav_action('freight64', 'Conference Room', pose_dict['Conference Room'])	






