CLEAN=manuscript-GEO-2011-0388
REVISED=manuscript-GEO-2011-0388-revised

all: final revised 

help:
	@echo "Targets:"
	@echo "  all: make the clean and the revised versions"
	@echo "  final: make the clean version"
	@echo "  revised: make the revised version"
	@echo "  wordcount: count the words in the source without the Latex stuff"
	@echo "  clean: clean up the build"

final: ${CLEAN}.pdf

revised: ${REVISED}.pdf

${CLEAN}.tex: head-clean.tex body.tex
	cat $< body.tex > $@

${CLEAN}.pdf: ${CLEAN}.tex
	pdflatex $<
	pdflatex $<	
	
${REVISED}.tex: head-revised.tex body.tex
	cat $< body.tex > $@

${REVISED}.pdf: ${REVISED}.tex
	pdflatex $<
	pdflatex $<
	
wordcount: ${CLEAN}.tex
	detex $< | wc -w

clean:
	rm ${REVISED}.pdf ${CLEAN}.pdf \
	${REVISED}.tex ${CLEAN}.tex \
	*.aux *.lof *.log *.out	
