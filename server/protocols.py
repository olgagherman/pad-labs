import asyncio
import logging
import json

from core.protocols import UdpMulticastProtocolMixin

LOGGER = logging.getLogger(__name__)


class BaseNodeProtocol(object):
    '''
    Base node Protocol.

    This base class provides some methods with default implementation.
    `server` is an instance of `server.nodes.ServerNode` to control the flow.
    '''
    def __init__(self, node, *args, **kwargs): # pylint: disable=unused-argument
        self.node = node

    def error_received(self, exc):
        LOGGER.error('An error was receveied %s', exc)

    def connection_lost(self, exc):
        LOGGER.error('Connection Lost %s', exc)


class NodeResponseUdpProtocol(UdpMulticastProtocolMixin, BaseNodeProtocol, asyncio.DatagramProtocol):
    '''
    Protocol which implements listening of info packets from the clients via unicast
    '''
    def connection_made(self, transport):
        self.init_multicast_transport(transport)
        self.transport = transport # pylint: disable=attribute-defined-outside-init

    def datagram_received(self, data, addr):
        LOGGER.debug('Received %s from %s', data, addr)
        client_address, client_port = self.node.get_info_response_message(data)
        message_to_send = json.dumps({
            'address': self.node.host,
            'port': self.node.port,
            'links': len(self.node.neighbor)
        }).encode('utf-8')
        LOGGER.debug('Sending %s', message_to_send)
        client_addr = (client_address, client_port)
        self.transport.sendto(message_to_send, client_addr)


class NodeResponseTcpProtocol(BaseNodeProtocol, asyncio.Protocol):
    '''
    Protocol which implements sending of data to the client via TCP
    '''
    def connection_made(self, transport):
        self.transport = transport # pylint: disable=attribute-defined-outside-init

    def data_received(self, data):
        LOGGER.debug('Received data - %s', data)
        message = self.node.get_data_response_message(data)
        LOGGER.debug('Sending - %s', message)
        self.transport.write(message)
