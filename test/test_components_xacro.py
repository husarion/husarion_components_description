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
    "LDR20": ["velodyne_puck", "velodyne", "velodyne", "lidar", ""],
    "CAM01": ["orbbec_astra", "link", "link", "camera_color", "camera"],
    "camera_box": ["front_camera", "link", "", "", "camera"],
    "CAM03": ["zed2", "camera_center", "camera_center", "camera_color", "zed"],
    "CAM04": ["zed2i", "camera_center", "camera_center", "camera_color", "zed"],
    "CAM05": ["zedm", "camera_center", "camera_center", "camera_color", "zed"],
    "CAM06": ["zedx", "camera_center", "camera_center", "camera_color", "zed"],
    "CAM12": ["oak_d_pro_poe", "link", "link", "color", "oak"],
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


def _ouster_lidar_joint(tmpdir_factory, type_name):
    dir = tmpdir_factory.mktemp(type_name)
    path = str(dir.join("components.yaml"))
    utils = ComponentsYamlParseUtils(path)
    utils.save_yaml({"components": [utils.create_component(type_name, "")]})
    urdf = xacro.process_file(xacro_path, mappings={"components_config_path": path})
    for joint in urdf.getElementsByTagName("joint"):
        child = joint.getElementsByTagName("child")[0].getAttribute("link")
        if child.endswith("os_lidar"):
            origin = joint.getElementsByTagName("origin")[0]
            xyz = [float(v) for v in origin.getAttribute("xyz").split()]
            rpy = [float(v) for v in origin.getAttribute("rpy").split()]
            return xyz, rpy
    raise AssertionError(f"no os_lidar joint for {type_name}")


def test_ouster_lidar_frame_matches_the_sensor(tmpdir_factory):
    # Ouster's lidar_to_sensor_transform: a 180 deg turn about z and the lidar origin's height,
    # 36.180 mm on OS0/OS1 and 74.296 mm on OS2. The driver stamps the cloud in os_lidar.
    for type_name, height in (("LDR10", 0.03618), ("LDR15", 0.03618), ("LDR17", 0.074296)):
        xyz, rpy = _ouster_lidar_joint(tmpdir_factory, type_name)
        assert abs(xyz[2] - height) < 1e-6, (type_name, xyz)
        assert abs(rpy[2] - 3.141592653589793) < 1e-6, (type_name, rpy)


def _render_camera_box(tmpdir_factory, folder, entries):
    config_path = tmpdir_factory.mktemp(folder).join("components.yaml")
    utils = ComponentsYamlParseUtils(str(config_path))
    utils.save_yaml({"components": entries})
    assert utils.does_urdf_parse(), f"camera_box failed to parse: {entries}"
    return utils._urdf


def _joints_to(urdf, child_link):
    joints = []
    for joint in urdf.getElementsByTagName("joint"):
        if joint.getElementsByTagName("child")[0].getAttribute("link") == child_link:
            joints.append(joint)
    return joints


def _origin(element):
    origin = element.getElementsByTagName("origin")[0]
    xyz = [float(v) for v in origin.getAttribute("xyz").split()]
    rpy = [float(v) for v in origin.getAttribute("rpy").split()]
    return xyz, rpy


def _box_of(urdf, link_name):
    for link in urdf.getElementsByTagName("link"):
        if link.getAttribute("name") == link_name:
            visual = link.getElementsByTagName("visual")[0]
            size = visual.getElementsByTagName("box")[0].getAttribute("size")
            return [float(v) for v in size.split()], _origin(visual)[0]
    raise AssertionError(f"no link {link_name}")


def _close(a, b):
    return all(abs(x - y) < 1e-6 for x, y in zip(a, b)) and len(a) == len(b)


def test_camera_box_default_name_gives_the_camera_node_frame(tmpdir_factory):
    # The camera node stamps camera_optical_frame by default; the default name must give it,
    # with exactly one parent each, so nothing else may publish it.
    urdf = _render_camera_box(
        tmpdir_factory,
        "camera_box_default",
        [{"type": "camera_box", "parent_link": "cover_link", "xyz": "0.2 0.0 0.05"}],
    )
    body = _joints_to(urdf, "camera_link")
    optical = _joints_to(urdf, "camera_optical_frame")
    assert len(body) == 1 and len(optical) == 1
    assert body[0].getElementsByTagName("parent")[0].getAttribute("link") == "cover_link"
    assert optical[0].getElementsByTagName("parent")[0].getAttribute("link") == "camera_link"
    assert body[0].getAttribute("type") == "fixed" and optical[0].getAttribute("type") == "fixed"
    assert _close(_origin(body[0])[0], [0.2, 0.0, 0.05])
    assert _close(_origin(body[0])[1], [0.0, 0.0, 0.0])


def test_camera_box_named(tmpdir_factory):
    urdf = _render_camera_box(
        tmpdir_factory,
        "camera_box_named",
        [
            {"type": "camera_box", "name": "rear_camera", "parent_link": "cover_link"},
            {"type": "camera_box", "parent_link": "cover_link"},
        ],
    )
    for frame in ("rear_camera_link", "rear_camera_optical_frame", "camera_link"):
        assert len(_joints_to(urdf, frame)) == 1, frame


def test_camera_box_optical_rotation(tmpdir_factory):
    urdf = _render_camera_box(
        tmpdir_factory,
        "camera_box_optical",
        [{"type": "camera_box", "parent_link": "cover_link", "rpy": "0.1 0.2 0.3"}],
    )
    xyz, rpy = _origin(_joints_to(urdf, "camera_optical_frame")[0])
    assert _close(xyz, [0.0, 0.0, 0.0])
    assert _close(rpy, [-math.pi / 2, 0.0, -math.pi / 2])
    assert _close(_origin(_joints_to(urdf, "camera_link")[0])[1], [0.1, 0.2, 0.3])


def test_camera_box_size(tmpdir_factory):
    # The box extends back from the lens: its centre is half the depth behind the origin.
    urdf = _render_camera_box(
        tmpdir_factory,
        "camera_box_size",
        [{"type": "camera_box", "parent_link": "cover_link", "size": "0.05 0.12 0.04"}],
    )
    size, centre = _box_of(urdf, "camera_link")
    assert _close(size, [0.05, 0.12, 0.04])
    assert _close(centre, [-0.025, 0.0, 0.0])


def test_camera_box_default_size(tmpdir_factory):
    urdf = _render_camera_box(
        tmpdir_factory,
        "camera_box_default_size",
        [{"type": "camera_box", "parent_link": "cover_link"}],
    )
    size, centre = _box_of(urdf, "camera_link")
    assert _close(size, [0.03, 0.08, 0.03])
    assert _close(centre, [-0.015, 0.0, 0.0])


def test_oak_d_pro_poe_frames(tmpdir_factory):
    # CAM12 gives the frames depthai stamps, each with one parent: oak_rgb_camera_optical_frame
    # and the stereo pair 75 mm apart (Luxonis' NG9097 datasheet), plus a collision box of the
    # datasheet's 111 x 40 x 31.3 mm.
    config_path = tmpdir_factory.mktemp("oak_d_pro_poe").join("components.yaml")
    utils = ComponentsYamlParseUtils(str(config_path))
    utils.save_yaml(
        {"components": [utils.create_component("CAM12", "", xyz="0.1 0.0 0.05")]}
    )
    assert utils.does_urdf_parse()
    urdf = utils._urdf

    body = _joints_to(urdf, "oak_link")
    assert len(body) == 1
    assert body[0].getElementsByTagName("parent")[0].getAttribute("link") == "cover_link"
    assert _close(_origin(body[0])[0], [0.1, 0.0, 0.05])

    for side, y in (("rgb", 0.0), ("left", 0.0375), ("right", -0.0375)):
        frame = _joints_to(urdf, f"oak_{side}_camera_frame")
        optical = _joints_to(urdf, f"oak_{side}_camera_optical_frame")
        assert len(frame) == 1 and len(optical) == 1, side
        assert frame[0].getElementsByTagName("parent")[0].getAttribute("link") == "oak_link"
        assert _close(_origin(frame[0])[0], [0.0, y, 0.0]), side
        assert _close(_origin(optical[0])[1], [-math.pi / 2, 0.0, -math.pi / 2]), side

    for link in urdf.getElementsByTagName("link"):
        if link.getAttribute("name") == "oak_model_collision":
            size = link.getElementsByTagName("box")[0].getAttribute("size")
            assert _close([float(v) for v in size.split()], [0.111, 0.040, 0.0313])
            break
    else:
        raise AssertionError("no oak_model_collision link")
