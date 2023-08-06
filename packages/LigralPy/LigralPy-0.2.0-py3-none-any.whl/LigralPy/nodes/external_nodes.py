import os
from typing import List, Dict
from .node import LigralNodeType, external_nodejsons_path


def get_module_id(class_name: str):
    """
    转换经过重写之后的module ID。
    比如UDPListenerDefault调用的模块名称还是UDPListener.
    """
    if class_name in external_ligral_nodetypes_dict:
        return external_ligral_nodetypes_dict[class_name].node_type
    else:
        return class_name


external_ligral_nodetypes: List[LigralNodeType] = [
    LigralNodeType.from_mdl_json(file.split(".")[0].strip(), "external")
    for file in os.listdir(external_nodejsons_path)
]
external_ligral_nodetypes_dict: Dict[str, LigralNodeType] = {
    node_json.title: node_json for node_json in external_ligral_nodetypes
}
