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

class MainWindow(QtGui.QWidget):
    
    def __init__(self):
        super(MainWindow, self).__init__()
        
        self.mainLayout = QtGui.QHBoxLayout() # main layout. plotLayout - xyzLayout - pathLayout
        self.plotLayout = QtGui.QVBoxLayout() # plot layout. 
        self.xyzWidgetLayout = QtGui.QVBoxLayout() # xyzWidgetsLayout that is used for the xyzWidgets QGroupBox
        self.xyzLayout = QtGui.QVBoxLayout() # xyzLayout that contains xyzWidgets.
        self.pathWigetsLayout = QtGui.QVBoxLayout()
        self.pathLayout = QtGui.QVBoxLayout()

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

        self.xyzWidgets = QtGui.QGroupBox("XYZ Visualization")

        loadButton = QtGui.QPushButton("Load XYZ File")
        loadButton.clicked.connect(self.loadXYZFile)
        
        shapeLabel = QtGui.QLabel("Shape")
        self.shapeCB = QtGui.QComboBox()
        self.shapeCB.addItems(["Circle", "Square"])
        self.shapeCB.setCurrentIndex(0)
        self.shapeCB.currentIndexChanged.connect(lambda: self.changeShape())

        transLabel = QtGui.QLabel("Transparency")

        self.transSlider = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.transSlider.valueChanged[int].connect(self.changeTrans)

        visibleAreas = QtGui.QGroupBox("Visible Areas")
        visibleAreas.setToolTip("Cannot excede the maximum number indicated next to the labels")

        visibleAreasLayout = QtGui.QVBoxLayout()

        self.viewAll = QtGui.QRadioButton("View All Areas")
        self.viewAll.toggled.connect(self.viewAllAreas)

        self.surfaceAreaButton = QtGui.QRadioButton("Surface Area")
        self.surfaceAreaButton.toggled.connect(self.makeSurfaceArea)

        self.meshSurfaceButton = QtGui.QRadioButton("Mesh Surface Area")
        self.meshSurfaceButton.toggled.connect(self.meshSurfaceArea)
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
        submitButton.clicked.connect(self.changeViewAreas)

        spacer = QtGui.QSpacerItem(0, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        
        doge = QtGui.QLabel()
        dogeImg = QtGui.QPixmap("/Users/soorinpark/Documents/School/ShaheenGroup/OPV_GUI/dogeicon.png")
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
        
        self.pathWidgets = QtGui.QGroupBox("Path Visualization")
        self.pathWidgetLayout = QtGui.QVBoxLayout()

        self.loadPathButton = QtGui.QPushButton("Load Path File")
        self.loadPathButton.clicked.connect(self.loadPathFile)

        self.chargeIdLabel = QtGui.QLabel("Charge ID")
        
        self.chargeIdCB = QtGui.QComboBox()
        self.chargeIdCB.setEnabled(False)
        self.chargeIdCB.currentIndexChanged.connect(lambda: self.selectChargeID())

        self.pathWidgetLayout.setAlignment(QtCore.Qt.AlignTop)
        self.pathWidgetLayout.addWidget(self.loadPathButton)
        self.pathWidgetLayout.addWidget(self.chargeIdLabel)
        self.pathWidgetLayout.addWidget(self.chargeIdCB)
        self.pathWidgets.setLayout(self.pathWidgetLayout)
    
        self.xyzLayout.addWidget(self.xyzWidgets)
        self.plotLayout.addWidget(self.plotWidget)
        self.pathLayout.addWidget(self.pathWidgets)
        
        self.mainLayout.addLayout(self.plotLayout)
        self.mainLayout.addLayout(self.xyzLayout)
        self.mainLayout.addLayout(self.pathLayout)

        self.plotAlreadyThere = False
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

    def loadXYZFile(self):
        
        xyzFileName = QtGui.QFileDialog.getOpenFileName(self, 'Load XYZ File', '.')
        try:
            with open(xyzFileName) as xyzFile:
                xyzData = xyzFile.readlines()
        except IOError:
            return

        if not ".xyz" in xyzFileName:
            QtGui.QMessageBox.about(self, "Error", "Not a xyz File")
            return

        if self.plotAlreadyThere:
            for i in range(0, self.previousDataSize):
                self.size[i] = 0

        dataLen = len(xyzData)

        self.pos = empty((dataLen, 3))
        self.size = empty((dataLen))
        self.color = empty((dataLen, 4))

        self.coloristhere = False
        
        #All the data points
        energy = []
        for i, j in enumerate(xyzData):
            
            xyzData[i] = xyzData[i].split('\t')
            del xyzData[i][0] # delete "C"
            self.pos[i] = tuple(xyzData[i][0:3])
            self.size[i] = .5
            energy.append(xyzData[i][3])
            #color[i] = (1, 0, 0, 0.5)
   
        maxPos = self.pos[dataLen - 1]

        self.normEnergy = self.normalizeEnergy(energy)
   		
        for i, j in enumerate(self.normEnergy):
            self.color[i] = hot(self.normEnergy[i])
            self.coloristhere = True

		# insert surfaceArea code here if needed

        self.xMaxPos = int(maxPos[0])
        self.yMaxPos = int(maxPos[1])
        self.zMaxPos = int(maxPos[2])

        self.xPlaneLabel.setText("X-Plane: Max %i" % self.xMaxPos)
        self.yPlaneLabel.setText("Y-Plane: Max %i" % self.yMaxPos)
        self.zPlaneLabel.setText("Z-Plane: Max %i" % self.zMaxPos)

        self.plot = gl.GLScatterPlotItem(pos=self.pos, size=self.size, color=self.color, pxMode=False)
        self.plotWidget.addItem(self.plot)
        self.plotAlreadyThere = True
        self.previousDataSize = dataLen

    def makeSurfaceArea(self):
        
        self.surfaceMade = True
        self.newPos = [None] * len(self.pos)
        self.newColor = [None] * len(self.color)

        if self.surfaceAreaButton.isChecked():
           
            self.xPlaneLE.setEnabled(False)
            self.yPlaneLE.setEnabled(False)
            self.zPlaneLE.setEnabled(False)

            for i in range(0, len(self.pos)):
                self.size[i] = 0

            for i in range(0, len(self.pos)):
                
                self.newPos[i] = self.pos[i].tolist()
                self.newColor[i] = self.color[i].tolist()

                if self.pos[i][0] == 0:
                    self.xVerts1.append(self.newPos[i])
                    self.xColors1.append(self.newColor[i])
                    self.size[i] = .5
                
                elif self.pos[i][0] == 14:
                    self.xVerts2.append(self.newPos[i])
                    self.xColors2.append(self.newColor[i])
                    self.size[i] = .5

                elif self.pos[i][1] == 0:
                    self.yVerts1.append(self.newPos[i])
                    self.yColors1.append(self.newColor[i])
                    self.size[i] = .5

                elif self.pos[i][1] == 14:
                    self.yVerts2.append(self.newPos[i])
                    self.yColors2.append(self.newColor[i])
                    self.size[i] = .5

                elif self.pos[i][2] == 0:
                    self.zVerts1.append(self.newPos[i])
                    self.zColors1.append(self.newColor[i])
                    self.size[i] = .5

                elif self.pos[i][2] == 14:
                    self.zVerts2.append(self.newPos[i])
                    self.zColors2.append(self.newColor[i])
                    self.size[i] = .5

        else:

            self.xPlaneLE.setEnabled(True)
            self.yPlaneLE.setEnabled(True)
            self.zPlaneLE.setEnabled(True)

        self.meshSurfaceButton.setEnabled(True)

    def meshSurfaceArea(self):

        
        if self.surfaceMade and self.meshSurfaceButton.isChecked():
           
            xFaces1 = map(list, itertools.product(range(self.xMaxPos),repeat=3))
            print self.xColors1
            self.xVerts1 = np.array(self.xVerts1)
            print self.xVerts1

            print "0"
            xMeshData1 = gl.MeshData(vertexes=self.xVerts1)
            print xMeshData1
            #xMeshArea1 = gl.GLMeshItem(vertexes=xVertsPlane1, vertexColors = xColors1)
            #xMeshArea1 = gl.GLMeshItem(meshdata=xMeshData1, smooth=False)
            print "1"
            xMeshArea1 = gl.GLMeshItem(meshdata=xMeshData1)
            #xMeshArea1 = gl.GLMeshItem(vertexes=self.xVerts1)
            print "2"
            print type(self.xVerts1)
            print self.xVerts1.shape
            #xMeshArea1.setGLOptions('opaque')
            self.plotWidget.removeItem(self.plot)
            print "3"
            self.plotWidget.addItem(xMeshArea1)
            print "4"

            """
            meshArea = gl.GLMeshItem(vertexes=self.meshVerts, vetexColors=self.meshColors)
            #meshArea.translate()
            meshArea.setGLOptions('opaque')
            self.plotWidget.addItem(self.plot)
            """
        else:
            print "NO!!"

    def normalizeEnergy(self, energy):
        
        normEnergy = []
        energy = map(float, energy)
        minEnergy = min(energy)
        maxEnergy = max(energy)

        for i in range(0, len(energy)):
            
            norm = (energy[i] - minEnergy) / (maxEnergy - minEnergy)
            normEnergy.append(norm)
            #print norm
        
        return normEnergy
    
    def changeShape(self):
    
        if self.shapeCB.currentText() == "Square":
            self.transSlider.blockSignals(True)
            self.plot.setGLOptions('opaque')

        else:
            self.transSlider.blockSignals(False)
    
    def changeTrans(self, value):
      
        
        alpha = float(value)/float(100)
        print alpha
        try:
            if self.coloristhere:
                
                for i in range(0, len(self.normEnergy)):
                    self.color[i] = hot(self.normEnergy[i], alpha)

            if value >= 98:
            
                self.plot.setGLOptions('translucent')
       
            else:

                self.plot.setGLOptions('additive')
        except AttributeError:
            QtGui.QMessageBox.about(self, "Error", "Must load a xyz file first.")


    def viewAllAreas(self):

            if self.viewAll.isChecked():

                self.xPlaneLE.setEnabled(False)
                self.yPlaneLE.setEnabled(False)
                self.zPlaneLE.setEnabled(False)
                
                for i in range(0, len(self.pos)):
                    self.size[i] = .5

            else:

                self.xPlaneLE.setEnabled(True)
                self.yPlaneLE.setEnabled(True)
                self.zPlaneLE.setEnabled(True)
    
    def changeViewAreas(self): 
   
        if not self.plotAlreadyThere:
            QtGui.QMessageBox.about(self, "Error", "Must load a xyz file first.")

        xPlaneArea = self.parseAreaInput(self.xPlaneLE, self.xMaxPos)
        yPlaneArea = self.parseAreaInput(self.yPlaneLE, self.xMaxPos)
        zPlaneArea = self.parseAreaInput(self.zPlaneLE, self.xMaxPos)
        
        visualizeThese = []
        for i in range(0, len(self.pos)):
            for x in range(0, len(xPlaneArea)):
                for y in range(0, len(yPlaneArea)):
                    for z in range(0, len(zPlaneArea)):
                        self.size[i] = 0
                        if ((self.pos[i][0] == xPlaneArea[x]) and (self.pos[i][1] == yPlaneArea[y]) and (self.pos[i][2] == zPlaneArea[z])): 
                            visualizeThese.append(i)
                            
        for j in range(0, len(visualizeThese)):
            self.size[visualizeThese[j]] = .5
            #print j, self.pos[visualizeThese[j]]

    def parseAreaInput(self, planeArea, maxPos):
        
        planeAreaLE = planeArea
        planeArea = str(planeArea.text())
        planeArea = planeArea.split(",")
        
        temp1 = []
        temp2 = []

        for i in range(0,len(planeArea)):
            if "-" in planeArea[i]:
                
                temp = planeArea[i].split("-")
                foo = int(temp[0]) 
                bar = int(temp[1])
                temp1 = range(foo, bar+1)
                planeArea.extend(temp1)
                temp2.append(planeArea[i])
            
        
        for i in range(0,len(temp2)):
            planeArea.remove(temp2[i])  
    
        if not planeArea[0]:
            planeArea = range(0, maxPos)
            planeAreaLE.setText("0-%i" % maxPos) 
        else:
            planeArea = map(int, planeArea)
            planeArea.sort()

        return planeArea


    def loadPathFile(self):
    
        pathFileName = QtGui.QFileDialog.getOpenFileName(self, 'Load Path File', '.')
        try:
            with open(pathFileName) as pathFile:
                pathData = pathFile.readlines()
        except IOError:
            return

        if not ".path" in pathFileName:
            QtGui.QMessageBox.about(self, "Error", "Not a Path File")
            return
            
    	dataLen = len(pathData)

        self.pos = empty((dataLen, 3))
        self.size = empty((dataLen))
        self.color = empty((dataLen, 4))
      
        chargeIdColorCode = {
                
                0: (1, 0, 0, .5), # Red
                1: (1, .5, 0, .5), # Orange
                2: (1, 1, 0, .5), # Yellow
                3: (.5, 1, 0, .5), # Spring Green
                4: (0, 1, 0, .5), # Green
                5: (0, 1, .5, .5), # Turquoise
                6: (0, 1, 1, .5), # Cyan
                7: (0, .5, 1, .5), # Ocean
                8: (0, 0, 1, .5), # Blue
                9: (.5, 0, 1, .5), # Violet
                10: (1, 0, 1, .5), # Magenta
                11: (1, 0, .5, .5), # Raspberry

                }


        idList = []
        self.chargeIdDic = {}

        for i, j in enumerate(pathData):
            
            pathData[i] = pathData[i].split(' ')
            self.pos[i] = tuple(pathData[i][0:3])
            
            idList.append(pathData[i][3])
            chargeID = int(pathData[i][3])
            
            if chargeID in self.chargeIdDic.keys():
                self.chargeIdDic.setdefault(chargeID, []).append(i)
            else:
                self.chargeIdDic[chargeID] = [i]

            self.size[i] = .5
            self.color[i] = chargeIdColorCode[chargeID]
            
        idList = list(set(idList)) 
        idList.sort()
        self.chargeIdCB.setEnabled(True)
        self.chargeIdCB.addItems(["View All"])
        self.chargeIdCB.addItems(idList)
        self.chargeIdCB.setCurrentIndex(0)

        """
        idList = list(set(idList))
        print idList
        self.normID = self.normalizeChargeID(idList)
        
        for i, j in enumerate(self.normID):
            self.color[i] = hot(self.normID[i])
            print self.color[i]
            self.coloristhere = True
        """
            
        maxPos = self.pos[dataLen - 1]

        xMaxPos = int(maxPos[0])
        yMaxPos = int(maxPos[1])
        zMaxPos = int(maxPos[2])

        self.plot = gl.GLScatterPlotItem(pos=self.pos, size=self.size, color=self.color, pxMode=False)
        self.plotWidget.addItem(self.plot)
        self.plotAlreadyThere = True
        self.previousDataSize = dataLen
           

    def selectChargeID(self):
        
        chargeID = self.chargeIdCB.currentText()

        if chargeID == "View All":
            for i in range(0, len(self.pos)):
                self.size[i] = .5
        else:
            chargeID = int(chargeID)
            
            for i in range(0, len(self.pos)):
                self.size[i] = 0
               
            

            for k, v in self.chargeIdDic.iteritems():
                for i in range(0, len(self.pos)):
                    if chargeID == k:
                        self.size[v] = .5


def main():

    app = QtGui.QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
