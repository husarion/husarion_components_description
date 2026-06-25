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

List the components you want under `components:`. Each entry selects a `type` — an
intuitive **name** or its historical **code** (both work, see
[Available components](#available-components)) — and where to mount it:

```yaml
components:
  - type: rplidar_s3        # intuitive name
    parent_link: cover_link
    xyz: 0.0 0.0 0.2
    rpy: 0.0 0.0 0.0

  - type: CAM06             # or the historical code (here: zed_x)
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
| `type`        | yes      | component name or code (see [Available components](#available-components)), or `custom` |
| `parent_link` | yes      | robot link the component is attached to                                             |
| `name`        | no       | local name; prefixes the component's frames so identical devices don't collide      |
| `xyz`         | no       | translation from `parent_link` `[m]`, default `0.0 0.0 0.0`                          |
| `rpy`         | no       | rotation from `parent_link` `[rad]`, default `0.0 0.0 0.0`                           |

Some types accept extra fields (e.g. `RCK` takes `elements`, `custom` takes `package`/`file`).

## Available components

Put the **Name** in `type:` (recommended) or the **Code** — both resolve to the same
component. Some devices have no code (e.g. `rplidar_c1`) and are selected by name only.
A few short aliases also work: `astra`, `realsense`, `oak`, `wibotic`.

### Frames & mounts

| Name               | Code   | Device                                         |
| ------------------ | ------ | ---------------------------------------------- |
| cover_access_panel | DEV01  | User Compartment Cover with Quick Access Panel |
| carrying_handles   | DEV02  | Handles for Carrying the Robot                 |
| mounting_plate     | DEV03  | Mounting Plate for Mounting Rails              |
| frame_370          | DEV04H | 370 mm High Frame for Sensors                  |
| frame_170          | DEV04L | 170 mm High Frame for Sensors                  |
| pillar_350         | DEV05  | 350 mm Pillar for Sensors                      |
| basket_railings    | DEV06  | Basket on Railings                             |
| gate_small         | DEV07  | Small Gate                                     |
| gate_small_rotated | DEV07T | Small Gate (rotated)                           |
| gate_large         | DEV09  | Large Gate                                     |
| rack               | RCK    | Rack made of profiles                          |

### Cameras

| Name           | Code  | Device               |
| -------------- | ----- | -------------------- |
| orbbec_astra   | CAM01 | Orbbec Astra         |
| realsense_d435 | CAM02 | Intel RealSense D435 |
| zed_2          | CAM03 | StereoLabs ZED 2     |
| zed_2i         | CAM04 | StereoLabs ZED 2i    |
| zed_m          | CAM05 | StereoLabs ZED M     |
| zed_x          | CAM06 | StereoLabs ZED X     |
| oak_d_pro      | CAM11 | Luxonis OAK-D-PRO    |

### Lidars

| Name           | Code  | Device         |
| -------------- | ----- | -------------- |
| rplidar_s1     | LDR01 | RPLIDAR S1     |
| rplidar_s2     | LDR02 | RPLIDAR S2     |
| rplidar_a2m12  | LDR03 | RPLIDAR A2M12  |
| rplidar_a3     | LDR04 | RPLIDAR A3     |
| rplidar_c1     | —     | RPLIDAR C1     |
| rplidar_s3     | LDR06 | RPLIDAR S3     |
| ouster_os0_32  | LDR10 | Ouster OS0-32  |
| ouster_os0_64  | LDR11 | Ouster OS0-64  |
| ouster_os0_128 | LDR12 | Ouster OS0-128 |
| ouster_os1_32  | LDR13 | Ouster OS1-32  |
| ouster_os1_64  | LDR14 | Ouster OS1-64  |
| ouster_os1_128 | LDR15 | Ouster OS1-128 |
| velodyne_puck  | LDR20 | Velodyne Puck  |
| velodyne_alpha_prime | LDR22 | Velodyne Alpha Prime |

### Manipulators

| Name                    | Code  | Device                       |
| ----------------------- | ----- | ---------------------------- |
| ur3e                    | MAN01 | Universal Robots UR3e        |
| ur5e                    | MAN02 | Universal Robots UR5e        |
| kinova_gen3_6dof        | MAN04 | 6DoF Kinova Gen3             |
| kinova_gen3_6dof_vision | MAN05 | 6DoF Kinova Gen3 + 3D vision |
| kinova_gen3_7dof        | MAN06 | 7DoF Kinova Gen3             |
| kinova_gen3_7dof_vision | MAN07 | 7DoF Kinova Gen3 + 3D vision |

> [!NOTE]
> The manipulators (code `MAN<X>`) must only be used within the simulation environment.
> Support for manipulators on a physical robot is implemented as separate software components.
> Please refer to [the official documentation](https://husarion.com/manuals/panther/manipulators).

### Grippers

| Name          | Code  | Device        |
| ------------- | ----- | ------------- |
| robotiq_2f_85 | GRP02 | Robotiq 2F-85 |

### Connectivity & power

| Name             | Code  | Device               |
| ---------------- | ----- | -------------------- |
| teltonika        | ANT02 | Teltonika 003R-00253 |
| wibotic_receiver | WCH01 | Wibotic receiver     |

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
