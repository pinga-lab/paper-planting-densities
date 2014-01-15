"""
Plot the synthetic data and model as well as the inversion results.
"""
import sys
import cPickle as pickle
import numpy
from fatiando import vis
from fatiando.mesher.volume import extract, vfilter
pyplot = vis.pyplot


def plot_data():
    data = numpy.loadtxt('data.txt', unpack=True)
    predicted = numpy.loadtxt('predicted.txt', unpack=True, usecols=[3, 4, 5])
    xs, ys = numpy.loadtxt('seeds.txt', unpack=True, usecols=[0, 1])
    x, y, z = data[0:3]
    tensor = data[-3:]
    shape = (60, 100)
    for comp, pred in zip(tensor, predicted):
        pyplot.figure(figsize=(4, 4))
        pyplot.subplots_adjust(bottom=0.2)
        pyplot.axis('scaled')
        levels = vis.contourf(y*0.001, x*0.001, comp, shape, 8, interpolate=True)
        pyplot.colorbar()
        vis.contour(y*0.001, x*0.001, pred, shape, levels, interpolate=True)
        pyplot.plot(ys*0.001, xs*0.001, '.w')        
        pyplot.xlabel('Horizontal coordinate y (km)')
        pyplot.ylabel('Horizontal coordinate x (km)')
    pyplot.show()
    
def plot_result():
    data = numpy.loadtxt('data.txt', unpack=True)
    x, y, z, topo = data[0:4]
    tensor = data[-3:]

    # Load the inversion results
    with open(sys.argv[1]) as f:
        results = pickle.load(f)
    predicted = results['predicted']

    shape = (60, 100)
    for true, pred in zip(tensor, predicted):
        pyplot.figure()
        pyplot.axis('scaled')
        levels = vis.contourf(y*0.001, x*0.001, true, shape, 12,
                              interpolate=True)
        pyplot.colorbar()
        vis.contour(y*0.001, x*0.001, pred, shape, levels, color='k',
                    interpolate=True)
        pyplot.xlabel('Horizontal coordinate y (km)')
        pyplot.ylabel('Horizontal coordinate x (km)')
    pyplot.show()

    extent = [x.min(), x.max(), y.min(), y.max(), -topo.max(), -400]
    #density_model = vfilter(900, 1200, 'density', results['mesh'])
    seeds = [results['mesh'][s] for s in results['seeds']]

    vis.mayavi_figure()
    vis.prisms3D(seeds, extract('density', seeds), vmin=0)
    #vis.prisms3D(density_model, extract('density', density_model), vmin=0)
    vis.prisms3D(results['mesh'], results['mesh'].props['density'], vmin=0)
    vis.add_axes3d(vis.add_outline3d(extent), ranges=[i*0.001 for i in extent],
        fmt='%.1f', nlabels=6)
    vis.wall_bottom(extent)
    vis.wall_north(extent)
    vis.mlab.show()

if __name__ == '__main__':
    
    if len(sys.argv) == 1:
        plot_data()
    if len(sys.argv) == 2:
        plot_result()
    

        
