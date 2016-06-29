#!/usr/local/bin/python
"""

OPV GUI
Written by Soo Park 2016 for Shaheen Group @ CU Boulder
Contact: soo.park@colorado.edu

"""

import sys
from PyQt4 import QtGui, QtCore
import pyqtgraph.examples
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from numpy import *

class MainWindow(QtGui.QWidget):
    
    def __init__(self):
        super(MainWindow, self).__init__()
        
        self.layout = QtGui.QVBoxLayout()
    
        self.plotWidget = gl.GLViewWidget()
        self.plotWidget.opts['distance'] = 100

        xgrid = gl.GLGridItem()
        ygrid = gl.GLGridItem()
        zgrid = gl.GLGridItem()
        
        self.plotWidget.addItem(xgrid)
        self.plotWidget.addItem(ygrid)
        self.plotWidget.addItem(zgrid)

        xgrid.setSize(30, 30, 30)
        ygrid.setSize(30, 30, 30)
        zgrid.setSize(30, 30, 30)

        xgrid.translate(-15, 15, 0)
        ygrid.translate(15, 15, 0)
        zgrid.translate(15, 15, 0)

        xgrid.rotate(90, 0, 1, 0)
        ygrid.rotate(90, 1, 0, 0)

        xgrid.scale(1, 1, 1)
        ygrid.scale(1, 1, 1)
        zgrid.scale(1, 1, 1)

        loadButton = QtGui.QPushButton("Load XYZ File")
        loadButton.clicked.connect(self.loadXYZFile)
        
        self.layout.addWidget(loadButton)
        self.layout.addWidget(self.plotWidget)

        self.setLayout(self.layout)
        self.resize(600, 600)
        self.setWindowTitle("3D Visualtization Area")
        self.show()

    def loadXYZFile(self):
        
        xyzFileName = QtGui.QFileDialog.getOpenFileName(self, 'Load XYZ File', '.')
        with open(xyzFileName) as xyzFile:
            xyzData = xyzFile.readlines()
        
        # I manually deleted the first two lines from the xyz file. 
        
        dataLen = len(xyzData)

        pos = empty((dataLen, 3))
        size = empty((dataLen))
        color = empty((dataLen, 4))

        xMax = 0
        yMax = 0
        zMax = 0

        
        """
        
        #All the data points
        
        for i, j in enumerate(xyzData):
            
            xyzData[i] = xyzData[i].split('\t')
            del xyzData[i][0] # delete "C"
            pos[i] = tuple(xyzData[i][0:3])
            size[i] = .5
            color[i] = (0.0, 1.0, 0.0, 0.5)
        """

        
        #Just the surface area
        
        for i, j in enumerate(xyzData):

            xyzData[i] = xyzData[i].split('\t')

            del xyzData[i][0]
            del xyzData[i][3]
            del xyzData[i][3]

            #print xyzData[i]

            if float(xyzData[i][0]) >= xMax:
                xMax = float(xyzData[i][0])

            if float(xyzData[i][1]) >= yMax:
                yMax = float(xyzData[i][1])

            if float(xyzData[i][2]) >= zMax:
                zMax = float(xyzData[i][2])
       

        # plot x-plane
        indexX1 = 0
        for x in range(0, int(xMax) + 1):
            for y in range(0, int(yMax) + 1):
                
                pos[indexX1] = (x, y, 0)
                size[indexX1] = .5
                color[indexX1] = (0.0, 1.0, 0.0, 0.5)
                #print indexX1, pos[indexX1]
                indexX1 = indexX1 + 1
        
        indexX2 = indexX1
        for x in range(0, int(xMax) + 1):
            for y in range(0, int(yMax) + 1):
                
                pos[indexX2] = (x, y, zMax)
                size[indexX2] = .5
                color[indexX2] = (0.0, 1.0, 0.0, 0.5)
                #print indexX2, pos[indexX2]
                indexX2 = indexX2 + 1
        

        # plot y-plane
        indexY1 = indexX2
        for y in range(0, int(yMax) + 1):
            for z in range(0, int(zMax) + 1):

                pos[indexY1] = (0, y, z)
                size[indexY1] = .5
                color[indexY1] = (0.0, 1.0, 0.0, 0.5)
                #print indexY1, pos[indexY1]
                indexY1 = indexY1 + 1

        indexY2 = indexY1
        for y in range(0, int(yMax) + 1):
            for z in range(0, int(zMax) + 1):

                pos[indexY2] = (xMax, y, z)
                size[indexY2] = .5
                color[indexY2] = (0.0, 1.0, 0.0, 0.5)
                #print indexY2, pos[indexY2]
                indexY2 = indexY2 + 1

        # plot z-plane
        indexZ1 = indexY2
        for z in range(0, int(zMax) + 1):
            for x in range(0, int(xMax) + 1):

                pos[indexZ1] = (x, 0, z)
                size[indexZ1] = .5
                color[indexZ1] = (0.0, 1.0, 0.0, 0.5)
                #print indexZ1, pos[indexZ1]
                indexZ1 = indexZ1 + 1


        indexZ2 = indexZ1
        for z in range(0, int(zMax) + 1):
            for x in range(0, int(xMax) + 1):

                pos[indexZ2] = (x, yMax, z)
                size[indexZ2] = .5
                color[indexZ2] = (0.0, 1.0, 0.0, 0.5)
                #print indexZ2, pos[indexZ2]
                indexZ2 = indexZ2 + 1

        print indexZ2


        """
        print xMax, yMax, zMax
        for x in range(0, int(xMax) + 1):
            for y in range(0, int(yMax) + 1):
                for z in range(0, int(zMax) + 1):
                    pos[x+y+z] = (x, y, z)
                    print pos[x+y+z]
                    size[x+y+z] = .5
                    color[x+y+z] = (0.0, 1.0, 0.0, 0.5)
        """

        plot = gl.GLScatterPlotItem(pos=pos, size=size, color=color, pxMode=False)
        self.plotWidget.addItem(plot)
        

           

def main():

    app = QtGui.QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
