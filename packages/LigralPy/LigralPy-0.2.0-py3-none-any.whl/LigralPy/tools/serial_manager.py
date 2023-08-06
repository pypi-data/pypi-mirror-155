import ast
import asyncio
import random
import re
import sys
import threading
import time
import serial_asyncio
from serial.serialutil import SerialException
import logging

logger = logging.getLogger(__name__)
from LigralPy.server.udp_echo_server import udp_echo_server
from ..server.udp_sender_async import sender_main

if sys.platform == "win32" and (3, 8, 0) <= sys.version_info < (3, 9, 0):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


class OutputProtocol(asyncio.Protocol):
    def __init__(
        self,
        on_conn_lost,
        serial_recv_queue: asyncio.Queue,
        udp_recv_queue: asyncio.Queue,
        loop: asyncio.ProactorEventLoop,
    ) -> None:
        self.buffer_str = ""
        self.on_conn_lost = on_conn_lost
        self.queue = serial_recv_queue
        self.udp_recv_queue = udp_recv_queue
        self._loop = loop
        self._udp_send_buffer = []

    def connection_made(self, transport):
        self.transport = transport
        transport.serial.rts = False
        asyncio.run_coroutine_threadsafe(self.get_from_queue(), self._loop)

    def data_received(self, data: bytes):
        try:
            self.buffer_str += data.decode("ascii")

            ret = re.search(r"\[[0-9\.\-, ]+\]", self.buffer_str)

            if ret is not None:
                start = ret.start()
                end = ret.end()
                s = self.buffer_str[start:end]
                self.buffer_str = self.buffer_str[end:]
                val = ast.literal_eval(s)
                asyncio.run_coroutine_threadsafe(self.put_into_queue(val), self._loop)
        except:
            import traceback

            traceback.print_exc()

    async def put_into_queue(self, value):
        await self.queue.put(value)
        await asyncio.sleep(0)

    async def write(self, value):
        await asyncio.sleep(0.01)
        self.transport.write(f"{value}\n".encode("ascii"))  # 这里需要加上换行符，否则会出现问题。

    async def get_from_queue(self):
        while 1:
            val = await self.udp_recv_queue.get()
            while self.udp_recv_queue.qsize() > 0:
                val = await self.udp_recv_queue.get()
            await self.write(val["data"]["value"])

    def connection_lost(self, exc):
        self.transport.loop.stop()
        self.on_conn_lost.set_result(True)

    def pause_writing(self):
        logger.info(
            f"pause writing, buffer size: {self.transport.get_write_buffer_size()}"
        )

    def resume_writing(self):
        logger.info(
            f"resumed writing, buffer size: {self.transport.get_write_buffer_size()}"
        )


async def main(loop, serial_recv_queue: asyncio.Queue, udp_recv_queue: asyncio.Queue):
    on_conn_lost = loop.create_future()
    coro = serial_asyncio.create_serial_connection(
        loop,
        lambda: OutputProtocol(on_conn_lost, serial_recv_queue, udp_recv_queue, loop),
        "COM3",
        baudrate=9600,
    )
    try:
        transport, protocol = await coro
    except SerialException as e:
        logger.error("Serial exception occured:", e)
        return
    try:
        await on_conn_lost
    finally:
        if loop.is_running():
            await loop.shutdown_asyncgens()
            loop.stop()
        if not loop.is_closed():
            loop.close()


class ConnectionManager:
    def __init__(self, evtloop: asyncio.ProactorEventLoop) -> None:
        self.loop = evtloop

        self.thread = threading.Thread(target=self.start_main, args=(evtloop,))
        self.thread.setDaemon(True)
        self.thread.start()
        self.serial_recv_queue = asyncio.Queue(10, loop=self.loop)
        self.udp_recv_queue = asyncio.Queue(10, loop=self.loop)

        self.loop.set_exception_handler(
            lambda loop, ctx: logger.error(
                "exception occured in the eventloop:", loop, ctx
            )
        )

    def start_main(self, loop: asyncio.ProactorEventLoop):
        asyncio.set_event_loop(loop)
        loop.run_forever()

    def add_task(self):
        """
        所有任务，尽量用协程实现！
        """
        future = self.loop.create_future()
        asyncio.run_coroutine_threadsafe(
            main(self.loop, self.serial_recv_queue, self.udp_recv_queue), self.loop
        )
        self.run_udp_receiver()
        self.run_udp_sender(future)

    def run_udp_sender(self, future: asyncio.Future):
        asyncio.run_coroutine_threadsafe(
            sender_main(self.loop, self.serial_recv_queue, future, 8789), self.loop
        )

    def run_udp_receiver(self):
        asyncio.run_coroutine_threadsafe(
            udp_echo_server(self.udp_recv_queue, 8790, self.loop), self.loop
        )

    def new_connection(self):
        pass

    def thread_start(self):
        pass


if __name__ == "__main__":
    evtloop = asyncio.new_event_loop()
    cm = ConnectionManager(evtloop)
    cm.add_task()
    for i in range(50):
        time.sleep(1)
