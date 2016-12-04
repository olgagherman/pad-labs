import asyncio
import logging
import socket
import struct


LOGGER = logging.getLogger(__name__)


class BaseNodeProtocol(object):
    '''
    Base node Protocol.

    This base class provides some methods with default implementation.
    `server` is an instance of `server.nodes.Node` to control the flow.
    '''
    def __init__(self, node, *args, **kwargs): # pylint: disable=unused-argument
        self.node = node

    def error_received(self, exc):
        LOGGER.error('An error was receveied %s', exc)

    def connection_lost(self, exc):
        LOGGER.error('Connection Lost %s', exc)


class NodeResponseUdpProtocol(BaseNodeProtocol, asyncio.DatagramProtocol):
    '''
    Protocol which implements listening of info packets from the clients via unicast
    '''
    def __init__(self, node, udp_address_group, *args, **kwargs):
        super().__init__(node, *args, **kwargs)
        self.udp_address_group = udp_address_group

    def init_multicast_transport(self, transport):
        sock = transport.get_extra_info('socket')
        group = socket.inet_aton('239.255.255.250')
        mreq = struct.pack('4sL', group, socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    def connection_made(self, transport):
        self.init_multicast_transport(transport)
        self.transport = transport # pylint: disable=attribute-defined-outside-init

    def datagram_received(self, data, addr):
        LOGGER.debug('Received %s from %s', data, addr)
        message = self.node.get_info_response_message(data)
        LOGGER.debug('Sending %s', message)
        client_addr = ('127.0.0.1', 14140) # TODO: You should get this from client's message
        self.transport.sendto(message, client_addr)


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
