# Chess

# Project Description

I came across network programming in my job, and I was fascinated by how it worked. Given my passion for chess, I decided to make a networked chess game to play with a friend. The game starts with a basic Tkinter entry widget to get the player's alias, and the rest of the game uses the Pygame module in Python. 

# Challenges

1. One of the major challenges I faced was getting the networking aspect of the game working. A thread needs to be made to be able to recieve the player's move at any time, but since Pygame and Tkinter are not threadsafe modules, it was a trying task to figure out how to structure the code, especially when the game had to create a messagebox to notify the player of an event, such as a checkmate or stalemate. The solution was to initialise these messageboxes in the main game thread, rather than the client thread that recieved messages from the server.
2. Another major challenge was the game logic itself. Most of the pieces had fairly manageable game logic, but handling checks, checkmates and stalemates was tricky. In chess, checks can be nullified by moving another piece in the way, creating a pin. These pieces cannot move if they are blocking the king from being put under check. Edge cases like double checks and discovered checks also have to be considered. It was easy enough to come up with an idea to check for all these cases, but to implement them and structure them was somewhat challenging.

# Features to be added

1. Castling, pawn promotion and en passant.
2. Functionality to undo moves
3. An embedded chatroom for the players to communicate
