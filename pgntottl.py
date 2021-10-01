# Converts PGN chess game representation format to turtle RDF representation
# Only works if starting board is the standard chess board
import sys
import chess.pgn
from rdflib import Graph, URIRef, Literal, BNode, Namespace
from rdflib.namespace import RDF

ch = Namespace("https://g33kex.github.com/ChessRDF/Chess.xml#")
sequences = Namespace("https://g33kex.github.io")
startingBoard = Namespace("https://g33kex.github.io/ChessRDF/StartingBoard.xml#")

g = Graph(identifier=sequences.KasparovVsTheWorld)
g.bind('chess', ch)
g.bind('sequences', 'sequences')
g.bind('startingBoard', startingBoard)


if len(sys.argv) != 2:
    print("Usage: pgntottl.py <game.pgn>")
    exit(1)

pgn = open(sys.argv[1])

game = chess.pgn.read_game(pgn)
print(game.headers)

board=game.board()

def addMove(move):
    piece = board.piece_at(move.from_square)
    piece_notation = str(board.piece_at(move.from_square)).upper()
    m = BNode()
    g.add((m, RDF.type, ch.Move))
    g.add((m, ch.color, color))
    return m


## We should include the board into the move graph with another graph. It seems hard to actually make reference to the starting graph as it is not the same actual piece... maybe look into that. 

# Set starting board (we could dynamically parse board but we assume players used the default board
sequence = BNode("m1")
g.add((sequence, RDF.type, ch.Sequence))
g.add((sequence, ch.startingBoard, startingBoard.StartingBoard))
for move in game.mainline_moves():
    move.
    addMove(move)
    print(piece_notation)
    board.push(move)
    #print(chess.square_name(move.from_square))

