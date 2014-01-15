"""
Run the inversion using a set of paramters
"""
import sys
import cPickle as pickle
import numpy
from fatiando.mesher.volume import PrismMesh3D, extract
from fatiando.inversion import harvester
from fatiando import logger

if len(sys.argv) != 2:
    print "Use python invert.py params_file"
    sys.exit()

log = logger.get()
logger.tofile('%s.log' % (sys.argv[1]))
log.info(logger.header())

# Get the parameters form the input file
params = __import__(sys.argv[1])

data = numpy.loadtxt('data.txt', unpack=True)
x, y, z, topo, gxx, gxy, gxz, gyy, gyz, gzz = data

datamods = [harvester.PrismGyyModule(x, y, z, gyy, norm=1),
            harvester.PrismGyzModule(x, y, z, gyz, norm=1),
            harvester.PrismGzzModule(x, y, z, gzz, norm=1)]

extent = [x.min(), x.max(), y.min(), y.max(), -topo.max(), -400]
mesh = PrismMesh3D(extent, params.shape)
mesh.carvetopo(x, y, topo)
seeds = harvester.sow(mesh, params.seeds)
log.info("Making the jury")
regul = harvester.ConcentrationRegularizer(seeds, mesh, params.mu, params.power)
jury = harvester.standard_jury(regul, thresh=params.thresh)
log.info("Running the inversion")
results, goals = harvester.harvest(seeds, mesh, datamods, jury)

for prop in results['estimate']:
    mesh.addprop(prop, results['estimate'][prop])

with open("predicted.txt", 'w') as f:
    pred = [x, y, z]
    pred.extend([dm.predicted for dm in datamods])
    numpy.savetxt(f, numpy.transpose(pred), fmt="%.4f")
    
with open(params.output, 'w') as f:
    output = {'mesh':mesh, 'goals':goals,
              'seeds':[s for s in extract('index', seeds)]}
    pickle.dump(output, f)

