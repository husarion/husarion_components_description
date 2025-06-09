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

import os

from ament_index_python import get_package_share_directory
from launch_ros.actions import Node
from nav2_common.launch import ReplaceString

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import (
    EnvironmentVariable,
    LaunchConfiguration,
    PythonExpression,
)


def generate_launch_description():
    husarion_components_description = get_package_share_directory(
        "husarion_components_description"
    )
    gz_bridge_config_path = os.path.join(
        husarion_components_description, "config", "gz_orbbec_astra_remappings.yaml"
    )

    robot_namespace = LaunchConfiguration("robot_namespace")
    device_namespace = LaunchConfiguration("device_namespace")
    gz_bridge_name = LaunchConfiguration("gz_bridge_name")

    device_namespace = PythonExpression(
        ["'", device_namespace, "' if '", device_namespace, "' else 'camera'"]
    )

    namespaced_gz_bridge_config_path = ReplaceString(
        source_file=gz_bridge_config_path,
        replacements={
            "<robot_namespace>": robot_namespace,
            "<device_namespace>": device_namespace,
        },
    )

    declare_device_namespace = DeclareLaunchArgument(
        "device_namespace",
        default_value="",
        description="Sensor namespace that will appear before all non absolute topics and TF frames, used for distinguishing multiple cameras on the same robot.",
    )

    declare_robot_namespace = DeclareLaunchArgument(
        "robot_namespace",
        default_value=EnvironmentVariable("ROBOT_NAMESPACE", default_value=""),
        description="Namespace which will appear in front of all topics (including /tf and /tf_static).",
    )

    declare_gz_bridge_name = DeclareLaunchArgument(
        "gz_bridge_name",
        default_value="gz_bridge",
        description="Name of gz bridge node.",
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
            declare_device_namespace,
            declare_robot_namespace,
            declare_gz_bridge_name,
            gz_bridge,
        ]
    )
