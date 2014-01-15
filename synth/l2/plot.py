"""
Plot the synthetic data and model as well as the inversion results.
"""
import sys
import cPickle as pickle
import numpy
from fatiando import vis
from fatiando.mesher.volume import extract, vfilter
pyplot = vis.pyplot


def plot_synth():
    # Load synthetic data
    data = numpy.loadtxt('data.txt', unpack=True)
    x, y, z = data[0:3]
    tensor = data[3:]
    with open('model.pickle') as f:
        model = pickle.load(f)
    for comp in tensor:
        shape = (26, 26)
        pyplot.figure(figsize=(5,4))
        pyplot.axis('scaled')
        levels = vis.contourf(y*0.001, x*0.001, comp, shape, 8)
        vis.contour(y*0.001, x*0.001, comp, shape, levels)
        pyplot.xlabel('Horizontal coordinate y (km)')
        pyplot.ylabel('Horizontal coordinate x (km)')
    pyplot.show()
    
    extent = [0, 5000, 0, 5000, 0, 1000]    
    vis.mayavi_figure()
    vis.prisms3D(model, extract('density', model))
    vis.add_axes3d(vis.add_outline3d(extent), ranges=[i*0.001 for i in extent],
        fmt='%.1f', nlabels=6)
    vis.wall_bottom(extent)
    vis.wall_north(extent)
    vis.mlab.show()

def plot_result():
    # Load synthetic data
    data = numpy.loadtxt('data.txt', unpack=True)
    x, y, z = data[0:3]
    tensor = data[3:]
    with open('model.pickle') as f:
        model = pickle.load(f)

    # Load the inversion results
    with open(sys.argv[1]) as f:
        results = pickle.load(f)
    predicted = results['predicted']

    shape = (26, 26)
    names = ['gxx', 'gxy', 'gxz', 'gyy', 'gyz', 'gzz']
    i = 0
    for true, pred in zip(tensor, predicted):
        pyplot.figure(figsize=(3.33,4))
        pyplot.axis('scaled')
        levels = vis.contourf(y*0.001, x*0.001, true, shape, 8)
        cb = pyplot.colorbar(orientation='horizontal', shrink=0.95)
        cb.set_ticks([l for j, l in enumerate(levels) if j%2 != 0])
        vis.contour(y*0.001, x*0.001, pred, shape, levels, color='k')
        pyplot.xlabel('Horizontal coordinate y (km)')
        pyplot.ylabel('Horizontal coordinate x (km)')
        pyplot.savefig('.'.join([names[i], 'pdf']))
        i += 1
    pyplot.show()

    extent = [0, 5000, 0, 5000, 0, 1000]
    density_model = vfilter(-2000, -1, 'density', results['mesh'])
    density_model.extend(vfilter(1, 2000, 'density', results['mesh']))
    seeds = [results['mesh'][s] for s in results['seeds']]

    vis.mayavi_figure()
    vis.prisms3D(model, extract('density', model), style='wireframe')
    vis.prisms3D(seeds, extract('density', seeds))
    vis.prisms3D(density_model, extract('density', density_model))
    vis.add_axes3d(vis.add_outline3d(extent), ranges=[i*0.001 for i in extent],
        fmt='%.1f', nlabels=3)
    vis.wall_bottom(extent)
    vis.wall_north(extent)
    vis.mlab.show()

if __name__ == '__main__':
    
    if len(sys.argv) == 1:
        plot_synth()
    if len(sys.argv) == 2:
        plot_result()
    

        
