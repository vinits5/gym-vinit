#! /usr/bin/python

import rospy
import math
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
import matplotlib.pyplot as plt
import tf
from tf.transformations import euler_from_quaternion
from std_srvs.srv import Empty
import time

velocity_publisher = rospy.Publisher('epuck2/cmd_vel',Twist,queue_size=10)

class EPUCK_GYM():
	def __init__(self):
		rospy.init_node('epuck_gym',anonymous=True)
		#self.pose_subscriber = rospy.Subscriber('/epuck2/odom_diffdrive',Odometry,self.callback_pose)
		#self.laser_subscriber = rospy.Subscriber('/scan',LaserScan,self.callback_scan)
		self.rate = rospy.Rate(10)

	def callback_pose(self,data):
		self.x = data.pose.pose.position.x
		self.y = data.pose.pose.position.y
		self.q0 = data.pose.pose.orientation.x
		self.q1 = data.pose.pose.orientation.y
		self.q2 = data.pose.pose.orientation.z
		self.q3 = data.pose.pose.orientation.w
		a = (self.q0,self.q1,self.q2,self.q3)
		self.euler = euler_from_quaternion(a)
		self.z = self.euler[2]*(180/math.pi)-90

	def callback_scan(self,data):
		self.data = data.ranges

	def get_position(self):
		self.unpause()
		self.epuck_pose = rospy.wait_for_message('epuck2/odom_diffdrive',Odometry,1)
		self.x = self.epuck_pose.pose.pose.position.x
		self.y = self.epuck_pose.pose.pose.position.y
		quaternion = (self.epuck_pose.pose.pose.orientation.x, self.epuck_pose.pose.pose.orientation.y, self.epuck_pose.pose.pose.orientation.z, self.epuck_pose.pose.pose.orientation.w)
		euler = euler_from_quaternion(quaternion)
		self.z = euler[2]*(180/math.pi)-90
		self.pause()
		return (self.x,self.y,self.z)

	def get_laser_data(self):
		self.unpause()
	 	self.data = rospy.wait_for_message('/scan',LaserScan,1)
		self.pause()
		return self.data.ranges

	def reset_world(self):
		reset_world = rospy.ServiceProxy('/gazebo/reset_world',Empty)
		reset_world()

	def pause(self):
		pause =  rospy.ServiceProxy('/gazebo/pause_physics',Empty)
		pause()

	def unpause(self):
		unpause = rospy.ServiceProxy('/gazebo/unpause_physics',Empty)
		unpause()

	def motion(self,linear_vel,angular_vel):
		self.unpause()
		vel = Twist()
		if linear_vel < 0.1:
			vel.linear.x = linear_vel
		else:
			vel.linear.x = 0.1
		if angular_vel < 1.5:
			vel.angular.z = angular_vel
		else:
			vel.angular.z = 1.5
		time_stamp = 0
		while time_stamp < 10:
			velocity_publisher.publish(vel)
			self.rate.sleep()
			time_stamp += 1
		self.stop()
		self.pause()

	def stop(self):
		vel = Twist()
		vel.linear.x = 0
		vel.angular.z = 0
		velocity_publisher.publish(vel)
