.PHONY: plot, plot-res plot-data

all: result.pickle 

synthetic: data.txt

	
data.txt: datagen.py
	python datagen.py

result.pickle: data.txt invert.py params.py
	python invert.py params

plot: plot-res


plot-res: result.pickle
	python plot.py result.pickle

plot-data: synthetic
	python plot.py

clean:
	rm data.txt model.pickle result.pickle *.log *.pyc
