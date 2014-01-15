SUP=supplement

all: supplement

supplement: ${SUP}.pdf

${SUP}.pdf: ${SUP}.tex
	pdflatex $<
	pdflatex $<

clean:
	rm ${SUP}.pdf \
	*.aux *.log *.out	
