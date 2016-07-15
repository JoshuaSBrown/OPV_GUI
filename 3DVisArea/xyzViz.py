#!/usr/local/bin/python

import sys
from PyQt4 import QtGui, QtCore
import pyqtgraph.examples
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from numpy import *
from matplotlib.cm import *
import itertools

class xyzViz(QtGui.QWidget):
    def __init__(self):
        super(xyzViz, self).__init__()

        # add init here

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

def main():

    app = QtGui.QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

