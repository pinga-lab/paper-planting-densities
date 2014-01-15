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

bounds = [0, 5000, 0, 5000, 0, 1500]
model = [Prism3D(500, 4500, 3000, 3500, 200, 700, {'density':1200}),
         Prism3D(3000, 4500, 1800, 2300, 200, 700, {'density':1200}),
         Prism3D(500, 1500, 500, 1500, 0, 800, {'density':600}),
         Prism3D(0, 800, 1800, 2300, 0, 200, {'density':600}),
         Prism3D(4000, 4800, 100, 900, 0, 300, {'density':600}),
         Prism3D(0, 2000, 4500, 5000, 0, 200, {'density':600}),              
         Prism3D(3000, 4200, 2500, 2800, 200, 700, {'density':-1000}),
         Prism3D(300, 2500, 1800, 2700, 500, 1000, {'density':-1000}),
         Prism3D(4000, 4500, 500, 1500, 400, 1000, {'density':-1000}),
         Prism3D(1800, 3700, 500, 1500, 300, 1300, {'density':-1000}),
         Prism3D(500, 4500, 4000, 4500, 400, 1300, {'density':-1000})]

with open('model.pickle', 'w') as f:
    pickle.dump(model, f)

shape = (51, 51)
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

