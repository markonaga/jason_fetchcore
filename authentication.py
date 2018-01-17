#!/usr/bin/python
# Copyright 2017 Fetch Robotics Inc.
# Author(s): Connor Anderson
# Contact: support@fetchrobotics.com

''' authentication.py

This code implements the Fetchcore Python SDK to authenticate a
client to the Fetchcore server. Once initialized, a user is
authenticated to Fetchcore.

'''

# Import from Fetchcore Python SDK
from fetchcore import configuration

''' ----------------------- User Variables -------------------------- '''
url = 'CUSTOMER.fetchcore-cloud.com'
fetchcore_username = 'USERNAME'
fetchcore_password = 'PASSWORD'
port = 443
ssl = True

''' -------------------------- Authenticate ----------------------------- '''
try:
    # Connect to Fetchcore using your credentials
    configuration.initialize_global_client(fetchcore_username,
                                           fetchcore_password, url, port, ssl)
    print("Authorized")
except:
    print("You are not authorized. Check your login credentials and try again.")
