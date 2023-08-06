from typing import Dict


class FlowChartSettings:
    """
    每一个图的设置项
    """

    def __init__(
        self,
        type,
    ) -> None:
        self.type: str = type

        assert self.type in {"main", "route"}  # 是主图或者路径

    def from_json(self, data: Dict):
        pass


class MainFlowchartSettings:
    def __init__(self, type: str) -> None:
        super().__init__(type)


class RouteSettings(FlowChartSettings):
    def __init__(
        self,
        name: str,
    ) -> None:
        super().__init__("route")
        self.name: str = name
        self.in_ports = []
        self.out_ports = []
