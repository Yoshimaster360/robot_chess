#!/usr/bin/env python
import numpy as np
from numpy import linalg
import rospy
from moveit_msgs.srv import GetPositionIK, GetPositionIKRequest, GetPositionIKResponse
from geometry_msgs.msg import PoseStamped
from moveit_commander import MoveGroupCommander
from intera_interface import gripper as robot_gripper
import tf2_ros

rospy.init_node('movement')   
# right_gripper = robot_gripper.Gripper('right_gripper')
tfBuffer = tf2_ros.Buffer()
rospy.sleep(1)
tfListener = tf2_ros.TransformListener(tfBuffer) 
rospy.sleep(1)


def initial_setup():
	#Calibrate the gripper (other commands won't work unless you do this first
	print('Calibrating...')
	# right_gripper.calibrate()  

	# trans = tfBuffer.lookup_transform("base","right_gripper_tip" , rospy.Time()) 
	
	cam = tfBuffer.lookup_transform("usb_cam","ar_marker_2" , rospy.Time()) 
	cam_to_ar = np.array([cam.transform.translation.x, cam.transform.translation.y, cam.transform.rotation.z])
	ar_to_cb = np.array([.259, 0, 0])
	ar_to_right_gripper = np.array([.1,.1,0])
	last_frame = cam_to_ar - ar_to_cb

	right_gripper_to_cb = ar_to_cb - ar_to_right_gripper

	initial_xyz = [trans.transform.translation.x, trans.transform.translation.y, trans.transform.translation.z]
	movement([initial_xyz[0]-right_gripper_to_cb, initial_xyz[0]-right_gripper_to_cb])

	return([last_frame, initial_xyz])

def get_move_data(move_string,canmove):
	# Assume Remove will come in as R-##-##
	# Asume Move will come in as M-##-##
	# Assume move_string is of the form [remove,move]
	if canmove == 1:
			if move_string[0][0] == 'R':
					remove_location = move_string[0][2:4]
					remove_destination = move_string[0][5:7]
			else:    
					remove_location = 'N'
	if canmove == 1:
			if move_string[1][0] == 'M':
					piece_location = move_string[1][2:4]
					piece_destination = move_string[1][5:7]
					
			else:
					print('Errors Occured')
					
	return(remove_location,remove_destination,piece_location,piece_destination)

# Defining the Grid Space
# Chess_Board_Grid_Space = cbgs
# Origin deviation of the form [x,y,theta]

def cbgs(origin_deviation):
	cb = np.array([[               [-.2002,.2002],  [-.143,.2002],  [-.0858,.2002],  [-.0286,.2002],  [.0286,.2002],  [.0858,.2002],  [.143,.2002],  [.2002,.2002]  ],
								 [ [-.2002,.143],   [-.143,.143],   [-.0858,.143],   [-.0286,.143],   [.0286,.143],   [.0858,.143],   [.143,.143],   [.2002,.143]   ], 
								 [ [-.2002,.0858],  [-.143,.0858],  [-.0858,.0858],  [-.0286,.0858],  [.0286,.0858],  [.0858,.0858],  [.143,.0858],  [.2002,.0858]  ],
								 [ [-.2002,.0286],  [-.143,.0286],  [-.0858,.0286],  [-.0286,.0286],  [.0286,.0286],  [.0858,.0286],  [.143,.0286],  [.2002,.0286]  ],
								 [ [-.2002,-.0286], [-.143,-.0286], [-.0858,-.0286], [-.0286,-.0286], [.0286,-.0286], [.0858,-.0286], [.143,-.0286], [.2002,-.0286] ],
								 [ [-.2002,-.0858], [-.143,-.0858], [-.0858,-.0858], [-.0286,-.0858], [.0286,-.0858], [.0858,-.0858], [.143,-.0858], [.2002,-.0858] ],
								 [ [-.2002,-.143],  [-.143,-.143],  [-.0858,-.143],  [-.0286,-.143],  [.0286,-.143],  [.0858,-.143],  [.143,-.143],  [.2002,-.143]  ],
								 [ [-.2002,-.2002], [-.143,-.2002], [-.0858,-.2002], [-.0286,-.2002], [.0286,-.2002], [.0858,-.2002], [.143,-.2002], [.2002,-.2002] ] ])
	
	if origin_deviation[0] != 0 or origin_deviation[1] != 0: 
			for i in range(cb.shape[0]):
					for j in range(cb.shape[1]):
							cb[i][j] = cb[i][j] + np.array([origin_deviation[0],origin_deviation[1]])
							
	if origin_deviation[2] != 0:
			theta = np.deg2rad(origin_deviation[2])        
			
			for i in range(cb.shape[0]):
					for j in range(cb.shape[1]):
							r = np.sqrt(cb[i][j][0]**2 + cb[i][j][1]**2)
							if i<=3 and j<=3:
									angle = np.arccos(np.abs(cb[i][j][0]/r))
									theta2 = theta + angle + np.pi/2 
									cb[i][j] = np.array([r*np.cos(theta2),r*np.sin(theta2)])
							if i<=3 and j>=4:
									angle = np.arccos(np.abs(cb[i][j][0]/r))                    
									theta1 = theta + angle                  
									cb[i][j] = np.array([r*np.cos(theta1),r*np.sin(theta1)])                    
							if i>=4 and j<=3:
									angle = np.arccos(np.abs(cb[i][j][0]/r))                    
									theta3 = theta + angle + np.pi
									cb[i][j] = np.array([r*np.cos(theta3),r*np.sin(theta3)])                    
							if i >=4 and j>=4:
									angle = np.arccos(np.abs(cb[i][j][0]/r))                    
									theta4 = theta + angle + np.pi*(3/2)
									cb[i][j] = np.array([r*np.cos(theta4),r*np.sin(theta4)])                    
							
	else:
			cb = cb
			
	return(cb)           

# Created Dictionary Function that returns a set of coordinates
# Coordinates come in a 1x3 array where the 0th index is remove coordinates 
# 1st index is the move from coordinates
# 2nd index is move to coordinates

def coordinates(origin_deviation, move_string, canmove,initial_xyz):
	gridmapping = {'A8':[0,0], 'B8':[0,1], 'C8':[0,2], 'D8':[0,3], 
								 'E8':[0,4], 'F8':[0,5], 'G8':[0,6], 'H8':[0,7],

								 'A7':[1,0], 'B7':[1,1], 'C7':[1,2], 'D7':[1,3], 
								 'E7':[1,4], 'F7':[1,5], 'G7':[1,6], 'H7':[1,7], 

								 'A6':[2,0], 'B6':[2,1], 'C6':[2,2], 'D6':[2,3], 
								 'E6':[2,4], 'F6':[2,5], 'G6':[2,6], 'H6':[2,7],

								 'A5':[3,0], 'B5':[3,1], 'C5':[3,2], 'D5':[3,3], 
								 'E5':[3,4], 'F5':[3,5], 'G5':[3,6], 'H5':[3,7],

								 'A4':[4,0], 'B4':[4,1], 'C4':[4,2], 'D4':[4,3], 
								 'E4':[4,4], 'F4':[4,5], 'G4':[4,6], 'H4':[4,7], 

								 'A3':[5,0], 'B3':[5,1], 'C3':[5,2], 'D3':[5,3], 
								 'E3':[5,4], 'F3':[5,5], 'G3':[5,6], 'H3':[5,7], 

								 'A2':[6,0], 'B2':[6,1], 'C2':[6,2], 'D2':[6,3], 
								 'E2':[6,4], 'F2':[6,5], 'G2':[6,6], 'H2':[6,7], 

								 'A1':[7,0], 'B1':[7,1], 'C1':[7,2], 'D1':[7,3], 
								 'E1':[7,4], 'F1':[7,5], 'G1':[7,6], 'H1':[7,7], 

								 '00':[3,7]                                      }
	
	cb = cbgs(origin_deviation)
	coor_remove_from = cb[gridmapping[get_move_data(move_string,canmove)[0]][0]][gridmapping[get_move_data(move_string,canmove)[0]][1]] + [initial_xyz[0], initial_xyz[1]] 
	coor_remove_to = cb[gridmapping[get_move_data(move_string,canmove)[1]][0]][gridmapping[get_move_data(move_string,canmove)[1]][1]] + [.1,.1] + [initial_xyz[0], initial_xyz[1]] 
	coor_move_from = cb[gridmapping[get_move_data(move_string,canmove)[2]][0]][gridmapping[get_move_data(move_string,canmove)[2]][1]] + [initial_xyz[0], initial_xyz[1]] 
	coor_move_to = cb[gridmapping[get_move_data(move_string,canmove)[3]][0]][gridmapping[get_move_data(move_string,canmove)[3]][1]] + [initial_xyz[0], initial_xyz[1]] 
	return([coor_remove_from,coor_remove_to,coor_move_from,coor_move_to])

def movement(des_coor, i, last_frame, move_string, canmove, initial_xyz):
	#Wait for the IK service to become available
	rospy.wait_for_service('compute_ik')
	received_info = True
	#Create the function used to call the service
	compute_ik = rospy.ServiceProxy('compute_ik', GetPositionIK)
	while received_info == True:           

		#Construct the requests
		request = GetPositionIKRequest()
		request.ik_request.group_name = "right_arm"
		request.ik_request.ik_link_name = "right_gripper_tip"
		request.ik_request.attempts = 30
		request.ik_request.pose_stamped.header.frame_id = "base"       
		
		#Set the desired orientation for the end effector HERE
		print(des_coor)
		request.ik_request.pose_stamped.pose.position.x = des_coor[0] 
		request.ik_request.pose_stamped.pose.position.y = des_coor[1] 
		request.ik_request.pose_stamped.pose.position.z = 0.25  # this should be a found constant        
		# Should be constant Determined by Experiment
		request.ik_request.pose_stamped.pose.orientation.x = 0.0 
		request.ik_request.pose_stamped.pose.orientation.y = 1.0
		request.ik_request.pose_stamped.pose.orientation.z = 0.0
		request.ik_request.pose_stamped.pose.orientation.w = 0.0
		
		if sum(ar_track(last_frame)[1]) == 0:
			try:
				#Send the request to the service
				response = compute_ik(request)
					
				#Print the response HERE
				print(response)
				if response.error_code.val == 1: 
					received_info = False
				else:
					received_info = False
				# received_info = False
				group = MoveGroupCommander("right_arm")

				# Setting position and orientation target
				group.set_pose_target(request.ik_request.pose_stamped)

				# Plan IK and execute
				group.go()
					
			except rospy.ServiceException, e:
				print "Service call failed: %s"%e

		else:
			origin_deviation = ar_track(last_frame)[1]
			des_coor = coordinates(origin_deviation, move_string, canmove,initial_xyz)[i]

	#Wait for the IK service to become available
	rospy.wait_for_service('compute_ik')
	received_info = True
	#Create the function used to call the service
	compute_ik = rospy.ServiceProxy('compute_ik', GetPositionIK)
	while received_info == True:           

		#Construct the requests
		request = GetPositionIKRequest()
		request.ik_request.group_name = "right_arm"
		request.ik_request.ik_link_name = "right_gripper_tip"
		request.ik_request.attempts = 30
		request.ik_request.pose_stamped.header.frame_id = "base"       
		
		#Set the desired orientation for the end effector HERE
		print(des_coor)
		request.ik_request.pose_stamped.pose.position.x = des_coor[0] 
		request.ik_request.pose_stamped.pose.position.y = des_coor[1] 
		request.ik_request.pose_stamped.pose.position.z = .09  # this should be a found constant        
		# Should be constant Determined by Experiment
		request.ik_request.pose_stamped.pose.orientation.x = 0.0 
		request.ik_request.pose_stamped.pose.orientation.y = 1.0
		request.ik_request.pose_stamped.pose.orientation.z = 0.0
		request.ik_request.pose_stamped.pose.orientation.w = 0.0
		
		try:
			#Send the request to the service
			response = compute_ik(request)
				
			#Print the response HERE
			print(response)
			if response.error_code.val == 1: 
				received_info = False
			else:
				received_info = False
			# received_info = False
			group = MoveGroupCommander("right_arm")

			# Setting position and orientation target
			group.set_pose_target(request.ik_request.pose_stamped)

			# Plan IK and execute
			group.go()
				
		except rospy.ServiceException, e:
			print "Service call failed: %s"%e




	if i == 0 or i==2:
		print("I AM RELEASING")
		release()
	
	#Wait for the IK service to become available
	rospy.wait_for_service('compute_ik')
	received_info = True
	#Create the function used to call the service
	compute_ik = rospy.ServiceProxy('compute_ik', GetPositionIK)
	while received_info == True:           

		#Construct the requests
		request = GetPositionIKRequest()
		request.ik_request.group_name = "right_arm"
		request.ik_request.ik_link_name = "right_gripper_tip"
		request.ik_request.attempts = 30
		request.ik_request.pose_stamped.header.frame_id = "base"       
		
		#Set the desired orientation for the end effector HERE
		print(des_coor)
		request.ik_request.pose_stamped.pose.position.x = des_coor[0] 
		request.ik_request.pose_stamped.pose.position.y = des_coor[1] 
		request.ik_request.pose_stamped.pose.position.z = .015  # this should be a found constant        
		# Should be constant Determined by Experiment
		request.ik_request.pose_stamped.pose.orientation.x = 0.0 
		request.ik_request.pose_stamped.pose.orientation.y = 1.0
		request.ik_request.pose_stamped.pose.orientation.z = 0.0
		request.ik_request.pose_stamped.pose.orientation.w = 0.0
		
		try:
			#Send the request to the service
			response = compute_ik(request)
				
			#Print the response HERE
			print(response)
			# if response. #figure out object deets later:
			#     received_info = False
			# else:
			#     received_info = True
			received_info = False
			group = MoveGroupCommander("right_arm")

			# Setting position and orientation target
			group.set_pose_target(request.ik_request.pose_stamped)

			# Plan IK and execute
			group.go()
				
		except rospy.ServiceException, e:
			print "Service call failed: %s"%e

	if i == 0 or i == 2:
		print("I AM GRABBING")
		grab()
	if i == 1 or i == 3:
		print("I AM RELEASING")
		release()

	#Wait for the IK service to become available
	rospy.wait_for_service('compute_ik')
	received_info = True
	#Create the function used to call the service
	compute_ik = rospy.ServiceProxy('compute_ik', GetPositionIK)
	while received_info == True:           

		#Construct the requests
		request = GetPositionIKRequest()
		request.ik_request.group_name = "right_arm"
		request.ik_request.ik_link_name = "right_gripper_tip"
		request.ik_request.attempts = 30
		request.ik_request.pose_stamped.header.frame_id = "base"       
		
		#Set the desired orientation for the end effector HERE
		print(des_coor)
		request.ik_request.pose_stamped.pose.position.x = des_coor[0] 
		request.ik_request.pose_stamped.pose.position.y = des_coor[1] 
		request.ik_request.pose_stamped.pose.position.z = 0.25  # this should be a found constant        
		# Should be constant Determined by Experiment
		request.ik_request.pose_stamped.pose.orientation.x = 0.0 
		request.ik_request.pose_stamped.pose.orientation.y = 1.0
		request.ik_request.pose_stamped.pose.orientation.z = 0.0
		request.ik_request.pose_stamped.pose.orientation.w = 0.0
		
		try:
			#Send the request to the service
			response = compute_ik(request)
				
			#Print the response HERE
			print(response)
			# if response. #figure out object deets later:
			#     received_info = False
			#     close_gripper = True
			# else:
			#     received_info = True
			received_info = False
			group = MoveGroupCommander("right_arm")

			# Setting position and orientation target
			group.set_pose_target(request.ik_request.pose_stamped)

			# Plan IK and execute
			group.go()
				
		except rospy.ServiceException, e:
			print "Service call failed: %s"%e


def grab():
	#Close the right gripper
	print('Closing...')
	right_gripper.close()
	rospy.sleep(.5)

def release():
	#Open the right gripper
	print('Opening...')
	right_gripper.open()
	rospy.sleep(.5)


def ar_track(last_frame):

	cam = tfBuffer.lookup_transform("usb_cam","ar_marker_2" , rospy.Time()) 
	print(cam)
	cam_to_ar = np.array([cam.transform.translation.x, cam.transform.translation.y, cam.transform.rotation.z])
	ar_to_cb = np.array([.259, 0, 0])
	current_frame = cam_to_ar - ar_to_cb
	if 	sum(abs(current_frame - last_frame)) >= .02:
		origin_deviation = current_frame - last_frame
		return(current_frame,origin_deviation)

	else:
		origin_deviation = [0,0,0]
		return(current_frame,origin_deviation)


def listen_for_data(last_frame, initial_xyz):
	#write and read the data file shit 
	
	move_string = []
	move_string.append('R-A8-00')
	move_string.append('M-D5-A8')
	canmove = 1
	ar_info = ar_track(last_frame)
	origin_deviation = ar_info[1]
	last_frame = ar_info[0]
	movement_coordinates = (coordinates(origin_deviation,move_string,canmove,initial_xyz))
	print(movement_coordinates)
	# for i in range(4):
	# 	movement(movement_coordinates[i], i, last_frame, move_string,canmove,initial_xyz)
	#Delete data in file	


#Python's syntax for a main() method
def main():
	print('Main Function')
	initial_config = initial_setup()
	last_frame = initial_config[0]
	initial_xyz = initial_config[1]
	listen_for_data(last_frame,initial_xyz)
if __name__ == '__main__':
	main()
	#Test


	# initial_xyz = initial_setup()
	# movement([.500,.447],0)   
	
	# move_string = []
	# move_string.append('R-A8-00')
	# move_string.append('M-D5-A8')
	# canmove = 1
	# origin_deviation=[0,0,0]
	# movement_coordinates = (coordinates(origin_deviation,move_string,canmove,initial_xyz))

	# for i in range(4):
	# 	movement(movement_coordinates[i], i)

	# move_string = []
	# move_string.append('R-A7-00')
	# move_string.append('M-A8-A7')
	# canmove = 1
	# origin_deviation=[0,0,0]
	# movement_coordinates = (coordinates(origin_deviation,move_string,canmove,initial_xyz))

	# for i in range(4):
	# 	movement(movement_coordinates[i], i)

	

