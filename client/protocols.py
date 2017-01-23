import asyncio
import logging
import json
from twisted.internet import reactor

from core.protocols import UdpMulticastProtocolMixin

LOGGER = logging.getLogger(__name__)
timeout = 2

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
        message = self.client.get_info_request_message().decode('utf-8')
        data = json.loads(message)
        LOGGER.debug('Connection made. Transport %s, Sending - %s:%s', transport, data['address'], data['port'])
        transport.sendto(message.encode('utf-8'))
        LOGGER.debug('Waiting for response')
        self.client.info_request_sent()


class ClientResponseUdpProtocol(BaseClientProtocol, asyncio.DatagramProtocol):
    '''
    Protocol which implements listening of info packets from nodes via unicast
    '''
    def connection_made(self, transport):
        self.timeout = reactor.callLater(timeout, self.time_out)

    def datagram_received(self, data, addr):
        LOGGER.debug('Received %s from %s', data, addr)
        node_info = self.client.process_info_response(data)

    def time_out():
        print("Time out")


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
