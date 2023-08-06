import asyncio
import json
import time


class EchoClientProtocol(asyncio.DatagramProtocol):
    def __init__(self, message, on_con_lost, initial_time: float, queue: asyncio.Queue):
        self.queue = queue
        self.message = message
        self.on_con_lost = on_con_lost
        self.transport = None
        self._last_send = 0
        self._initial_time = initial_time
        self._loop: asyncio.ProactorEventLoop = asyncio.get_event_loop()

        asyncio.run_coroutine_threadsafe(self.put(), self._loop)

    def connection_made(self, transport):
        self.transport = transport
        asyncio.run_coroutine_threadsafe(self.async_send(), self._loop)

    async def put(self):
        for i in range(8):
            await self.queue.put(i)

    async def async_send(self):
        while 1:
            val = await self.queue.get()
            self.message = json.dumps({"label": 0, "data": {"value": val}})
            self.transport.sendto(self.message.encode())

    def start_send_loop(self):
        self._loop.run_in_executor()

    def datagram_received(self, data, addr):
        print("->Received:", data.decode())

    def error_received(self, exc):
        print("Error received:", exc)

    def connection_lost(self, exc):
        print("Connection closed")
        self.on_con_lost.set_result(True)


async def sender_main(
    loop: asyncio.ProactorEventLoop,
    queue: asyncio.Queue,
    future: asyncio.Future,
    port: int,
):
    t0 = time.time()
    on_con_lost = loop.create_future()
    message = "Hello World!"

    transport, protocol = await loop.create_datagram_endpoint(
        lambda: EchoClientProtocol(message, on_con_lost, t0, queue),
        remote_addr=("127.0.0.1", port),
    )

    try:
        await on_con_lost
    finally:
        transport.close()
        future.set_result(True)
