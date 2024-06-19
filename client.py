from protocols import Protocols
import socket
import json

BUFFSIZE = 1024
FORMAT = 'utf-8'

class Client:

	def __init__(self):

		self.host = 'localhost'
		self.port = 6677
		self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.clientsocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
		self.clientsocket.connect((self.host, self.port))
		self.colour = ''
		self.alias = ''
		self.opponent_alias = ''

	def disconnect(self):
		self.clientsocket.close()


	def json_convert_send(self, message):

		message = json.dumps(message)

		try:
			self.clientsocket.send(message.encode(FORMAT))

		except Exception as e:
			print(e)


	def json_convert_recv(self):

		message = self.clientsocket.recv(BUFFSIZE).decode(FORMAT)
		message = json.loads(message)
		tag = next(iter(message.keys()))
		item = next(iter(message.values()))
		
		return tag, item

