from fatiando.mesher.volume import Prism3D

props = {'density':1000}
props2 = {'density':1500}
model = [Prism3D(400, 600, 300, 500, 200, 400, props),
         Prism3D(400, 600, 400, 600, 400, 600, props),
         Prism3D(400, 600, 500, 700, 600, 800, props),
         Prism3D(450, 550, 200, 300, 200, 300, props2)]
datafile = 'data-pos-pos.txt'
