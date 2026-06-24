# husarion_components_description

URDF models of sensors and other components offered alongside Husarion robots.

## Overview

Components (cameras, lidars, frames, manipulators, …) are attached to a robot from a
single YAML config: a list of entries, each picking a component by its `type` code and
placing it on a parent link. Husarion robot packages (e.g. `rosbot_description`) read this
config and build the URDF for you; you can also instantiate a component's xacro macro
directly (see [Advanced](#advanced-direct-xacro-include)).

## Build

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

## Usage via config

List the components you want under `components:`. Each entry selects a `type` (see
[Available components](#available-components)) and where to mount it:

```yaml
components:
  - type: LDR06
    parent_link: cover_link
    xyz: 0.0 0.0 0.2
    rpy: 0.0 0.0 0.0

  - type: CAM06
    name: front
    parent_link: camera_mount_link
    xyz: -0.01 0.0 0.02
    rpy: 0.0 0.0 0.0

  - type: RCK
    name: rack
    parent_link: mount_link
    xyz: 0.0 0.0 0.0
    rpy: 0.0 0.0 0.0
    elements:
      - length: 0.42
        xyz: 0.185 0.0 0.21
        rpy: 0.0 0.0 1.5708
      - length: 0.2
        xyz: 0.185 0.2 0.1
        rpy: 0.0 1.5708 0.0
      - length: 0.2
        xyz: 0.185 -0.2 0.1
        rpy: 0.0 1.5708 0.0
```

### Config schema

| field         | required | description                                                                         |
| ------------- | -------- | ----------------------------------------------------------------------------------- |
| `type`        | yes      | component code (see [Available components](#available-components)), or `custom`      |
| `parent_link` | yes      | robot link the component is attached to                                             |
| `name`        | no       | local name; prefixes the component's frames so identical devices don't collide      |
| `xyz`         | no       | translation from `parent_link` `[m]`, default `0.0 0.0 0.0`                          |
| `rpy`         | no       | rotation from `parent_link` `[rad]`, default `0.0 0.0 0.0`                           |

Some types accept extra fields (e.g. `RCK` takes `elements`, `custom` takes `package`/`file`).

## Available components

### Frames & mounts

| Code   | Device Name               |
| ------ | ------------------------- |
| DEV01  | Cover with Access Panel   |
| DEV02  | Carrying Handles          |
| DEV03  | Wooden Mounting Plate     |
| DEV04H | 370 mm High Frame         |
| DEV04L | 170 mm High Frame         |
| DEV05  | 350 mm Pillar             |
| DEV06  | Basket on Railings        |
| DEV07  | 475 mm Small Gate         |
| DEV07T | 350 mm Rotated Small Gate |
| DEV09  | Large Gate                |
| RCK    | Rack made of profiles     |

### Cameras

| Code  | Device Name      |
| ----- | ---------------- |
| CAM01 | Orbbec Astra     |
| CAM03 | StereoLabs ZED 2 |
| CAM04 | StereoLabs ZED 2i |
| CAM05 | StereoLabs ZED M |
| CAM06 | StereoLabs ZED X |
| CAM11 | Luxonis OAK-D-PRO |

### Lidars

| Code  | Device Name    |
| ----- | -------------- |
| LDR01 | RPLIDAR S1     |
| LDR06 | RPLIDAR S3     |
| LDR10 | Ouster OS0-32  |
| LDR11 | Ouster OS0-64  |
| LDR12 | Ouster OS0-128 |
| LDR13 | Ouster OS1-32  |
| LDR14 | Ouster OS1-64  |
| LDR15 | Ouster OS1-128 |
| LDR20 | Velodyne Puck  |

### Manipulators

| Code  | Device Name                 |
| ----- | --------------------------- |
| MAN01 | Universal Robots UR3e       |
| MAN02 | Universal Robots UR5e       |
| MAN04 | 6DoF Kinova Gen3            |
| MAN05 | 6DoF Kinova Gen3 + 3D vision |
| MAN06 | 7DoF Kinova Gen3            |
| MAN07 | 7DoF Kinova Gen3 + 3D vision |

> [!NOTE]
> The manipulators (code `MAN<X>`) must only be used within the simulation environment.
> Support for manipulators on a physical robot is implemented as separate software components.
> Please refer to [the official documentation](https://husarion.com/manuals/panther/manipulators).

### Grippers

| Code  | Device Name  |
| ----- | ------------ |
| GRP02 | Robotiq 2F-85 |

### Connectivity & power

| Code  | Device Name          |
| ----- | -------------------- |
| ANT02 | Teltonika 003R-00253 |
| WCH01 | Wibotic receiver     |

## Custom component

Use `type: custom` to attach your own URDF/xacro (with its meshes) without adding a new
component code. The referenced file must define a macro with the standard component
signature (`parent_link`, `xyz`, `rpy`, `component_name`, `robot_namespace`,
`use_tf_prefix`); its name defaults to `custom_component` and can be overridden with
`macro_name`.
See [urdf/custom_component_example.urdf.xacro](urdf/custom_component_example.urdf.xacro)
for a runnable, copy-paste template.

```yaml
components:
  - type: custom
    package: my_robot_description # resolved as $(find package)/file
    file: urdf/my_sensor.urdf.xacro
    # ...or drop `package` and give an absolute path (handy locally, not portable):
    # file: /home/user/my_sensor.urdf.xacro
    # macro_name: my_macro # optional, defaults to custom_component
    name: my_sensor
    parent_link: cover_link
    xyz: 0.0 0.0 0.1
    rpy: 0.0 0.0 0.0
```

Fields specific to `custom`:

| field        | required | description                                                                        |
| ------------ | -------- | ---------------------------------------------------------------------------------- |
| `package`    | no       | ROS package containing `file`. Omit to use an absolute `file` path (handy locally, but not portable - prefer a package) |
| `file`       | yes      | path to your xacro; resolved against `package` when present, otherwise absolute     |
| `macro_name` | no       | name of the macro to call inside `file`, default `custom_component`                 |

Reference meshes from your package with `package://my_robot_description/meshes/...`
(portable), or - only with the absolute-path form - by an absolute `file://` URI.

## Advanced: direct xacro include

Instead of the config you can instantiate a component's macro directly in your own xacro:

```xml
<!-- include file with definition of xacro macro of the component -->
<xacro:include filename="$(find husarion_components_description)/urdf/slamtec_rplidar.urdf.xacro" ns="lidar" />

<!-- evaluate the macro and place the component on the robot -->
<xacro:lidar.slamtec_rplidar
  parent_link="cover_link"
  xyz="0.0 0.0 0.0"
  rpy="0.0 0.0 0.0" />
```

Common macro parameters:

- `component_name` [*string*, default: **''**] local namespace to distinguish two identical devices. Called `name` in the config.
- `parent_link` [*string*, default: **None**] parent link to which the component is attached.
- `xyz` [*float list*, default: **0.0 0.0 0.0**] translation between the component base and parent link, in **m**.
- `rpy` [*float list*, default: **0.0 0.0 0.0**] rotation between the parent link and component base, in **rad**.
- `robot_namespace` [*string*, default: **''**] global namespace common to the entire robot. Not present in the config.
- `model` [*string*, default: **''**] selects the manufacturer model variant. Not present in the config.
- `use_tf_prefix` [*bool*, default: **True**] use `robot_namespace` as a prefix for all frame_ids. Useful when every robot has its own tf tree. Not present in the config.

Some components define their own specific parameters - refer to their definition for more info.
