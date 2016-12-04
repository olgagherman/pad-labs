import asyncio

from .protocols import (
    ClientRequestTcpProtocol, ClientRequestUdpProtocol, ClientResponseUdpProtocol
)

class Client(object):
    def __init__(
            self,
            loop,
            udp_group_address=None, udp_group_port=None,
            udp_address=None, udp_port=None,
            ):
        self.loop = loop
        self.udp_group_address = udp_group_address
        self.udp_group_port = udp_group_port
        self.udp_address = udp_address
        self.udp_port = udp_port

    def get_info_request_message(self):
        message = 'Info Request'
        return message.encode('utf-8')

    def get_data_request_message(self):
        message = 'Data Request'
        return message.encode('utf-8')

    def process_info_response(self, data):
        # data = data.decode('utf-8')
        pass

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
            lambda: ClientResponseUdpProtocol(self), self.udp_address, self.udp_port,
        ))
        return t

    def run(self):
        multicast_task = asyncio.Task(self.loop.create_datagram_endpoint(
            lambda: ClientRequestUdpProtocol(self, self.udp_group_address),
            '0.0.0.0', self.udp_group_port,
        ))
        unicast_task = self.run_udp_server()
        self.loop.run_until_complete([
            unicast_task,
            multicast_task,
        ])
        self.loop.run_forever()
