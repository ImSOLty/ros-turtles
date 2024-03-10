#!/usr/bin/python3

import rospy
import time
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from turtlesim.srv import Spawn
from turtle_commander import TurtleCommander, TurtlePosition


class TurtleCommanderNode:
    UPDATE_DELAY = 0.1

    def __init__(self):
        self._init_node()
        self._commander = TurtleCommander(self.turtle_speed)

    def run(self):
        while not rospy.is_shutdown():
            self._exec()
            time.sleep(self.UPDATE_DELAY)

    def _read_params(self):
        try:
            self.turtle_x, self.turtle_y = map(float, rospy.get_param('~turtle_coordinates').split()[:2])
            self.turtle_speed = rospy.get_param('~turtle_speed')
            self.turtle_target = rospy.get_param('~turtle_target')
            self.turtle_name = rospy.get_param('~turtle_name')
        except Exception as error:
            rospy.logerr(f"Ошибка парсинга параметров: {error}")

    @staticmethod
    def _create_turtle(turtle_name: str, x: float, y: float):
        spawn = rospy.ServiceProxy('/spawn', Spawn)
        spawn(x, y, 0.0, turtle_name)

    def _init_node(self):
        rospy.init_node('turtle_template')
        rospy.wait_for_service('/spawn')

        self._read_params()
        self._create_turtle(self.turtle_name, self.turtle_x, self.turtle_y)

        rospy.Subscriber(f'/{self.turtle_target}/pose', Pose, self._update_target_pos_callback)
        rospy.Subscriber(f'/{self.turtle_name}/pose', Pose, self._update_self_pos_callback)
        self.velocity_publisher = rospy.Publisher(f'/{self.turtle_name}/cmd_vel', Twist, queue_size=10)

    def _update_target_pos_callback(self, msg):
        self._commander.update_target_position(TurtlePosition(msg.x, msg.y, msg.theta))

    def _update_self_pos_callback(self, msg):
        self._commander.update_position(TurtlePosition(msg.x, msg.y, msg.theta))

    def _exec(self):
        movement = self._commander.calculate_movement()
        msg = Twist()
        msg.linear.x = movement.x_linear_velocity
        msg.linear.y = movement.y_linear_velocity
        msg.angular.z = movement.z_angular_velocity
        self.velocity_publisher.publish(msg)


if __name__ == '__main__':
    node = TurtleCommanderNode()
    node.run()
