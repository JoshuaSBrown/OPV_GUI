#!/usr/bin/env python
"""

OPV GUI
Written by Soo Park 2016 for Shaheen Group @ CU Boulder
Contact: soo.park@colorado.edu

"""

import sys
import os
from PyQt4 import QtGui, QtCore
# import pyqtgraph as pg
import pyqtgraph.opengl as gl
# from numpy import *
# from matplotlib.cm import *
# import itertools
import xyzViz
import pathViz
import percViz
import trapViz
from worker import clearBox


class MainWindow(QtGui.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        # imported modules
        xyz = xyzViz.xyzViz()
        path = pathViz.pathViz()
        perc = percViz.percViz()
        trap = trapViz.trapViz()

        # main layout declaration
        # main layout. plotLayout - xyzLayout - pathLayout
        self.mainLayout = QtGui.QHBoxLayout()
        # plot layout. Look at this to add a button
        self.plotLayout = QtGui.QVBoxLayout()
        # xyzWidgetsLayout that is used for the xyzWidgets QGroupBox
        self.xyzWidgetLayout = QtGui.QVBoxLayout()
        # xyzLayout that contains xyzWidgets.
        self.xyzLayout = QtGui.QVBoxLayout()
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
        """
        XYZ Visualization
        """
        self.xyzWidgets = QtGui.QGroupBox("XYZ Visualization")

        loadButton = QtGui.QPushButton("Load XYZ File")

        xyzShapeLabel = QtGui.QLabel("Shape")
        self.xyzShapeCB = QtGui.QComboBox()
        self.xyzShapeCB.addItems(["Circle", "3D Cube"])
        self.xyzShapeCB.setCurrentIndex(0)

        transLabel = QtGui.QLabel("Transparency")
        self.transSlider = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.transSlider.valueChanged[int].connect(xyz.changeTrans)

        visibleAreas = QtGui.QGroupBox("Visible Areas")
        visibleAreas.setToolTip("Cannot excede the +\
         maximum number indicated next to the labels")
        visibleAreasLayout = QtGui.QVBoxLayout()
        self.viewAll = QtGui.QRadioButton("View All Areas")

        self.surfaceAreaButton = QtGui.QRadioButton("Surface Area")
        self.surfaceAreaButton.toggled.connect(xyz.makeSurfaceArea)

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

        spacer = QtGui.QSpacerItem(0, 0, QtGui.QSizePolicy.Minimum,
                                   QtGui.QSizePolicy.Expanding)

        doge = QtGui.QLabel()
        dogeImg = QtGui.QPixmap(
            str(os.path.abspath(os.path.join("images", "dogeicon.png"))))
        dogeSmall = dogeImg.scaledToWidth(100)
        doge.setPixmap(dogeSmall)
        doge.setAlignment(QtCore.Qt.AlignCenter)

        visibleAreasLayout.addWidget(self.viewAll)
        visibleAreasLayout.addWidget(self.surfaceAreaButton)
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
        self.xyzWidgetLayout.addWidget(xyzShapeLabel)
        self.xyzWidgetLayout.addWidget(self.xyzShapeCB)
        self.xyzWidgetLayout.addWidget(transLabel)
        self.xyzWidgetLayout.addWidget(self.transSlider)
        self.xyzWidgetLayout.addWidget(visibleAreas)
        self.xyzWidgetLayout.addItem(spacer)
        self.xyzWidgetLayout.addWidget(doge)
        self.xyzWidgets.setLayout(self.xyzWidgetLayout)

        # connections
        submitButton.clicked.connect(
            lambda: xyz.changeViewAreas(self.plotAlreadyThere, self.xPlaneLE, self.yPlaneLE, self.zPlaneLE)
        )

        loadButton.clicked.connect(
            lambda: xyz.loadXYZFile(self.plotWidget, self.plotAlreadyThere, self.xPlaneLabel, self.yPlaneLabel, self.zPlaneLabel)
        )

        self.xyzShapeCB.currentIndexChanged.connect(
            lambda: xyz.changeShape(self.xyzShapeCB, self.transSlider))

        self.viewAll.toggled.connect(
            lambda: xyz.viewAllAreas(self.viewAll, self.xPlaneLE, self.yPlaneLE, self.zPlaneLE)
        )
        """
        PATH Visualization
        """
        self.pathWidgets = QtGui.QGroupBox("Path Visualization")
        self.pathWidgetLayout = QtGui.QVBoxLayout()
        self.loadPathButton = QtGui.QPushButton("Load Path File")

        self.pathChargeIdLabel = QtGui.QLabel("Charge ID")
        self.pathChargeIdCB = QtGui.QComboBox()
        self.clearBox = QtGui.QPushButton("Clear Graph")
        self.pathChargeIdCB.setEnabled(False)

        pathShapeLabel = QtGui.QLabel("Shape")
        self.pathShapeCB = QtGui.QComboBox()
        self.pathShapeCB.addItems(["Circle", "Square"])
        self.pathShapeCB.setCurrentIndex(0)

        self.pathWidgetLayout.setAlignment(QtCore.Qt.AlignTop)
        self.pathWidgetLayout.addWidget(self.loadPathButton)
        self.pathWidgetLayout.addWidget(self.pathChargeIdLabel)
        self.pathWidgetLayout.addWidget(self.pathChargeIdCB)
        self.pathWidgetLayout.addWidget(pathShapeLabel)
        self.pathWidgetLayout.addWidget(self.pathShapeCB)
        self.pathWidgets.setLayout(self.pathWidgetLayout)
        self.pathWidgetLayout.addWidget(self.clearBox)

        self.clearBox.clicked.connect(
            lambda: clearBox(self.plotWidget)
        )

        self.loadPathButton.clicked.connect(
            lambda: path.loadPathFile(self.plotWidget, self.pathChargeIdCB))

        self.pathChargeIdCB.currentIndexChanged.connect(
            lambda: path.selectPathChargeID(self.pathChargeIdCB))

        self.pathShapeCB.currentIndexChanged.connect(
            lambda: path.changeShape(self.pathShapeCB))
        """
        PERC Visualization
        """
        self.percWidgets = QtGui.QGroupBox("Perc Visualization")
        self.percWidgetLayout = QtGui.QVBoxLayout()
        self.loadPercButton = QtGui.QPushButton("Load Perc File")

        self.percChargeIdLabel = QtGui.QLabel("Charge ID")

        self.percChargeIdCB = QtGui.QComboBox()
        self.percChargeIdCB.setEnabled(False)
        self.percChargeIdCB.currentIndexChanged.connect(
            lambda: perc.selectPercChargeID(self.plotWidget))

        self.loadPercButton.clicked.connect(
            lambda: perc.loadPercFile(self.percChargeIdCB, self.plotWidget))

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
        self.trapChargeIdCB.currentIndexChanged.connect(
            lambda: trap.selectTrapChargeID(self.plotWidget))

        self.loadTrapButton.clicked.connect(
            lambda: trap.loadTrapFile(self.trapChargeIdCB, self.plotWidget))

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
    ex = MainWindow()  # NOQA
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
