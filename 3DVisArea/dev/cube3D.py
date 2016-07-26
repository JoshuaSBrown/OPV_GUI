from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph_modified as pg
import pyqtgraph_modified.opengl as gl
import numpy as np
import matplotlib.cm 


def normalizeEnergy(energy):
        
    normEnergy = []
    energy = map(float, energy)
    minEnergy = min(energy)
    maxEnergy = max(energy)

    for i in range(0, len(energy)):
            
        norm = (energy[i] - minEnergy) / (maxEnergy - minEnergy)
        normEnergy.append(norm)
            #print norm
        
    return normEnergy



app = QtGui.QApplication([])

view = gl.GLViewWidget()
view.show()
view.setCameraPosition(azimuth=180)
grid = gl.GLGridItem()
grid.scale(1,1,1)
view.addItem(grid)

# verts and faces to create a cube
verts = np.array([
[0, 0, 0], #0
[0, 0, 1], #1
[0, 1, 0], #2
[0, 1, 1], #3
[1, 0, 0], #4
[1, 0, 1], #5
[1, 1, 0], #6
[1, 1, 1] #7
])

faces = np.array([
[0, 4, 6],
[0, 6, 2],
[1, 5, 7],
[1, 7, 3],
[2, 6, 3],
[3, 7, 6],
[0, 4, 1],
[1, 5, 4],
[4, 5, 7],
[4, 6, 7],
[0, 1, 3],
[0, 2, 3]
])

faceColors = np.array([
    [1, 0, 0, 0.3],
    [1, 0, 0, 0.3],
    [1, 0, 0, 0.3],
    [1, 0, 0, 0.3],
    [1, 0, 0, 0.3],
    [1, 0, 0, 0.3],
    [1, 0, 0, 0.3],
    [1, 0, 0, 0.3],
    [1, 0, 0, 0.3],
    [1, 0, 0, 0.3],
    [1, 0, 0, 0.3],
    [1, 0, 0, 0.3]

])

cube = verts[faces]


fileName = "/Users/soorinpark/Documents/School/ShaheenGroup/OPV_GUI/Data/DataT300Vx0.3Vy0Vz0R1Energy.xyz"
with open(fileName) as file:
    xyzData = file.readlines()

del xyzData[:2]

xyz = np.empty((len(xyzData), 3), float)
colors = np.zeros(shape=(len(xyzData),4))
energy = []

for i, j in enumerate(xyzData):
            
    xyzData[i] = xyzData[i].split('\t')
    del xyzData[i][0] # delete "C"
    xyz[i][0] = xyzData[i][0]
    xyz[i][1] = xyzData[i][1]
    xyz[i][2] = xyzData[i][2]
    energy.append(xyzData[i][4])
    
normEnergy = normalizeEnergy(energy)
for i in range(0, len(normEnergy)):
    colors[i] = matplotlib.cm.hot(normEnergy[i])

        
"""
# data that contains [x, y, z, color]
data = [[0, 0, 0, .5], [0, 0, 1, .25]]
#data = [[0, 0, 0, .123], [0, 0, 1, .234], [0, 1, 0, .345], [0, 1, 1, .456], [1, 0, 0, .567], [1, 0, 1, .678], [1, 1, 0, .789], [1, 1, 1, .890]]
data = np.array(data)

xyz = np.empty((len(data), 3), int)
colors = np.zeros(shape=(len(data),4))
#colors = np.array([[1, 0, 0, 1], [0, 1, 0, 1]])

for i in range(0, len(data)):
    xyz[i][0] = data[i][0]
    xyz[i][1] = data[i][1]
    xyz[i][2] = data[i][2]
    colors[i] = matplotlib.cm.hot(data[i][3])

"""


colors = colors.repeat(36, axis=0)
cube = np.tile(cube, (xyz.shape[0], 1, 1))
xyz = xyz.repeat(36, axis=0).reshape(cube.shape[0],3,3)

final = cube + xyz

"""
print len(final), len(colors)
for i in range(0, len(final)):
    print cube[i], "+\n", xyz[i], "=\n",  final[i], "\n|", colors[i]
    print "----------------------------------"
    if (i+1) % 12 == 0:
        print "----------------------------------\n"
"""

m1 = gl.GLMeshItem(vertexes=final, faceColors=colors, smooth=False)
m1.setGLOptions('opaque')
view.addItem(m1)

if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()