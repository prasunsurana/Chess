from chessboard import ChessBoard
import itertools
import math
import copy

def calculateSquare(game: ChessBoard, coord):

	col = math.floor((coord[0] - game.spacing)/game.length)
	row = math.floor((coord[1] - game.spacing)/game.length)

	return [row, col]

def checkLegalMoves(src, colour, opp_colour, gameConfig):

	if gameConfig[src[0]][src[1]][1] == 'p':

		return legalPawnMoves(src, colour, opp_colour, gameConfig)

	if gameConfig[src[0]][src[1]][1] == 'n':

		return legalKnightMoves(src, colour, opp_colour, gameConfig)

	if gameConfig[src[0]][src[1]][1] == 'b':

		return legalBishopMoves(src, colour, opp_colour, gameConfig)

	if gameConfig[src[0]][src[1]][1] == 'r':

		return legalRookMoves(src, colour, opp_colour, gameConfig)

	if gameConfig[src[0]][src[1]][1] == 'q':

		return (legalBishopMoves(src, colour, opp_colour, gameConfig) + legalRookMoves(src, colour, opp_colour, gameConfig))

	if gameConfig[src[0]][src[1]][1] == 'k':

		return kingCheckMoves(src, colour, opp_colour, gameConfig)

def legalPawnMoves(src, colour, opp_colour, gameConfig):

	possible_moves = []

	if gameConfig[src[0]][src[1]][0] == colour:

		if src[0] > 0: # modify later for pawn promotion!

			if gameConfig[src[0]-1][src[1]] == '--':

				possible_moves.append([src[0]-1, src[1]])

				if src[0] == 6 and gameConfig[src[0]-2][src[1]] == '--':

					possible_moves.append([src[0]-2, src[1]])

			if src[1] > 0 and gameConfig[src[0]-1][src[1]-1][0] == opp_colour:

				possible_moves.append([src[0]-1, src[1]-1])

			if src[1] < len(gameConfig)-1 and gameConfig[src[0]-1][src[1]+1][0] == opp_colour:

				possible_moves.append([src[0]-1, src[1]+1])

	return possible_moves

def legalKnightMoves(src, colour, opp_colour, gameConfig):

	possible_moves = []

	offsets = [-2,-1,1,2]
	directions = list(itertools.product(offsets, repeat=2))
	directions = list(filter(lambda a: abs(a[0]) != abs(a[1]), directions))

	for direction in directions:

		if src[0] + direction[0] < 0 or src[0] + direction[0] >= len(gameConfig) or \
		   src[1] + direction[1] < 0 or src[1] + direction[1] >= len(gameConfig) or \
		   gameConfig[src[0] + direction[0]][src[1] + direction[1]][0] == colour:
		   continue

		else:
			possible_moves.append([src[0] + direction[0], src[1] + direction[1]])

	return possible_moves

def legalBishopMoves(src, colour, opp_colour, gameConfig):

	topright, topleft, bottomleft, bottomright = True, True, True, True
	possible_moves = []

	def diagPathFinder(row, col, rdelta, cdelta, direction, colour, opp_colour):

		if row + rdelta < 0 or row + rdelta >= len(gameConfig) or \
		   col + cdelta < 0 or col + cdelta >= len(gameConfig) or \
		   gameConfig[row + rdelta][col + cdelta][0] == colour:
		   return None

		else:

			if gameConfig[row + rdelta][col + cdelta][0] == opp_colour:
				direction = False

			possible_moves.append([row+rdelta, col+cdelta])

			if direction:
				diagPathFinder(row+rdelta, col+cdelta, rdelta, cdelta, direction, colour, opp_colour)

	directions = [(-1,1, topright),(1,1, bottomright),(1,-1,bottomleft),(-1,-1,topleft)]

	for item in directions:
		orig = copy.deepcopy(src)
		diagPathFinder(orig[0], orig[1], item[0], item[1], item[2], colour, opp_colour)

	return possible_moves

def legalRookMoves(src, colour, opp_colour, gameConfig):

	up, right, down, left = True, True, True, True
	possible_moves = []

	def straightPathFinder(row, col, rdelta, cdelta, direction, colour, opp_colour):

		if row + rdelta < 0 or row + rdelta >= len(gameConfig) or \
		   col + cdelta < 0 or col + cdelta >= len(gameConfig) or \
		   gameConfig[row + rdelta][col + cdelta][0] == colour:
		   return None

		else:

			if gameConfig[row + rdelta][col + cdelta][0] == opp_colour:
				direction = False

			possible_moves.append([row+rdelta, col+cdelta])

			if direction:
				straightPathFinder(row+rdelta, col+cdelta, rdelta, cdelta, direction, colour, opp_colour)

	directions = [(-1,0, up),(0,1, right),(1,0,down),(0,-1,left)]

	for item in directions:
		orig = copy.deepcopy(src)
		straightPathFinder(orig[0], orig[1], item[0], item[1], item[2], colour, opp_colour)

	return possible_moves

def legalKingMoves(src, colour, opp_colour, gameConfig):

	possible_moves = []

	offsets = [-1, 0, 1]
	directions = list(itertools.product(offsets, repeat=2))
	
	for direction in directions:

		if src[0] + direction[0] < 0 or src[0] + direction[0] >= len(gameConfig) or \
		   src[1] + direction[1] < 0 or src[1] + direction[1] >= len(gameConfig) or \
		   gameConfig[src[0] + direction[0]][src[1] + direction[1]][0] == colour:
		   continue

		else:
			possible_moves.append([src[0] + direction[0], src[1] + direction[1]])


	return possible_moves

def kingCheckMoves(src, colour, opp_colour, gameConfig):

	possible_moves = []

	offsets = [-1, 0, 1]
	directions = list(itertools.product(offsets, repeat=2))

	def pawnCheck(centre, colour, opp_colour, gameConfig):

		if centre[0] > 0 and centre[1] > 0 and gameConfig[centre[0]-1][centre[1]-1] == f'{opp_colour}p':

			return True

		elif centre[0] > 0 and centre[1] < len(gameConfig)-1 and gameConfig[centre[0]-1][centre[1]+1] == f'{opp_colour}p':

			return True

		else: 

			return False

	def knightCheck(centre, colour, opp_colour, gameConfig):

		offsets = [-2,-1,1,2]
		leaps = list(itertools.product(offsets, repeat=2))
		leaps = list(filter(lambda a: abs(a[0]) != abs(a[1]), leaps))

		for leap in leaps:

			if centre[0] + leap[0] < 0 or centre[0] + leap[0] >= len(gameConfig) or \
			   centre[1] + leap[1] < 0 or centre[1] + leap[1] >= len(gameConfig) or \
			   gameConfig[centre[0] + leap[0]][centre[1] + leap[1]][0] == colour:
			   continue

			elif gameConfig[centre[0] + leap[0]][centre[1] + leap[1]] == f'{opp_colour}n':

				return True

		return False

	def diagonalCheck(centre, colour, opp_colour, gameConfig):

		topright, topleft, bottomleft, bottomright = True, True, True, True

		def diagPathFinder(row, col, rdelta, cdelta, direction, colour, opp_colour):

			if row + rdelta < 0 or row + rdelta >= len(gameConfig) or \
			   col + cdelta < 0 or col + cdelta >= len(gameConfig) or \
			   (gameConfig[row + rdelta][col + cdelta][0] == colour and \
			   gameConfig[row + rdelta][col + cdelta][1] != 'k'):
			   return False

			else:

				if gameConfig[row + rdelta][col + cdelta] == f'{opp_colour}q' or \
				   gameConfig[row + rdelta][col + cdelta] == f'{opp_colour}b':
					return True

				elif gameConfig[row + rdelta][col + cdelta] == '--' or gameConfig[row + rdelta][col + cdelta] == f'{colour}k':
					return diagPathFinder(row+rdelta, col+cdelta, rdelta, cdelta, direction, colour, opp_colour)

				else:
					return False

		directions = [(-1,1, topright),(1,1, bottomright),(1,-1,bottomleft),(-1,-1,topleft)]

		for item in directions:
			orig = copy.deepcopy(centre)
			if diagPathFinder(orig[0], orig[1], item[0], item[1], item[2], colour, opp_colour):
				return True

		return False

	def straightCheck(centre, colour, opp_colour, gameConfig):

		up, right, down, left = True, True, True, True

		def straightPathFinder(row, col, rdelta, cdelta, direction, colour, opp_colour):

			if row + rdelta < 0 or row + rdelta >= len(gameConfig) or \
			   col + cdelta < 0 or col + cdelta >= len(gameConfig) or \
			   (gameConfig[row + rdelta][col + cdelta][0] == colour and \
			   	gameConfig[row + rdelta][col + cdelta][1] != 'k'):
				return False

			else:

				if gameConfig[row + rdelta][col + cdelta] == f'{opp_colour}q' or \
				   gameConfig[row + rdelta][col + cdelta] == f'{opp_colour}r':
					return True

				elif gameConfig[row + rdelta][col + cdelta] == '--' or gameConfig[row + rdelta][col + cdelta] == f'{colour}k':
					return straightPathFinder(row+rdelta, col+cdelta, rdelta, cdelta, direction, colour, opp_colour)

				else: 
					return False

		directions = [(-1,0, up),(0,1, right),(1,0,down),(0,-1,left)]

		for item in directions:
			orig = copy.deepcopy(centre)
			if straightPathFinder(orig[0], orig[1], item[0], item[1], item[2], colour, opp_colour):
				return True

		return False

	def kingClash(centre, colour, opp_colour, gameConfig):

		offsets = [-1, 0, 1]
		directions = list(itertools.product(offsets, repeat=2))

		for direction in directions:

			if centre[0] + direction[0] < 0 or centre[0] + direction[0] >= len(gameConfig) or \
			   centre[1] + direction[1] < 0 or centre[1] + direction[1] >= len(gameConfig) or \
			   gameConfig[centre[0] + direction[0]][centre[1] + direction[1]][0] == colour:
			   continue

			else: 

				if gameConfig[centre[0] + direction[0]][centre[1] + direction[1]] == f'{opp_colour}k':
					return True

				else: continue

		return False


	for direction in directions:

		if src[0] + direction[0] < 0 or src[0] + direction[0] >= len(gameConfig) or \
		   src[1] + direction[1] < 0 or src[1] + direction[1] >= len(gameConfig) or \
		   gameConfig[src[0] + direction[0]][src[1] + direction[1]][0] == colour:
		   continue

		else:

			centre = [src[0] + direction[0], src[1] + direction[1]]

			if not pawnCheck(centre, colour, opp_colour, gameConfig) and \
			   not knightCheck(centre, colour, opp_colour, gameConfig) and \
			   not diagonalCheck(centre, colour, opp_colour, gameConfig) and \
			   not straightCheck(centre, colour, opp_colour, gameConfig) and \
			   not kingClash(centre, colour, opp_colour, gameConfig):
			   possible_moves.append(centre)

	print(f'Possible king moves: {possible_moves}')
	return possible_moves

def isPinned(src, colour, opp_colour, gameConfig, kingPos):

	axis = [src[0] - kingPos[0], src[1] - kingPos[1]]

	print(f'Axis = {axis}')

	if abs(axis[0]) == abs(axis[1]):
		axis[0] = int(axis[0]/abs(axis[0]))
		axis[1] = int(axis[1]/abs(axis[1]))

	elif abs(axis[0]) == 0:
		axis[1] = int(axis[1]/abs(axis[1]))

	elif abs(axis[1]) == 0:
		axis[0] = int(axis[0]/abs(axis[0]))

	else:
		return False

	print(f'Normalised Axis = {axis}')

	def checkPinned(src, row, col, rdelta, cdelta, colour, opp_colour, gameConfig):

		print('\n')
		print('------------')
		print(f'Coords = {row},{col}')
		print(f'Exploring: {row + rdelta},{col+cdelta}')
		print('------------')

		if row + rdelta < 0 or row + rdelta >= len(gameConfig) or \
		   col + cdelta < 0 or col + cdelta >= len(gameConfig):
		   return False

		print(f'Piece = {gameConfig[row+rdelta][col+cdelta]}')

		if [row + rdelta, col + cdelta] == src:
			print('skipping...')
			return checkPinned(src, row+rdelta, col+cdelta, rdelta, cdelta, colour, opp_colour, gameConfig)

		else:

			if gameConfig[row + rdelta][col + cdelta][0] == colour:
				print('bumped into your own piece!')
				return False

			elif gameConfig[row + rdelta][col + cdelta][0] == opp_colour:

				if abs(rdelta) == abs(cdelta) and (\
					gameConfig[row + rdelta][col + cdelta][1] == 'q' or \
					gameConfig[row + rdelta][col + cdelta][1] == 'b'):
					print('diagonal check!')
					return True

				elif (rdelta == 0 or cdelta) == 0 and (\
					gameConfig[row + rdelta][col + cdelta][1] == 'q' or \
					gameConfig[row + rdelta][col + cdelta][1] == 'r'):
					print('straight check!')
					return True

				else: return False

			else:

				return checkPinned(src, row+rdelta, col+cdelta, rdelta, cdelta, colour, opp_colour, gameConfig)

	return checkPinned(src, kingPos[0], kingPos[1], axis[0], axis[1], colour, opp_colour, gameConfig)

def axisCheck(kingPos, gameConfig, colour, opp_colour):

	""" Find all pinned pieces and checks. If it returns multiple axes lists inside the totalAxisSquares list,
	we know that there is a double check on the king, and thus the only eligible move is for the king to move.
	If it is a single check, we can either move the king, or block the check with another piece. If a piece is 
	pinned, we cannot move it, unless it is in the same axis in which the king is being checked. """

	directions = [[-1,0], [-1,1], [0,1], [1,1], [1,0], [1,-1], [0,1], [-1,-1]]
	totalAxisSquares = []
	pinnedPieces = []

	for direction in directions:

		axisSquares = []
		dirCopy = copy.deepcopy(direction)
		pinExists = False

		while True:

			# Check if square is out of bounds. If it is, and a pin exists, delete the previous pinned piece
			if kingPos[0] + direction[0] < 0 or kingPos[0] + direction[0] >= len(gameConfig) or \
		   	   kingPos[1] + direction[1] < 0 or kingPos[1] + direction[1] >= len(gameConfig):
		   	   
		   	   if pinExists:
		   	   	del pinnedPieces[-1]

		   	   break

			piece = gameConfig[kingPos[0] + direction[0]][kingPos[1] + direction[1]]

			# If along a diagonal axis
			if abs(direction[0]) == abs(direction[1]):

		   		# If player's own piece
				if piece[0] == colour:

		   			if not pinExists:

		   				# If no pin exists yet, add piece to the list of pinned pieces
		   				pinnedPieces.append([kingPos[0] + direction[0], kingPos[1] + direction[1]])
		   				pinExists = True

		   				# Update to next square
		   				direction[0] += dirCopy[0]
		   				direction[1] += dirCopy[1]

		   			else:

		   				# If there's already a pinned, means neither piece is pinned, so delete the last pin
		   				del pinnedPieces[-1]
		   				break


		   		# If opponent's piece
				elif piece[0] == opp_colour:

		   			# If it is a queen, bishop or a pawn in the diagonal axis
		   			if piece[1] == 'q' or piece[1] == 'b' or (piece[1] == 'p' and abs(direction[0]) == 1):

		   				# If there are no pieces in the way blocking the check, add to the axis list and return
		   				if not pinExists:
				   			axisSquares.append([kingPos[0] + direction[0], kingPos[1] + direction[1]])
				   			totalAxisSquares.append(axisSquares)
			   		
			   		break

			   	# If blank square
				elif piece == '--':

		   			# If there is no pin, add to the list of axis squares
		   			if not pinExists:
		   				axisSquares.append([kingPos[0] + direction[0], kingPos[1] + direction[1]])

		   			# Update to next square
		   			direction[0] += dirCopy[0]
		   			direction[1] += dirCopy[1]

		   	# Along straight axes
			else:

				if piece[0] == colour:

		   			if not pinExists:

		   				pinnedPieces.append([kingPos[0] + direction[0], kingPos[1] + direction[1]])
		   				pinExists = True

		   				direction[0] += dirCopy[0]
		   				direction[1] += dirCopy[1]

		   			else:

		   				del pinnedPieces[-1]
		   				break

				elif piece[0] == opp_colour:

		   			# If it is a queen or a rook in the straight axis
		   			if piece[1] == 'q' or piece[1] == 'r':

		   				if not pinExists:
				   			axisSquares.append([kingPos[0] + direction[0], kingPos[1] + direction[1]])
				   			totalAxisSquares.append(axisSquares)

				   	else:

				   		if pinExists:
				   			del pinnedPieces[-1]
			   		
			   		break

				elif piece == '--':

		   			if not pinExists:
		   				axisSquares.append([kingPos[0] + direction[0], kingPos[1] + direction[1]])

		   			direction[0] += dirCopy[0]
		   			direction[1] += dirCopy[1]


	leaps = [[-2,1], [-1,2], [1,2], [2,1], [2,-1], [1,-2], [-1,-2], [-2,-1]]

	# Check all potential checks by knights
	for leap in leaps:

		if kingPos[0] + leap[0] < 0 or kingPos[0] + leap[0] >= len(gameConfig) or \
	   	   kingPos[1] + leap[1] < 0 or kingPos[1] + leap[1] >= len(gameConfig):
	   	   continue

		if gameConfig[kingPos[0] + leap[0]][kingPos[1] + leap[1]] == f'{opp_colour}n':
			totalAxisSquares.append([kingPos[0] + leap[0], kingPos[1] + leap[1]])

	return pinnedPieces, totalAxisSquares

def pinAxis(src, kingPos, gameConfig, colour, opp_colour):

	""" Finds all squares that a pinned piece is able to move, i.e. along the axis in which the king would 
	otherwise be checked if the pinned piece was not in the way. """

	axis = [src[0] - kingPos[0], src[1] - kingPos[1]]

	if abs(axis[0]) == abs(axis[1]):
		axis[0] = int(axis[0]/abs(axis[0]))
		axis[1] = int(axis[1]/abs(axis[1]))

	elif abs(axis[0]) == 0:
		axis[1] = int(axis[1]/abs(axis[1]))

	elif abs(axis[1]) == 0:
		axis[0] = int(axis[0]/abs(axis[0]))

	axisSquares = []

	axisCopy = copy.deepcopy(axis)

	while True:

		if gameConfig[kingPos[0] + axis[0]][kingPos[1] + axis[1]][0] == opp_colour:
			axisSquares.append([kingPos[0] + axis[0], kingPos[1] + axis[1]])
			return axisSquares

		else:
			axisSquares.append([kingPos[0] + axis[0], kingPos[1] + axis[1]])
			axis[0] += axisCopy[0]
			axis[1] += axisCopy[1]





def checkBlockers(kingPos, gameConfig, axis, colour, opp_colour):

	def pawnBlocker(square, gameConfig, colour, opp_colour):

		# If the square in the axis is empty
		if gameConfig[square[0]][square[1]] == '--':

			# If there is a pawn 1 or 2 spaces behind that can block the check
			if (square[0] < len(gameConfig)-1 and gameConfig[square[0]+1][square[1]]) == f'{colour}p' or (square[0] == 4 and gameConfig[square[0]+2][square[1]] == f'{colour}p'):

				return True

		# If the pawn is able to capture the checking piece
		elif gameConfig[square[0]][square[1]][0] == opp_colour:

			if (square[0] < len(gameConfig) and square[1] > 0 and gameConfig[square[0]+1][square[1]-1] == f'{colour}p') or (square[0] < len(gameConfig) and square[1] < len(gameConfig)-1 and gameConfig[square[0]+1][square[1]+1] == f'{colour}p'):

				return True

		return False

	def knightBlocker(square, gameConfig, colour, opp_colour):

		offsets = [-2,-1,1,2]
		directions = list(itertools.product(offsets, repeat=2))
		directions = list(filter(lambda a: abs(a[0]) != abs(a[1]), directions))

		for direction in directions:

			if square[0] + direction[0] < 0 or square[0] + direction[0] >= len(gameConfig) or \
			   square[1] + direction[1] < 0 or square[1] + direction[1] >= len(gameConfig):
			   continue

			elif gameConfig[square[0] + direction[0]][square[1] + direction[1]] == f'{colour}n':

				return True

		return False

	def diagBlocker(square, gameConfig, colour, opp_colour):

		directions = [[-1,1], [1,1], [1,-1], [-1,-1]]

		def diagPathFinder(square, direction, gameConfig, colour, opp_colour):

			if square[0] + direction[0] < 0 or square[0] + direction[0] >=len(gameConfig) or \
			   square[1] + direction[1] < 0 or square[1] + direction[1] >=len(gameConfig) or \
			   gameConfig[square[0] + direction[0]][square[1] + direction[1]][0] == opp_colour:
			   return False

			else:

				if gameConfig[square[0] + direction[0]][square[1] + direction[1]] == f'{colour}q' or \
				   gameConfig[square[0] + direction[0]][square[1] + direction[1]] == f'{colour}b':

					return True

				elif gameConfig[square[0] + direction[0]][square[1] + direction[1]] == '--':

					return diagPathFinder([square[0] + direction[0],square[1] + direction[1]], direction, gameConfig, colour, opp_colour)

				else:

					return False

		for direction in directions:
			orig = copy.deepcopy(square)
			if diagPathFinder(orig, direction, gameConfig, colour, opp_colour):
				return True

		return False

	def straightBlocker(square, gameConfig, colour, opp_colour):

		directions = [[-1,0], [1,0], [0,-1], [0,1]]

		def straightPathFinder(square, direction, gameConfig, colour, opp_colour):

			if square[0] + direction[0] < 0 or square[0] + direction[0] >=len(gameConfig) or \
			   square[1] + direction[1] < 0 or square[1] + direction[1] >=len(gameConfig) or \
			   gameConfig[square[0] + direction[0]][square[1] + direction[1]][0] == opp_colour:
			   return False

			else:

				if gameConfig[square[0] + direction[0]][square[1] + direction[1]] == f'{colour}q' or \
				   gameConfig[square[0] + direction[0]][square[1] + direction[1]] == f'{colour}r':

					return True

				elif gameConfig[square[0] + direction[0]][square[1] + direction[1]] == '--':

					return straightPathFinder([square[0] + direction[0],square[1] + direction[1]], direction, gameConfig, colour, opp_colour)

				else:

					return False

		for direction in directions:
			orig = copy.deepcopy(square)
			if straightPathFinder(orig, direction, gameConfig, colour, opp_colour):
				return True

		return False

	for square in axis:

		if pawnBlocker(square, gameConfig, colour, opp_colour) or knightBlocker(square, gameConfig, colour, opp_colour) or \
		   diagBlocker(square, gameConfig, colour, opp_colour) or straightBlocker(square, gameConfig, colour, opp_colour):
		   return True

	return False
