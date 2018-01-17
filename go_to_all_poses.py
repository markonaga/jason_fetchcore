#!/usr/bin/python
# Copyright 2017 Fetch Robotics Inc.
# Author(s): Connor Anderson
# Contact: support@fetchrobotics.com


""" go_to_all_poses.py

This code implements the Fetchcore Python SDK to drive a robot
to all the poses within a given map.

"""

# Import from Fetchcore Python SDK
from fetchcore import configuration
from fetchcore.resources.maps import Map
from fetchcore.resources.robots import Robot
from fetchcore.resources.actions import NavigateAction
from fetchcore.resources import Task

# Standard import libraries
from time import sleep
from datetime import datetime


''' ----------------------- User Variables -------------------------- '''
url = 'CUSTOMER.fetchcore-cloud.com'
fetchcore_username = 'USERNAME'
fetchcore_password = 'PASSWORD'
port = 443
ssl = True
robot_name = "freightXX"
mapNumber = 20				# Map number (map url will contain this number)
posePause = 10				# Pause at every pose for this amount of seconds


''' -------------------------- Authenticate ----------------------------- '''
try:
    # Connect to Fetchcore using your credentials
    configuration.initialize_global_client(fetchcore_username,
                                           fetchcore_password, url, port, ssl)
except:
    print("You are not authorized. Check your login credentials and try again.")


''' --------------------- Print Maps and Poses -------------------------- '''
# Print all maps
print "Available maps: "
maps = Map.list()
for map in maps:
    print("Map Name: " + map.name)
    print("Map ID Number: " + str(map.id))

# Show all poses on selected map and load custom poses
print("Available poses on Map: ")
map = Map.load(mapNumber)
poses = map.poses
# Sort poses alphabetically by name
sorted_poses = sorted(poses, key=lambda k: k.name)
for pose in sorted_poses:
    print(pose.name)

# Load the robot
robot = Robot.load(robot_name)

''' --------------------- Send Robot to Poses -------------------------- '''
current_pose = 0
while (current_pose < len(sorted_poses)):
    # Get desired position and convert to x,y,theta
    goal_pose = {
        "x": sorted_poses[current_pose].x,
        "y": sorted_poses[current_pose].y,
        "theta": sorted_poses[current_pose].theta
    }
    # Create nav action
    nav_action = NavigateAction(goal_pose=goal_pose)
    # Create nav task
    nav_task = Task(name="Nav to Poses", type="NAVIGATE",
                    actions=[nav_action], robot=robot)
    # Save task to update remote server
    nav_task.save()

    # Wait until navigating is done to switch to next position
    while (True):
        # Refresh the task to get the latest state on the server
        nav_task.refresh()

        # If we're done with the task, switch to the next task
        if nav_task.status == "COMPLETE" or nav_task.status == "PREEMPTED" or \
                nav_task.status == "FAILED" or nav_task.status == "CANCELED":
            current_pose += 1
            break
        else:
            print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') +
                  " - Task is now " + nav_task.status +
                  " Pose " + sorted_poses[current_pose].name)

        sleep(1)
