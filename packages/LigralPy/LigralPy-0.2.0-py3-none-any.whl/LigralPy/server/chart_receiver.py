from typing import Any, Dict, Iterable, Set

from flask import g
from .ws import send_queue
import sys
import socket
import json
import threading
import time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import logging

logger = logging.getLogger(__name__)


class Figure:
    def __init__(self, fig, ax):
        self.fig = fig
        self.ax = ax
        self.curves = {}
        self.showed = np.zeros((1, 1))

    def __getitem__(self, item):
        if isinstance(self.ax, np.ndarray):
            return self.ax[item]
        elif item == (0, 0) or item == 0:
            return self.ax

    def show(self, row, col):
        self.showed[row, col] = 1

    def is_showed(self):
        return (self.showed == 1).all()


class EchartsFigure:
    def __init__(self, parent: "EChartsAgg", name: str) -> None:
        self.parent = parent
        self.name = name

    def suptitle(self, title):
        self.parent.plots[self.name]["title"]["text"] = title


class EchartsAx:
    def __init__(self, parent: "EChartsAgg", name: str, ax_index=0) -> None:
        self.parent = parent
        self.name = name
        self.ax_index = 0


class EChartsAgg:
    """
    轻量化、专为科学计算定制的agg。
    """

    def __init__(self) -> None:
        self.canvas_grid_initialized = False
        self.plots: Dict[str, Dict[str:Any]] = {}
        self.plotted_plots: Set[str] = set()

    def init_canvas_grid(self, name: str, rows: int, cols: int):
        self.plots[name] = {
            "title": {"text": "----", "left": "center", "top": 0},
            "grid": [],
            "xAxis": [],
            "yAxis": [],
            "series": [],
        }
        config = self.plots[name]
        for row in range(rows):
            for col in range(cols):
                grid_index = row * cols + col
                h_margins = {}
                v_margins = {}
                if col == 0:
                    h_margins = {"left": "7%"}
                elif col == cols - 1:
                    h_margins = {"right": "7%"}
                if row == 0:
                    v_margins = {"top": "7%"}
                elif row == rows - 1:
                    h_margins = {"bottom": "7%"}
                width = (100 - 7 * 2 - (cols - 1) * 6) / cols
                height = (100 - 7 * 2 - (rows - 1) * 6) / rows

                grid_params = {"width": f"{width}%", "height": f"{height}%"}
                grid_params.update(h_margins)
                grid_params.update(v_margins)
                config["toolbox"] = (
                    {
                        "show": True,
                        "feature": {
                            "dataZoom": {"yAxisIndex": "none"},
                            "dataView": {"readOnly": False},
                            "restore": {},
                            "saveAsImage": {},
                        },
                    },
                )
                config["grid"].append(grid_params)
                config["xAxis"].append({"gridIndex": grid_index, "nameLocation": "middle"})
                config["yAxis"].append({"gridIndex": grid_index, "nameLocation": "middle"})
                config["series"].append(
                    {
                        "name": "UNDEFINED",
                        "type": "line",
                        "showSymbol": False,
                        "xAxisIndex": grid_index,
                        "yAxisIndex": grid_index,
                        "data": [],
                    }
                )
        self.canvas_grid_initialized = True

    def subplots(self, rows: int, cols: int, figID: str):
        if figID not in self.plots:
            self.init_canvas_grid(figID, rows, cols)
        return EchartsFigure(self, figID), EchartsAx(self, figID, 0)

    def set_title(self, figID: str, title: str):
        self.plots[figID]["title"]["text"] = title

    def set_label(self, figID: str, row, col, x_label: str, y_label: str):
        grid_index = row * 2 + col
        self.plots[figID]["xAxis"][grid_index]["name"] = x_label
        self.plots[figID]["yAxis"][grid_index]["name"] = y_label

    def set_data(
        self, figID: str, series_id: int, x: Iterable[float], y: Iterable[float]
    ):
        assert len(x) == len(y)
        l = []
        x = json.loads(x.to_json(orient="split"))["data"]
        y = json.loads(y.to_json(orient="split"))["data"]
        for i in range(len(x)):
            l.append([x[i], y[i]])
        try:
            self.plots[figID]["series"][series_id]["data"] = l
        except KeyError as e:
            raise KeyError(f"{figID}, {series_id}, {self.plots}")

    def set_fig_plotted(self, figID: str):
        self.plotted_plots.add(figID)

    @property
    def all_figs_plotted(self) -> bool:
        for figID in self.plots.keys():
            if figID not in self.plotted_plots:
                return False
        return True


class PlotterHandler:
    def __init__(self, agg="mpl"):
        self.plotter = EChartsAgg()

        self.figs: Dict[str, Figure] = {}
        self.pools = []
        self.dfs = {}
        self.handle = self.handler_wrapper(self.handle)

    def clear(self):
        self.figs = {}
        self.pools = []
        self.dfs = {}

    def invoke(self, label, data):
        # self.pools.append((label, data))
        self.handle(label, data)

    def handler_wrapper(self, handler):
        def wrapper(label, data):
            try:
                handler(label, data)
            except KeyError as e:
                import traceback

                traceback.print_exc()
                print(f"ERROR: invalid packet: {e}")

        return wrapper

    def flush_plotter(self):
        """
        清空plotter，并且将其中的一切数据推向websocket.
        """
        send_queue.put(json.dumps(self.plotter.plots))
        self.plotter = EChartsAgg()

    def handle(self, label, data):
        if label == 0xFFF0:  # 数据所在的文件信息
            if data["file"] in self.dfs:
                df = self.dfs[data["file"]]
            else:
                df = pd.read_csv(data["file"], skipinitialspace=True)
                self.dfs[data["file"]] = df
            x = df[data["x"]]
            y = df[data["y"]]
            print("data", data["fig"], self.figs)
            self.plotter.set_data(data["fig"], data["curve"], x, y)
            self.plotter.set_fig_plotted(data["fig"])
            if self.plotter.all_figs_plotted:
                # self.flush_plotter()
                print("flush plotter!")
            print(f"fig {data['fig']} is plotted!")
        elif label == 0xFFC0:
            # figure = self.figs[data["fig"]]
            # figure.curves[data["curve"]] = None, data["row"], data["col"]
            pass
        elif label == 0xFFB0:
            self.plotter.subplots(
                data["rows"], data["cols"], figID=data["fig"])
            self.plotter.set_title(data["fig"], data["title"])

        elif label == 0xFFA0:
            print(data)
            self.plotter.set_label(
                data["fig"], data['row'], data['col'], data["xlabel"], data["ylabel"])
        else:
            pass


def task(serverSock: socket.socket, handler: PlotterHandler):
    logger.info(f"chart udp receiver started at {serverSock.getsockname()}")
    while True:
        packetbytes, addr = serverSock.recvfrom(1024)
        packet = json.loads(packetbytes)
        label, data = packet["label"], packet["data"]
        if label < 0xFF00:
            continue
        handler.invoke(label, data)
        if label in (0xFFF0, 0xFFC0, 0xFFB0, 0xFFA0):
            print(
                f"INFO: received packet label: {hex(label)}, content: {packet}")


_handler_th = None
_mainloop_th = None
_plotter_handler: PlotterHandler = None


def flush():
    global _plotter_handler
    _plotter_handler.flush_plotter()


def chart_handler_main():
    global _handler_th, _mainloop_th, _plotter_handler

    UDP_IP_ADDRESS = "127.0.0.1"
    UDP_PORT_NO = 8784

    serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serverSock.bind((UDP_IP_ADDRESS, UDP_PORT_NO))

    handler = PlotterHandler("echarts")
    _plotter_handler = handler
    _handler_th = threading._start_new_thread(task, (serverSock, handler))
