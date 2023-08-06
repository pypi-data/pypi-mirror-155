from typing import Any, Dict, List, Union
import os
import json
from pyparsing import Optional


from LigralPy.tools.translation import _trans
from .appearance_manager import appearance_manager


class Argument:
    def __init__(self, name: str, type: str) -> None:
        self.name = name
        self.type = type


class Parameter:
    def __init__(self, name: str, type: str, default: Any) -> None:
        self.name = name
        self.type = type
        self.value = None
        self.default = Any


internal_nodejsons_path = os.path.join(os.path.dirname(__file__), "nodejsons")
external_nodejsons_path = os.path.join(
    os.path.dirname(__file__), "external_nodejsons")


class LigralNodeType:
    def __init__(self) -> None:
        self.category: str = "internal"  # internal, custom和external
        self.node_type: str = ""  # 实际对应的Ligral节点类型
        self.title = ""  # 展示的文字信息
        self.input_args_labels = []
        self.output_ports_labels = []

        self.docs = ""  # 节点的简介或者文档
        self.parameters = []
        self.input_variable: Optional[bool] = None
        self.output_variable: Optional[bool] = None

    def _self_check(self):
        assert self.category in {"internal", "external", "custom"}
        assert self.input_variable is not None
        assert self.output_variable is not None

    def to_frontend_json(self):
        """
        转换为前端所需的json格式。

        """
        return {
            "id": self.node_type,
            "title": _trans(self.title),
            "description": self.docs,
            "params": self.parameters,
            "inputs": [
                {"name": label, "type": "any"} for label in self.input_args_labels
            ],
            "outputs": [
                {"name": label, "type": "any"} for label in self.output_ports_labels
            ],
            "category": self.category,
            "appearance": appearance_manager.get_appearance(self.node_type).to_json(),
            "inputVariable": self.input_variable,
            "outputVariable": self.output_variable
        }

    @classmethod
    def from_route(cls, filename: str) -> "LigralNodeType":
        node_type = LigralNodeType()
        with open(filename) as f:
            d = json.load(f)
        info = d["info"]
        node_type.node_type = info["name"]
        node_type.title = info["name"]
        node_type.docs = "...description"
        node_type.input_args_labels = [
            label["name"] for label in info["settings"]["inPorts"]
        ]
        node_type.output_ports_labels = [
            label["name"] for label in info["settings"]["outPorts"]
        ]
        node_type.parameters = []
        node_type.category = "custom"
        node_type.input_variable = False
        node_type.output_variable = False
        node_type._self_check()
        return node_type

    @classmethod
    def from_mdl_json(cls, node_type: str, mdl_type: str = "internal"):
        nodejsons_path = (
            internal_nodejsons_path
            if mdl_type == "internal"
            else external_nodejsons_path
        )

        json_filepath = os.path.join(nodejsons_path, node_type + ".mdl.json")
        if not os.path.exists(json_filepath):
            raise FileNotFoundError(f"{json_filepath} does not exist!")

        with open(json_filepath) as f:
            mdl_json: Dict = json.load(f)
            if mdl_type == "external":  # 如果是外部定义的节点类型，就需要单独处理以下了。
                with open(
                    os.path.join(
                        internal_nodejsons_path, mdl_json["from-type"] +
                        ".mdl.json"
                    )
                ) as f2:
                    internal_mdl_json = json.load(f2)
                # 用外部节点类型来覆盖。
                internal_mdl_json.update(mdl_json)
                mdl_json = internal_mdl_json
                assert mdl_json["type"] != mdl_json["from-type"], (
                    "External node cannot have the same name as"
                    f" the internal node {mdl_json['type']} it inherited"
                )
            return cls.from_dict(mdl_json, mdl_type)

    def get_name(self):
        return self.module_name

    @classmethod
    def from_dict(cls, props_dict: Dict[str, Any], mdl_type: str = "internal"):
        n = LigralNodeType()
        n.load(props_dict, mdl_type)
        n._self_check()
        return n

    def load(
        self,
        mdl_dict: Dict[str, Union[List[str], List[Dict], bool]],
        mdl_type: str = "internal",
    ):
        """
        从加载后的mdl.json文件中读取信息并且实例化。
        """
        assert mdl_type in {"internal",
                            "external"}  # mdl_type的意思是，是ligral自身产生的，还是外部的。
        self.category = mdl_type
        self.node_type = (
            mdl_dict["type"] if mdl_type == "internal" else mdl_dict["from-type"]
        )
        self.title = mdl_dict["type"]
        self.docs = mdl_dict["document"]
        self.input_args_labels = mdl_dict["in-ports"]
        self.output_ports_labels = mdl_dict["out-ports"]
        self.parameters = mdl_dict["parameters"]
        self.input_variable = mdl_dict['in-port-variable']
        self.output_variable = mdl_dict['out-port-variable']

    def put_argument(self, arg_index: int, arg_value: Any):
        self.input_values[arg_index].put(arg_value)

    def get_arguments(self):
        arg_values: List[Any] = []
        for q in self.input_values:
            if q.empty():
                return None, False
            else:
                arg_values.append(q.get())
        return arg_values, True

    def execute(self):
        """
        外层的运行
        这一层不用自定义。
        """
        args, status = self.get_arguments()
        if status:
            return self.run(*args), True
        else:
            return None, False

    def run(self, *args):
        """
        内层的运行
        这一层需要自定义
        """
        pass

    def get_output_ports(self):
        pass

    def gen_ligral_json(self):
        output_ports = []
        for out_port in self.get_output_ports():
            destinations = []
            for conn_line in out_port.get_connected_lines():
                in_port = conn_line.end_port.text
                destination_id = conn_line.end_port.node.id
                destinations.append({"id": destination_id, "in-port": in_port})
            output_ports.append(
                {"name": out_port.text, "destination": destinations})
        return {
            "id": self.id,
            "type": self.get_name(),
            "parameters": [{"name": k, "value": v} for k, v in self.info.items()],
            "out-ports": output_ports,
        }


internal_ligral_nodetypes: List[LigralNodeType] = [
    LigralNodeType.from_mdl_json(file.split(".")[0].strip())
    for file in os.listdir(internal_nodejsons_path)
]
internal_ligral_nodetypes_dict: Dict[str, LigralNodeType] = {
    node_json.title: node_json for node_json in internal_ligral_nodetypes
}
