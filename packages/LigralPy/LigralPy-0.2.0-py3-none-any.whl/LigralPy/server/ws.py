from concurrent.futures import thread
import queue
import time
from flask import Flask
from flask_sock import Sock
import threading


class WSManager:
    def __init__(self) -> None:
        self.websockets = {}

    def add(self, ws):
        self.websockets[id(ws)] = ws

    def remove(self, ws):
        self.websockets.pop(id(ws))


def send_loop():
    while 1:
        value = send_queue.get()
        ws_keys = list(ws_mgr.websockets.keys())
        for ws_key in ws_keys:
            ws = ws_mgr.websockets[ws_key]
            print("connected", ws.connected)
            if ws.connected:
                ws.send(value)
            else:
                ws_mgr.remove(ws)


def register_websocket_handlers(app: Flask):

    global sock  # 设置成global才可。
    app.config["SOCK_SERVER_OPTIONS"] = {"ping_interval": 25}
    sock = Sock(app)

    @sock.route("/api/echo")
    def echo(ws):
        """
        # The ws object has the following methods:
        # - ws.send(data)
        # - ws.receive(timeout=None)
        # - ws.close(reason=None, message=None)
        """
        ws_mgr.add(ws)
        while True:
            data = ws.receive()
            send_queue.put(data)
            # ws.send(data)


sock = None

send_queue = queue.Queue(1024)
ws_mgr = WSManager()
send_th = threading.Thread(target=send_loop)
send_th.setDaemon(True)
send_th.start()
