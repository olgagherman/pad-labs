import asyncio

class Server:
    udp_address = {
        "host": "239.255.255.1",
        "port": 8000
    }
    tcp_address = {
        "host": "127.0.0.1",
        "port": 0
    }
    neighbor_nodes = {
        "node": {"host": "", "port": ""}
    }

    #server expects the client to request port and number of links
    async def listen_udp():

    #server expects other services to request stored information
    async def listen_tcp():

    #server sends to client port and number of links
    async def discovery_info():

    #server sends to client information colected from other servers
    async def transport_info():

    #server requests information from other servers
    async def request_neighbor_info():
