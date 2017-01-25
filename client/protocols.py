import asyncio
import logging
import json

from core.protocols import UdpMulticastProtocolMixin

LOGGER = logging.getLogger(__name__)
UDP_TRANSPORT = None
TIMEOUT = 5
TIMED_OUT = False

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
        self.client.loop.call_later(TIMEOUT, self.time_out)
        LOGGER.debug('Waiting for response')

    def time_out(self):
        LOGGER.debug("Time out!")
        TIMED_OUT = True
        maven = self.client.info_request_sent()
        if bool(maven):
            loop = asyncio.get_event_loop()
            try:
                task = self.client.run_tcp_server(self.client.udp_address, self.client.udp_port)
                loop.run_until_complete(task)
                loop.run_forever()
            except Exception:
                LOGGER.error("Cannot connect to maven")
        else:
            LOGGER.debug("No response from nodes")



class ClientResponseUdpProtocol(BaseClientProtocol, asyncio.DatagramProtocol):
    '''
    Protocol which implements listening of info packets from nodes via unicast
    '''
    def datagram_received(self, data, addr):
        if TIMED_OUT:
            LOGGER.debug('Too late received %s from %s', data, addr)
        else:
            LOGGER.debug('Received %s from %s', data, addr)
            node_info = self.client.process_info_response(data)


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
