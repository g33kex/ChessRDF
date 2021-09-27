## RDF Issues

- Problem with ColoredElement: maybe use subclass for colors?
	* But colors are inherently a player for moves, pieces, and players
	* But not for squares
	* What links a move to the player that did the move? For now is is that the player is the white player and the move is white, but that's not good in rdf there would need to be a direct link
	* Maybe use a subgraph that contains the player (and info about them) and link the subgraph with a property such as ownedBy? or madeBy?  
- Problem with Game: should the winner by a Player or just an enumeration like "draw, white, black"? Same problem as previoys one...
- Should we get rid of the `a rdf:Class` ? It seems pretty useless when there is a subclass... but it's needed when there is none so why not put it anyway?

## OWL? Issues

- Nothing says that ListOfMoves contains Moves

