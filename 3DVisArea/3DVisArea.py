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

        for i, j in enumerate(xyzData):
            
            xyzData[i] = xyzData[i].split('\t')
            del xyzData[i][0] # delete "C"
            pos[i] = tuple(xyzData[i][0:3])
            size[i] = .5
            color[i] = (0.0, 1.0, 0.0, 0.5)
            



        plot = gl.GLScatterPlotItem(pos=pos, size=size, color=color, pxMode=False)
        self.plotWidget.addItem(plot)
        

           

def main():

    app = QtGui.QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
