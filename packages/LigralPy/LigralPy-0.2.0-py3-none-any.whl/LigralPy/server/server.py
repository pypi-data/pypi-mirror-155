from lib2to3.pgen2.token import tok_name
import queue
import random
import shutil
import socket
import string
import struct
import subprocess
import datetime
import json
import os
import logging
import threading
import time
from tokenize import Token
from flask import (
    Flask,
    abort,
    make_response,
    render_template,
    request,
    current_app,
    g as app_ctx,
    session,
)

from LigralPy.nodes.nodes_mgr import (
    get_all_node_files,
    get_all_route_jsons,
    get_file_by_chart_name,
    get_main_graph,
    load_from_route_json,
)
from LigralPy.server.chart_receiver import chart_handler_main, flush

from ..config import STATIC_FOLDER, get_workdir
from ..nodes import get_all_nodetype_jsons
from ..tools.chart_parser import parse_graph_with_route, rename_chart
from .ws import register_websocket_handlers
from .project import project_blueprint
from .filesystem import file_system

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
assert os.path.exists(STATIC_FOLDER)
app = Flask(
    __name__,
    static_folder=STATIC_FOLDER,
    static_url_path="",
    template_folder=STATIC_FOLDER,
)
app.config['SECRET_KEY'] = os.urandom(24)
app.register_blueprint(project_blueprint)
app.register_blueprint(file_system)


def gen_token():
    char_list = []
    for i in range(20):
        char_list.append(random.choice(string.ascii_letters+string.digits))
    return "".join(char_list)


TOKEN = gen_token()
print("Token is:", TOKEN)


@app.route("/", methods=["GET"])
def root():
    return render_template("index.html")


def is_loopback(host):
    """
    检测一个地址是否为本机。
    https://stackoverflow.com/questions/47885832/determine-if-host-is-localhost
    """
    # loopback_checker = {
    #     socket.AF_INET: lambda x: struct.unpack('!I', socket.inet_aton(x))[0] >> (32-8) == 127,
    #     socket.AF_INET6: lambda x: x == '::1'
    # }
    # for family in (socket.AF_INET, socket.AF_INET6):
    #     try:
    #         r = socket.getaddrinfo(host, None, family, socket.SOCK_STREAM)
    #     except socket.gaierror:
    #         return False
    #     for family, _, _, _, sockaddr in r:
    #         if not loopback_checker[family](sockaddr[0]):
    #             return False
    if host.strip() in ("127.0.0.1", "localhost"):
        return True
    else:
        return False


@app.before_request
def logging_before():
    app_ctx.start_time = time.perf_counter()

    # print(request.args.get("token"))

    # print("user_info", session.get("token"))
    token = session.get("token")
    # print("user_info", TOKEN, token)
    # session["token"] = TOKEN
    if is_loopback(request.remote_addr):
        return
    if token != TOKEN:
        print("Aborted!")
        abort(make_response(
            "You are not visiting LigralPy in localhost, and the token does not match.", 403))


@app.after_request
def logging_after(response):
    total_time = time.perf_counter() - app_ctx.start_time
    time_in_ms = int(total_time * 1000)
    current_app.logger.info(
        "%s ms %s %s %s", time_in_ms, request.method, request.path, dict(
            request.args)
    )
    return response


@app.route("/api/cards", methods=["GET", "POST"])
def cards():
    return json.dumps(get_all_nodetype_jsons() + get_all_route_jsons())


@app.route("/api/chart", methods=["GET"])
def chart():
    query = request.args.get("query")
    type = request.args.get("type")
    assert type in {"file_name", "chart_name"}
    if type == "file_name":
        file_path = query
    else:
        file_path = get_file_by_chart_name(query)
    with open(file_path) as f:
        return f.read()


@app.route("/api/save", methods=["POST"])
def handler_save_chart():
    data = json.loads(request.get_data())
    assert data["type"] in {"file_name", "chart_name"}
    if data["type"] == "file_name":
        file_path = data["query"]
    else:
        file_path = get_file_by_chart_name(data["query"])
    with open(file_path, "w") as f:
        f.write(json.dumps(json.loads(data["data"]), indent=4))
    return "Save data succeeded!"


@app.route("/api/new-route", methods=["POST"])
def handler_new_route():
    data = json.loads(request.get_data())
    graph_name = data["name"]
    with open(os.path.join(get_workdir(), graph_name + ".route.json"), "w") as f:
        json.dump(
            {
                "nodes": [],
                "edges": [],
                "info": {
                    "name": graph_name,
                    "type": "route",
                    "settings": {"inPorts": [], "outPorts": []},
                },
            },
            f,
            indent=4,
        )

    return "New Route Succeeded!"


@app.route("/api/rename-chart", methods=["POST"])
def handler_rename_chart():
    data = json.loads(request.get_data())
    last_name = data["lastName"]
    new_name = data["newName"]
    rename_chart(last_name, new_name)
    return "Rename chart succeeded!"


@app.route("/api/all-charts", methods=["GET"])
def all_charts():
    """
    返回所有图，包含主图和子图。
    """
    files = get_all_node_files()
    charts = []
    for file in files:
        basename = os.path.basename(file)
        if basename.endswith(".main.json"):
            chart_type = "main"
            with open(file) as f:
                chart_name = json.load(f)["info"]["name"]
        else:
            chart_type = "route"
            chart_name = load_from_route_json(file)["id"]

        charts.append({"chartType": chart_type,
                      "label": chart_name, "fileName": file})
    return json.dumps(charts)


@app.route("/api/run", methods=["POST"])
def run():
    global th
    try:
        workdir = get_workdir()

    except FileNotFoundError as e:
        res = make_response(str(e), 400)
        abort(res)  # 返回错误信息
    logger.debug("debug!")
    main_graph_json = get_main_graph()
    logger.debug("main graph got!")

    parsed_flowchart = parse_graph_with_route(main_graph_json)
    # 创建临时路径，存储仿真结果。
    tmp_path = os.path.join(workdir, "simulation_results")
    if not os.path.exists(tmp_path):
        os.mkdir(tmp_path)
    logger.debug("route parsed!")
    proj_name = "tmp_proj"

    t = datetime.datetime.now().strftime("%Y-%m-%d--%H-%M-%S")
    new_folder = os.path.join(tmp_path, proj_name + "+" + t)
    os.mkdir(new_folder)
    # copy all sourcefiles to the new_folder for backup.
    for file in get_all_node_files():
        logger.debug("copying file" + file + " to " + new_folder)
        shutil.copy(file, os.path.join(new_folder))
    logger.debug("files copied!")
    ligral_json_file = os.path.join(new_folder, "run.lig.json")
    ligral_json_file_in_wd = os.path.join(workdir, "run.lig.json")
    with open(ligral_json_file, "w") as f:
        f.write(json.dumps(parsed_flowchart, indent=4))
    with open(ligral_json_file_in_wd, "w") as f:
        f.write(json.dumps(parsed_flowchart, indent=4))
    logger.debug("Starting the ligral process...")
    p=subprocess.Popen(["ligral", "run.lig.json", "--json"], cwd=new_folder)
    
    logger.warning("TODO: 目前是定时清空，还需要监听进程来进行判断！！")
    th = threading.Timer(2, flush)
    th.setDaemon(True)
    th.start()

    return "Ligral Run!"


register_websocket_handlers(app)
chart_handler_main()


def run_server():
    app.run(port=5000)
