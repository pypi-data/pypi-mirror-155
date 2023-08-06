class RoutePort:
    def __init__(self, name: str, type: str, conn_node: str, conn_port: str) -> None:
        self.name: str = name
        self.type = type
        self.connected_node: str = conn_node
        self.connected_port: str = conn_port
        assert type in {"input", "output"}

    def to_lig_json(
        self,
    ):

        return {
            "name": self.name,
            self.type + "-id": self.connected_node,
            self.type + "-port": self.connected_port,
        }

    def from_fe_json(self, fe_json):
        return RoutePort(
            fe_json["name"], fe_json["type"], fe_json["connNode"], fe_json["connPort"]
        )


class Group:
    def __init__(self) -> None:
        pass
