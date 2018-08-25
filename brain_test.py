from __future__ import print_function
import numpy as np

from visbrain import Brain
from visbrain.objects import SourceObj, ConnectObj
from visbrain.io import download_file, path_to_visbrain_data

# Create an empty kwargs dictionnary :
kwargs = {}

# ____________________________ DATA ____________________________

# Load the xyz coordinates and corresponding subject name :
'''
download_file('xyz_sample.npz')
mat = np.load(path_to_visbrain_data('xyz_sample.npz'))
xyz, subjects = mat['xyz'], mat['subjects']

print(xyz.shape)
print(subjects.shape)
'''

mat = np.load('weight.npz')
xyz, subjects = mat['arr_0'][0], mat['arr_1'][0]

xyz = np.random.rand(583,3)
xyz = xyz * 70
subjects = np.random.rand(3, 583)
subjects = subjects * 70

#subjects = xyz * 2.7
'''for i in range(583):
    for j in range(3):
        xyz[i][j] = xyz1[i][j]
        subjects[i][j] = subjects1[i][j]
'''
#xyz = xyz * 3000
#subjects = subjects * 3000
#print(xyz)
subjects = subjects[0]
print(xyz.shape)
print(subjects.shape)

#N = xyz.shape[0]  # Number of electrodes
N = 583
# Now, create some random data between [-50,50]
data = np.random.uniform(-50, 50, len(subjects))

"""Create the source object :
"""
s_obj = SourceObj('SourceObj1', xyz, data, color='crimson', alpha=.5,
                  edge_width=2., radius_min=2., radius_max=10.)

"""
To connect sources between them, we create a (N, N) array.
This array should be either upper or lower triangular to avoid
redondant connections.
"""
connect = 1000 * np.random.rand(N, N)               # Random array of connections
connect[np.tril_indices_from(connect)] = 0  # Set to zero inferior triangle

"""
Because all connections are not necessary interesting, it's possible to select
only certain either using a select array composed with ones and zeros, or by
masking the connection matrix. We are giong to search vealues between umin and
umax to limit the number of connections :
"""
umin, umax = 30, 31

# 1 - Using select (0: hide, 1: display):
select = np.zeros_like(connect)
select[(connect > umin) & (connect < umax)] = 1

# 2 - Using masking (True: hide, 1: display):
connect = np.ma.masked_array(connect, mask=True)
connect.mask[np.where((connect > umin) & (connect < umax))] = False

print('1 and 2 equivalent :', np.array_equal(select, ~connect.mask + 0))

"""Create the connectivity object :
"""
c_obj = ConnectObj('ConnectObj1', xyz, connect, color_by='strength',
                   dynamic=(.1, 1.), cmap='gnuplot', vmin=umin + .2,
                   vmax=umax - .1, under='red', over='green',
                   clim=(umin, umax), antialias=True)

"""Finally, pass source and connectivity objects to Brain :
"""
vb = Brain(source_obj=s_obj, connect_obj=c_obj)

vb.show()