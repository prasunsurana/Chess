from chessboard import ChessBoard
import itertools
import math
import copy

def calculateSquare(game: ChessBoard, coord):

	""" Calculates the indices for the board squares based on the location of the mouse click. """

	col = math.floor((coord[0] - game.spacing)/game.length)
	row = math.floor((coord[1] - game.spacing)/game.length)

	return [row, col]



def checkLegalMoves(src, colour, opp_colour, gameConfig):

	piece = gameConfig[src[0]][src[1]][1]

	if piece == 'p':

		return legalPawnMoves(src, colour, opp_colour, gameConfig)

	if piece == 'n':

		return legalKnightMoves(src, colour, opp_colour, gameConfig)

	if piece == 'b':

		return legalBishopMoves(src, colour, opp_colour, gameConfig)

	if piece == 'r':

		return legalRookMoves(src, colour, opp_colour, gameConfig)

	if piece == 'q':

		return (legalBishopMoves(src, colour, opp_colour, gameConfig) + legalRookMoves(src, colour, opp_colour, gameConfig))

	if piece == 'k':

		return kingCheckMoves(src, colour, opp_colour, gameConfig)



def legalPawnMoves(src, colour, opp_colour, gameConfig):

	""" Calculates all legal pawn moves, including 1 or 2 steps forward, or capturing diagonally. """

	x, y = src[0], src[1]
	possible_moves = []

	# If the player's piece
	if gameConfig[x][y][0] == colour:

		if x > 0: # modify later for pawn promotion!

			# If the square in front of the pawn is unoccupied
			if gameConfig[x-1][y] == '--':

				possible_moves.append([x-1, y])

				# If the pawn is on the 6th rank and the front 2 squares are unoccupied, it is able to move 2 squares
				if x == 6 and gameConfig[x-2][y] == '--':

					possible_moves.append([x-2, y])

			# If there is an enemy pawn diagonally to the left, it can be captured
			if y > 0 and gameConfig[x-1][y-1][0] == opp_colour:

				possible_moves.append([x-1, y-1])

			# If there is an enemy pawn diagonally to the right, it can be captured
			if y < len(gameConfig)-1 and gameConfig[x-1][y+1][0] == opp_colour:

				possible_moves.append([x-1, y+1])

	return possible_moves



def legalKnightMoves(src, colour, opp_colour, gameConfig):

	possible_moves = []

	# All combinations of coordinates a knight can move to
	offsets = [-2,-1,1,2]
	directions = list(itertools.product(offsets, repeat=2))
	directions = list(filter(lambda a: abs(a[0]) != abs(a[1]), directions))

	for direction in directions:

		x, y = src[0] + direction[0], src[1] + direction[1]

		# If the square is out of bounds or occupied by the player's own piece, the knight cannot move there
		if x < 0 or x >= len(gameConfig) or \
		   y < 0 or y >= len(gameConfig) or \
		   gameConfig[x][y][0] == colour:
		   continue

		else:
			possible_moves.append([x, y])

	return possible_moves



def legalBishopMoves(src, colour, opp_colour, gameConfig):

	possible_moves = []

	def diagPathFinder(row, col, rdelta, cdelta, direction, colour, opp_colour):

		""" Recursive function to find moves in each diagonal. """

		x, y = row + rdelta, col + cdelta

		# If the square is out of bounds or occupied by the player's own piece, the bishop or queen cannot move there
		if x < 0 or x >= len(gameConfig) or \
		   y < 0 or y >= len(gameConfig) or \
		   gameConfig[x][y][0] == colour:
		   return None

		else:

			# If the square is occupied by an enemy piece, the bishop or queencan capture it
			if gameConfig[x][y][0] == opp_colour:
				direction = False

			possible_moves.append([x, y])

			# If there is no enemy piece in the way, look at the next square in the diagonal
			if direction:
				diagPathFinder(x, y, rdelta, cdelta, direction, colour, opp_colour)

	directions = [(-1,1),(1,1),(1,-1),(-1,-1)]

	# Explore each diagonal from the bishops's or queen's position
	for item in directions:
		orig = copy.deepcopy(src)
		diagPathFinder(orig[0], orig[1], item[0], item[1], item[2], colour, opp_colour)

	return possible_moves



def legalRookMoves(src, colour, opp_colour, gameConfig):

	possible_moves = []

	def straightPathFinder(row, col, rdelta, cdelta, direction, colour, opp_colour):

		""" Recursive function to find  moves in each rank or file. """

		x, y = row + rdelta, col + cdelta

		if x < 0 or x >= len(gameConfig) or \
		   y < 0 or y >= len(gameConfig) or \
		   gameConfig[x][y][0] == colour:
		   return None

		else:

			# If the square is occupied by an enemy piece, the rook or queen can capture it
			if gameConfig[x][y][0] == opp_colour:
				direction = False

			possible_moves.append([x, y])

			# If there is no enemy piece in the way, look at the next square in the rank or file
			if direction:
				straightPathFinder(x, y, rdelta, cdelta, direction, colour, opp_colour)

	directions = [(-1,0),(0,1),(1,0),(0,-1)]

	# Explore each diagonal from the bishops's or queen's position
	for item in directions:
		orig = copy.deepcopy(src)
		straightPathFinder(orig[0], orig[1], item[0], item[1], item[2], colour, opp_colour)

	return possible_moves



def legalKingMoves(src, colour, opp_colour, gameConfig):

	possible_moves = []

	# All combinations of coordinates a king can move to
	offsets = [-1, 0, 1]
	directions = list(itertools.product(offsets, repeat=2))
	
	for direction in directions:

		x, y = src[0] + direction[0], src[1] + direction[1]

		# If out of bounds or square contains player's own piece, ignore
		if x < 0 or x >= len(gameConfig) or \
		   y < 0 or y >= len(gameConfig) or \
		   gameConfig[x][y][0] == colour:
		   continue

		# Otherwise, append to the list of possible moves
		else:
			possible_moves.append([x, y])


	return possible_moves



def kingCheckMoves(src, colour, opp_colour, gameConfig):

	""" Checks all squares that the king can move to, filtering out those that are attacked by enemy pieces. """

	possible_moves = []

	# All possible combination of coordinates the king can move to
	offsets = [-1, 0, 1]
	directions = list(itertools.product(offsets, repeat=2))


	def pawnCheck(centre, colour, opp_colour, gameConfig):

		x, y = centre

		# If the square is being attacked diagonally by a pawn from the left
		if x > 0 and y > 0 and gameConfig[x-1][y-1] == f'{opp_colour}p':

			return True

		# If the square is being attacked diagonally by a pawn from the left
		elif x > 0 and y < len(gameConfig)-1 and gameConfig[x-1][y+1] == f'{opp_colour}p':

			return True

		else: 

			return False

	def knightCheck(centre, colour, opp_colour, gameConfig):

		# All combinations of coordinates that the knight can move to
		offsets = [-2,-1,1,2]
		leaps = list(itertools.product(offsets, repeat=2))
		leaps = list(filter(lambda a: abs(a[0]) != abs(a[1]), leaps))

		for leap in leaps:

			x, y = centre[0] + leap[0], centre[1] + leap[1]

			# If the square is out of bounds or occupied by player's own piece, ignore
			if x < 0 or x >= len(gameConfig) or \
			   y < 0 or y >= len(gameConfig) or \
			   gameConfig[x][y][0] == colour:
			   continue

			# If the square is occupied by an enemy knight
			elif gameConfig[x][y] == f'{opp_colour}n':

				return True

		return False



	def diagonalCheck(centre, colour, opp_colour, gameConfig):

		def diagPathFinder(row, col, rdelta, cdelta, direction, colour, opp_colour):

			x, y = row + rdelta, col + cdelta

			# If the square is out of bounds or player's own piece, end search in that direction
			if x < 0 or x >= len(gameConfig) or \
			   y < 0 or y >= len(gameConfig) or \
			   (gameConfig[x][y][0] == colour and \
			   gameConfig[x][y][1] != 'k'):
			   return False

			else:

				# If the square is occupied by an enemy queen or bishop, the king cannot move into that diagonal
				if gameConfig[x][y] == f'{opp_colour}q' or \
				   gameConfig[x][y] == f'{opp_colour}b':
					return True

				# If the piece is blank or is occupied by our own king, continue searching
				elif gameConfig[x][y] == '--' or gameConfig[x][y] == f'{colour}k':
					return diagPathFinder(x, y, rdelta, cdelta, direction, colour, opp_colour)

				else:
					return False

		directions = [(-1,1),(1,1),(1,-1),(-1,-1)]

		for item in directions:
			orig = copy.deepcopy(centre)
			if diagPathFinder(orig[0], orig[1], item[0], item[1], item[2], colour, opp_colour):
				return True

		return False



	def straightCheck(centre, colour, opp_colour, gameConfig):

		def straightPathFinder(row, col, rdelta, cdelta, direction, colour, opp_colour):

			x, y = row + rdelta, col + cdelta

			# If the square is out of bounds or player's own piece, end search in that direction
			if x < 0 or x >= len(gameConfig) or \
			   y < 0 or y >= len(gameConfig) or \
			   (gameConfig[x][y][0] == colour and \
			   	gameConfig[x][y][1] != 'k'):
				return False

			else:

				# If the square is occupied by an enemy queen or rook, the king cannot move into that rank or file
				if gameConfig[x][y] == f'{opp_colour}q' or \
				   gameConfig[x][y] == f'{opp_colour}r':
					return True

				# If the piece is blank or is occupied by our own king, continue searching
				elif gameConfig[x][y] == '--' or gameConfig[x][y] == f'{colour}k':
					return straightPathFinder(x, y, rdelta, cdelta, direction, colour, opp_colour)

				else: 
					return False

		directions = [(-1,0),(0,1),(1,0),(0,-1)]

		for item in directions:
			orig = copy.deepcopy(centre)
			if straightPathFinder(orig[0], orig[1], item[0], item[1], item[2], colour, opp_colour):
				return True

		return False



	def kingClash(centre, colour, opp_colour, gameConfig):

		offsets = [-1, 0, 1]
		directions = list(itertools.product(offsets, repeat=2))

		for direction in directions:

			x, y = centre[0] + direction[0], centre[1] + direction[1]

			# If the square is out of bounds or the square is occupied by our own piece, ignore
			if x < 0 or x >= len(gameConfig) or \
			   y < 0 or y >= len(gameConfig) or \
			   gameConfig[x][y][0] == colour:
			   continue

			else: 

				# If the square contains the enemy king, the king cannot move next to it
				if gameConfig[x][y] == f'{opp_colour}k':
					return True

				else: continue

		return False



	for direction in directions:

		x, y = src[0] + direction[0], src[1] + direction[1]

		if x < 0 or x >= len(gameConfig) or \
		  y < 0 or y >= len(gameConfig) or \
		   gameConfig[x][y][0] == colour:
		   continue

		else:

			centre = [x, y]

			# If the square is not being checked by any of the enemy pieces, it is safe for the king to move there
			if not pawnCheck(centre, colour, opp_colour, gameConfig) and \
			   not knightCheck(centre, colour, opp_colour, gameConfig) and \
			   not diagonalCheck(centre, colour, opp_colour, gameConfig) and \
			   not straightCheck(centre, colour, opp_colour, gameConfig) and \
			   not kingClash(centre, colour, opp_colour, gameConfig):
			   possible_moves.append(centre)

	return possible_moves



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

			x, y = kingPos[0] + direction[0], kingPos[1] + direction[1]

			# Check if square is out of bounds. If it is, and a pin exists, delete the previous pinned piece
			if x < 0 or x >= len(gameConfig) or \
		   	   y < 0 or y >= len(gameConfig):
		   	   
		   	   if pinExists:
		   	   	del pinnedPieces[-1]

		   	   break

			piece = gameConfig[x][y]

			# If along a diagonal axis
			if abs(direction[0]) == abs(direction[1]):

		   		# If player's own piece
				if piece[0] == colour:

		   			if not pinExists:

		   				# If no pin exists yet, add piece to the list of pinned pieces
		   				pinnedPieces.append([x, y])
		   				pinExists = True

		   				# Update to next square
		   				direction[0] += dirCopy[0]
		   				direction[1] += dirCopy[1]

		   			else:

		   				# If there's already a pin, means neither piece is pinned, so delete the last pin
		   				del pinnedPieces[-1]
		   				break


		   		# If opponent's piece
				elif piece[0] == opp_colour:

		   			# If it is a queen, bishop or a pawn in the diagonal axis
		   			if piece[1] == 'q' or piece[1] == 'b' or (piece[1] == 'p' and abs(direction[0]) == 1):

		   				# If there are no pieces in the way blocking the check, add to the axis list and return
		   				if not pinExists:
				   			axisSquares.append([x, y])
				   			totalAxisSquares.append(axisSquares)
			   		
			   		break

			   	# If blank square
				elif piece == '--':

		   			# If there is no pin, add to the list of axis squares
		   			if not pinExists:
		   				axisSquares.append([x, y])

		   			# Update to next square
		   			direction[0] += dirCopy[0]
		   			direction[1] += dirCopy[1]

		   	# Along straight axes
			else:

				if piece[0] == colour:

		   			if not pinExists:

		   				pinnedPieces.append([x, y])
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
				   			axisSquares.append([x, y])
				   			totalAxisSquares.append(axisSquares)

				   	else:

				   		if pinExists:
				   			del pinnedPieces[-1]
			   		
			   		break

				elif piece == '--':

		   			if not pinExists:
		   				axisSquares.append([x, y])

		   			direction[0] += dirCopy[0]
		   			direction[1] += dirCopy[1]


	leaps = [[-2,1], [-1,2], [1,2], [2,1], [2,-1], [1,-2], [-1,-2], [-2,-1]]

	# Check all potential checks by knights
	for leap in leaps:

		x, y = kingPos[0] + leap[0], kingPos[1] + leap[1]

		if x < 0 or x >= len(gameConfig) or \
	   	   y < 0 or y >= len(gameConfig):
	   	   continue

		if gameConfig[x][y] == f'{opp_colour}n':
			totalAxisSquares.append([x, y])

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

		x, y = kingPos[0] + axis[0], kingPos[1] + axis[1]

		if gameConfig[x][y][0] == opp_colour:
			axisSquares.append([x, y])
			return axisSquares

		else:
			axisSquares.append([x, y])
			axis[0] += axisCopy[0]
			axis[1] += axisCopy[1]



def checkBlockers(kingPos, gameConfig, axis, colour, opp_colour):

	def pawnBlocker(square, gameConfig, colour, opp_colour):

		x, y = square[0], square[1]

		# If the square in the axis is empty
		if gameConfig[x][y] == '--':

			# If there is a pawn 1 or 2 spaces behind that can block the check
			if (x < len(gameConfig)-1 and gameConfig[x+1][y]) == f'{colour}p' or (x == 4 and gameConfig[x+2][y] == f'{colour}p'):

				return True

		# If the pawn is able to capture the checking piece
		elif gameConfig[x][y][0] == opp_colour:

			if (x < len(gameConfig) and y > 0 and gameConfig[x+1][y-1] == f'{colour}p') or (x < len(gameConfig) and y < len(gameConfig)-1 and gameConfig[x+1][y+1] == f'{colour}p'):

				return True

		return False



	def knightBlocker(square, gameConfig, colour, opp_colour):

		# All possible combinations of coordinates that the knight can move to
		offsets = [-2,-1,1,2]
		directions = list(itertools.product(offsets, repeat=2))
		directions = list(filter(lambda a: abs(a[0]) != abs(a[1]), directions))

		for direction in directions:

			x, y = square[0] + direction[0], square[1] + direction[1]
			piece = gameConfig[x][y]

			# If the square is out of bounds
			if x < 0 or x >= len(gameConfig) or \
			   y < 0 or y >= len(gameConfig):
			   continue

			# If the square is occupied by our own knight, it can block the check
			elif piece == f'{colour}n':

				return True

		return False



	def diagBlocker(square, gameConfig, colour, opp_colour):

		directions = [[-1,1], [1,1], [1,-1], [-1,-1]]

		def diagPathFinder(square, direction, gameConfig, colour, opp_colour):

			x, y = square[0] + direction[0], square[1] + direction[1]
			piece = gameConfig[x][y]

			# If the square is out of bounds or occupied by the player's own piece, end the searching in that diagonal
			if x < 0 or x >= len(gameConfig) or \
			   y < 0 or y >= len(gameConfig) or \
			   piece[0] == opp_colour:
			   return False

			else:

				if piece == f'{colour}q' or \
				   piece == f'{colour}b':

					return True

				elif piece == '--':

					return diagPathFinder([x,y], direction, gameConfig, colour, opp_colour)

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

			x, y = square[0] + direction[0], square[1] + direction[1]
			piece = gameConfig[x][y]

			# If square is out of bounds or occupied by player's own piece, end search in that rank or file
			if x < 0 or x >=len(gameConfig) or \
			   y < 0 or y >=len(gameConfig) or \
			   piece[0] == opp_colour:
			   return False

			else:

				if piece == f'{colour}q' or \
				   piece == f'{colour}r':

					return True

				elif piece == '--':

					return straightPathFinder([x,y], direction, gameConfig, colour, opp_colour)

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
