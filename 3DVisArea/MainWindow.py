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
from matplotlib.cm import *
import itertools

import xyzViz, pathViz, percViz, trapViz

class MainWindow(QtGui.QWidget):
    
    def __init__(self):
        super(MainWindow, self).__init__()
        
        # import modules
        xyz = xyzViz.xyzViz()
        path = pathViz.pathViz()
        perc = percViz.percViz()
        trap = trapViz.trapViz()
        
        # main layout declaration
        self.mainLayout = QtGui.QHBoxLayout() # main layout. plotLayout - xyzLayout - pathLayout
        self.plotLayout = QtGui.QVBoxLayout() # plot layout. 
        self.xyzWidgetLayout = QtGui.QVBoxLayout() # xyzWidgetsLayout that is used for the xyzWidgets QGroupBox
        self.xyzLayout = QtGui.QVBoxLayout() # xyzLayout that contains xyzWidgets.
        self.pathWigetsLayout = QtGui.QVBoxLayout()
        self.pathLayout = QtGui.QVBoxLayout()
        self.percWidgetsLayout = QtGui.QVBoxLayout()
        self.percLayout = QtGui.QVBoxLayout()
        self.trapWidgetsLayout = QtGui.QVBoxLayout()
        self.trapLayout = QtGui.QVBoxLayout()
        
		# Plotting and Grids
        self.plotWidget = gl.GLViewWidget()
        self.plotWidget.setFixedSize(600, 600)
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

        self.plotAlreadyThere = False
        self.currentPlotObj = None

        # xyz Visualization
        self.xyzWidgets = QtGui.QGroupBox("XYZ Visualization")

        loadButton = QtGui.QPushButton("Load XYZ File")
        
        shapeLabel = QtGui.QLabel("Shape")
        self.shapeCB = QtGui.QComboBox()
        self.shapeCB.addItems(["Circle", "Square"])
        self.shapeCB.setCurrentIndex(0)

        transLabel = QtGui.QLabel("Transparency")

        self.transSlider = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.transSlider.valueChanged[int].connect(xyz.changeTrans)

        visibleAreas = QtGui.QGroupBox("Visible Areas")
        visibleAreas.setToolTip("Cannot excede the maximum number indicated next to the labels")

        visibleAreasLayout = QtGui.QVBoxLayout()

        self.viewAll = QtGui.QRadioButton("View All Areas")

        self.surfaceAreaButton = QtGui.QRadioButton("Surface Area")
        self.surfaceAreaButton.toggled.connect(xyz.makeSurfaceArea)

        self.meshSurfaceButton = QtGui.QRadioButton("Mesh Surface Area")
        self.meshSurfaceButton.toggled.connect(xyz.meshSurfaceArea)
        self.meshSurfaceButton.setEnabled(False)

        self.xPlaneLabel = QtGui.QLabel("X-Plane")
        self.xPlaneLabel.setToolTip("ex) 1,4-7,15,17")
        self.yPlaneLabel = QtGui.QLabel("Y-Plane")
        self.yPlaneLabel.setToolTip("ex) 1,4-7,15,17")
        self.zPlaneLabel = QtGui.QLabel("Z-Plane")
        self.zPlaneLabel.setToolTip("ex) 1,4-7,15,17")
        
        self.xPlaneLE = QtGui.QLineEdit()
        self.yPlaneLE = QtGui.QLineEdit()
        self.zPlaneLE = QtGui.QLineEdit()

        submitButton = QtGui.QPushButton("Submit")

        submitButton.clicked.connect(lambda: xyz.changeViewAreas(self.plotAlreadyThere, self.xPlaneLE, self.yPlaneLE, self.zPlaneLE))
        loadButton.clicked.connect(lambda: xyz.loadXYZFile(self.plotWidget, self.plotAlreadyThere, self.xPlaneLabel, self.yPlaneLabel, self.zPlaneLabel))
        self.shapeCB.currentIndexChanged.connect(lambda: xyz.changeShape(self.shapeCB, self.transSlider))
        self.viewAll.toggled.connect(lambda: xyz.viewAllAreas(self.viewAll, self.xPlaneLE, self.yPlaneLE, self.zPlaneLE))

        spacer = QtGui.QSpacerItem(0, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        
        doge = QtGui.QLabel()
        dogeImg = QtGui.QPixmap("/Users/soorinpark/Documents/School/ShaheenGroup/OPV_GUI/images/dogeicon.png")
        dogeSmall = dogeImg.scaledToWidth(100)
        doge.setPixmap(dogeSmall)
        doge.setAlignment(QtCore.Qt.AlignCenter)

        visibleAreasLayout.addWidget(self.viewAll)
        visibleAreasLayout.addWidget(self.surfaceAreaButton)
        visibleAreasLayout.addWidget(self.meshSurfaceButton)
        visibleAreasLayout.addWidget(self.xPlaneLabel)
        visibleAreasLayout.addWidget(self.xPlaneLE)
        visibleAreasLayout.addWidget(self.yPlaneLabel)
        visibleAreasLayout.addWidget(self.yPlaneLE)
        visibleAreasLayout.addWidget(self.zPlaneLabel)
        visibleAreasLayout.addWidget(self.zPlaneLE)
        visibleAreasLayout.addWidget(submitButton)
        visibleAreas.setLayout(visibleAreasLayout)

        # adding widgets to respective layouts
        self.xyzWidgetLayout.setAlignment(QtCore.Qt.AlignTop)
        self.xyzWidgetLayout.addWidget(loadButton)
        self.xyzWidgetLayout.addWidget(shapeLabel)
        self.xyzWidgetLayout.addWidget(self.shapeCB)
        self.xyzWidgetLayout.addWidget(transLabel)
        self.xyzWidgetLayout.addWidget(self.transSlider)
        self.xyzWidgetLayout.addWidget(visibleAreas)
        self.xyzWidgetLayout.addItem(spacer)
        self.xyzWidgetLayout.addWidget(doge)
        self.xyzWidgets.setLayout(self.xyzWidgetLayout)
        
        # path
        self.pathWidgets = QtGui.QGroupBox("Path Visualization")
        self.pathWidgetLayout = QtGui.QVBoxLayout()

        self.loadPathButton = QtGui.QPushButton("Load Path File")
        self.loadPathButton.clicked.connect(path.loadPathFile)

        self.pathChargeIdLabel = QtGui.QLabel("Charge ID")
        
        self.pathChargeIdCB = QtGui.QComboBox()
        self.pathChargeIdCB.setEnabled(False)
        self.pathChargeIdCB.currentIndexChanged.connect(lambda: path.selectPathChargeID)

        self.pathWidgetLayout.setAlignment(QtCore.Qt.AlignTop)
        self.pathWidgetLayout.addWidget(self.loadPathButton)
        self.pathWidgetLayout.addWidget(self.pathChargeIdLabel)
        self.pathWidgetLayout.addWidget(self.pathChargeIdCB)
        self.pathWidgets.setLayout(self.pathWidgetLayout)
        
        self.percWidgets = QtGui.QGroupBox("Perc Visualization")
        self.percWidgetLayout = QtGui.QVBoxLayout()
        
        self.loadPercButton = QtGui.QPushButton("Load Perc File")
        
        self.percChargeIdLabel = QtGui.QLabel("Charge ID")
        
        self.percChargeIdCB = QtGui.QComboBox()
        self.percChargeIdCB.setEnabled(False)
        self.percChargeIdCB.currentIndexChanged.connect(lambda: perc.selectPercChargeID(self.plotWidget))
       
        self.loadPercButton.clicked.connect(lambda: perc.loadPercFile(self.percChargeIdCB, self.plotWidget))

        self.percWidgetLayout.setAlignment(QtCore.Qt.AlignTop)
        self.percWidgetLayout.addWidget(self.loadPercButton)
        self.percWidgetLayout.addWidget(self.percChargeIdLabel)
        self.percWidgetLayout.addWidget(self.percChargeIdCB)
        self.percWidgets.setLayout(self.percWidgetLayout)
        
        self.trapWidgets = QtGui.QGroupBox("Trap Visualization")
        self.trapWidgetLayout = QtGui.QVBoxLayout()
        
        self.loadTrapButton = QtGui.QPushButton("Load Trap File")
        
        self.trapChargeIdLabel = QtGui.QLabel("Charge ID")
        
        self.trapChargeIdCB = QtGui.QComboBox()
        self.trapChargeIdCB.setEnabled(False)
        self.trapChargeIdCB.currentIndexChanged.connect(lambda: trap.selectTrapChargeID(self.plotWidget))
       
        self.loadTrapButton.clicked.connect(lambda: trap.loadTrapFile(self.trapChargeIdCB, self.plotWidget))

        self.trapWidgetLayout.setAlignment(QtCore.Qt.AlignTop)
        self.trapWidgetLayout.addWidget(self.loadTrapButton)
        self.trapWidgetLayout.addWidget(self.trapChargeIdLabel)
        self.trapWidgetLayout.addWidget(self.trapChargeIdCB)
        self.trapWidgets.setLayout(self.trapWidgetLayout)
				    
        self.xyzLayout.addWidget(self.xyzWidgets)
        self.plotLayout.addWidget(self.plotWidget)
        self.pathLayout.addWidget(self.pathWidgets)
        self.percLayout.addWidget(self.percWidgets)
        self.trapLayout.addWidget(self.trapWidgets)

        self.mainLayout.addLayout(self.plotLayout)
        self.mainLayout.addLayout(self.xyzLayout)
        self.mainLayout.addLayout(self.pathLayout)
        self.mainLayout.addLayout(self.percLayout)
        self.mainLayout.addLayout(self.trapLayout)


        self.previousDataSize = 0
        self.surfaceMade = False

        self.meshVerts = []
        self.xVerts1 = []
        self.xVerts2 = []
        self.yVerts1 = []
        self.yVerts2 = []
        self.zVerts1 = []
        self.zVerts2 = []
        self.xColors1 = []
        self.xColors2 = []
        self.yColors1 = []
        self.yColors2 = []
        self.zColors1 = []
        self.zColors2 = []

        self.setLayout(self.mainLayout)
        self.resize(800, 600)
        self.setWindowTitle("3D Visualization Area")
        self.show()


def main():

    app = QtGui.QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
