SOURCE=Chess.ttl
SITE=Chess.xml Example.xml StartingBoard.xml Index.xml
OUT=out.png
FORMAT=trig

default:
	rapper ${SOURCE} -i ${FORMAT} -o dot | dot -Tpng -o${OUT}

publish: ${SITE}

%.xml: %.ttl
	 rapper $< -i ${FORMAT} -o rdfxml > docs/$@

validate: 
	python3 -c "import rdflib.graph; graph = rdflib.graph.ConjunctiveGraph(); graph.parse('Chess.ttl', format='trig'); print(graph.serialize(format='json-ld'))" > Chess.jsonld
	pyshacl -f turtle -df json-ld Chess.jsonld

clean:
	rm ${OUT}
