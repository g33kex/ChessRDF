SOURCE=chess.ttl
SITE_SOURCES=chess.ttl
OUT=out.png
FORMAT=trig

default:
	rapper ${SOURCE} -i ${FORMAT} -o dot | dot -Tpng -o${OUT}

publish:
	cp ${SITE_SOURCES} docs/

clean:
	rm ${OUT}
