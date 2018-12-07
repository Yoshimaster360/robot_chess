#!/usr/bin/env python
print("woooooo")
import numpy as np
from numpy import linalg
import rospy
from moveit_msgs.srv import GetPositionIK, GetPositionIKRequest, GetPositionIKResponse
from geometry_msgs.msg import PoseStamped
from moveit_commander import MoveGroupCommander
from intera_interface import gripper as robot_gripper
import tf2_ros
from std_msgs.msg import String
from std_msgs.msg import Float64
from std_msgs.msg import Float64MultiArray
j = 0
information = open('data','r')
movement_string, remove_string = [i.rstrip() for i in information.readlines()]
print("WELCOME DATA RECEIVED")

def ar_track(last_frame):

	cam = tfBuffer.lookup_transform("usb_cam","ar_marker_2" , rospy.Time()) 
	print(cam)
	cam_to_ar = np.array([cam.transform.translation.x, cam.transform.translation.y, cam.transform.rotation.z])
	ar_to_cb = np.array([.1, .1, 0])
	current_frame = cam_to_ar - ar_to_cb
	if 	sum(abs(current_frame - last_frame)) >= .02:
		canmove = [1.0]
		origin_deviation = current_frame - last_frame
		move_string = []
		move_string.append(remove_string)
		move_string.append(movement_string)
		move_set = origin_deviation
		
		pub_move_set = Float64MultiArray(data=move_set)
		
		# Publish our string to the 'origin_deviation' topic
		movement_set.publish(pub_move_set)
		print('I have Published')

		return(current_frame,origin_deviation)
	

	else:
		canmove = [1.0]
		origin_deviation = [0,0,0]
		move_string = []
		move_string.append(remove_string)
		move_string.append(movement_string)
		move_set = origin_deviation		
		
		pub_move_set = Float64MultiArray(data=move_set)
		
		# Publish our string to the 'origin_deviation' topic
		movement_set.publish(pub_move_set)
		print('I have Published')

		return(current_frame,origin_deviation)


#Python's syntax for a main() method
def main():
	print('Main Function')
while __name__ == '__main__' and j < 3:
	main()
	#Test
	rospy.init_node('controller')   
	tfBuffer = tf2_ros.Buffer()
	rospy.sleep(1)
	tfListener = tf2_ros.TransformListener(tfBuffer) 
	rospy.sleep(1)
	
	movement_set = rospy.Publisher('movement_set', Float64MultiArray, queue_size=10)
	r = rospy.Rate(10)
	print('defined publisher')

	test = ar_track([0,0,0])
	current_frame = test[0]
	origin_deviation = test[1]
	print(current_frame)
	print(origin_deviation)

	j = j+1
