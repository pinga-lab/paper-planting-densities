import cPickle as pickle
import pylab
import numpy
from enthought.mayavi import mlab

import fatiando.inv.gplant as gplant
import fatiando.grav.synthetic as synthetic
import fatiando.mesh
import fatiando.utils as utils
import fatiando.vis as vis

# Get a logger
log = utils.get_logger()
# Set logging to a file
utils.set_logfile('interp-model-gen.log')
# Log a header with the current version info
log.info(utils.header())

# GENERATE SYNTHETIC DATA
################################################################################
# Make the prism model
model = []
model.append({'x1':1000, 'x2':2000, 'y1':1000, 'y2':2000, 'z1':1000, 'z2':2000,
               'value':1000})
model = numpy.array(model)

x1, x2 = 0, 3000
y1, y2 = 0, 3000
z1, z2 = 0, 3000
extent = [x1, x2, y1, y2, -z2, -z1]

# Now calculate all the components of the gradient tensor and contaminate the
# data with gaussian noise
error = 0.2
fields = ['gzz', 'gyz']
data = {}
for i, field in enumerate(fields):
    data[field] = synthetic.from_prisms(model, x1=0, x2=3000, y1=0, y2=3000,
                                        nx=50, ny=50, height=150, field=field)
    data[field]['value'] = utils.contaminate(data[field]['value'],
                                                    stddev=error,
                                                    percent=False)
    data[field]['error'] = error*numpy.ones(len(data[field]['value']))

# PERFORM THE INVERSION
################################################################################
#~ # Generate a prism mesh
mesh = fatiando.mesh.prism_mesh(x1=x1, x2=x2, y1=y1, y2=y2, z1=z1, z2=z2,
                                nx=30, ny=30, nz=30)
 
# Set the seeds and save them for later use
log.info("Setting seeds in mesh:")
seeds = []
seeds.append(gplant.get_seed((1501, 1501, 1501), 1000, mesh))

# Make a mesh for the seeds to plot them
seed_mesh = numpy.array([seed['cell'] for seed in seeds])
#~ 
#~ # Run the inversion
#~ results = gplant.grow(data, mesh, seeds, compactness=10**(4), power=3,
                      #~ threshold=10**(-3), norm=2, neighbor_type='reduced',
                      #~ jacobian_file=None, distance_type='radial')
#~ 
#~ # Unpack the results and calculate the adjusted data
#~ estimate, residuals, misfits, goals = results
#~ fatiando.mesh.fill(estimate, mesh)
#~ adjusted = gplant.adjustment(data, residuals)

#with open('mesh.pickle', 'w') as f:
#    pickle.dump(mesh, f)

with open('mesh.pickle') as f:
    mesh = pickle.load(f)

# PLOT THE INVERSION RESULTS
################################################################################
log.info("Plotting")

# Plot the adjusted model plus the skeleton of the synthetic model
fig = mlab.figure(size=(600,730))
fig.scene.background = (1, 1, 1)
fig.scene.magnification = 6

#p = vis.plot_prism_mesh(seed_mesh, style='surface')
#p.actor.mapper.scalar_visibility = False
#p.actor.property.edge_visibility = False
#p.actor.property.color = (0,0,0)

p = vis.plot_prism_mesh(fatiando.mesh.vfilter(mesh,900,1001), style='surface')
#p.actor.mapper.scalar_visibility = False
#p.actor.property.edge_visibility = False
#p.actor.property.color = (0,0,0)

p = vis.plot_prism_mesh(mesh, style='surface', opacity=0.4)
#p.actor.mapper.scalar_visibility = False
#p.actor.property.color = (0,0,0)
p.actor.property.line_width = 5

#a = mlab.axes(p, nb_labels=0, extent=extent, color=(0,0,0))
#a.label_text_property.color = (0,0,0)
#a.title_text_property.color = (0,0,0)
#a.axes.label_format = ""
#a.axes.x_label, a.axes.y_label, a.axes.z_label = "", "", ""
#a.property.line_width = 3

for field, pos, scale in zip(fields, [500, 2000], [25, 40]):
    Y, X, Z = utils.extract_matrices(data[field])
    p = mlab.contour_surf(X, Y, Z, contours=10, colormap='Greys')
    p.contour.filled_contours = True
    p.actor.actor.position = (0,0,pos)
    p.actor.actor.scale = (1,1,scale)

    #a = mlab.axes(p, nb_labels=0, extent=[0,3000,0,3000,pos,pos + scale*Z.max()], color=(0,0,0))
    #a.label_text_property.color = (0,0,0)
    #a.title_text_property.color = (0,0,0)
    #a.axes.label_format = ""
    #a.axes.x_label, a.axes.y_label, a.axes.z_label = "", "", ""
    #a.property.line_width = 3
    
fig.scene.camera.position = [-3146.9567922907049, -9163.4060799024755, 5741.7604134051016]
fig.scene.camera.focal_point = [1480.0106958881547, 1276.2836085370318, -489.3486831029677]
fig.scene.camera.view_angle = 30.0
fig.scene.camera.view_up = [0.18978015606974949, 0.43982063770127594, 0.87780481829059498]
fig.scene.camera.clipping_range = [6859.577664775763, 20934.256064206005]
mlab.show()
