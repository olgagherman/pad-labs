import asyncio
import collections
from .class_server import Server

_SERVERS = []

def run_server():
    loop = asyncio.get_event_loop()
    server = Server()
    Server.listen_udp(server)
    '''task = asyncio.Task(loop.create_datagram_endpoint(Server, local_addr=(Server.tcp_address["host"], Server.tcp_address["port"])))
    transport, server = loop.run_until_complete(task)
    try:
        loop.run_forever()
    finally:
        transport.close()
    loop.close()'''
