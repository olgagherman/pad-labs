import logging
from asyncio import Protocol


LOGGER = logging.getLogger(__name__)


class BaseClientProtocol(Protocol):
    '''
    Base client Protocol.

    This base class provides some methods with default implementation.
    `client` is an instance of `client.app.Client` for control of the flow.
    '''
    def __init__(self, client):
        self.client = client

    def error_received(self, exc):
        LOGGER.error('An error was receveied %s', exc)

    def connection_lost(self, exc):
        LOGGER.error('Connection Lost %s', exc)


class ClientRequestUdpProtocol(BaseClientProtocol):
    '''
    Protocol which implements requesting of data from nodes via multicast
    '''
    def connection_made(self, transport):
        message = self.client.get_info_request_message()
        LOGGER.debug('Connection made. Transport %s, Sending - %s', transport, message)
        transport.sendto(message)
        LOGGER.debug('Waiting for response')
        self.client.info_request_sent()


class ClientResponseUdpProtocol(BaseClientProtocol):
    '''
    Protocol which implements listening of info packets from nodes via unicast
    '''
    def datagram_received(self, data, addr):
        LOGGER.debug('Received %s from %s', data, addr)
        self.client.process_info_response(data)

class ClientRequestTcpProtocol(BaseClientProtocol):
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
