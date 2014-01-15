FMT=pdf
PARAMS=params-pos-neg-full.py params-pos-neg-one.py params-pos-neg-wrong.py params-pos-pos-full.py params-pos-neg-full-under.py params-pos-neg-full-over.py
PICKLES=${PARAMS:.py=.pickle}
ADJFIGS=${PARAMS:.py=.pdf}
RESFIGS=${PARAMS:.py=-result.png}

.PHONY: plot

invert: ${PICKLES}

synthetic: data-pos-neg.txt data-pos-pos.txt

data-%.txt: datagen.py model-%.py
	python $^
	
params-%.pickle: invert.py params-%.py 
	python $^

params-pos-neg-full.pickle: data-pos-neg.txt
params-pos-neg-full-under.pickle: data-pos-neg.txt
params-pos-neg-full-over.pickle: data-pos-neg.txt
params-pos-neg-one.pickle: data-pos-neg.txt
params-pos-neg-wrong.pickle: data-pos-neg.txt
params-pos-pos-full.pickle: data-pos-pos.txt

adjustment: ${ADJFIGS}

params-pos-neg-%.pdf: plot-adjustment.py params-pos-neg-%.pickle data-pos-neg.txt
	python $^

params-pos-pos-%.pdf: plot-adjustment.py params-pos-pos-%.pickle data-pos-pos.txt
	python $^

result: ${RESFIGS} plot-axis.py
	python plot-axis.py model-pos-pos.py

params-pos-neg-%-result.png: plot-res.py params-pos-neg-%.pickle model-pos-neg.py
	python $^
	
params-pos-pos-%-result.png: plot-res.py params-pos-pos-%.pickle model-pos-pos.py
	python $^

clean:
	rm *.pyc data-*.txt *.log *.pickle *.pdf *.png
