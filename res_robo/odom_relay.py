#=================================================================
#Author : Eshanth Eshwar M
#email : eshwareshanth@gmail.com
#=================================================================


import rclpy

from rclpy.node import Node
from nav_msgs.msg import Odometry


publisher = None


def odom_callback(msg):
    publisher.publish(msg)


def main():

    global publisher

    rclpy.init()

    node = Node("odom_relay")

    publisher = node.create_publisher(
        Odometry,
        "/odom",
        10
    )

    node.create_subscription(
        Odometry,
        "/diff_drive_controller/odom",
        odom_callback,
        10
    )

    print("Relaying:")
    print("/diff_drive_controller/odom  --->  /odom")

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
