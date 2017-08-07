from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import threading
import json
from EventEmitter import EventEmitter


class SingleClientHandler(WebSocket):
    def sendValue(self, key, value):
        message = json.dumps({ key: value })
        self.sendMessage(message)

    # @override
    def handleMessage(self):
        print('Message received:', self.data)

    # @override
    def handleConnected(self):
        print('New client connected:', self.address)
        self.sendValue('location', {'latitude': 46.2044, 'longitude': 6.1432});

        EventEmitter.get().on_temperature += lambda x: self.sendValue('temperature', x)
        EventEmitter.get().on_pressure += lambda x: self.sendValue('pressure', x)
        EventEmitter.get().on_location += lambda x: self.sendValue('location', x)
        EventEmitter.get().on_combined_event_count += lambda x: self.sendValue('combined_event_count', x)

        # unused
        #EventEmitter.get().on_magnetism += lambda x: self.sendValue('magnetism', x)


    # @override
    def handleClose(self):
        print('Client disconnected:', self.address)


class WebSocketHandler(object):
    def __init__(self, port):
        self._port = port

    def run(self):
        server = SimpleWebSocketServer('', self._port, SingleClientHandler)
        server.serveforever()


class WebSocket(object):
    def async_start(port=9000):
        web_socket_handler = WebSocketHandler(port=port)
        thread = threading.Thread(target=web_socket_handler.run)
        thread.start()

