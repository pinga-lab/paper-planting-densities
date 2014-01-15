DPI=600
CMYKPROF=CMYK/USWebCoatedSWOP.icc
FIG1=Figure1.tiff
FIG2=Figure2.tiff
FIG3=Figure3.tiff
FIG4=Figure4.tiff
FIG5=Figure5a.tiff Figure5b.tiff Figure5c.tiff
FIG6=Figure6.tiff
FIG7=Figure7.tiff
FIG8=Figure8.tiff
FIG9=Figure9.tiff
FIG10=Figure10.tiff
FIG11=Figure11a.tiff Figure11b.tiff Figure11c.tiff
FIG12=Figure12.tiff
CFIGURES= ${FIG2} ${FIG4} ${FIG5} ${FIG10} ${FIG11} ${FIG12}
BWFIGURES=${FIG1} ${FIG3} ${FIG6} ${FIG7} ${FIG8} ${FIG9}

all: ${CFIGURES} ${BWFIGURES}
	test -d tiffs || mkdir tiffs
	mv *.tiff tiffs

Figure%.tiff: Figure%.png
	convert $< -colorspace CMYK -profile ${CMYKPROF} -density ${DPI} -compress LZW +adjoin $@

test:
	identify -verbose tiffs/Figure*.tiff | \
	grep -i -E "(image|format|resolution|colorspace|type|base type|print size|compression)"

clean:
	rm -r tiffs
