# husarion_components_description

URDF models of sensors and other components offered alongside with Husarion robots

## Available URDF Sensors

<div align="center">

| Code  | Device Name                  |
| ----- | ---------------------------- |
| ANT02 | Teltonika 003R-00253         |
| CAM01 | Orbbec Astra                 |
| CAM03 | StereoLabs ZED 2             |
| CAM04 | StereoLabs ZED 2i            |
| CAM05 | StereoLabs ZED M             |
| CAM06 | StereoLabs ZED X             |
| CAM11 | Luxonis OAK-D-PRO            |
| LDR01 | RPLIDAR S1                   |
| LDR06 | RPLIDAR S3                   |
| LDR10 | Ouster OS0-32                |
| LDR11 | Ouster OS0-64                |
| LDR12 | Ouster OS0-128               |
| LDR13 | Ouster OS1-32                |
| LDR14 | Ouster OS1-64                |
| LDR15 | Ouster OS1-128               |
| LDR20 | Velodyne Puck                |
| MAN01 | Universal Robots UR3e        |
| MAN02 | Universal Robots UR5e        |
| MAN04 | 6DoF Kinova Gen3             |
| MAN05 | 6DoF Kinova Gen3 + 3D vision |
| MAN06 | 7DoF Kinova Gen3             |
| MAN07 | 7DoF Kinova Gen3 + 3D vision |
| GRP02 | Robotiq 2F-85                |
| WCH01 | Wibotic receiver             |

</div>

## Including sensor

First build the package by running:

```bash
# create workspace folder and clone husarion_components_description
mkdir -p ros2_ws/src
cd ros2_ws
git clone https://github.com/husarion/husarion_components_description.git src/husarion_components_description

# in case the package will be used within simulation
export HUSARION_ROS_BUILD_TYPE=simulation

rosdep update --rosdistro $ROS_DISTRO
rosdep install -i --from-path src --rosdistro $ROS_DISTRO -y
colcon build
```

To include the sensor, use the following code:

```xml
<!-- include file with definition of xacro macro of sensor -->
<xacro:include filename="$(find husarion_components_description)/urdf/slamtec_rplidar.urdf.xacro" ns="lidar" />

<!-- evaluate the macro and place the sensor on robot -->
<xacro:lidar.slamtec_rplidar
  parent_link="cover_link"
  xyz="0.0 0.0 0.0"
  rpy="0.0 0.0 0.0" />
```

A list of parameters can be found here:

- `parent_link` [*string*, default: **None**] parent link to which sensor should be attached.
- `xyz` [*float list*, default: **0.0 0.0 0.0**] 3 float values defining translation between base of a sensor and parent link. Values in **m**.
- `rpy` [*float list*, default: **0.0 0.0 0.0**] 3 float values define rotation between parent link and base of a sensor. Values in **rad**.
- `namespace` [*string*, default: **''**] global namespace common to the entire robot.
- `device_namespace` [*string*, default: **''**] local namespace allowing to distinguish two identical devices from each other.

- `model` [*string*, default: **''**] model argument that appears when you want to load the appropriate model from a given manufacturer.

Some sensors can define their specific parameters. Refer to their definition for more info.
