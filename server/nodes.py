'''
Implementation of the serve nodes
'''
import asyncio
import socket

from .protocols import NodeResponseUdpProtocol, NodeResponseTcpProtocol

class ServerNode(object):
    '''
    ServerNode is an unit of executable async code which can be distributed
    to an arbitrary infrastructure.
    '''
    def __init__(
            self,
            loop,
            udp_group_address, udp_group_port,
            neighbor,
            host, port,
        ):
        self.loop = loop
        self.udp_group_address = udp_group_address
        self.udp_group_port = udp_group_port
        self.neighbor = neighbor
        self.host = host
        self.port = port

    def get_data_response_message(self, client_data):
        '''
        Returns a message for the client based on client's request contained in
        `client_data`.
        '''
        return 'You said - {}'.format(client_data.decode())

    def get_info_request_message(self, client_data):
        '''
        Returns a message to the client about the info node.
        '''
        return 'You said - {}'.format(client_data.decode())

    def run_tcp_server(self):
        '''
        Runs a TCP server and returns an `asyncio.Task` instance.
        '''
        t = asyncio.Task(self.loop.create_server(
            lambda: NodeResponseTcpProtocol(self),
            self.host, self.port,
        ))
        return t

    def run_udp_multicast_server(self):
        '''
        Runs a UDP multicast server and returns an `asyncio.Task` instance.
        '''
        t = asyncio.Task(self.loop.create_datagram_endpoint(
            lambda: NodeResponseUdpProtocol(self, self.udp_group_address),
            local_addr=('0.0.0.0', self.udp_group_port),
            family=socket.AF_INET,
        ))
        return t

    def run(self):
        '''
        Entry point for the node
        '''
        self.loop.run_until_complete(asyncio.wait([
            self.run_tcp_server(),
            self.run_udp_multicast_server(),
        ]))
        self.loop.run_forever()
