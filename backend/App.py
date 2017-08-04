from StaticContentServer import StaticContentServer
from DummyDataGenerator import DummyDataGenerator
from WebSocket import WebSocket
from Constants import Constants

StaticContentServer.async_start(port=Constants.static_content_port)
WebSocket.async_start(port=Constants.web_socket_port)

DummyDataGenerator.async_start()

