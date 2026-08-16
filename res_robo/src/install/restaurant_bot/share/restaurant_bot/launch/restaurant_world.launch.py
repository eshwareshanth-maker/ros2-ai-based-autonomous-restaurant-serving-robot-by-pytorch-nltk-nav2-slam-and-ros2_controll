from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription

from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node

from ament_index_python.packages import get_package_share_directory

import os
import xacro


def generate_launch_description():

    pkg = get_package_share_directory('restaurant_bot')


    # ================= WORLD =================

    world_file = os.path.join(
        pkg,
        'worlds',
        'restaurant.world'
    )


    # ================= ROBOT DESCRIPTION =================

    xacro_file = os.path.join(
        pkg,
        'urdf',
        'restaurant_bot.urdf.xacro'
    )


    robot_description = xacro.process_file(
        xacro_file
    ).toxml()



    # ================= GAZEBO =================

    gazebo = IncludeLaunchDescription(

        PythonLaunchDescriptionSource(

            os.path.join(

                get_package_share_directory('gazebo_ros'),

                'launch',

                'gazebo.launch.py'

            )

        ),

        launch_arguments={

            'world': world_file

        }.items()

    )


    # ================= ROBOT STATE PUBLISHER =================

    robot_state_publisher = Node(

        package='robot_state_publisher',

        executable='robot_state_publisher',

        output='screen',

        parameters=[

            {

                'robot_description': robot_description,

                'use_sim_time': True

            }

        ]

    )


    # ================= SPAWN ROBOT =================

    spawn_robot = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
          '-entity','restaurant_bot',
          '-topic','robot_description',

          '-x','3.0',
          '-y','0.0',
          '-z','0.2'
        ],
        output='screen'
    )

    joint_state_broadcaster_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=[
           'joint_state_broadcaster',
           '--controller-manager',
           '/controller_manager'
        ],
        output='screen',
    )

    diff_drive_controller_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=[
        'diff_drive_controller',
        '--controller-manager',
        '/controller_manager'
    ],
    output='screen',
    )
    
    return LaunchDescription([

        gazebo,

        robot_state_publisher,

        spawn_robot,
        
        joint_state_broadcaster_spawner,

        diff_drive_controller_spawner,

    ])
