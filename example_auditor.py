#/usr/bin/python
"""Sample auditor implementation. This is an example of how to invoke
the auditing framework for a particular service <example_service>

All service-related functionality, such as logging in / out etc should be
implemented by the user, who then will invoke the auditing framework to
carry out the tests to be performed
"""

# import any libraries required . This varies from service to service
# and should be specified by the user
import time
import random
import string
import datetime
import json
import os
import sys

# class containing API calls for setting location, loggin in/out etc
# This is a class which is service-specific and should be implemented
# by the user willing to use the framework -- NOT PROVIDED HERE
import example_service


# Import Auditor Class and other libraries from the auditing
# framework that are necessary
from auditor import Auditor
import auditor_constants as const
from libs import earth

#
#  Specify Credentials of other user-info to be used
#

#device ids to be used for clients
DEVICE_ID1 = '54adab89499e9beda93c905d'
DEVICE_ID2 = '56ddab89499e9eeda93c905d'

users= [
    ['ankskywalker66@gmail.com', 'fakefake'],
    ['oliv.summer13@gmail.com', 'fakefake']
]

brng = 180
travel_dist = 0
center_coords = [40.807849, -73.962121]


class Tester(Auditor):
    """ Tester class, to test <example_service>. This class should be
    implemented per-service but always inherit from Auditor class.
    """

    def auditor_get_distance(self, user_a, user_b, user_loc):
        """Implement auditor_get_distace. This is a sample invocation, could be
            anything, depending on the nature of <example_service>
        """
        # A sample login, to get an access token for users a, b from
        # <example_service>. Parameters passed in this example are
        # (username, password, current coordinates, accuracy, device ID)
        usera_crdnt = example_service.login(users[user_a][0],
                                     users[user_a][1],
                                     center_coords,
                                     30 + random.uniform(-20, 10),
                                     DEVICE_ID1)
        usera_acc_token = usera_crdnt['access_token']
        userb_crdnt = example_service.login(users[user_b][0],
                                     users[user_b][1],
                                     center_coords,
                                     30 + random.uniform(-20, 10),
                                     DEVICE_ID2)
        userb_acc_token = usera_crdnt['access_token']

        # User a requests for the location of user b
        userb = example_service.get_friend_info(usera_acc_token,
                                                   users[user_b][0])
        userb_id = str(userb['id'])
        rspn = example_service.get_user_location(usera_acc_token,
                                          user_loc,
                                          str(30 + random.uniform(-20, 10)),
                                          userb_id)

        # Return the responce to the auditing framework
        if rspn is None:
            return (None, 1)
        else:
            return (float(rspn[2]) / 1000, 1)


    def auditor_set_location(self, user, lat, lon):
        """Sets the location of user a to (lat, lon) and returns the response
        to the auditing framework
        """
        # Login to <example_service>
        user_crdnt = example_service.login(users[user][0],
                                    users[user][1],
                                    center_coords,
                                    30 + random.uniform(-20, 10),
                                    DEVICE_ID1)
        user_acc_token = user_crdnt['access_token']
        # update location of user
        update = example_service.update_location(user_acc_token,
                                       DEVICE_ID1,
                                       [lat, lon],
                                       str(30 + random.uniform(-20, 10)),
                                       [lat, lon],
                                       str(30 + random.uniform(-20, 10)),
                                        '')
        if update is False:
            return (False, 1)
        else:
            return (True, 1)


# Invoke auditing framework tests: pass the name of the
# service and the users to be used
t = Tester("example_service", [0, 1])
# run the speed limit test
t.test_speed_limit()
# run the query limit test
t.test_query_limit()
# run DUDP attack
t.test_dudp_attack([0.321869, 1.60934, 8.04672, 32.1869, 64.3738])
# run RUDP attack
t.test_rudp_attack([[[0.1, float('inf')], 0.03, const.ROUNDING.BOTH]])
