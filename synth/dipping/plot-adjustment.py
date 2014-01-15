"""
Plot the synthetic data and model as well as the inversion results.
"""
import sys
import cPickle as pickle
import numpy
from fatiando import vis
from fatiando.mesher.volume import extract, vfilter
pyplot = vis.pyplot

# Load the inversion results
name = sys.argv[1].split('.')[0]
with open(sys.argv[1]) as f:
    results = pickle.load(f)
predicted = results['predicted']

# Load synthetic data
data = numpy.loadtxt(sys.argv[2], unpack=True)
x, y, z = data[0:3]
tensor = data[3:]

fdir = 'figs'

shape = (51, 51)
pyplot.figure(figsize=(3.33,4))
pyplot.axis('scaled')
levels = vis.contourf(y*0.001, x*0.001, tensor[-1], shape, 6)
pyplot.colorbar(orientation='horizontal', shrink=0.8)
vis.contour(y*0.001, x*0.001, predicted[-1], shape, levels, color='k',
    style='dashed', linewidth=1.0)
pyplot.xlabel('Horizontal coordinate y (km)')
pyplot.ylabel('Horizontal coordinate x (km)')
pyplot.savefig('.'.join([name, 'pdf']))
#pyplot.show()
