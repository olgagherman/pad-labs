import asyncio
import logging

from core.protocols import UdpMulticastProtocolMixin

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


class ClientRequestUdpProtocol(UdpMulticastProtocolMixin, BaseClientProtocol, asyncio.DatagramProtocol):
    '''
    Protocol which implements requesting of data from nodes via multicast
    '''
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
