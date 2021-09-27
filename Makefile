SOURCE=chess.ttl
OUT=out.png
FORMAT=trig

default:
	rapper ${SOURCE} -i ${FORMAT} -o dot | dot -Tpng -o${OUT}
clean:
	rm ${OUT}
