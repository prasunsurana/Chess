from CTkMessagebox import CTkMessagebox
from tkinter import messagebox
import chessboard
from protocols import Protocols
from boardfunctions import *
from client import Client
from tkinter import *
import customtkinter
from sys import exit
from move import *
import pyautogui
import threading
import itertools
import socket
import pygame
import math
import copy
import time
import json
import sys

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class PlayerNameInputGUI():

	def __init__(self):

		""" A class to display an entry GUI to get the player's alias. """

		# Empty alias, integrate Client object to the GUI
		self.alias = ''
		self.client = Client()

		customtkinter.set_appearance_mode('dark')
		customtkinter.set_default_color_theme('dark-blue')

		# Create Tkinter window
		self.root = customtkinter.CTk()
		self.root.title('Chess')
		self.root.geometry('600x100+400+400')

		# Create entry box to get player alias
		self.entry = customtkinter.CTkEntry(self.root,
			placeholder_text='Enter an alias',
			height=100,
			width=500,
			font=('Georgia',25),
			corner_radius=50,
			text_color='#333634',
			placeholder_text_color='#888a89',
			fg_color=('black', '#b3daf2'),
			state='normal'
		)

		# After the user presses the Return key, it triggers the self.clear method.
		self.entry.bind('<Return>', self.clear)
		self.entry.pack(pady=20)

		# If the user closes the window, it triggers the self.terminate method.
		self.root.protocol('WM_DELETE_WINDOW', self.terminate)

		# Start the tkinter mainloop
		self.root.mainloop()


	# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
		
	def clear(self, *args):

		""" Destroys the entry widget, and displays a label to show that it is waiting for the opponent to connect. """

		if self.entry.get():

			# Save the user's entry as the player alias, and delete the entry box
			self.alias = self.entry.get()
			self.entry.destroy()

			time.sleep(0.5)

			# Display 'waiting for opponent' and send alias to server
			self.wait = customtkinter.CTkLabel(self.root, text='Waiting for opponent...', font=('Georgia',30))
			self.wait.pack(pady=30)
			self.client.json_convert_send({Protocols.OPPONENT_ALIAS:self.alias})

			# Listens for opponent's alias from the server
			tag, item = self.client.json_convert_recv()
			if tag == Protocols.OPPONENT_ALIAS:
				self.client.opponent_alias = item

			# Listens for randomized colour for this game from the server
			tag, item = self.client.json_convert_recv()
			if tag == Protocols.COLOUR:
				self.client.colour = item
				self.root.destroy()
				Player(self.client.colour, self.client)

	# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

	def terminate(self):

		""" If the user closes the window, send a disconnect message to the server. """

		self.client.json_convert_send({Protocols.DISCONNECT: None})
		self.client.disconnect()
		exit()



# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class Player:

	""" A class to create the chess game. """

	def __init__(self, colour, client):

		# Default board configuration
		self.gameConfig = [['br', 'bn', 'bb', 'bq', 'bk', 'bb', 'bn', 'br'],
					      ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
					      ['--', '--', '--', '--', '--', '--', '--', '--'],
					      ['--', '--', '--', '--', '--', '--', '--', '--'],
					      ['--', '--', '--', '--', '--', '--', '--', '--'],
					      ['--', '--', '--', '--', '--', '--', '--', '--'],
					      ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
					      ['wr', 'wn', 'wb', 'wq', 'wk', 'wb', 'wn', 'wr']]

		# Initialise basic game information
		self.client = client
		self.alias = self.client.alias
		self.opponent_alias = self.client.opponent_alias
		self.colour = colour
		self.opponent_colour = 'b' if self.colour == 'w' else 'w'
		self.turn = True if self.colour == 'w' else False
		self.king = [7,4] if self.colour =='w' else [7,3]
		self.oppKing = [0,4] if self.colour == 'w' else [0,3]
		self.check = False
		self.oppCheck = False
		self.messageArg = False

		# If the player is black, rotate the board so the black pieces are on their side
		if self.colour == 'b':
			self.rotate_board(self.gameConfig)

		self.kingMoves = kingCheckMoves(self.king, self.colour, self.opponent_colour, self.gameConfig)
		self.pinnedPieces, self.axisSquares = axisCheck(self.king, self.gameConfig, self.colour, self.opponent_colour)


		self.game_active = True
		self.width = 1300
		self.height = 800
		self.moveStack = []

		# Delete alias, opponent alias and colour attributes from the client, as they are now 
		# stored as atrributes in the Player instance
		del self.client.alias 
		del self.client.opponent_alias
		del self.client.colour

		self.moveStack.append(copy.deepcopy(self.gameConfig))
		self.my_latest = copy.deepcopy(self.gameConfig)

		# Start a thread to receive messages from the server
		messageThread = threading.Thread(target=self.client_receive, daemon=True).start()

		self.play_game()

	# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

	def rotate_board(self, board):

		""" Rotate the self.gameConfig 2D array so it can be correctly displayed for each player. """

		for i in range(2):
			board = list(map(list, zip(*board[::-1])))

		self.gameConfig = board

	# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

	def get_opp_king_pos(self, board):

		""" Get the position of the enemy king. """

		for r in range(len(board)):
			for c in range(len(board[r])):
				if board[r][c] == f'{self.opponent_colour}k':
					self.oppKing = [r,c]

	# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

	def client_receive(self):

		""" Receives messages from the server. """

		while True:

			try:

				# Receives messages from the server
				tag, item = self.client.json_convert_recv()

				# If the tag is a new game configuration after the opponent has made the move, save it and rotate the array
				if tag == Protocols.GAMECONFIG or tag == Protocols.CHECK :

					self.rotate_board(item)
					self.moveStack.append(copy.deepcopy(self.gameConfig))
					self.get_opp_king_pos(self.gameConfig)
					self.turn = not self.turn

					# Player is under check
					if tag == Protocols.CHECK:
						self.check = True

					# Check all legal king moves
					self.kingMoves = kingCheckMoves(self.king, self.colour, self.opponent_colour, self.gameConfig)

					# Find all pinned pieces and axes along which there are checks
					self.pinnedPieces, self.axisSquares = axisCheck(self.king, self.gameConfig, self.colour, self.opponent_colour)
					print(f'pins = {self.pinnedPieces}')
					print(f'axis squares = {self.axisSquares}')

					if not self.kingMoves:

						if self.check:

							# add function for no defenders available here, and sending checkmate protocol is conditioned on that
							self.client.json_convert_send({Protocols.CHECKMATE:None})
							self.messageArg = Protocols.CHECKMATE

						else: 

							stalemate = True

							for r in range(len(self.gameConfig)):
								for c in range(len(self.gameConfig[r])):
									if self.gameConfig[r][c][0] == self.colour:
										if checkLegalMoves([r,c], self.colour, self.opponent_colour, self.gameConfig):
											stalemate = False
											break

							if stalemate:
								self.client.json_convert_send({Protocols.STALEMATE:None})
								self.messageArg = Protocols.STALEMATE

					# Opponent escapes from check
					if self.oppCheck:
						self.oppCheck = not self.oppCheck

				elif tag == Protocols.CHECKMATE:
					self.messageArg = Protocols.CHECKMATE

				# If the opponent has left, notify the player and exit the game
				elif tag == Protocols.DISCONNECT:
					self.messageArg = Protocols.DISCONNECT

			except Exception as e:

				print(e)
				self.client.disconnect()
				exit()

	# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

	def display_message(self, tag):

		if tag == Protocols.CHECKMATE:

				msg = messagebox.showinfo(message="Game over by checkmate!", title="Game Over")
				# msg = CTkMessagebox(title='Game Over', message='Game ended by checkmate!', option_1='Close')

		elif tag == Protocols.STALEMATE:

			msg = messagebox.showinfo(message="You drew by stalemate!", title="Game Over")
			# msg = CTkMessagebox(title='Game Over', message='You drew by stalemate!', option_1='Close')

		elif tag == Protocols.DISCONNECT:

			msg = messagebox.showerror(message="Your opponent disconnected", title="Connection Lost")
			# msg = CTkMessagebox(title='Connection Error', message='Your opponent has disconnected!', option_1='Close')

		if msg == 'OK':
				self.client.json_convert_send({Protocols.SHUTDOWN: None})
				msg.destroy()
				exit()

	# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

	def play_game(self):

		""" Start the pygame gameloop. """

		# Initialise the pygame window
		pygame.init()
		screen = pygame.display.set_mode((self.width, self.height))
		pygame.display.set_caption('Chess')
		clock = pygame.time.Clock()

		print(self.colour)

		source, dest = 0, 0

		# Main gameloop
		while True: 

			if self.messageArg:
				self.display_message(self.messageArg)
				break

			for event in pygame.event.get():

				# If the user closes the window, send a disconnect message to the server
				if event.type == pygame.QUIT:
					self.client.json_convert_send({Protocols.DISCONNECT:None})
					pygame.quit()
					exit()

				# If the user clicks the mouse button
				if event.type == pygame.MOUSEBUTTONDOWN:

					# Only enable the movement of a piece of it is the user's turn
					if self.turn:

						# Get coordinates of mouse click
						mouseLoc = pygame.mouse.get_pos()

						# If the player presses the undo button, undo the last move
						if game.undo_rect.collidepoint(mouseLoc):

							if len(self.moveStack) > 1 and not self.turn:

								self.moveStack = self.moveStack[:-1]
								self.gameConfig = self.moveStack[-1]
								self.turn = not self.turn
								idx = (idx + 1) % 2


						# If the user clicked within the boundaries of the board
						if game.topleft[0] <= mouseLoc[0] <= game.bottomright[0] and game.topleft[1] <= mouseLoc[1] <= game.bottomright[1]:
							
							# If the user has clicked a piece for the first time
							if source == 0:
								sourceSQ = calculateSquare(game, mouseLoc)

								# If the user clicked on their own piece, store as the piece to be moved
								if self.gameConfig[sourceSQ[0]][sourceSQ[1]][0] == self.colour:
									source = mouseLoc

								else:
									source, sourceSQ = 0, 0
							
							# If the user had already clicked a piece before, this click is where they want the piece to go
							else:
								dest = mouseLoc
								destSQ = calculateSquare(game, dest)

								# If the user clicks on another piece of the same colour, select this piece instead as the one to be moved
								if self.gameConfig[destSQ[0]][destSQ[1]][0] == self.colour:

									source = mouseLoc
									sourceSQ = destSQ
									dest = 0
									destSQ = 0

								# If the user clicks on a square that is empty or has a black piece:
								else:

									# Generate all legal moves
									if sourceSQ == self.king:
										possible_moves = self.kingMoves
									else:
										possible_moves = checkLegalMoves(sourceSQ, self.colour, self.opponent_colour, self.gameConfig)

									# 1. Legal move, no check, not pinned
									# 2. Legal move, check, not pinned, in axis of pinning
									# 3. Legal move, check, pinned, in axis of pinning

									# Check if the destination square is legal
									if destSQ in possible_moves:

										if self.check:

											print('check...')

											# If there is a double check by the opponent, the player can only move the king
											if len(self.axisSquares) > 1:

												print('double check!!')

												if self.gameConfig[sourceSQ[0]][sourceSQ[1]] == f'{self.colour}k':

													# If moving the king out of check, make self.check False
													self.check = not self.check
													
													# Update king's position
													self.king = destSQ

													# Make the move and update the board, store the latest configuration and send it to the server
													move = Move(sourceSQ, destSQ)
													move.updateBoard(self.gameConfig, sourceSQ, destSQ)
													self.moveStack.append(copy.deepcopy(self.gameConfig))

													oppPinnedPieces, oppAxisSquares = axisCheck(self.oppKing, self.gameConfig, self.opponent_colour, self.colour)

													if oppAxisSquares:
														self.oppCheck = True

													if self.oppCheck:
														self.client.json_convert_send({Protocols.CHECK:self.gameConfig})
													else:
														self.client.json_convert_send({Protocols.GAMECONFIG:self.gameConfig})

													source, dest = 0, 0
													self.check = not self.check
													self.turn = not self.turn

												else:

													source, dest = 0, 0

											# Single check
											else: 

												print('single check...')

												# If piece is moved to any square in the axis of pinning including capturing checking piece
												if any(destSQ in sublist for sublist in self.axisSquares) or sourceSQ == self.king:

													print('we"re in!!')

													# Make the move and update the board and store the latest configuration
													move = Move(sourceSQ, destSQ)
													move.updateBoard(self.gameConfig, sourceSQ, destSQ)
													self.moveStack.append(copy.deepcopy(self.gameConfig))

													# If it was the king being moved, update the king's position
													if sourceSQ == self.king:
														self.king = destSQ

													# Check pinned pieces and axis squares for the opponent's king
													oppPinnedPieces, oppAxisSquares = axisCheck(self.oppKing, self.gameConfig, self.opponent_colour, self.colour)

													# If axis squares list is not empty, it means we checked them, so change the flag to true
													if oppAxisSquares:
														self.oppCheck = True

													# Notify the opponent if they are under check, and send the new board configuration
													if self.oppCheck:
														self.client.json_convert_send({Protocols.CHECK:self.gameConfig})
													else:
														self.client.json_convert_send({Protocols.GAMECONFIG:self.gameConfig})

													source, dest = 0, 0
													self.check = not self.check
													self.turn = not self.turn

												else:

													source, dest = 0, 0

										else:

											if sourceSQ not in self.pinnedPieces or (sourceSQ in self.pinnedPieces and destSQ in pinAxis(sourceSQ, self.king, self.gameConfig, self.colour, self.opponent_colour)):

												# Make the move, update the board and store the latest configuration
												move = Move(sourceSQ, destSQ)
												move.updateBoard(self.gameConfig, sourceSQ, destSQ)
												self.moveStack.append(copy.deepcopy(self.gameConfig))

												# If it was the king being moved, update the king's position
												if sourceSQ == self.king:
													self.king = destSQ

												oppPinnedPieces, oppAxisSquares = axisCheck(self.oppKing, self.gameConfig, self.opponent_colour, self.colour)

												if oppAxisSquares:
													self.oppCheck = True

												# Notify the opponent if they are under check, and send the new board configuration
												if self.oppCheck:
													self.client.json_convert_send({Protocols.CHECK:self.gameConfig})
												else:
													self.client.json_convert_send({Protocols.GAMECONFIG:self.gameConfig})

												source, dest = 0, 0
												self.turn = not self.turn

											else:

												source, dest = 0, 0

									else:

										source, dest = 0, 0


						else: 

							if source != 0:
								source = 0


			if self.game_active:

				game = ChessBoard(screen, self.moveStack[-1], self.my_latest, self.alias, self.opponent_alias, 
								  self.check, list(reversed(self.king)), self.oppCheck, list(reversed(self.oppKing)))
				self.my_latest = copy.deepcopy(self.gameConfig)

			pygame.display.update()
			clock.tick(60)

	# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


PlayerNameInputGUI()




















































