SOURCE=chess.ttl
SITE=chess.json
OUT=out.png
FORMAT=trig

default:
	rapper ${SOURCE} -i ${FORMAT} -o dot | dot -Tpng -o${OUT}

publish: ${SITE}

%.json: %.ttl
	 rapper $< -i ${FORMAT} -o json > docs/$@

clean:
	rm ${OUT}
