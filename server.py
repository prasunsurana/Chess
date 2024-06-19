from protocols import Protocols
import threading
import random
import socket
import json
import time

FORMAT = 'utf-8'
BUFFSIZE = 1024
DISCONNECT_MESSAGE = '!DISCONNECT'

class Server:

	def __init__(self, host='localhost', port=6677):

		# Initialise base attributes, establish socket 
		self.host = host
		self.port = port
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.server.bind((self.host, self.port))

		# Lists to keep track of players and their aliases
		self.clients = []
		self.aliases = []

		self.sent_aliases = False
		self.no_clients = 0

	# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

	def handle(self, conn, addr):

		""" Executes different tasks based on messages from clients. """

		print(f'CONNECTED TO {addr}!')

		connected = True

		try:

			while connected:

				# Listen for messages from client
				tag, item = self.json_convert_recv(conn)

				# If the client sends their alias, store the client's socket and alias
				if tag == Protocols.OPPONENT_ALIAS:
					self.clients.append(conn)
					self.aliases.append(item)

				# Once both players have sent their aliases:
				if not self.sent_aliases and len(self.aliases) == 2:

					# Send each player their opponent's alias
					for i in range(len(self.clients)):
						self.json_convert_send({Protocols.OPPONENT_ALIAS:f'{self.aliases[(i+1)%2]}'}, self.clients[i])

					# Randomize colours for each player
					idxw = random.randint(0,1)
					idxb = (idxw + 1) % 2
					colours = {idxw:'w', idxb:'b'}

					# Send each player their colour
					for i in range(len(self.clients)):
						self.json_convert_send({Protocols.COLOUR:colours[i]}, self.clients[i])

					self.sent_aliases = True

				# If a player closes the game, remove them from records and notify the other player
				if tag == Protocols.DISCONNECT:

					try:

						print(tag)

						index = self.clients.index(conn)
						del self.clients[index]
						del self.aliases[index]

						if self.clients:
							self.json_convert_send({Protocols.DISCONNECT:None}, self.clients[0])

						connected = False

					except:

						conn.close()
						self.server.close()
						exit()

				# If a shutdown message is received, close all connections and close the server
				if tag == Protocols.SHUTDOWN:

					index = self.clients.index(conn)
					del self.clients[index]
					del self.aliases[index]

					if self.clients:
						self.json_convert_send({Protocols.DISCONNECT:None}, self.clients[0])

					connected = False


					for client in self.clients:
						client.close()

					self.server.close()
					self.server.shutdown()
					exit()

				if tag == Protocols.GAMECONFIG or tag == Protocols.CHECK or tag == Protocols.CHECKMATE or tag == Protocols.STALEMATE:

					for client in self.clients:
						if client != conn:
							self.json_convert_send({tag:item}, client)

			# Close the connection with a player once while loop has been exited
			conn.close()

		except Exception as e:

			print(e)
			for client in self.clients:
				client.close()

			exit()

	# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

	def json_convert_send(self, message, conn):

		""" Converts a message to JSON format and sends to client. """

		message = json.dumps(message)

		try:
			conn.send(message.encode(FORMAT))
		except Exception as e:
			print(e)

	# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

	def json_convert_recv(self, conn):

		""" Receives a message from a client, converts it from JSON format and returns the message tag and item. """
		message = conn.recv(BUFFSIZE).decode(FORMAT)
		message = json.loads(message)
		tag = next(iter(message.keys()))
		item = next(iter(message.values()))

		return tag, item

	# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

	def receive(self):

		""" Listens for connection with a client and creates a thread to receive messages from them. """

		while True:

			self.server.listen(2)
			conn, addr = self.server.accept()
			self.no_clients += 1
			thread = threading.Thread(target=self.handle, args=(conn,addr,), daemon=True)
			thread.start()


server = Server()
server.receive()