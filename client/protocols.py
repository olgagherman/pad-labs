import asyncio
import logging
import socket
import struct


LOGGER = logging.getLogger(__name__)


class BaseClientProtocol(object):
    '''
    Base client Protocol.

    This base class provides some methods with default implementation.
    `client` is an instance of `client.app.Client` for control of the flow.
    '''
    def __init__(self, client, *args, **kwargs): # pylint: disable=unused-argument
        self.client = client

    def error_received(self, exc):
        LOGGER.error('An error was receveied %s', exc)

    def connection_lost(self, exc):
        LOGGER.error('Connection Lost %s', exc)


class ClientRequestUdpProtocol(BaseClientProtocol, asyncio.DatagramProtocol):
    '''
    Protocol which implements requesting of data from nodes via multicast
    '''
    def __init__(self, client, udp_address_group, *args, **kwargs):
        super().__init__(client, *args, **kwargs)
        self.udp_address_group = udp_address_group

    def init_multicast_transport(self, transport):
        sock = transport.get_extra_info('socket')
        group = socket.inet_aton('239.255.255.250')
        mreq = struct.pack('4sL', group, socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    def connection_made(self, transport):
        self.init_multicast_transport(transport)

        message = self.client.get_info_request_message()
        LOGGER.debug('Connection made. Transport %s, Sending - %s', transport, message)
        transport.sendto(message)
        LOGGER.debug('Waiting for response')
        self.client.info_request_sent()


class ClientResponseUdpProtocol(BaseClientProtocol, asyncio.DatagramProtocol):
    '''
    Protocol which implements listening of info packets from nodes via unicast
    '''
    def datagram_received(self, data, addr):
        LOGGER.debug('Received %s from %s', data, addr)
        self.client.process_info_response(data)

class ClientRequestTcpProtocol(BaseClientProtocol, asyncio.Protocol):
    '''
    Protocl which implements retrieving of data from a node via TCP
    '''
    def connection_made(self, transport):
        message = self.client.get_data_request_message()
        LOGGER.debug('Connection made. Transport %s, Sending - %s', transport, message)
        transport.write(message)
        LOGGER.debug('Waiting for response')

    def data_received(self, data):
        LOGGER.debug('Received data - %s', data)
        self.client.process_data_response(data)
