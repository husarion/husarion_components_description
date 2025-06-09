#!/usr/bin/env python3

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

import yaml
from launch_ros.actions import Node

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import EnvironmentVariable, LaunchConfiguration


def launch_setup(context, *args, **kwargs):
    components_config_path = LaunchConfiguration("components_config_path").perform(context)
    robot_namespace = LaunchConfiguration("robot_namespace")
    device_namespace = LaunchConfiguration("device_namespace")

    components_config = None
    if components_config_path == "":
        return []

    with open(os.path.join(components_config_path)) as file:
        components_config = yaml.safe_load(file)

    actions = []

    for component in components_config["components"]:
        component_type = component["type"]
        if component_type == "WCH02":

            component_xyz = [x for x in component["xyz"].split()]
            component_rpy = [x for x in component["rpy"].split()]

            spawn_station = Node(
                package="ros_gz_sim",
                executable="create",
                arguments=[
                    "-name",
                    [robot_namespace, "_", device_namespace, "_station"],
                    "-topic",
                    "station_description",
                    "-x",
                    component_xyz[0],
                    "-y",
                    component_xyz[1],
                    "-z",
                    component_xyz[2],
                    "-R",
                    component_rpy[0],
                    "-P",
                    component_rpy[1],
                    "-Y",
                    component_rpy[2],
                ],
                namespace=robot_namespace,
                emulate_tty=True,
            )

            actions.append(spawn_station)

    return actions


def generate_launch_description():
    declare_components_config_path_arg = DeclareLaunchArgument(
        "components_config_path",
        default_value="",
        description=(
            "Additional components configuration file. Components described in this file "
            "are dynamically included in Panther's urdf."
            "Panther options are described here "
            "https://husarion.com/manuals/panther/panther-options/"
        ),
    )

    declare_device_namespace = DeclareLaunchArgument(
        "device_namespace",
        default_value="",
        description="Device namespace that will appear before all non absolute topics and TF frames, used for distinguishing multiple cameras on the same robot.",
    )

    declare_robot_namespace = DeclareLaunchArgument(
        "robot_namespace",
        default_value=EnvironmentVariable("ROBOT_NAMESPACE", default_value=""),
        description="Namespace which will appear in front of all topics (including /tf and /tf_static).",
    )

    return LaunchDescription(
        [
            declare_components_config_path_arg,
            declare_device_namespace,
            declare_robot_namespace,
            OpaqueFunction(function=launch_setup),
        ]
    )
