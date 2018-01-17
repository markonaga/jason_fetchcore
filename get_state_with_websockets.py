#!/usr/bin/python
# Copyright 2017 Fetch Robotics Inc.
# Author(s): Connor Anderson
# Contact: support@fetchrobotics.com

""" get_state_with_websockets.py

This code implements the Fetchcore Python SDK to get the location (in x, y, and
theta) of a selected robot using websockets.

"""

# Import from Fetchcore Python SDK
from fetchcore import configuration
from fetchcore.client import FetchcoreClient

# Standard import libraries
from time import sleep


''' ----------------------- User Variables -------------------------- '''
url = 'CUSTOMER.fetchcore-cloud.com'
fetchcore_username = 'USERNAME'
fetchcore_password = 'PASSWORD'
port = 443
ssl = True
robot_name = "freightXX"


''' -------------------------- Websocket Callback ----------------------------- '''
# Callback function to print the current position and battery level
# of a specified robot


def _printRobotState(resource, action, type):
    if type == "ROBOTSTATE":
        if resource.robot == robot_name:
            # Parse out information for current position and battery level
            current_location = []
            current_location.append(resource.current_pose["x"])
            current_location.append(resource.current_pose["y"])
            current_location.append(resource.current_pose["theta"])

            print("Current Location: ")
            print("X: " + str(current_location[0]))
            print("Y: " + str(current_location[1]))
            print("Theta: " + str(current_location[2]))


''' -------------------------- Authenticate ----------------------------- '''
try:
    # Create and authorize a Fetchcore client
    client = FetchcoreClient(
        fetchcore_username, fetchcore_password, host=url, port=port, ssl=ssl)
    client.connect()
    print("Authorized")
except:
    print("You are not authorized. Check your login credentials and try again.")
    exit(-1)


''' -------------------------- Subscribe to Robots ----------------------------- '''
client.subscribe_to_robots(_printRobotState)


''' ---------------- Keep Program Running Until Exit  -------------------- '''
while (True):

    try:
        sleep(10)
    except KeyboardInterrupt:
        break
    except Exception as e:
        print 'Encountered exception:', e
        break

# Close websocket to terminate script
print "Exiting..."
client.unsubscribe_from_robots()
client.disconnect()
