from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import threading
import json
from EventEmitter import EventEmitter


class SingleClientHandler(WebSocket):
    def sendDataValue(self, key, value):
        message = json.dumps({'data': { key: value }})
        self.sendMessage(message)

    def sendControlValue(self, key, value):
        message = json.dumps({'control': { key: value }})
        self.sendMessage(message)

    # @override
    def handleMessage(self):
        print('Message received:', self.data)

    # @override
    def handleConnected(self):
        print('New client connected:', self.address)
        EventEmitter.get().on_temperature += lambda x: self.sendDataValue('temperature', x)
        EventEmitter.get().on_pressure += lambda x: self.sendDataValue('pressure', x)

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

