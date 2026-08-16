# ros2-ai-based-autonomous-restaurant-serving-robot-by-pytorch-nltk-nav2-slam-and-ros2_controll

# NLP-Driven Autonomous Restaurant Service Robot

## Overview

This project is a complete ROS2 and Gazebo simulation of an autonomous restaurant delivery robot. It bridges the gap between natural language understanding and real-time robot control. By typing a natural language request (e.g., "table 5" or "kitchen"), customers can command the robot. The system uses a trained PyTorch model to classify the intent, maps that intent to a specific spatial goal, and relies on the ROS2 Nav2 stack to autonomously plan the path and navigate while avoiding obstacles.

---

## Features & Workflow

* **Natural Language Processing:** Customers input text requests which are tokenized and preprocessed (stemming/lemmatization) using NLTK.
* **Intent Classification:** A PyTorch neural network classifies the preprocessed text into a specific service intent.
* **Autonomous Navigation:** The classified intent is mapped to a spatial pose and published as a `NavigateToPose` goal. The full ROS2 Nav2 stack takes over to drive the robot to the correct location.
* **Real-Time Obstacle Avoidance:** The Nav2 planner and controller dynamically route around obstacles within the custom simulated restaurant environment.
* **Robust Lifecycle Management:** Features proper launch sequencing using `OnProcessExit` event handlers, ensuring that `ros2_control` controllers only spawn after Gazebo and the robot state publisher are fully ready.

---

## Technical Stack

* **Robotics Middleware:** ROS2 (Humble)
* **Hardware Simulation:** Gazebo, `ros2_control`, `diff_drive_controller`
* **Localization & Mapping:** SLAM Toolbox, AMCL (nav2_bringup)
* **Navigation:** ROS2 Nav2 Stack (planner, controller, behavior server)
* **Machine Learning & NLP:** PyTorch, NLTK (Python)

---

## Setup & Installation

**1. Prepare the Workspace**
Extract the package into your ROS2 workspace and install dependencies:

```bash
cd ~/res_robo/src
unzip restaurant_bot.zip
cd ~/res_robo
rosdep install --from-paths src --ignore-src -r -y

```

**2. Build the Package**
Compile the specific robot package and source the workspace:

```bash
colcon build --packages-select restaurant_bot
source install/setup.bash

```

---

## Execution Guide

**1. Launch the Simulation Environment**
Start Gazebo with the custom restaurant world and bounded perimeter walls:

```bash
ros2 launch restaurant_bot restaurant_world.launch.py

```

(Alternatively, you can test the base simulation using `ros2 launch restaurant_bot gazebo.launch.py`)

**2. Mapping the Environment (SLAM)**
To create a new map of the environment, launch the SLAM Toolbox in online asynchronous mode:

```bash
ros2 launch slam_toolbox online_async_launch.py use_sim_time:=True

```

**3. Autonomous Navigation (Nav2 & AMCL)**
Once a map is saved (e.g., `my_map.yaml`), launch the Nav2 stack with AMCL localization:

```bash
ros2 launch nav2_bringup bringup_launch.py map:=/home/vboxuser/res_robo/my_map.yaml slam:=False use_sim_time:=True

```

**4. Visualization (RViz2)**
Open RViz2 using the default Nav2 view to provide 2D pose estimates and monitor navigation:

```bash
LIBGL_ALWAYS_SOFTWARE=1 ros2 run rviz2 rviz2 -d /opt/ros/humble/share/nav2_bringup/rviz/nav2_default_view.rviz

```

---

## Teleoperation & Controller Testing

**Keyboard Teleoperation:**
To manually control the robot using your keyboard, you can use the `teleop_twist_keyboard` package alongside the custom relay script. Open two separate terminals and run:

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard

```

```bash
python3 ~/cmd_vel_relay.py

```

**Direct Command Publishing:**
Alternatively, you can test the differential drive controller and verify the `gazebo_ros2_control` plugin configuration by publishing velocity commands directly via the terminal:

* **Drive Forward:**
```bash
ros2 topic pub -r 10 /diff_drive_controller/cmd_vel_unstamped geometry_msgs/msg/Twist "{linear: {x: 0.3}, angular: {z: 0.0}}"

```


* **Rotate Left:**
```bash
ros2 topic pub -r 10 /diff_drive_controller/cmd_vel_unstamped geometry_msgs/msg/Twist "{linear: {x: 0.0}, angular: {z: 0.8}}"

```


* **Rotate Right:**
```bash
ros2 topic pub -r 10 /diff_drive_controller/cmd_vel_unstamped geometry_msgs/msg/Twist "{linear: {x: 0.0}, angular: {z: -0.8}}"

```


* **Drive Backward:**
```bash
ros2 topic pub -r 10 /diff_drive_controller/cmd_vel_unstamped geometry_msgs/msg/Twist "{linear: {x: -0.3}, angular: {z: 0.0}}"

```
