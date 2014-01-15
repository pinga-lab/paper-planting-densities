"""
Run the inversion using a set of paramters
"""
import sys
import cPickle as pickle
import numpy
from fatiando.mesher.volume import PrismMesh3D, extract
from fatiando.inversion import harvester
from fatiando import logger

log = logger.get()
logger.tofile('invert-%s.log' % (sys.argv[1].split('.')[0]))
log.info(logger.header())

# Get the parameters form the input file
params = __import__(sys.argv[1].split('.')[0])

log.info("Using data file: %s" % (params.datafile))
log.info("Using parameter file: %s" % (sys.argv[1]))

data = numpy.loadtxt(params.datafile, unpack=True)
x, y, z, gxx, gxy, gxz, gyy, gyz, gzz = data

datamods = [harvester.PrismGxxModule(x, y, z, gxx, norm=1),
            harvester.PrismGxyModule(x, y, z, gxy, norm=1),
            harvester.PrismGxzModule(x, y, z, gxz, norm=1),
            harvester.PrismGyyModule(x, y, z, gyy, norm=1),
            harvester.PrismGyzModule(x, y, z, gyz, norm=1),
            harvester.PrismGzzModule(x, y, z, gzz, norm=1)]

extent = [0, 1000, 0, 1000, 0, 1000]
mesh = PrismMesh3D(extent, params.shape)
seeds = harvester.sow(mesh, params.seeds)
regul = harvester.ConcentrationRegularizer(seeds, mesh, params.mu, params.power)
jury = harvester.standard_jury(regul, thresh=params.thresh)
results, goals = harvester.harvest(seeds, mesh, datamods, jury)
log.info("Calculating standard deviations:")
stds = [numpy.std(dm.obs - dm.predicted) for dm in datamods]
log.info("  %s" % (' '.join('%.4f' % (s) for s in stds)))
log.info("Goal is actually misfit.")
log.info("Regularizer: %g" % (regul.reg))
for prop in results['estimate']:
    mesh.addprop(prop, results['estimate'][prop])
with open("%s.pickle" % (sys.argv[1].split('.')[0]), 'w') as f:
    output = {'mesh':mesh, 'goals':goals,
              'predicted':[dm.predicted  for dm in datamods],
              'seeds':[s for s in extract('index', seeds)]}
    pickle.dump(output, f)

