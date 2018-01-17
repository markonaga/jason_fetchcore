#!/usr/bin/python
# Copyright 2017 Fetch Robotics Inc.
# Author(s): Connor Anderson
# Contact: support@fetchrobotics.com

""" get_robot_info.py

This code implements the Fetchcore Python SDK to get the location (in x, y, and
theta) and battery level of a selected robot.

"""

# Import from Fetchcore Python SDK
from fetchcore import configuration
from fetchcore.resources.robots import RobotState

# Standard import libraries
from time import sleep


''' ----------------------- User Variables -------------------------- '''
url = 'CUSTOMER.fetchcore-cloud.com'
fetchcore_username = 'USERNAME'
fetchcore_password = 'PASSWORD'
port = 443
ssl = True
robot_name = "freightXX"


''' -------------------------- Authenticate ----------------------------- '''
try:
    # Connect to Fetchcore using your credentials
    configuration.initialize_global_client(fetchcore_username,
                                           fetchcore_password, url, port, ssl)
    print("Authorized")
except:
    print("You are not authorized. Check your login credentials and try again.")


''' ---------------- Get Position and Battery Levels -------------------- '''
while (True):

    # GET the information for the given robot_name
    robotState = RobotState.load(robot_name)

    # Parse out information for current position and battery level
    current_location = []
    current_location.append(robotState.current_pose["x"])
    current_location.append(robotState.current_pose["y"])
    current_location.append(robotState.current_pose["theta"])
    battery_level = robotState.battery_level

    print("\n\rBattery level: " + str("%.2f" % (battery_level * 100)) + "%")
    print("Current Location: ")
    print("X: " + str(current_location[0]))
    print("Y: " + str(current_location[1]))
    print("Theta: " + str(current_location[2]))
    sleep(1)
