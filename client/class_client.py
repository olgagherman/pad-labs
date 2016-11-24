import socket
import asyncio
import json

class Client:
    tcp_address = {
        "host": "127.0.0.1",
        "port": 9999
    }
    udp_address = {
        "host": "239.255.255.1",
        "port": 8888
    }

    def connection_made(self, transport):
        self.transport = transport
        self.transport_request(self.transport)

    #client request to all servers port and number of links
    def transport_request(self, transport):
        message = {
            "command": "discovery",
            "payload": self.tcp_address
        }
        jsonMessage = json.dumps(message).encode('utf-8')
        print('Sending address "{}" and port "{}"'.format(self.tcp_address["host"], self.tcp_address["port"]))
        self.transport.sendto(jsonMessage)

    def discovery_request(self):
        message = self.prepare_discovery_message()
        self.send_discovery(message)
        print("Sent discovery request")

    def send_discovery(self, message):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        print("Sending message")
        sock.sendto(message, (self.udp_address["host"], self.udp_address["port"]))

    def prepare_discovery_message(self):
        message = {
            "command": "discovery",
            "payload": self.tcp_address
        }
        jsonMessage = json.dumps(message).encode('utf-8')
        return jsonMessage

    #client request some objects from maven
    #async def trasport_request():

    #client expects from all servers port and number of links
    #async def discovery_listen():

    #client expects some objects from servers
    #async def transport_listen():
