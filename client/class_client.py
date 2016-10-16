import socket
import asyncio

class Client:
    tcp_address = {
        "host": "127.0.0.1",
        "port": 9999
    }
    udp_address = {
        "host": "127.0.0.1",
        "port": 8888
    }

    #client request to all servers port and number of links
    async def discovery_request():

    #client request some objects from maven
    async def trasport_request():

    #client expects from all servers port and number of links
    async def discovery_listen():

    #client expects some objects from servers
    async def transport_listen():
