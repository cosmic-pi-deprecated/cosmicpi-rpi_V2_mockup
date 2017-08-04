from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import threading
import time
import json
import random

class SocketHandler(object):
	def __init__(self, socket):
		self._socket = socket

	def run(self):
		while True:
			time.sleep(1)
			
			temperature = random.uniform(20, 30)
			message = json.dumps({'temperature': temperature})
			self._socket.sendMessage(message)
			
			pressure = random.uniform(950, 1100)
			message = json.dumps({'pressure': pressure})
			self._socket.sendMessage(message)
            

class WebSocketHandler(WebSocket):
	def handleMessage(self):
		# self.sendMessage(self.data)
		pass

	def handleConnected(self):
		print(self.address, 'connected')
		
		socket_handler = SocketHandler(socket=self)
		thread = threading.Thread(target=socket_handler.run)
		thread.start()
		
	def handleClose(self):
		print(self.address, 'closed')


server = SimpleWebSocketServer('', 9000, WebSocketHandler)

server.serveforever()


