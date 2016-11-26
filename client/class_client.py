import socket
import asyncio
import json

class Client:
    tcp_address = {
        "host": "127.0.0.1",
        "port": 9999
    }

    def connection_made(self, transport):
        print("Client")
        #self.transport = transport
        #self.transport_request(self.transport)

    def datagram_received(self, data, addr):
        #payload = self.dispatch_message(data)
        print("datagram_received: ", addr)

    def connection_lost(self, exc):
        print('closing transport', exc)
        loop = asyncio.get_event_loop()
        loop.stop()

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
        self.wait_nodes_response()

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

    def wait_nodes_response(self):
        print("Waiting response from nodes...")
        loop = asyncio.get_event_loop()
        task = asyncio.Task(loop.create_datagram_endpoint(Client, local_addr=(self.tcp_address["host"], self.tcp_address["port"])))
        transport, server = loop.run_until_complete(task)
        try:
            loop.run_forever()
        finally:
            transport.close()
        loop.close()


    #client request some objects from maven
    #async def trasport_request():

    #client expects from all servers port and number of links
    #async def discovery_listen():

    #client expects some objects from servers
    #async def transport_listen():
