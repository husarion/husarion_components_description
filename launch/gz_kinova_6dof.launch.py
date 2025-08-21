# Copyright 2024 Husarion sp. z o.o.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from nav2_common.launch import ReplaceString

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import (
    EnvironmentVariable,
    LaunchConfiguration,
    PathJoinSubstitution,
)


def generate_launch_description():
    robot_namespace = LaunchConfiguration("robot_namespace")
    component_name = LaunchConfiguration("component_name")

    initial_joint_controllers = PathJoinSubstitution(
        [
            FindPackageShare("husarion_components_description"),
            "config",
            "kinova_6dof_controllers.yaml",
        ]
    )

    gz_bridge_name = LaunchConfiguration("gz_bridge_name")
    gz_bridge_config_path = PathJoinSubstitution(
        [
            FindPackageShare("husarion_components_description"),
            "config",
            "gz_kinova_remappings.yaml",
        ]
    )

    namespaced_gz_bridge_config_path = ReplaceString(
        source_file=gz_bridge_config_path,
        replacements={
            "<robot_namespace>": robot_namespace,
            "<component_name>": component_name,
        },
    )

    namespaced_initial_joint_controllers_path = ReplaceString(
        source_file=initial_joint_controllers,
        replacements={
            "- joint": ["- ", component_name, "_joint"],
            "  joint_trajectory_controller:": [
                "  ",
                component_name,
                "_joint_trajectory_controller:",
            ],
            "  robotiq_gripper_controller:": [
                "  ",
                component_name,
                "_robotiq_gripper_controller:",
            ],
            "robotiq_85_left_knuckle_joint": [component_name, "_robotiq_85_left_knuckle_joint"],
        },
    )

    declare_component_name = DeclareLaunchArgument(
        "component_name",
        default_value="",
        description="Sensor namespace that will appear before all non absolute topics and TF frames, used for distinguishing multiple cameras on the same robot.",
    )

    declare_robot_namespace = DeclareLaunchArgument(
        "robot_namespace",
        default_value=EnvironmentVariable("ROBOT_NAMESPACE", default_value=""),
        description="Namespace which will appear in front of all topics (including /tf and /tf_static).",
    )

    # There may be other controllers of the joints, but this is the initially-started one
    initial_joint_controller_spawner_started = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            [component_name, "_joint_trajectory_controller"],
            "-t",
            "joint_trajectory_controller/JointTrajectoryController",
            "-c",
            "controller_manager",
            "--controller-manager-timeout",
            "10",
            "--namespace",
            robot_namespace,
            "--param-file",
            namespaced_initial_joint_controllers_path,
        ],
        namespace=robot_namespace,
    )

    robot_hand_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            [component_name, "_robotiq_gripper_controller"],
            "-t",
            "position_controllers/GripperActionController",
            "-c",
            "controller_manager",
            "--controller-manager-timeout",
            "10",
            "--namespace",
            robot_namespace,
            "--param-file",
            namespaced_initial_joint_controllers_path,
        ],
        namespace=robot_namespace,
    )

    gz_bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        name=gz_bridge_name,
        parameters=[{"config_file": namespaced_gz_bridge_config_path}],
        namespace=robot_namespace,
        output="screen",
    )

    return LaunchDescription(
        [
            declare_component_name,
            declare_robot_namespace,
            initial_joint_controller_spawner_started,
            robot_hand_controller_spawner,
            gz_bridge,
        ]
    )
