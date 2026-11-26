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


import ast
import math
import os
import xml
import xml.dom
import xml.dom.minidom

import xacro
import yaml
from ament_index_python.packages import get_package_share_directory

husarion_components_description = get_package_share_directory("husarion_components_description")
xacro_path = os.path.join(husarion_components_description, "test/component.urdf.xacro")

# Type: [component_name, link_name, sensor_link_name, sensor_name, default_component_name]
components_types_with_names = {
    "DEV01": ["", "dev01_link", "", "", ""],
    "DEV02": ["", "dev02_link", "", "", ""],
    "DEV03": ["", "dev03_link", "", "", ""],
    "DEV04H": ["", "dev04h_link", "", "", ""],
    "DEV04L": ["", "dev04l_link", "", "", ""],
    "DEV05": ["", "dev05_link", "", "", ""],
    "DEV06": ["", "dev06_link", "", "", ""],
    "DEV07": ["", "dev07_link", "", "", ""],
    "DEV07T": ["", "dev07t_link", "", "", ""],
    "DEV09": ["", "dev09_link", "", "", ""],
    "LDR01": ["slamtec_rplidar_s1", "laser", "laser", "lidar", ""],
    "LDR06": ["slamtec_rplidar_s3", "laser", "laser", "lidar", ""],
    "LDR10": ["ouster_os0_32", "os_lidar", "os_lidar", "lidar", ""],
    "LDR11": ["ouster_os0_64", "os_lidar", "os_lidar", "lidar", ""],
    "LDR12": ["ouster_os0_128", "os_lidar", "os_lidar", "lidar", ""],
    "LDR13": ["ouster_os1_32", "os_lidar", "os_lidar", "lidar", ""],
    "LDR14": ["ouster_os1_64", "os_lidar", "os_lidar", "lidar", ""],
    "LDR15": ["ouster_os1_128", "os_lidar", "os_lidar", "lidar", ""],
    "LDR16": ["ouster_os2_32", "os_lidar", "os_lidar", "lidar", ""],
    "LDR17": ["ouster_os2_64", "os_lidar", "os_lidar", "lidar", ""],
    "LDR18": ["ouster_os2_128", "os_lidar", "os_lidar", "lidar", ""],
    "LDR40": ["ouster_osdome_64", "os_lidar", "os_lidar", "lidar", ""],
    "LDR41": ["ouster_osdome_128", "os_lidar", "os_lidar", "lidar", ""],
    "LDR20": ["velodyne_puck", "velodyne", "velodyne", "lidar", ""],
    "LDR22": ["velodyne_alpha_prime", "velodyne", "velodyne", "lidar", ""],
    "LDR50": ["livox_mid360", "livox_frame", "livox_frame", "lidar", ""],
    "CAM01": ["orbbec_astra", "link", "link", "camera_color", "camera"],
    "CAM03": ["zed2", "camera_center", "camera_center", "camera_color", "zed"],
    "CAM04": ["zed2i", "camera_center", "camera_center", "camera_color", "zed"],
    "CAM05": ["zedm", "camera_center", "camera_center", "camera_color", "zed"],
    "CAM06": ["zedx", "camera_center", "camera_center", "camera_color", "zed"],
    "CAM07": [
        "realsense_d555",
        "link",
        "link",
        "intel_realsense_d555_color",
        "camera",
    ],
    "MAN01": ["ur3e", "base_link", "", "", "ur"],
    "MAN02": ["ur5e", "base_link", "", "", "ur"],
    # "MAN03": ["kinova_lite",               "base_link",    "",         "",""], use_isaac error
    # "MAN04": ["kinova_gen3_6dof", "base_link", "", "", ""],
    # "MAN05": [
    #     "kinova_gen3_6dof",
    #     "base_link",
    #     "camera_color_frame",
    #     "camera_sensor",
    #     "kinova_gen3_6dof",
    # ],
    # "MAN06": ["kinova_gen3_7dof", "base_link", "", "", ""],
    # "MAN07": [
    #     "kinova_gen3_7dof",
    #     "base_link",
    #     "camera_color_frame",
    #     "camera_sensor",
    #     "kinova_gen3_7dof",
    # ],
    # "GRP01": [], not implemented in robotiq_description
    "GRP02": ["robotiq", "robotiq_85_base_link", "", "", "robotiq"],
    # "GRP03": ["robotiq", "robotiq_140_base_link", "", "", ""], not implemented in robotiq_description,
    "WCH01": ["wibotic_receiver", "mount_link", "", "", "wibotic_receiver"],
}


class ComponentsYamlParseUtils:
    __test__ = False

    def __init__(self, components_config_path: str) -> None:
        self.components_config_path = components_config_path
        self._urdf = xml.dom.minidom.Document()

    def save_yaml(self, node: yaml.Node) -> None:
        with open(self.components_config_path, mode="w", encoding="utf-8") as file:
            yaml.dump(node, file, default_flow_style=False)

    def create_component(
        self,
        type: str,
        component_name: str,
        parent_link="cover_link",
        xyz="0.0 0.0 0.0",
        rpy="0.0 0.0 0.0",
    ) -> dict:
        component = {
            "type": type,
            "parent_link": parent_link,
            "xyz": xyz,
            "rpy": rpy,
        }

        if component_name != "":
            component["name"] = component_name

        return component

    def does_urdf_parse(self) -> bool:
        try:
            self._urdf = xacro.process_file(
                xacro_path, mappings={"components_config_path": self.components_config_path}
            )
        except xacro.XacroException as e:
            print(f"XacroException: {e}")
            return False
        return True

    def does_link_exist(self, doc: xml.dom.minidom.Document, link_name: str) -> bool:
        links = doc.getElementsByTagName("link")
        for link in links:
            if link.getAttribute("name") == link_name:
                return True
        return False

    def does_sensor_name_exist(
        self, doc: xml.dom.minidom.Document, link_name: str, sensor_name: str
    ) -> bool:
        gazebos_tags = doc.getElementsByTagName("gazebo")
        for tag in gazebos_tags:
            if tag.getAttribute("reference") == link_name:
                sensors = doc.getElementsByTagName("sensor")
                for sensor in sensors:
                    if sensor.getAttribute("name") == sensor_name:
                        return True

        return False

    def get_sensor_topic(self, sensor_name: str) -> str:
        for sensor in self._urdf.getElementsByTagName("sensor"):
            if sensor.getAttribute("name") != sensor_name:
                continue

            topics = sensor.getElementsByTagName("topic")
            if len(topics) == 1 and topics[0].firstChild is not None:
                return topics[0].firstChild.data

        raise AssertionError(f"Topic for sensor {sensor_name} not found")

    def test_component(self, component: dict, expected_result: list, components_config_path: str):
        names = components_types_with_names[component["type"]]
        component_model_name = names[0]
        link_name = names[1]
        sensor_link_name = names[2]
        sensor_name = names[3]
        default_component_name = names[4]

        namespaced_link_name = link_name
        namespaced_sensor_link_name = sensor_link_name
        namespaced_sensor_name = sensor_name

        component_name = ""
        if "name" in component:
            component_name = component["name"]

        if component_name == "":
            component_name = default_component_name

        if component_name != "":
            namespaced_link_name = component_name + "_" + namespaced_link_name
            namespaced_sensor_link_name = component_name + "_" + namespaced_sensor_link_name
            namespaced_sensor_name = component_name + "_" + namespaced_sensor_name

        if self.does_urdf_parse() != expected_result[0]:
            assert (
                False
            ), f"Expected prase result {expected_result[0]} with file {components_config_path} and component {component_model_name}."

        if self.does_link_exist(self._urdf, namespaced_link_name) != expected_result[1]:
            assert (
                False
            ), f"Link name: {namespaced_link_name}. Expected result {expected_result[1]} with file {components_config_path} and component {component_model_name} for this urdf {self._urdf.toprettyxml()}."

        if (
            names[2] != ""
            and self.does_sensor_name_exist(
                self._urdf, namespaced_sensor_link_name, namespaced_sensor_name
            )
            != expected_result[2]
        ):
            assert (
                False
            ), f"Sensor name: {namespaced_sensor_name}, sensor link name: {namespaced_sensor_link_name}. Expected result {expected_result[2]} with file {components_config_path} and component {component_model_name} for this urdf ."


def test_all_good_single_components(tmpdir_factory):
    for type_name, value in components_types_with_names.items():
        component_name = value[0]
        folder_name = component_name

        if "DEV" in type_name:
            folder_name = type_name

        dir = tmpdir_factory.mktemp(folder_name)
        components_config_path = dir.join(folder_name + "_test_components.yaml")

        utils = ComponentsYamlParseUtils(str(components_config_path))
        components = {
            "components": [
                utils.create_component(type_name, component_name),
                utils.create_component(type_name, ""),
            ],
        }

        utils.save_yaml(components)

        for component in components["components"]:
            utils.test_component(component, [True, True, True], str(components_config_path))


def test_zed_uses_v5_topics(tmpdir_factory):
    components_config_path = tmpdir_factory.mktemp("zed_v5").join("components.yaml")
    utils = ComponentsYamlParseUtils(str(components_config_path))
    utils.save_yaml(
        {
            "components": [
                utils.create_component("CAM03", "front_camera"),
            ],
        }
    )

    assert utils.does_urdf_parse()
    assert (
        utils.get_sensor_topic("front_camera_camera_color")
        == "front_camera/zed_node/rgb/color/rect/image"
    )
    assert (
        utils.get_sensor_topic("front_camera_camera_depth")
        == "front_camera/zed_node/depth/depth_registered"
    )


MESH_URI_PREFIX = "package://husarion_components_description/"


def _render_single(tmpdir_factory, type_name, component_name="front"):
    config_path = tmpdir_factory.mktemp(type_name).join("config.yaml")
    utils = ComponentsYamlParseUtils(str(config_path))
    utils.save_yaml({"components": [utils.create_component(type_name, component_name)]})
    assert utils.does_urdf_parse(), f"{type_name} failed to parse"
    return utils._urdf


def test_mesh_files_exist(tmpdir_factory):
    for type_name in components_types_with_names:
        urdf = _render_single(tmpdir_factory, type_name)
        for mesh in urdf.getElementsByTagName("mesh"):
            uri = mesh.getAttribute("filename")
            if not uri.startswith(MESH_URI_PREFIX):
                continue
            path = os.path.join(husarion_components_description, uri.removeprefix(MESH_URI_PREFIX))
            assert os.path.isfile(path), f"{type_name}: mesh {uri} does not exist"


def _gz_bridge_launch_names():
    """Component code -> gz launch name, read from gz_components.launch.py."""
    launch_path = os.path.join(husarion_components_description, "launch/gz_components.launch.py")
    with open(launch_path, encoding="utf-8") as file:
        tree = ast.parse(file.read())
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Assign)
            and isinstance(node.targets[0], ast.Name)
            and node.targets[0].id == "components_types_with_names"
        ):
            return ast.literal_eval(node.value)
    raise AssertionError("components_types_with_names not found in gz_components.launch.py")


def test_gz_sensor_topics_are_bridged(tmpdir_factory):
    """Every gz sensor topic of a bridged component is present in its gz bridge config
    (directly or as the `<topic>/points` point cloud published by gz)."""
    for type_name, launch_name in _gz_bridge_launch_names().items():
        if type_name not in components_types_with_names:
            continue
        bridge_config_path = os.path.join(
            husarion_components_description, f"config/gz_{launch_name}_remappings.yaml"
        )
        if not os.path.isfile(bridge_config_path):
            continue

        with open(bridge_config_path, encoding="utf-8") as file:
            bridge_config = file.read()
        bridge_config = bridge_config.replace("<robot_namespace>", "").replace(
            "<component_name>", "/front"
        )
        bridged_topics = set()
        for entry in yaml.safe_load(bridge_config):
            for key in ("topic_name", "gz_topic_name"):
                if key in entry:
                    bridged_topics.add(entry[key].lstrip("/"))

        urdf = _render_single(tmpdir_factory, type_name)
        for sensor in urdf.getElementsByTagName("sensor"):
            topic = sensor.getElementsByTagName("topic")[0].firstChild.data.lstrip("/")
            assert (
                topic in bridged_topics or topic + "/points" in bridged_topics
            ), f"{type_name}: gz topic {topic} is not bridged in {bridge_config_path}"


def _rpy_to_matrix(roll, pitch, yaw):
    cr, sr = math.cos(roll), math.sin(roll)
    cp, sp = math.cos(pitch), math.sin(pitch)
    cy, sy = math.cos(yaw), math.sin(yaw)
    return [
        [cy * cp, cy * sp * sr - sy * cr, cy * sp * cr + sy * sr],
        [sy * cp, sy * sp * sr + cy * cr, sy * sp * cr - cy * sr],
        [-sp, cp * sr, cp * cr],
    ]


def _compose(parent, child):
    """Compose (rotation, translation) transforms: parent * child."""
    (r_a, t_a), (r_b, t_b) = parent, child
    rot = [[sum(r_a[i][k] * r_b[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
    trans = [sum(r_a[i][k] * t_b[k] for k in range(3)) + t_a[i] for i in range(3)]
    return rot, trans


def _frames_from(urdf, root):
    """Transforms of every link below `root`, relative to `root`."""
    children = {}
    for joint in urdf.getElementsByTagName("joint"):
        parent = joint.getElementsByTagName("parent")[0].getAttribute("link")
        child = joint.getElementsByTagName("child")[0].getAttribute("link")
        xyz, rpy = [0.0] * 3, [0.0] * 3
        origins = joint.getElementsByTagName("origin")
        if origins:
            if origins[0].getAttribute("xyz"):
                xyz = [float(v) for v in origins[0].getAttribute("xyz").split()]
            if origins[0].getAttribute("rpy"):
                rpy = [float(v) for v in origins[0].getAttribute("rpy").split()]
        children.setdefault(parent, []).append((child, (_rpy_to_matrix(*rpy), xyz)))

    identity = ([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]], [0.0, 0.0, 0.0])
    frames, stack = {root: identity}, [root]
    while stack:
        link = stack.pop()
        for child, transform in children.get(link, []):
            frames[child] = _compose(frames[link], transform)
            stack.append(child)
    return frames


def _render_xacro(tmpdir_factory, folder, content):
    path = tmpdir_factory.mktemp(folder).join("reference.urdf.xacro")
    with open(str(path), mode="w", encoding="utf-8") as file:
        file.write(content)
    return xacro.process_file(str(path))


def _assert_same_frames(type_name, ours, reference, root, ignored=(), overrides=None):
    """Our frames must match the manufacturer frames (names and poses relative to `root`).
    `ignored` - links not compared, `overrides` - {link: expected translation} where we
    deliberately differ from the manufacturer description."""
    overrides = overrides or {}
    our_frames = {k: v for k, v in _frames_from(ours, root).items() if k not in ignored}
    ref_frames = {k: v for k, v in _frames_from(reference, root).items() if k not in ignored}
    assert set(our_frames) == set(ref_frames), (
        f"{type_name}: frame names differ from the manufacturer description - "
        f"missing: {sorted(set(ref_frames) - set(our_frames))}, "
        f"extra: {sorted(set(our_frames) - set(ref_frames))}"
    )
    for link, (ref_rot, ref_trans) in ref_frames.items():
        our_rot, our_trans = our_frames[link]
        expected = overrides.get(link, ref_trans)
        for i in range(3):
            assert (
                abs(our_trans[i] - expected[i]) < 1e-6
            ), f"{type_name}: {link} position {our_trans} != {expected}"
            for j in range(3):
                assert (
                    abs(our_rot[i][j] - ref_rot[i][j]) < 1e-6
                ), f"{type_name}: {link} orientation differs from the manufacturer description"


def _assert_gz_frames_exist(type_name, urdf):
    links = {link.getAttribute("name") for link in urdf.getElementsByTagName("link")}
    for gazebo in urdf.getElementsByTagName("gazebo"):
        if gazebo.getAttribute("reference"):
            assert (
                gazebo.getAttribute("reference") in links
            ), f"{type_name}: gazebo reference {gazebo.getAttribute('reference')} not in URDF"
    for frame_id in urdf.getElementsByTagName("gz_frame_id"):
        assert (
            frame_id.firstChild.data in links
        ), f"{type_name}: gz_frame_id {frame_id.firstChild.data} not in URDF"


ZED_REFERENCE_XACRO = """<robot name="reference" xmlns:xacro="http://wiki.ros.org/xacro">
  <link name="cover_link" />
  <xacro:include filename="$(find husarion_components_description)/urdf/stereolabs_zed.urdf.xacro"
    ns="camera" />
  <xacro:camera.zed_camera parent_link="cover_link" model="{model}" />
</robot>"""


def test_zed_frames_match_zed_description(tmpdir_factory):
    """Own ZED descriptions (Husarion meshes) keep the frames of zed_description, so the
    zed-ros2-wrapper data lands in the right place. Fails when Stereolabs changes them."""
    for type_name, model in {"zed_2": "zed2", "zed_2i": "zed2i", "zed_x": "zedx"}.items():
        ours = _render_single(tmpdir_factory, type_name, component_name="")
        reference = _render_xacro(
            tmpdir_factory, f"ref_{model}", ZED_REFERENCE_XACRO.format(model=model)
        )
        _assert_same_frames(type_name, ours, reference, root="zed_camera_link")
        _assert_gz_frames_exist(type_name, ours)


EXAMPLE_XACRO = os.path.join(
    husarion_components_description, "urdf/custom_component_example.urdf.xacro"
)


def _render_custom(tmpdir_factory, folder, entry):
    config_path = tmpdir_factory.mktemp(folder).join("config.yaml")
    with open(str(config_path), mode="w", encoding="utf-8") as file:
        yaml.dump({"components": [entry]}, file)
    utils = ComponentsYamlParseUtils(str(config_path))
    assert utils.does_urdf_parse(), f"custom component failed to parse: {entry}"
    return utils


def test_custom_component_with_package(tmpdir_factory):
    utils = _render_custom(
        tmpdir_factory,
        "custom_pkg",
        {
            "type": "custom",
            "name": "my_sensor",
            "package": "husarion_components_description",
            "file": "urdf/custom_component_example.urdf.xacro",
            "parent_link": "cover_link",
            "xyz": "0.0 0.0 0.1",
            "rpy": "0.0 0.0 0.0",
        },
    )
    assert utils.does_link_exist(utils._urdf, "my_sensor_link")


def test_custom_component_with_absolute_path(tmpdir_factory):
    utils = _render_custom(
        tmpdir_factory,
        "custom_abs",
        {
            "type": "custom",
            "name": "my_sensor",
            "file": EXAMPLE_XACRO,
            "parent_link": "cover_link",
        },
    )
    assert utils.does_link_exist(utils._urdf, "my_sensor_link")


def test_custom_component_with_macro_name_override(tmpdir_factory):
    fixture = tmpdir_factory.mktemp("custom_macro").join("renamed.urdf.xacro")
    with open(str(fixture), mode="w", encoding="utf-8") as file:
        file.write(
            '<robot xmlns:xacro="http://wiki.ros.org/xacro">'
            '<xacro:macro name="my_macro" '
            "params=\"parent_link xyz:='0 0 0' rpy:='0 0 0' "
            "component_name:='' robot_namespace:='' use_tf_prefix:=True component:={}\">"
            '<link name="${component_name}_link"/>'
            '<joint name="${parent_link}_to_${component_name}_joint" type="fixed">'
            '<parent link="${parent_link}"/><child link="${component_name}_link"/>'
            '<origin xyz="${xyz}" rpy="${rpy}"/></joint>'
            "</xacro:macro></robot>"
        )
    utils = _render_custom(
        tmpdir_factory,
        "custom_macro_cfg",
        {
            "type": "custom",
            "name": "renamed",
            "file": str(fixture),
            "macro_name": "my_macro",
            "parent_link": "cover_link",
        },
    )
    assert utils.does_link_exist(utils._urdf, "renamed_link")


def test_custom_component_receives_raw_component_dict(tmpdir_factory):
    """The dispatcher forwards the full yaml entry as `component`, so a custom
    macro can read its own extra keys beyond the standard signature (e.g.
    camera_mount's camera_mount_angle_1/2)."""
    fixture = tmpdir_factory.mktemp("custom_extra").join("extra.urdf.xacro")
    with open(str(fixture), mode="w", encoding="utf-8") as file:
        file.write(
            '<robot xmlns:xacro="http://wiki.ros.org/xacro">'
            '<xacro:macro name="with_extra" '
            "params=\"parent_link xyz:='0 0 0' rpy:='0 0 0' "
            "component_name:='' robot_namespace:='' use_tf_prefix:=True component:={}\">"
            "<link name=\"${component_name}_${component['extra_field']}_link\"/>"
            '<joint name="${parent_link}_to_${component_name}_joint" type="fixed">'
            '<parent link="${parent_link}"/>'
            "<child link=\"${component_name}_${component['extra_field']}_link\"/>"
            '<origin xyz="${xyz}" rpy="${rpy}"/></joint>'
            "</xacro:macro></robot>"
        )
    utils = _render_custom(
        tmpdir_factory,
        "custom_extra_cfg",
        {
            "type": "custom",
            "name": "sensor",
            "file": str(fixture),
            "macro_name": "with_extra",
            "parent_link": "cover_link",
            "extra_field": "hello",
        },
    )
    assert utils.does_link_exist(utils._urdf, "sensor_hello_link")
