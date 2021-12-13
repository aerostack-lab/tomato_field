#!/usr/bin/env python3

import mission_execution_control as mxc
import rospy
from aerostack_msgs.msg import ListOfBeliefs
from belief_manager_msgs.srv import *
import math
import time  

path = [[9, 0, 1],[9, 1.2, 1], [2.15, 1.2, 1], [2.15, 2.80, 1], [9, 2.80, 1], [0, 0, 1]]

def mission():
	print("Starting mission...")
	addBelief = rospy.ServiceProxy("/drone2/add_belief", AddBelief)
	print("Taking off...")
	print("Paying attention to robots...")
	mxc.startTask('PAY_ATTENTION_TO_ROBOT_MESSAGES')

	print("informing position to robots...")
	mxc.startTask('INFORM_POSITION_TO_ROBOTS')
	mxc.executeTask('TAKE_OFF')
	mxc.startTask('FOLLOW_PATH')
	print("FOLLOW_PATH...")
	#mxc.startTask('FOLLOW_PATH')
	#mxc.executeTask('SEND_PATH', path = [ [1, -1, 1] , [1, 1, 1] , [-1, 1, 1] , [-1, -1, 1], [0, 0, 1] ], speed = 0.5)
	for point in path:
		mxc.executeTask('SEND_PATH',path = [point], speed = 0.5, yaw_mode = 0)
		if (point == [9, 1.2, 1]):
			time.sleep(30)

	print("LAND...")
	mxc.executeTask('LAND', speed = 0.3)
	query = "message(drone1, all_plants_inspected)"
	addBelief(belief_expression=query)


	print('Finish mission...')
