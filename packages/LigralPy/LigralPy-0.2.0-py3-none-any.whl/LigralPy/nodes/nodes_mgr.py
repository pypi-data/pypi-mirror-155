from cmath import inf
from typing import Any, Callable, Dict, List, Tuple
import json
import os

from .appearance_manager import appearance_manager


from ..config import get_workdir

from .node import (
    LigralNodeType,
    internal_ligral_nodetypes,
    internal_ligral_nodetypes_dict,
)
from .external_nodes import external_ligral_nodetypes, external_ligral_nodetypes_dict


def get_all_nodetype_jsons():
    classes_list = [
        node.to_frontend_json()
        for node in internal_ligral_nodetypes + external_ligral_nodetypes
    ]
    return classes_list


def load_from_route_json(filename: str):
    """
    从.route.json中加载。
    """
    with open(filename) as f:
        d = json.load(f)
    info = d["info"]
    n = LigralNodeType()
    n.node_type = info["name"]
    n.title = info["name"]
    n.docs = "....description"
    n.parameters = []
    n.input_variable = False
    n.output_variable = False
    n.category = "custom"

    n.input_args_labels = [label["name"]
                           for label in info["settings"]['inPorts']]
    n.output_ports_labels = [label["name"]
                             for label in info["settings"]['outPorts']]
    
    n._self_check()
    return n.to_frontend_json()


def search_for_custom_nodes(node_name: str) -> LigralNodeType:
    """
    在工作路径下寻找用户自定义的模块
    """
    wd = get_workdir()
    all_nodes = []
    for file in os.listdir(wd):
        if file.endswith(".route.json"):
            node = LigralNodeType.from_route(os.path.join(wd, file))
            all_nodes.append(node.node_type)
            if node.node_type == node_name:
                return node
    raise ValueError(
        f'Custom node "{node_name}" is not found in current workdir {wd}. All custom routes are: {all_nodes}'
    )


def get_all_custom_nodes() -> List[Dict]:
    wd = get_workdir()
    all_nodes: List[Dict] = []
    for file in os.listdir(wd):
        if file.endswith(".route.json"):
            with open(os.path.join(wd, file)) as f:
                all_nodes.append(json.load(f))
    return all_nodes


def search_graph(name: str) -> Tuple[str, Dict]:
    wd = get_workdir()
    for file in os.listdir(wd):
        if is_graph_source_file(file):
            file_path = os.path.join(wd, file)
            with open(file_path) as f:
                content = json.load(f)
                if content["info"]["name"] == name:
                    return (file_path, content)
    raise FileNotFoundError(f"name {name} is not found!")


def for_each_graph(callback: Callable[[Dict[str, Any]], None], indent=4, modify=True):
    wd = get_workdir()
    modified_graphs: Dict[str, Dict] = {}
    for file in os.listdir(wd):
        if is_graph_source_file(file):
            with open(os.path.join(wd, file)) as f:
                graph = json.load(f)
            callback(graph)
            modified_graphs[graph["info"]["name"]] = graph
            if modify:
                with open(os.path.join(wd, file), "w") as f:
                    json.dump(graph, f, indent=indent)

    return modified_graphs


def get_main_graph() -> Dict:
    """
    Get the main graph inside the main directory.
    """
    wd = get_workdir()
    target_file = ""
    count = 0
    for file in os.listdir(wd):
        if file.endswith(".main.json"):
            count += 1
            target_file = file
    if count == 0:
        raise ValueError(f"No *.main.json is found in the workdir {wd}")
    elif count > 1:
        raise ValueError(
            f"More than one *.main.json are found in the workdir {wd}")
    with open(os.path.join(wd, target_file)) as f:
        return json.load(f)


def is_graph_source_file(file_name: str):
    return file_name.endswith((".main.json", ".route.json"))


def get_all_node_files() -> List[str]:
    """
    返回的元组里面为 绝对路径，相对路径
    """
    node_files = []
    wd = get_workdir()
    for file in os.listdir(wd):
        file_abs_path = os.path.join(wd, file)
        if is_graph_source_file(file_abs_path):
            node_files.append(file_abs_path)
    return node_files


def is_out_port_variable(node_name: str) -> bool:
    if node_name in internal_ligral_nodetypes_dict:
        return internal_ligral_nodetypes_dict[node_name].output_variable
    elif node_name in external_ligral_nodetypes_dict:
        return external_ligral_nodetypes_dict[node_name].output_variable
    else:
        return False


def get_output_ports(node_name: str):
    """
    搜索节点的输出端口。
    如果节点不是用户定义的，再从默认节点中搜索！
    """
    if (
        node_name not in internal_ligral_nodetypes_dict.keys()
        and node_name not in external_ligral_nodetypes_dict
    ):
        custom_node = search_for_custom_nodes(node_name)
        return [output for output in custom_node.output_ports_labels]
    else:
        if node_name in internal_ligral_nodetypes_dict:
            return internal_ligral_nodetypes_dict[node_name].output_ports_labels
        elif node_name in external_ligral_nodetypes_dict:
            return external_ligral_nodetypes_dict[node_name].output_ports_labels
        else:
            raise ValueError(
                f"Node {node_name} not found in either the custom nodes set nor the defaule node set."
            )


def get_all_route_jsons():
    wd = get_workdir()
    all_nodes: List[Dict] = []
    for file in os.listdir(wd):
        if file.endswith(".route.json"):
            all_nodes.append(load_from_route_json(os.path.join(wd, file)))
    return all_nodes


def get_file_by_chart_name(chart_name: str) -> str:
    """
    通过图的名字，获取文件名
    """
    wd = get_workdir()
    for file in os.listdir(wd):
        if is_graph_source_file(file):
            absolute_path = os.path.join(wd, file)
            with open(absolute_path) as f:
                if json.load(f)["info"]["name"] == chart_name:
                    return absolute_path
