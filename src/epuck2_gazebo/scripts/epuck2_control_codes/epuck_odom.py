#!/usr/bin/env python
import rospy
from nav_msgs.msg import Odometry
import time

x = 0

def callback(data):
#    rospy.loginfo("I heard %f", data.pose.pose.position.x)
    x = data.pose.pose.position.x
    print(x)

def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('epuck_odom', anonymous=True)
#    r = rospy.Rate(1)
#    while not rospy.is_shutdown():
    rospy.Subscriber("/epuck2/odom_diffdrive", Odometry, callback,queue_size=100)
#	r.sleep()
    rospy.spin()
#    time.sleep(1)
    # spin() simply keeps python from exiting until this node is stopped
    #rospy.spin()

if __name__ == '__main__':
    listener()
