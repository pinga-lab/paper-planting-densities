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
x, y, z, gxx, gxy, gxz, gyy, gyz, gzz = data

datamods = [harvester.PrismGxxModule(x, y, z, gxx, norm=2),
            harvester.PrismGxyModule(x, y, z, gxy, norm=2),
            harvester.PrismGxzModule(x, y, z, gxz, norm=2),
            harvester.PrismGyyModule(x, y, z, gyy, norm=2),
            harvester.PrismGyzModule(x, y, z, gyz, norm=2),
            harvester.PrismGzzModule(x, y, z, gzz, norm=2)]

extent = [0, 5000, 0, 5000, 0, 1000]
mesh = PrismMesh3D(extent, params.shape)
seeds = harvester.sow(mesh, params.seeds)
regul = harvester.ConcentrationRegularizer(seeds, mesh, params.mu, params.power)
jury = harvester.standard_jury(regul, thresh=params.thresh)
results, goals = harvester.harvest(seeds, mesh, datamods, jury)

for prop in results['estimate']:
    mesh.addprop(prop, results['estimate'][prop])
with open(params.output, 'w') as f:
    output = {'mesh':mesh, 'goals':goals,
              'predicted':[dm.predicted  for dm in datamods],
              'seeds':[s for s in extract('index', seeds)]}
    pickle.dump(output, f)

