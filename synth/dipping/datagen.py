"""
Generate synthetic tensor data form a dipping body model.
"""
import sys
import numpy
from fatiando import potential, logger, gridder, utils
from fatiando.mesher.volume import Prism3D

log = logger.tofile('datagen-%s.log' % (sys.argv[1].split('.')[0]))
log.info(logger.header())

modelfile = __import__(sys.argv[1].split('.')[0])
model = modelfile.model

shape = (51, 51)
bounds = [0, 1000, 0, 1000, 0, 1000]
area = bounds[0:4]
noise = 0.5
x, y, z = gridder.regular(area, shape, z=-150)
tensor = (potential.prism.gxx(x, y, z, model),
          potential.prism.gxy(x, y, z, model),
          potential.prism.gxz(x, y, z, model),
          potential.prism.gyy(x, y, z, model),
          potential.prism.gyz(x, y, z, model),
          potential.prism.gzz(x, y, z, model))
tensor_noisy = [utils.contaminate(d, noise) for d in tensor]
data = [x, y, z]
data.extend(tensor_noisy)

with open(modelfile.datafile, 'w') as f:
    f.write("# Noise corrupted tensor components:\n")
    f.write("#   noise = %g Eotvos\n" % (noise))
    f.write("# x   y   z   gxx   gxy   gxz   gyy   gyz   gzz\n")
    numpy.savetxt(f, numpy.array(data).T)

