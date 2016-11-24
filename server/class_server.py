import asyncio
import json
import socket
import struct
#from run_server import _CONFIG

class Server:
    tcp_address = {
        "host": "127.0.0.1",
        "port": 9999
    }
    udp_address = {
        "host": "239.255.255.1",
        "port": 8888
    }
    neighbor_nodes = {
        "node": {"host": "", "port": ""}
    }

    def connection_made(self, transport):
        print('Connected\n', transport)
        self.transport = transport

    #server expects the client to request port and number of links
    def datagram_received(self, data, addr):
        payload = self.dispatch_message(data)
        print("Received with udp from: ", addr)
        #self.discovery_info()

    #server expects other services to request stored information
    def listen_udp(self):
        print("Connected with udp")
        message = self.get_discovery_message()
        print('Request from client: host "{} and port {}'.format(message.get("host"), message.get("port")))

    def get_discovery_message(self):
        sock = self.run_listener_udp()
        print("Receiving data: ")
        message = self.dispatch_message(sock.recv(10240))
        return message

    def run_listener_udp(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.udp_address["host"], self.udp_address["port"]))
        mreq = struct.pack("4sl", socket.inet_aton(self.udp_address["host"]), socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        return sock

    def dispatch_message(self, data):
        message = json.loads(data.decode('utf-8'))
        if message.get("command") == "discovery":
            payload = message.get("payload")
        else:
            print("Not discovery command")
        return payload
