import json
import os
from typing import Union

from LigralPy.config import get_workdir
from LigralPy.tools.translation import _trans


class Undefined:
    pass


class ProjectConfig:
    def __init__(self) -> None:
        self.python: Union[str, Undefined] = Undefined()
        self.inner_plotter: Union[bool, Undefined] = Undefined()
        self.step_size: Union[float, Undefined] = Undefined()
        self.stop_time: Union[float, Undefined] = Undefined()
        self.realtime: Union[bool, Undefined] = Undefined()
        self.load()

    def load(self):
        wd = get_workdir()
        settings_file = os.path.join(wd, "ligralpy-project-settings.json")
        if not os.path.exists(settings_file):
            self.dump()
        with open(settings_file, "r") as f:
            loaded_settings = json.load(f)
            settings_keys = list(self.__dict__.keys())
            for settings_key in settings_keys:
                if settings_key in loaded_settings:
                    self.__dict__[settings_key] = loaded_settings[settings_key]

    def dump(self):
        wd = get_workdir()
        with open(os.path.join(wd, "ligralpy-project-settings.json"), "w") as f:
            settings_to_dump = {
                k: v for k, v in self.__dict__.items() if not isinstance(v, Undefined)
            }
            json.dump(settings_to_dump, f)

    def to_ligral_config(self):
        return [
            {"item": k, "value": v}
            for k, v in self.__dict__.items()
            if not isinstance(v, Undefined)
        ]

    def get_help(self, help_item: str):
        try:
            help = {
                "python": _trans("The path of python executable"),
                "inner_plotter": _trans("If inner plotter is enabled"),
                "step_size": _trans("The time interval of each step."),
                "stop_time": _trans("The stop time of simulation"),
                "realtime": _trans("If realtime simulation is enabled")
            }[help_item]
            return help
        except KeyError as e:
            raise KeyError(f"{help_item} is not a valid setting item.")

    def to_frontend_struct(self):
        return {
            k: {

                "Type": "string",
                "Default": None,
                "Required": True,
                "Meta": None,
                "Translation": _trans(k),
                "Help": self.get_help(k),
                "Value": v if not isinstance(v, Undefined) else None,
            } for k, v in self.__dict__.items()
        }
