from asyncio.log import logger
import os
import json
import appdirs

LIGRALPY_ROOT = os.path.dirname(__file__)
DEMOS_FOLDER = os.path.join(LIGRALPY_ROOT, "demos")
LIGRAL_APPDATA_FOLDER = appdirs.user_data_dir("Ligral")
UNINITIALIZED_WORKDIR = "UNINITIALIZED"
STATIC_FOLDER = os.path.join(LIGRALPY_ROOT, "static")
CONFIG_FILE = os.path.join(LIGRAL_APPDATA_FOLDER, "config.json")

if not os.path.exists(LIGRAL_APPDATA_FOLDER):
    os.makedirs(LIGRAL_APPDATA_FOLDER)


def set_workdir(workdir: str):
    """
    设置工作路径
    """
    global _workdir
    if not os.path.exists(workdir):
        raise FileNotFoundError(f"Workdir {workdir} is not found!")
    _workdir = workdir
    _configs.on_set_workdir(workdir)


def get_workdir():
    """
    获取工作路径
    """
    if _workdir == "UNINITIALIZED":
        raise FileNotFoundError(
            "Workdir is uninitialized. Please use `set_workdir()` to initialize the workdir."
        )
    return _workdir


def get_recent_projects():
    return _configs.recent_project_paths


class Configs:
    def __init__(self) -> None:
        self.last_workdir = UNINITIALIZED_WORKDIR
        self.ligral_executable = "ligral"
        self.main_server_port = 5000
        self.graph_draw_port = 8784
        self.recent_project_paths = []

        self.load_configs()

    def dump_configs(self):
        with open(CONFIG_FILE, "w") as f:
            json.dump(self.__dict__, f)

    def on_set_workdir(self, new_workdir: str):

        self.last_workdir = new_workdir
        self.recent_project_paths.append(new_workdir)
        self.recent_project_paths = list(set(self.recent_project_paths))
        self.dump_configs()

    def load_configs(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE) as f:
                cfg = json.load(f)
                for k, v in cfg.items():
                    self.__setattr__(k, v)
        else:
            self.dump_configs()
        logger.info(f"current config is: {self.__dict__}")


_workdir = UNINITIALIZED_WORKDIR
_configs = Configs()
if os.path.exists(_configs.last_workdir):
    _workdir = _configs.last_workdir


# if _workdir == "UNINITIALIZED":
#     _workdir = os.getcwd()
