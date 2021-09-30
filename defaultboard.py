# Generates the turtle code for a RDF representation of the starting board of a game of chess
from rdflib import Graph, URIRef, Literal, BNode, Namespace
from rdflib.namespace import RDF

n = Namespace("http://localhost/")
g = Graph()
g.bind('', n)

# Adds a square to the graph
def addSquare(color, coordinates):
	square = BNode(coordinates)
	g.add((square, RDF.type, n.Square))
	g.add((square, n.color, color))
	g.add((square, n.coordinates, Literal(coordinates)))
	return square

# Adds a piece to the graph
def addPiece(color, kind):
	piece = BNode()
	g.add((piece, RDF.type, kind))
	g.add((piece, n.color, color))
	return piece

# Create board
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
board = [[None for i in range(8)] for j in range(8)]

for i in range(1, 9):
	for j in range(1, 9):
		color = n.White if (i+j)%2 else n.Black
		square = addSquare(color, letters[i-1]+str(j))
		board[i-1][j-1] = square

for i in range(8):
	for j in range(8):
		if i<7:
			g.add((board[i][j], n.left, board[i+1][j]))
		if i>0: 
			g.add((board[i][j], n.right, board[i-1][j]))
		if j<7:
			g.add((board[i][j], n.top, board[i][j+1]))
		if j>0:
			g.add((board[i][j], n.bottom, board[i][j-1]))

# Add pieces

for i in range(8):
	for j in (1, 6):
		color = n.White if j==1 else n.Black
		g.add((board[i][j], n.hasPiece, addPiece(color, n.Pawn)))

for j in (0, 7):
	color = n.White if j==0 else n.Black
	g.add((board[0][j], n.hasPiece, addPiece(color, n.Rook)))
	g.add((board[1][j], n.hasPiece, addPiece(color, n.Knight)))
	g.add((board[2][j], n.hasPiece, addPiece(color, n.Bishop)))
	g.add((board[3][j], n.hasPiece, addPiece(color, n.Queen)))
	g.add((board[4][j], n.hasPiece, addPiece(color, n.King)))
	g.add((board[5][j], n.hasPiece, addPiece(color, n.Bishop)))
	g.add((board[6][j], n.hasPiece, addPiece(color, n.Knight)))
	g.add((board[7][j], n.hasPiece, addPiece(color, n.Rook)))

print(g.serialize())
