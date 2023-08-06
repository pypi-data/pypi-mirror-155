import json
import os
import platform
import subprocess
from flask import Blueprint, abort, make_response, request

from LigralPy.config import (
    UNINITIALIZED_WORKDIR,
    get_workdir,
    set_workdir,
    get_recent_projects,
)
from LigralPy.tools.project_config import ProjectConfig

project_blueprint = Blueprint("project", __name__, url_prefix="/api/project")


@project_blueprint.route("/new-project", methods=["POST"])
def create_project():
    """
    创建一个新的项目
    /Users/hzy/Develops/ligral-simulation/myproject
    """
    data = json.loads(request.get_data())
    name = data["name"]
    wd = data["workdir"]
    wd = os.path.join(wd, name)
    if not os.path.exists(wd):
        if not os.path.exists(os.path.dirname(wd)):
            abort(
                make_response(
                    f"Directory not found and cannot be created." "Directory:{wd}", 400
                )
            )
        else:
            os.mkdir(wd)
    if len(os.listdir(wd)) > 0:
        abort(make_response(f"Target directory {wd} is not empty!", 400))
    template = {
        "nodes": [],
        "edges": [],
        "info": {
            "name": name,
            "type": "main",
            "settings": {"inPorts": [], "outPorts": []},
        },
    }

    main_json_path = os.path.join(wd, f"{name}.main.json")

    with open(main_json_path, "w") as f:
        json.dump(template, f)
    set_workdir(wd)
    return "Project created successfully!"


@project_blueprint.route("/open-project", methods=["POST"])
def open_project():
    data = json.loads(request.get_data())
    wd = data["workdir"]
    assert os.path.exists(wd)
    for file in os.listdir(wd):
        if file.endswith(".main.json"):
            set_workdir(wd)
            return "Project Opened!"
    abort(
        make_response(
            "Open project failed because no main ligral file inside the directory!", 400
        )
    )


@project_blueprint.route("/recent-projects", methods=["GET"])
def handler_recent_project():
    return json.dumps(
        [
            {"name": os.path.basename(project_path), "path": project_path}
            for project_path in get_recent_projects()
        ]
    )


@project_blueprint.route("/initial-info", methods=["GET"])
def get_initial_info():
    try:
        workdir = get_workdir()
    except FileNotFoundError:
        workdir = UNINITIALIZED_WORKDIR
    return {"workdir": workdir}


@project_blueprint.route("/open-folder", methods=["POST"])
def open_folder():
    data = json.loads(request.get_data())
    opentype = data["type"]
    if opentype == "cwd":
        directory = get_workdir()
    else:
        pass
    if not os.path.exists(directory):
        abort(
            make_response(f"Directory {directory} does not exist on this machine!", 400)
        )
    # 对于在windows平台下的情形
    if platform.system().lower().find("windows") != -1:
        files = os.listdir(directory)
        if len(files) == 0:
            abort(make_response(f"No files in directory {directory}!", 400))
        selected_file = os.path.join(directory, files[0])
        cmd = f"explorer /select,{selected_file}"
        subprocess.Popen(cmd)
        
    # 对于苹果系统
    elif platform.system().lower().find("darwin")!=-1:
        subprocess.Popen(['open', directory])
    else:
        abort(
            make_response(
                f"Opening directory on current operating system is not implemented yet",
                400,
            )
        )
    return "open succeeded"


@project_blueprint.route("/simulation-config", methods=["GET"])
def get_simulation_config():
    pc = ProjectConfig()
    struct =  json.dumps(pc.to_frontend_struct())
    return struct
    