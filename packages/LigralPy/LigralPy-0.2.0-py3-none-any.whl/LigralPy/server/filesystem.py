from typing import List
import json
import os.path
import string
import platform
from flask import Blueprint, abort, make_response, request

from LigralPy.config import UNINITIALIZED_WORKDIR

file_system = Blueprint("fs", __name__, url_prefix="/api/fs")


def get_disk_symbols() -> List[str]:
    """
    获取windows系统的所有盘符
    """
    assert platform.system().lower() == "windows"
    disk_symbols = []
    for ch in string.ascii_uppercase:
        s = f"{ch}:/"
        if os.path.exists(s):
            disk_symbols.append({"name": s, "type": "directory"})
    return disk_symbols


def get_all_file_items(directory: str):
    files = []
    directories = []
    for item in os.listdir(directory):
        abspath = os.path.join(directory, item)
        if os.path.isfile(abspath):
            files.append({"name": item, "type": "file"})
        else:
            directories.append({"name": item, "type": "directory"})
    files.sort(key=lambda item: item["name"])
    directories.sort(key=lambda item: item["name"])
    return directories + files


def rewrite_uninitialized_directory(directory: str):
    """
    如果工作路径为未初始化，则默认定义到桌面。
    """
    if directory == UNINITIALIZED_WORKDIR:
        return os.path.join(os.path.expanduser("~"), "Desktop")

    return directory


@file_system.route("get-fs-items")
def all_fs_items():
    directory: str = request.args.get("directory")
    directory = rewrite_uninitialized_directory(directory)
    if os.path.exists(directory):
        return json.dumps(
            {
                "currentDirectory": directory,
                "fsItemsList": get_all_file_items(directory),
            }
        )
    else:
        abort(make_response(f"Directory {directory} does not exist!", 400))


@file_system.route("goto-parent-dir")
def go_to_parent():
    directory: str = request.args.get("directory")
    directory = rewrite_uninitialized_directory(directory)
    sub_dir = directory
    directory = os.path.dirname(directory)
    if os.path.samefile(sub_dir, directory) and platform.system().lower() == "windows":
        return json.dumps({"currentDirectory": "", "fsItemsList": get_disk_symbols()})
    else:
        return json.dumps(
            {
                "currentDirectory": directory,
                "fsItemsList": get_all_file_items(directory),
            }
        )


@file_system.route("goto-sub-dir")
def go_to_sub():
    directory: str = request.args.get("directory")
    subdir: str = request.args.get("subdir")
    directory = rewrite_uninitialized_directory(directory)
    directory = os.path.join(directory, subdir)
    return json.dumps(
        {"currentDirectory": directory, "fsItemsList": get_all_file_items(directory)}
    )
