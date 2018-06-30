import rospy
import EPUCK_GYM

bot = EPUCK_GYM.EPUCK_GYM()
bot.reset_world()
print(bot.get_laser_data())
print(bot.get_position())
bot.motion(0.1,0)
