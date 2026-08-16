#=================================================================
#Author : Eshanth Eshwar M
#email : eshwareshanth@gmail.com
#=================================================================


import rclpy
from rclpy.node import  Node
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import String

received = False
go = ""

rclpy.init()
node = rclpy.create_node('goal_pose_publisher')
pub = node.create_publisher(PoseStamped, '/goal_pose', 10)



def callback(msg):
    global go, received
    go = msg.data
    node.get_logger().info(f'subscriber: "{msg.data}"')
    print("Received destination: ", go)
    received = True

node.create_subscription(
        String,
        '/msg_topic',
        callback,
        10
      )


def main():
    global go, received
      
    # named locations - get the values (x, y, z) of the location you need
    locations = {
        'kitchen': {'x':-0.3817234933376312, 'y':0.02502373978495598, 'z': 0.64825453125},
        'tableone': {'x':0.9762235879879898071, 'y':3.3404734134134674072, 'z': 0.6661376953125},
        'tabletwo': {'x':5.197628021240234, 'y':3.1972391605377197, 'z': 0.67416381359375},
        'tablethree': {'x':9.088723182678223, 'y':3.3970651626586914, 'z': -0.001373291015625},
        'tablefour': {'x':4.017457485198975, 'y':9.173336982705, 'z':-0.001434326171875},
        'tablefive': {'x':6.074239253997803, 'y':5.7206993102734, 'z':-0.001434326171875},
        'tablesix': {'x':8.190852165222168, 'y':2.421475887298584, 'z':-0.005340576171875},
        'tableseven': {'x':3.7346034049987793, 'y':10.03469276482227, 'z':-0.001434326171875},
        'tableeight': {'x':4.543452739715576, 'y':5.87551212310791, 'z':-0.001434326171875},
        'tablenine': {'x':5.176090240478516, 'y':2.363809108734131, 'z':-0.005340576171875},
        'tableten': {'x':8.058374404907227, 'y':8.8929023744004907227, 'z':0.002532958984375},
        'tableeleven': {'x':6.428528308868408, 'y':6.4285283308868408, 'z':-0.001434326171875},
        'tabletweleve': {'x':4.419790744781494, 'y':16.103622436523438, 'z':0.002471923828125},
    }

    try:
        while rclpy.ok():
            rclpy.spin_once(node, timeout_sec=0.1)
            
            print(f"Received destination: {name}")

             
            if not received:
                continue

            destination = go
            name = destination
            
            if name not in locations:
                print("Unknown location.")
                continue
            x = locations[name]['x']
            y = locations[name]['y']
            z = locations[name]['z']

            

            goal = PoseStamped()
            goal.header.frame_id = 'map'
            goal.header.stamp = node.get_clock().now().to_msg()
            goal.pose.position.x = x
            goal.pose.position.y = y
            goal.pose.position.z = z
            
            goal.pose.orientation.x = 0.0
            goal.pose.orientation.y = 0.0
            goal.pose.orientation.z = 0.0
            goal.pose.orientation.w = 1.0

            pub.publish(goal)
            print(f"Published goal: x={x}, y={y}, z={z}")
            received = False  
    except KeyboardInterrupt:
        pass

    
    
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
