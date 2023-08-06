import asyncio
from asyncio.log import logger
import json
import time


class EchoServerProtocol:
    def __init__(self, recv_queue: asyncio.Queue, loop: asyncio.ProactorEventLoop):
        self.recv_queue = recv_queue
        self._loop = loop

    def connection_made(self, transport):
        self.transport = transport

    async def put_into_queue(self, value):
        await self.recv_queue.put(value)

    def datagram_received(self, data, addr):
        t_receive = time.time()
        message = data.decode()
        res = json.loads(message)

        asyncio.run_coroutine_threadsafe(self.put_into_queue(res), self._loop)
        # self.transport.sendto(data, addr)


async def udp_echo_server(queue: asyncio.Queue, port=8790, loop=None):
    try:
        logger.info("Starting UDP server")
        if loop is None:
            loop = asyncio.get_running_loop()
        transport, protocol = await loop.create_datagram_endpoint(
            lambda: EchoServerProtocol(queue, loop), local_addr=("127.0.0.1", port)
        )
        try:
            await asyncio.sleep(36000000)  # Serve for 1 hour.
        finally:
            logger.info("Asyncio已经到时间，现在关闭......")
            transport.close()

    except:
        import traceback

        traceback.print_exc()
