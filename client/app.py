import asyncio
import socket
import json

from .protocols import (
    ClientRequestTcpProtocol, ClientRequestUdpProtocol, ClientResponseUdpProtocol
)

NODE_INFO = dict()

class Client(object):
    def __init__(
            self,
            loop,
            udp_group_address='239.255.255.250', udp_group_port=14141,
            udp_address='127.0.0.1', udp_port=14140,
            ):
        self.loop = loop
        self.udp_group_address = udp_group_address
        self.udp_group_port = udp_group_port
        self.udp_address = udp_address
        self.udp_port = udp_port

    def get_info_request_message(self):
        message = json.dumps({
            'address': self.udp_address,
            'port': self.udp_port
        }).encode('utf-8')
        return message

    def get_data_request_message(self):
        message = 'Data Request'
        return message.encode('utf-8')

    def process_info_response(self, data):
        node_info = json.loads(data.decode('utf-8'))
        NODE_INFO[len(NODE_INFO)] = dict()
        NODE_INFO[len(NODE_INFO)] = node_info
        return node_info

    def process_data_response(self, data):
        # data = data.decode('utf-8')
        pass

    def info_request_sent(self):
        pass

    def run_tcp_server(self, host, port):
        t = asyncio.Task(self.loop.create_connection(
            lambda: ClientRequestTcpProtocol(self), host, port,
        ))
        return t

    def run_udp_server(self):
        t = asyncio.Task(self.loop.create_datagram_endpoint(
            lambda: ClientResponseUdpProtocol(self),
            local_addr=(self.udp_address, self.udp_port),
        ))
        return t

    def run(self):
        self.run_udp_server()
        multicast_task = asyncio.Task(self.loop.create_datagram_endpoint(
            lambda: ClientRequestUdpProtocol(self, self.udp_group_address),
            remote_addr=(self.udp_group_address, self.udp_group_port),
            family=socket.AF_INET,
        ))
        self.loop.run_until_complete(multicast_task)
        self.loop.run_forever()
