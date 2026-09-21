# ==============================================================================
# Copyright (c) 2025 ORCA
#
# This file is part of ORCA and is licensed under the MIT License.
# You may use, copy, modify, and distribute this file under the terms of the MIT License.
# See the LICENSE file at the root of this repository for full license information.
# ==============================================================================

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution, Command
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue

def generate_launch_description():
    # Example usages:
    # - ros2 launch orcahand_description orcahand.launch.py
    # - ros2 launch orcahand_description orcahand.launch.py urdf_file:=v1/models/urdf/orcahand_left.urdf
    # - ros2 launch orcahand_description orcahand.launch.py gui:=true

    # Launch argument for a URDF path relative to the package root.
    urdf_file_arg = DeclareLaunchArgument(
        'urdf_file',
        default_value='v2/models/urdf/orcahand_right.urdf',
        description='URDF file to load from the orcahand_description package'
    )

    # Construct the full path to the URDF/XACRO file using the argument
    orcahand_description_path = PathJoinSubstitution([
        FindPackageShare('orcahand_description'),
        LaunchConfiguration('urdf_file')
    ])

    # Launch argument to use the joint_state_publisher GUI (sliders)
    gui_arg = DeclareLaunchArgument(
        'gui',
        default_value='false',
        description='Start joint_state_publisher_gui instead of joint_state_publisher'
    )

    # RViz config path (static)
    orcahand_rviz_config_path = PathJoinSubstitution([
        FindPackageShare('orcahand_description'),
        'rviz',
        'config.rviz'
    ])

    return LaunchDescription([
        urdf_file_arg,
        gui_arg,

        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{
                'robot_description': ParameterValue(
                    Command(['xacro ', orcahand_description_path]),
                    value_type=str
                )
            }],
        ),

        Node(
            package='joint_state_publisher',
            executable='joint_state_publisher',
            name='joint_state_publisher',
            output='screen',
            condition=UnlessCondition(LaunchConfiguration('gui')),
        ),

        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            name='joint_state_publisher_gui',
            output='screen',
            condition=IfCondition(LaunchConfiguration('gui')),
        ),

        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            arguments=['-d', orcahand_rviz_config_path],
        ),
    ])
