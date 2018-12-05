#!/usr/bin/env python
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

def ar_track(last_frame):

	cam = tfBuffer.lookup_transform("usb_cam","ar_marker_2" , rospy.Time()) 
	print(cam)
	cam_to_ar = np.array([cam.transform.translation.x, cam.transform.translation.y, cam.transform.rotation.z])
	ar_to_cb = np.array([.1, .1, 0])
	current_frame = cam_to_ar - ar_to_cb
	if 	sum(abs(current_frame - last_frame)) >= .02:
		origin_deviation = current_frame - last_frame
		return(current_frame,origin_deviation)

	else:
		origin_deviation = [0,0,0]
		return(current_frame,origin_deviation)

	#  to sprintf in C or MATLAB)
	pub_origin_deviation = origin_deviation

	# Publish our string to the 'origin_deviation' topic
	origin_deviation.publish(pub_origin_deviation)

	# Use our rate object to sleep until it is time to publish again
	r.sleep()

#Python's syntax for a main() method
def main():
	print('Main Function')
if __name__ == '__main__':
	main()
	#Test
	rospy.init_node('controller')   
	tfBuffer = tf2_ros.Buffer()
	rospy.sleep(1)
	tfListener = tf2_ros.TransformListener(tfBuffer) 
	rospy.sleep(1)
	
	origin_deviation = rospy.Publisher('origin_deviation', Float64MultiArray, queue_size=10)
	r = rospy.Rate(10)


	test = ar_track([0,0,0])
	current_frame = test[0]
	origin_deviation = test[1]
	print(current_frame)
	print(origin_deviation)
