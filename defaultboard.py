# Generates the turtle code for a RDF representation of the starting board of a game of chess
from rdflib import Graph, URIRef, Literal, BNode, Namespace
from rdflib.namespace import RDF

chess = Namespace("https://g33kex.github.io/ChessRDF/Chess.xml#")
startingBoard = Namespace("https://g33kex.github.io/ChessRDF/StartingBoard.xml#")
g = Graph(identifier=startingBoard.StartingBoard)
g.bind('chess', chess)
g.bind('startingBoard', startingBoard)

# Adds a square to the graph
def addSquare(color, coordinates):
    square = startingBoard[coordinates]
    g.add((square, RDF.type, chess.Square))
    g.add((square, chess.color, color))
    g.add((square, chess.coordinates, Literal(coordinates)))
    return square

# Adds a piece to the graph and put in on a square
def addPiece(color, kind, square):
    kind_notation = 'P' if kind == chess.Pawn else 'R' if kind == chess.Rook else 'B' if kind == chess.Bishop else 'N' if kind == chess.Knight else 'Q' if kind == chess.Queen else 'K'
    piece = startingBoard[kind_notation + (g.value(square, chess.coordinates))]
    g.add((piece, RDF.type, kind))
    g.add((piece, chess.color, color))
    g.add((square, chess.hasPiece, piece))
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
        addPiece(color, chess.Pawn, board[i][j])

for j in (0, 7):
    color = chess.White if j==0 else chess.Black
    addPiece(color, chess.Rook,board[0][j])
    addPiece(color, chess.Knight,board[1][j])
    addPiece(color, chess.Bishop,board[2][j])
    addPiece(color, chess.Queen,board[3][j])
    addPiece(color, chess.King,board[4][j])
    addPiece(color, chess.Bishop, board[5][j])
    addPiece(color, chess.Knight,board[6][j])
    addPiece(color, chess.Rook,board[7][j])

print(g.serialize(format="trig"))
