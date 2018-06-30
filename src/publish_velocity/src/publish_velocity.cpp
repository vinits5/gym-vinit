#include<ros/ros.h>
#include<geometry_msgs/Twist.h>
#include<stdlib.h>
#include<math.h>
#include <sensor_msgs/LaserScan.h>
int main(int argc , char **argv)  {
// initialize the ROS system and become a node.
ros::init(argc,argv,"publish_velocity");
ros::NodeHandle nh;
//Create a Publisher object.
ros::Publisher pub = nh.advertise<geometry_msgs::Twist>("epuck2/cmd_vel",1000);
// Seed the  random number generator

// Loop at 2Gz until the node is shut down
ros::Rate rate(2);
while(ros::ok()){

// Create and fill in the message .The four fields ,which are ignored by turtlesim ,default to zero.
geometry_msgs::Twist msg;
msg.linear.x=0.2;
pub.publish(msg);
geometry_msgs::Twist turn_cmd;
turn_cmd.angular.z = 1.57;
// PUblish the message
pub.publish(turn_cmd);
// Wait until it's time for another iteration 
rate.sleep();
}
}
