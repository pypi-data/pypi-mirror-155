import json
import os
from typing import ClassVar, Dict


class Appearance:
    def __init__(
        self,
        type: str = "rect",
        figure_mode: str = "none",
        source: str = "",
        xScale=None,
        yScale=None,
    ) -> None:
        assert type in {"triangle", "rect"}
        assert figure_mode in {"latex", "icon", "none"}
        self.type = type
        self.figure_mode = figure_mode
        self.source = source
        self.xScale = xScale
        self.yScale = yScale

    def to_json(self):
        return {
            "type": self.type,
            "figureMode": self.figure_mode,
            "source": self.source,
            "yScale": self.yScale,
            "xScale": self.xScale,
        }


class AppearanceManager:
    def __init__(self) -> None:
        self.class_appearances: Dict[str, Appearance] = {}
        with open(os.path.join(os.path.dirname(__file__), "appearances.json")) as f:
            d = json.load(f)
            for k, v in d.items():
                self.register_appearance(
                    k,
                    Appearance(
                        v["type"],
                        v["figure_mode"],
                        v["source"],
                        v.get("x_scale"),
                        v.get("y_scale"),
                    ),
                )

    def register_appearance(self, class_name: str, appearance: Appearance):
        self.class_appearances[class_name] = appearance

    def get_appearance(self, class_name: str) -> Appearance:
        if class_name in self.class_appearances:
            return self.class_appearances[class_name]
        else:
            return Appearance()


appearance_manager = AppearanceManager()
