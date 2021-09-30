SOURCE=chess.ttl
SITE=chess.html
OUT=out.png
FORMAT=trig

default:
	rapper ${SOURCE} -i ${FORMAT} -o dot | dot -Tpng -o${OUT}

publish: ${SITE}

%.html: %.ttl
	cp $< docs/$@

clean:
	rm ${OUT}
