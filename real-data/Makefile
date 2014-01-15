.PHONY: plot, plot-res plot-data

all: result.pickle 

result.pickle: data.txt invert.py params.py
	python invert.py params

plot: plot-res


plot-res: result.pickle
	python plot.py result.pickle

plot-data:
	python plot.py

clean:
	rm result.pickle *.log *.pyc
