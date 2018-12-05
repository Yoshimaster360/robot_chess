#!/usr/bin/env python
import numpy as np
from numpy import linalg
import rospy
from moveit_msgs.srv import GetPositionIK, GetPositionIKRequest, GetPositionIKResponse
from geometry_msgs.msg import PoseStamped
from moveit_commander import MoveGroupCommander
from intera_interface import gripper as robot_gripper
import tf2_ros

def ar_track(last_frame):

	cam = tfBuffer.lookup_transform("usb_cam","ar_marker_2" , rospy.Time()) 
	print(cam)
	cam_to_ar = np.array([cam.transform.translation.x, cam.transform.translation.y, cam.transform.rotation.z])
	ar_to_cb = np.array([.1, .1, 0])
	current_frame = cam_to_ar - ar_to_cb
	if 	sum(abs(current_frame - last_frame)) >= .02:
		origin_devation = current_frame - last_frame
		return(current_frame,origin_devation)

	else:
		return(current_frame,[0, 0, 0])

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
	test = ar_track([0,0,0])
	current_frame = test[0]
	origin_devation = test[1]
	print(current_frame)
	print(origin_devation)
