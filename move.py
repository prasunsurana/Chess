import pygame

def printstack(gameConfig):

	for row in gameConfig:
		print(row)

	print('\n')

class Move():

	def __init__(self, source, dest):

		self.source = source
		self.dest = dest

	def updateBoard(self, gameConfig, sourceSQ, destSQ):

		# self.playSoundEffect(gameConfig, sourceSQ, destSQ)

		gameConfig[destSQ[0]][destSQ[1]] = gameConfig[sourceSQ[0]][sourceSQ[1]]
		gameConfig[sourceSQ[0]][sourceSQ[1]] = '--'

	# def playSoundEffect(self, gameConfig, sourceSQ, destSQ):

	# 	if gameConfig[sourceSQ[0]][sourceSQ[1]] != '--' and gameConfig[destSQ[0]][destSQ[1]] == '--':
	# 		move.play()
		
	# 	elif gameConfig[sourceSQ[0]][sourceSQ[1]] != '--' and gameConfig[destSQ[0]][destSQ[1]] != '--':
	# 		capture.play()
