#!/usr/bin/env python3

import mission_execution_control as mxc
import rospy
from aerostack_msgs.msg import ListOfBeliefs
from belief_manager_msgs.srv import *
import math
import time  

landing_zone = [[6, -1+2.0, 1], [6, 3.4+2.0, 1]]

def stopwatch(seconds):
	start = time.time()
	time.perf_counter()
	elapsed = 0
	while elapsed < seconds:
		checkMission = "unfertilized(?x)"
		success , unification = mxc.queryBelief(checkMission)
		if (success):
			return False
		elapsed = time.time() - start
		print ("loop cycle time: %f, seconds count: %02d" % (time.perf_counter() , elapsed))
		time.sleep(1)
	return True 

def mission():
	print("Starting mission...")
	print("Paying attention to robots...")
	mxc.startTask('PAY_ATTENTION_TO_ROBOT_MESSAGES')

	print("informing position to robots...")
	mxc.startTask('INFORM_POSITION_TO_ROBOTS')
	addBelief1 = rospy.ServiceProxy("/drone1/add_belief", AddBelief)
	removeBelief1 = rospy.ServiceProxy("/drone1/remove_belief", RemoveBelief)
	landing = "landing_zone(100, (0, -2, 0))"
	mxc.addBelief(landing, True)
	landing = "landing_zone(101, (6, -1, 0))"
	mxc.addBelief(landing, True)
	landing = "landing_zone(102, (6, 3.4, 0))"
	mxc.addBelief(landing, True)
	while (True):
		query = "unfertilized(?x)"
		success , unification = mxc.queryBelief(query)
		print (query)
		print (success)

		if success:
			
			print(unification['x'])
			plant= str(unification['x'])
			state = "flight_state(1, ?y)"
			success, unification = mxc.queryBelief(state)

			if success:
				if (str(unification['y'] == "LANDED")):
					mxc.executeTask('TAKE_OFF')

			mxc.startTask('FOLLOW_PATH')
			query2 = "position(" + plant + ",?y)"			
			success, unification = mxc.queryBelief(query2)
			print (success)
			print (str(unification['y']))
			position = str(unification['y'])
			position = position.replace("(", "").replace(")", "").split(",")
			x = position[0].replace(" ", "")
			y = position[1].replace(" ", "")
			z = 1.0
			traject = [[float(x), float(y) + 2.0, z]]
			print (traject)
			mxc.executeTask('SEND_PATH', path=traject, speed = 0.5, yaw_mode = 0)
			traject = [[float(x), float(y) + 2.0, z-0.5]]
			mxc.executeTask('SEND_PATH', path=traject, speed = 0.3, yaw_mode = 0)
			query3 = "unfertilized("+ plant + ")"
			mxc.removeBelief(query3)
			print ("aqui llega")
			removeBelief1(belief_expression=query3)
			query4 = "fertilized("+ plant + ")"
			mxc.addBelief(query4, True)
			addBelief1(belief_expression=query4, multivalued=True)
			traject = [[float(x), float(y) + 2.0, z]]
			print (traject)
			mxc.executeTask('SEND_PATH', path=traject, speed = 0.5, yaw_mode = 0)
			getPose = "position(1, ?y)"
			success, unification = mxc.queryBelief(getPose)
			pose = str(unification['y'])
			pose = pose.replace("(", "").replace(")", "").split(",")
			x = pose[0].replace(" ", "")
			y = pose[1].replace(" ", "")
			distanceout = 0
			land_pad = 0
			for i, point in enumerate(landing_zone, 0):
				distance = ((((point[0] - float(x) )**2) + ((point[1]-float(y))**2) )**0.5)
				if (distanceout == 0):
					distanceout = distance
					land_pad = 0
				elif (distance < distanceout):
					distanceout = distance
					land_pad = i
			if (stopwatch(5)==True):
				mxc.executeTask('SEND_PATH', path=[landing_zone[land_pad]], speed = 0.5, yaw_mode = 0)
				mxc.executeTask('LAND', speed = 0.3)
			query5="message(?x)"
			success, unification = mxc.queryBelief(query5)
			if (success):
				break

	print('Finish mission...')
