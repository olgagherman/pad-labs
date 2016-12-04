import socket
import struct

from .settings import UDP_GROUP_ADDRESS


class UdpMulticastProtocolMixin(object):
    '''
    This mixin provides a method to setup UDP multicast for the transport
    '''
    udp_group_address = UDP_GROUP_ADDRESS # Override this in constructor if needed

    def init_multicast_transport(self, transport):
        sock = transport.get_extra_info('socket')
        group = socket.inet_aton(self.udp_group_address)
        mreq = struct.pack('4sL', group, socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
