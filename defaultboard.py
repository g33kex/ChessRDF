# Generates the turtle code for a RDF representation of the starting board of a game of chess
from rdflib import Graph, URIRef, Literal, BNode, Namespace
from rdflib.namespace import RDF

chess = Namespace("https://g33kex.github.io/ChessRDF/Chess.json#")
startingBoard = Namespace("https://g33kex.github.io/ChessRDF/StartingBoard.json#")
g = Graph(identifier=startingBoard.StartingBoard)
g.bind('chess', chess)
g.bind('startingBoard', startingBoard)

# Adds a square to the graph
def addSquare(color, coordinates):
	square = BNode(coordinates)
	g.add((square, RDF.type, chess.Square))
	g.add((square, chess.color, color))
	g.add((square, chess.coordinates, Literal(coordinates)))
	return square

# Adds a piece to the graph
def addPiece(color, kind):
	piece = BNode()
	g.add((piece, RDF.type, kind))
	g.add((piece, chess.color, color))
	return piece

# Create board
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
board = [[None for i in range(8)] for j in range(8)]

for i in range(1, 9):
	for j in range(1, 9):
		color = chess.White if (i+j)%2 else chess.Black
		square = addSquare(color, letters[i-1]+str(j))
		board[i-1][j-1] = square

for i in range(8):
	for j in range(8):
		if i<7:
			g.add((board[i][j], chess.left, board[i+1][j]))
		if i>0: 
			g.add((board[i][j], chess.right, board[i-1][j]))
		if j<7:
			g.add((board[i][j], chess.top, board[i][j+1]))
		if j>0:
			g.add((board[i][j], chess.bottom, board[i][j-1]))

# Add pieces

for i in range(8):
	for j in (1, 6):
		color = chess.White if j==1 else chess.Black
		g.add((board[i][j], chess.hasPiece, addPiece(color, chess.Pawn)))

for j in (0, 7):
	color = chess.White if j==0 else chess.Black
	g.add((board[0][j], chess.hasPiece, addPiece(color, chess.Rook)))
	g.add((board[1][j], chess.hasPiece, addPiece(color, chess.Knight)))
	g.add((board[2][j], chess.hasPiece, addPiece(color, chess.Bishop)))
	g.add((board[3][j], chess.hasPiece, addPiece(color, chess.Queen)))
	g.add((board[4][j], chess.hasPiece, addPiece(color, chess.King)))
	g.add((board[5][j], chess.hasPiece, addPiece(color, chess.Bishop)))
	g.add((board[6][j], chess.hasPiece, addPiece(color, chess.Knight)))
	g.add((board[7][j], chess.hasPiece, addPiece(color, chess.Rook)))

print(g.serialize(format="trig"))
