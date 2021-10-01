SOURCE=Chess.ttl
SITE=Chess.xml Example.xml StartingBoard.xml Index.xml
OUT=out.png
FORMAT=trig

default:
	rapper ${SOURCE} -i ${FORMAT} -o dot | dot -Tpng -o${OUT}

publish: ${SITE}

%.xml: %.ttl
	 rapper $< -i ${FORMAT} -o rdfxml > docs/$@

clean:
	rm ${OUT}
