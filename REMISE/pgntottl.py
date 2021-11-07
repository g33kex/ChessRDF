# Converts PGN chess game representation format to turtle RDF representation
# Only works if starting board is the standard chess board
import sys
import chess.pgn
import urllib
from rdflib import Graph, URIRef, Literal, BNode, Namespace, Dataset, ConjunctiveGraph
from rdflib.namespace import RDF

ch = Namespace("https://g33kex.github.io/ChessRDF/Chess.xml#")
index = Namespace("https://g33kex.github.io/ChessRDF/Index.xml#")
games = Namespace("https://g33kex.github.io/ChessRDF/Games.xml#")
foaf = Namespace("http://xmlns.com/foaf/spec/#")


if len(sys.argv) != 2:
    print("Usage: pgntottl.py <game.pgn>")
    exit(1)

pgn = open(sys.argv[1])
game = chess.pgn.read_game(pgn)
board=game.board()

game_url = urllib.parse.quote(game.headers['Event'])

## Create dataset
ds = Dataset()
ds.bind('chess', ch)
ds.bind('games', games)
ds.bind('', index)
ds.bind('foaf', foaf)

## Make stating board graph
def square_at(coordinate):
    return next(board_graph[:ch.coordinates:Literal(coordinate)])

def piece_at(coordinate):
    return next(board_graph[square_at(coordinate):ch.hasPiece:]) 

board_graph = ds.graph(games[game_url+"_board"])
startingBoard = ConjunctiveGraph()
startingBoard.parse("StartingBoard.trig", format='trig')

for triple in startingBoard:
    board_graph.add(triple)

## Make sequences graph

g = ds.graph(games[game_url+"_sequences"])

pieces_map = {}

def addMove(move):
    piece = board.piece_at(move.from_square)
    piece_color = ch.White if board.piece_at(move.from_square).color == chess.WHITE  else ch.Black
    piece_rdf = None
    if piece not in pieces_map:
        piece_rdf = piece_at(chess.square_name(move.from_square))
        pieces_map[piece] = piece_rdf
    else:
        piece_rdf = pieces_map[piece]
    m = BNode()
    g.add((m, RDF.type, ch.Move))
    g.add((m, ch.color, piece_color))
    g.add((m, ch.notation, Literal(move.uci())))
    if(board.is_kingside_castling(move)):
        g.add((m, ch.castleKingSide, Literal(True)))
    elif(board.is_queenside_castling(move)):
        g.add((m, ch.castleQueenSide, Literal(True)))
    else:
        g.add((m, ch.destinationSquare, square_at(chess.square_name(move.to_square))))
        g.add((m, ch.piece, piece_rdf))

    if board.is_en_passant(move):
        print("en passant piece taken not supported yet")
    elif board.is_capture(move):
        captured_piece = board.piece_at(move.to_square)
        captured_piece_rdf = None
        if captured_piece not in pieces_map:
            captured_piece_rdf = piece_at(chess.square_name(move.to_square))
            pieces_map[piece] = captured_piece_rdf
        else:
            captured_piece_rdf = pieces_map[captured_piece]
        g.add((m, ch.pieceTaken, captured_piece_rdf))

    if move.promotion is not None:
        promoted_piece = BNode()
        piece_type = chess.Piece(move.promotion, board.piece_at(move.from_square).color).symbol().upper()
        rdf_chess_type = ch.Queen if piece_type == "Q" else ch.Knight if piece_type == "N" else ch.Root if piece_type == "R" else ch.Bishop
        g.add((promoted_piece, RDF.type, rdf_chess_type))
        g.add((m, ch.pawnPromotion, promoted_piece))
    return m


## We should include the board into the move graph with another graph. It seems hard to actually make reference to the starting graph as it is not the same actual piece... maybe look into that. 

# Set starting board (we could dynamically parse board but we assume players used the default board
rdf_sequence = BNode()
g.add((rdf_sequence, RDF.type, ch.Sequence))
g.add((rdf_sequence, ch.startingBoard, board_graph.identifier))
for move in game.mainline_moves():
    rdf_move = addMove(move)
    g.add((rdf_sequence, RDF.first, rdf_move))
    rdf_sequence = BNode()
    g.add((rdf_sequence, RDF.rest, rdf_sequence))
    board.push(move)
    #print(chess.square_name(move.from_square))

#print(g.serialize(format='trig'))

## Make game graph
game_graph = ds

game_rdf = index[game_url]
game_graph.add((game_rdf, RDF.type, ch.Game))

whitePlayer_rdf = BNode()
blackPlayer_rdf = BNode()
game_graph.add((game_rdf, ch.whitePlayer, whitePlayer_rdf))
game_graph.add((game_rdf, ch.blackPlayer, blackPlayer_rdf))

game_graph.add((whitePlayer_rdf, foaf.name, Literal(game.headers['White'])))
game_graph.add((blackPlayer_rdf, foaf.name, Literal(game.headers['Black'])))

game_graph.add((game_rdf, ch.moves, g.identifier))

## Print the dataset
print(ds.serialize(format='trig'))

