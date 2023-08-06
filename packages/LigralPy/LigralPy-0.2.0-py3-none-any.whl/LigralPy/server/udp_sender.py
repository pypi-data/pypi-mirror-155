# 不需要建立连接
import socket
import json
import threading
import time

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def test_send():
    last_send = time.time()
    while 1:
        while 1:
            t = time.time()
            if t - last_send > 0.001:
                break
        b = json.dumps(
            {"label": 0, "data": {"aaa": time.time(), "out": 111111, "out2": 111115}}).encode("ascii")
        s.sendto(b, ("127.0.0.1", 8900))
        last_send = t


if __name__ == "__main__":
    th = threading.Thread(target=test_send)
    th.setDaemon(True)
    th.start()
    while 1:
        time.sleep(1)
