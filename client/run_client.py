import asyncio
from .class_client import Client

def run_client():
    client = Client()
    Client.discovery_request(client)
    '''loop = asyncio.get_event_loop()
    run_client(loop, (Client.tcp_address["host"], Client.tcp_address["port"]))
    task = asyncio.Task(loop.create_datagram_endpoint(Client, remote_addr=addr))
    loop.run_until_complete(task)'''
