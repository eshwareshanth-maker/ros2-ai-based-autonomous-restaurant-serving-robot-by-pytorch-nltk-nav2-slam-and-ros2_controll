#=================================================================
#Author : Eshanth Eshwar M
#email : eshwareshanth@gmail.com
#=================================================================


import math
import rclpy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist


STOP_DIST      = 0.03
FRONT_HALF_ANG = math.radians(20)
ANG_SPEED      = 0.6
LIN_SPEED      = 0.08
TURN_45_TIME   = math.radians(45) / ANG_SPEED
BACKUP_TIME    = 1.0


state = 'IDLE'   # IDLE , TURN_RIGHT , TURN_LEFT , BACKUP  TURN_LEFT2
state_start_time = None
latest_scan = None
cmd_pub = None
node = None


def get_front_min(scan):
    n = len(scan.ranges)
    if n == 0:
        return float('inf')
    center = int((0 - scan.angle_min) / scan.angle_increment)
    half_idx = int(FRONT_HALF_ANG / scan.angle_increment)
    lo = max(0, center - half_idx)
    hi = min(n, center + half_idx)
    vals = [r for r in scan.ranges[lo:hi] if not math.isinf(r) and not math.isnan(r) and r > 0.0]
    return min(vals) if vals else float('inf')


def scan_cb(msg):
    global latest_scan
    latest_scan = msg


def elapsed():
    return (node.get_clock().now() - state_start_time).nanoseconds / 1e9


def set_state(new_state):
    global state, state_start_time
    state = new_state
    state_start_time = node.get_clock().now()


def control_loop():
    global state

    if latest_scan is None:
        return

    front = get_front_min(latest_scan)

    if state == 'IDLE':
        if front < STOP_DIST:
            set_state('TURN_RIGHT')
        return   # don't publish, let Nav2 drive

    twist = Twist()

    if state == 'TURN_RIGHT':
        twist.angular.z = -ANG_SPEED
        if elapsed() >= TURN_45_TIME:
            if get_front_min(latest_scan) < STOP_DIST:
                set_state('TURN_LEFT')
            else:
                set_state('IDLE')
                return

    elif state == 'TURN_LEFT':
        twist.angular.z = ANG_SPEED
        if elapsed() >= (TURN_45_TIME * 2):
            if get_front_min(latest_scan) < STOP_DIST:
                set_state('BACKUP')
            else:
                set_state('IDLE')
                return

    elif state == 'BACKUP':
        twist.linear.x = -LIN_SPEED
        if elapsed() >= BACKUP_TIME:
            set_state('TURN_LEFT2')

    elif state == 'TURN_LEFT2':
        twist.angular.z = ANG_SPEED
        if elapsed() >= TURN_45_TIME:
            set_state('IDLE')
            return

    cmd_pub.publish(twist)


def main():
    global cmd_pub, node, state_start_time
    rclpy.init()
    node = rclpy.create_node('obstacle_avoidance_node')

    node.create_subscription(LaserScan, '/scan', scan_cb, 10)
    cmd_pub = node.create_publisher(Twist, '/cmd_vel', 10)

    state_start_time = node.get_clock().now()
    node.create_timer(0.05, control_loop)

    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
