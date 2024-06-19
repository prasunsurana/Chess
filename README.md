# Chess

# Project Description

I came across network programming in my job, and I was fascinated by how it worked. Given my passion for chess, I decided to make a networked chess game to play with a friend. The game starts with a basic Tkinter entry widget to get the player's alias, and the rest of the game uses the Pygame module in Python. 

# Program Files

1. server.py - Server that handles all communication between clients, as well as assigning of player colours
2. client.py - Client that recieves and sends messages to server in JSON format
3. chessboard.py - Responsible for the graphical aspects of the game. Draws the chessboard and pieces, and notifies both players when a king is under check, as well as sound effects.
4. move.py - Updates the 2D array which represents the board configuration after a move has been made
5. boardfunctions.py - Contains all the game logic, namely calculating the square coordinates based on the location of mouse click, and all movement logic related to every piece, pins, checks, etc.
6. protocols.py - Defines events that each player communicates to the other, such as check, checkmate, stalemate, disconnect, etc

# How it works

1. One player has to first run server.py
2. Both players can then run main.py, which will spawn a Tkinter entry widget
3. The main.py file imports the client.py file and establishes a connection with the server once they have entered their alias.
4. Once the player aliases have been exchanged by the server, the Tkinter widget is killed and the pygame loop starts, displaying the chessboard.
5. Events in the game are defined by Protocols, such as a regular move, denoted as Protocols.GAMECONFIG, or check (Protocols.CHECK), stalemate (Protocols.STALEMATE), and so on.
6. If a player closes the game, it sends a Protocol.DISCONNECT message to the server, which broadcasts it to the other player, and notifies them.

# Challenges

1. One of the major challenges I faced was getting the networking aspect of the game working. A thread needs to be made to be able to recieve the player's move at any time, but since Pygame and Tkinter are not threadsafe modules, it was a trying task to figure out how to structure the code, especially when the game had to create a messagebox to notify the player of an event, such as a checkmate or stalemate. The solution was to initialise these messageboxes in the main game thread, rather than the client thread that recieved messages from the server.
2. Another major challenge was the game logic itself. Most of the pieces had fairly manageable game logic, but handling checks, checkmates and stalemates was tricky. In chess, checks can be nullified by moving another piece in the way, creating a pin. These pieces cannot move if they are blocking the king from being put under check. Edge cases like double checks and discovered checks also have to be considered. It was easy enough to come up with an idea to check for all these cases, but to implement them and structure them was somewhat challenging.

# Features to be added

1. Castling, pawn promotion and en passant
2. Functionality to undo moves
3. Functionality to resign and notify opponent
4. An embedded chatroom for the players to communicate
5. The server to shut down properly when both players have left
6. Reduce boilerplate in main.py and boardfunctions.py
