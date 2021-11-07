validate: 
	python3 -c "import rdflib.graph; graph = rdflib.graph.ConjunctiveGraph(); graph.parse('Chess.trig', format='trig'); print(graph.serialize(format='json-ld'))" > Chess.jsonld
	pyshacl -f turtle -df turtle -ef json-ld -e Chess.jsonld -s chess_shacl.ttl kasparov_turtle.ttl 
