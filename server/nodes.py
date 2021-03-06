'''
Implementation of the serve nodes
'''
import logging
import asyncio
import socket
import json

from .protocols import NodeResponseUdpProtocol, NodeResponseTcpProtocol


LOGGER = logging.getLogger(__name__)

class ServerNode(object):
    '''
    ServerNode is an unit of executable async code which can be distributed
    to an arbitrary infrastructure.
    '''
    def __init__(
            self,
            node_id,
            loop,
            udp_group_address, udp_group_port,
            neighbor,
            host, port,
            data
        ):
        self.id = node_id
        self.loop = loop
        self.udp_group_address = udp_group_address
        self.udp_group_port = udp_group_port
        self.neighbor = neighbor
        self.host = host
        self.port = port
        self.data = data

    def get_data_response_message(self, client_data):
        '''
        Returns a message for the client based on client's request contained in
        `client_data`.
        '''
        message = self.serialize(self.data)
        return message.encode('utf-8')

    def get_info_response_message(self, client_data):
        '''
        Returns a message to the client about the info node.
        '''
        LOGGER.debug('Node %s - processing datagram', self.id)
        data = json.loads(client_data.decode('utf-8'))
        return data['address'], data['port']

    def serialize(self, data):
        """Transforms a model into a dictionary which can be dumped to JSON."""
        result = dict()
        for k,obj in data.items():
            result[k] = json.dumps(obj)
        return json.dumps(result)

    def run_tcp_server(self):
        '''
        Runs a TCP server and returns an `asyncio.Task` instance.
        '''
        LOGGER.debug('Running TCP server - Node %s', self.id)
        t = asyncio.Task(self.loop.create_server(
            lambda: NodeResponseTcpProtocol(self),
            self.host, self.port,
        ))
        return t

    def run_udp_multicast_server(self):
        '''
        Runs a UDP multicast server and returns an `asyncio.Task` instance.
        '''
        LOGGER.debug('Running UDP multicast server - Node %s', self.id)
        t = asyncio.Task(self.loop.create_datagram_endpoint(
            lambda: NodeResponseUdpProtocol(self, self.udp_group_address),
            local_addr=('0.0.0.0', self.udp_group_port),
            family=socket.AF_INET,
        ))
        return t

    async def run(self):
        '''
        Entry point for the node. It's a coroutine

        You may return just result of `asyncio.wait` from this method and run
        `run_forever` from an external function.
        '''
        return await asyncio.wait([self.run_tcp_server(), self.run_udp_multicast_server()])
