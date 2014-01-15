"""
Generate synthetic tensor data form a dipping body model.
"""
import cPickle as pickle
import numpy
from fatiando import potential, logger, gridder, utils
from fatiando.mesher.volume import Prism3D

log = logger.get()
logger.tofile('datagen.log')
log.info(logger.header())

bounds = [0, 5000, 0, 5000, 0, 1000]
model = [Prism3D(600, 1200, 200, 4200, 400, 900, {'density':1000}),
         Prism3D(1500, 4500, 2500, 3000, 300, 800, {'density':-1000}),
         Prism3D(3000, 4000, 1000, 2000, 200, 800, {'density':700}),
         Prism3D(2700, 3200, 3700, 4200, 0, 900, {'density':900})]

with open('model.pickle', 'w') as f:
    pickle.dump(model, f)

shape = (26, 26)
area = bounds[0:4]
noise = 5
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

with open('data.txt', 'w') as f:
    f.write("# Noise corrupted tensor components:\n")
    f.write("#   noise = %g Eotvos\n" % (noise))
    f.write("# x   y   z   gxx   gxy   gxz   gyy   gyz   gzz\n")
    numpy.savetxt(f, numpy.array(data).T)

