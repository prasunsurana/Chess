import pygame
import itertools

pygame.font.init()
pygame.mixer.init()
move = pygame.mixer.Sound('ImagesSounds/movesound.mp3')
capture = pygame.mixer.Sound('ImagesSounds/capturesound.mp3')
font = pygame.font.SysFont('Times', 50)
font_opp = pygame.font.SysFont('Times', 50)

class ChessBoard:

	colours = ['#dcd3ea', '#01307a'] # Can also use itertools.cycle

	def __init__(self, screen, gameConfig, prevGameState, alias, opponent, check, kingPosition, oppCheck, oppKingPosition):

		self.width, self.height = screen.get_size()

		self.length = (self.height*0.85)/8
		self.spacing = (self.height - (self.length*8))/2

		rows, columns = len(gameConfig[0]), len(gameConfig)

		for r in range(rows):

			for c in range(columns):
				
				# Draw the chessboard squares with alternating colours
				pygame.draw.rect(screen, self.colours[(r + c) % 2], pygame.Rect(self.spacing + (self.length * r), 
																			self.spacing + (self.length * c), 
																			self.length, 
																			self.length))

				# If the player's king is under check, change the king's square colour to red
				if check and [r,c] == kingPosition:
					pygame.draw.rect(screen, '#f54242', pygame.Rect(self.spacing + (self.length * r), 
																			self.spacing + (self.length * c), 
																			self.length, 
																			self.length))

				# If the opponent's king is under check, change the opponent's king's square colour to red
				if oppCheck and [r,c] == oppKingPosition:
					pygame.draw.rect(screen, '#f54242', pygame.Rect(self.spacing + (self.length * r), 
																			self.spacing + (self.length * c), 
																			self.length, 
																			self.length))

				currentState, prevState = gameConfig[c][r], prevGameState[c][r]
				# if currentState != prevState:
				# 	print(f'DIFFERENCE! {currentState} {prevState}')
				
				# Draw pieces
				if currentState != '--':
					piece = pygame.image.load(f'ImagesSounds/{currentState}.png').convert_alpha()
					piece = pygame.transform.scale(piece, (self.length, self.length))
					screen.blit(piece, pygame.Rect(self.spacing + (self.length * r), 
												   self.spacing + (self.length * c), 
												   self.length, 
												   self.length))

					# Play move sound if moving to an empty square
					if prevState == '--':
						# print(f'move: {currentState}, {prevState}')
						move.play()

					# Play capture sound if capturing a piece
					if prevState != '--' and currentState != prevState:
						# print(f'capture: {currentState}, {prevState}')
						capture.play()


				self.topleft = (self.spacing, self.spacing)
				self.bottomright = (self.spacing + (self.length*8), self.spacing + (self.length * 8))

				# Draw text labels for each player
				nametag = font.render(alias, True, 'white')
				screen.blit(nametag, (200, 600))
				# opponent_nametag = font_opp.render(opponent, True, 'white')
				# screen.blit(opponent_nametag, (200,600))

				# Draw undo button
				undo = pygame.image.load('ImagesSounds/undo.png').convert_alpha()
				undo = pygame.transform.scale(undo, (20,20))
				self.undo_rect = undo.get_rect(topleft = (715, 755))
				screen.blit(undo, self.undo_rect)
