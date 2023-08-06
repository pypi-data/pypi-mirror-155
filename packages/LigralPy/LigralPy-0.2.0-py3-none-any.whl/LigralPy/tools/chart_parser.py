from asyncio.log import logger
import sys
import json
from typing import Any, Dict, List
from LigralPy.nodes.external_nodes import get_module_id

from LigralPy.nodes.nodes_mgr import (
    for_each_graph,
    get_all_custom_nodes,
    get_all_route_jsons,
    get_output_ports,
    is_out_port_variable,
    search_graph,
)
from LigralPy.tools.project_config import ProjectConfig

from ..models.group import Group


def parse_settings(chart: str):
    settings = chart["settings"]


def link_groups(chart: Dict):
    """
    对于含有route的图，需要连接主图和子图。
    """
    groups = Group(chart["groups"])


def parse_route(route_json: Dict):
    print(route_json)
    route_info = route_json["info"]
    models = parse_sub_graph(route_json)
    name = route_info["name"]
    settings = route_info["settings"]
    in_ports = [
        {
            "name": port["name"],
            "input-id": port["connectedNode"],
            "input-port": port["connectedPort"],
        }
        for port in settings["inPorts"]
    ]
    out_ports = [
        {
            "name": port["name"],
            "output-id": port["connectedNode"],
            "output-port": port["connectedPort"],
        }
        for port in settings["outPorts"]
    ]
    return {
        "name": name,
        "in-ports": in_ports,
        "out-ports": out_ports,
        "models": models,
    }


def parse_sub_graph(chart):
    # 当前节点号， 输出端口号，随后为一个数组，存储对应当前节点号和端口号的所有边。
    query_dict_by_node_and_outport: Dict[str, Dict[str, List[Dict[str, str]]]] = {}
    for edge in chart["edges"]:
        srcNode = edge["srcNode"]
        srcEndpointID = edge["srcEndpointID"]
        print(query_dict_by_node_and_outport)
        print("======"*5)
        if srcNode in query_dict_by_node_and_outport:
            if srcEndpointID not in query_dict_by_node_and_outport[srcNode]:
                query_dict_by_node_and_outport[srcNode][srcEndpointID] = []
            query_dict_by_node_and_outport[srcNode][srcEndpointID].append(edge)
        else:
            query_dict_by_node_and_outport[srcNode] = {srcEndpointID: [edge]}
        
    nodes_list: Dict[str, Any] = []
    nodes_in_ligral = []
    for node in chart["nodes"]:
        if is_out_port_variable(node['type']):
            output_ports = node['outputPorts']
        else:
            output_ports = get_output_ports(node["type"])
        # output_ports = get_output_ports(node["type"])
        node_id = node["id"]
        if node_id in query_dict_by_node_and_outport:  # 该节点有出边
            current_node_endpoints = query_dict_by_node_and_outport[node["id"]]
        else:
            current_node_endpoints = {}  # 该节点无出边
        n = {
            "id": node["id"],
            "type": get_module_id(node["type"]),
            "parameters": node["params"],
            "out-ports": [
                {
                    "name": output_port_name,
                    "destination": [
                        {
                            "id": edge_spec["destNode"],
                            "in-port": edge_spec["destEndpointID"],
                        }
                        for edge_spec in current_node_endpoints.get(output_port_name)
                    ],
                }
                for output_port_name in output_ports
                if current_node_endpoints.get(output_port_name) is not None
            ],
        }
        nodes_in_ligral.append(n)
    return nodes_in_ligral


def parse_graph(chart, project_config=None):
    # 当前节点号， 输出端口号，随后为一个数组，存储对应当前节点号和端口号的所有边。
    query_dict_by_node_and_outport: Dict[str, Dict[str, List[Dict[str, str]]]] = {}
    for edge in chart["edges"]:
        srcNode = edge["srcNode"]
        srcEndpointID = edge["srcEndpointID"]
        if (
            srcNode in query_dict_by_node_and_outport
            and srcEndpointID in query_dict_by_node_and_outport[srcNode]
        ):
            query_dict_by_node_and_outport[srcNode][srcEndpointID].append(edge)
        else:
            if not srcNode in query_dict_by_node_and_outport:
                query_dict_by_node_and_outport[srcNode] = {}
            query_dict_by_node_and_outport[srcNode][srcEndpointID] = [edge]
    nodes_list: Dict[str, Any] = []
    nodes_in_ligral = []
    for node in chart["nodes"]:
        if is_out_port_variable(node['type']):
            output_ports = node['outputPorts']
        else:
            output_ports = get_output_ports(node["type"])
        
        node_id = node["id"]
        if node_id in query_dict_by_node_and_outport:  # 该节点有出边
            current_node_endpoints = query_dict_by_node_and_outport[node["id"]]
        else:
            current_node_endpoints = {}  # 该节点无出边
        try:
            n = {
                "id": node["id"],
                "type": get_module_id(node["type"]),
                "parameters": node["params"],
                "out-ports": [
                    {
                        "name": output_port_name,
                        "destination": [
                            {
                                "id": edge_spec["destNode"],
                                "in-port": edge_spec["destEndpointID"],
                            }
                            for edge_spec in current_node_endpoints[output_port_name]
                        ],
                    }
                    for output_port_name in output_ports
                ],
            }
        except KeyError as e:
            logger.error(f"Key error occured in {current_node_endpoints}, key {e}")
            raise e
        nodes_in_ligral.append(n)
    return {
        "models": nodes_in_ligral,
        "settings": [{"item": "python", "value": sys.executable}]
        + ProjectConfig().to_ligral_config(),
    }


def parse_graph_with_route(chart_main_json: dict):
    main_graph = parse_graph(chart_main_json)
    print(main_graph)
    groups = []
    for node in get_all_custom_nodes():
        group = parse_route(node)
        groups.append(group)
    main_graph["groups"] = groups
    return main_graph


def rename_chart(last_name: str, new_name: str):
    file, graph = search_graph(last_name)
    graph["info"]["name"] = new_name
    with open(file, "w") as f:
        json.dump(graph, f)

    def callback(graph: Dict[str, Any]):
        for node in graph["nodes"]:
            if node["type"] == last_name:
                node["type"] = new_name

    for_each_graph(callback)
