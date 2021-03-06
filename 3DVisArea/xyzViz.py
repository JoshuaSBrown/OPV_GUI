#!/usr/bin/env python

import sys
from PyQt4 import QtGui, QtCore
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from numpy import *
from matplotlib.cm import *
from worker import Worker, Slave  # , clearBox

# import itertools


class xyzViz(QtGui.QWidget):

    mysignal = QtCore.pyqtSignal(list, bool)
    slaves = QtCore.pyqtSignal(list, ndarray, ndarray, int, int)
    slaveArr = []

    def __init__(self):
        super(xyzViz, self).__init__()

    def loadXYZFile(self, plotWidget, plotAlreadyThere, xPlaneLabel,
                    yPlaneLabel, zPlaneLabel, progress_bar):
        self.__init__()
        self.plotWidget = plotWidget
        self.xPlaneLabel = xPlaneLabel
        self.yPlaneLabel = yPlaneLabel
        self.zPlaneLabel = zPlaneLabel
        self.progress = progress_bar
        widgetItems = plotWidget.items
        prevPlot = []
        self.color = []
        # self.xyzData = []

        if len(widgetItems) > 3:
            for i in range(3, len(widgetItems)):
                prevPlot.append(widgetItems[i])

#         try:
#             plotWidget.removeItem(prevPlot)
#         except:
#             print "No older plots to remove"
        self.dataLen = 0

        xyzFileName = QtGui.QFileDialog.getOpenFileName(
            self, 'Load XYZ File', '../Data')

        if ".xyz" not in xyzFileName:
            QtGui.QMessageBox.about(self, "Error",
                                    "Not a .xyz File or is currupted")
            return

        self.worker = Worker(xyzFileName, self.mysignal, ".xyz")
        self.worker.start()
        self.mysignal.connect(self.printData)

        if plotAlreadyThere:
            self.size = zeros(self.previousDataSize)

    def printData(self, xyzData, mybool):
        if not mybool:
            QtGui.QMessageBox.about(self, "Error",
                                    "Not a .xyz File or is currupted")
            return
        del xyzData[:2]
        dataLen = len(xyzData)
        self.xyzData = xyzData
        # All the data points
        self.energy = zeros(dataLen)
        self.normEnergy = self.energy[:]
        self.pos = empty((dataLen, 3))
        self.size = ones((dataLen)) / 2
        self.color = empty((dataLen, 4))
        self.previousDataSize = dataLen
        self.coloristhere = False
        self.slaves.connect(self.processData)
        numThreads = 10
        self.coloristhere = True
        self.numThreads = numThreads
        self.progress.setMaximum(self.numThreads)
        self.progress.setMinimum(0)
        self.progress.setValue(0)
        step = int(dataLen / numThreads)
        self.num = 0
        for i in range(1, numThreads):
            temp = Slave(self.xyzData, self.energy,
                         step * (i - 1), step * i, self.pos, self.slaves)
            temp.start()
            self.slaveArr.append(temp)
        final = Slave(self.xyzData, self.energy,
                      step * (numThreads - 1), dataLen, self.pos, self.slaves)
        final.start()
        self.slaveArr.append(final)

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

    def changeShape(self, shapeCB, transSlider):
        if shapeCB.currentText() == "Square":
            transSlider.blockSignals(True)
            # self.plot.setGLOptions('opaque')
            self.cubeViz()

        else:
            self.plot.setGLOptions('additive')
            transSlider.blockSignals(False)

    def changeTrans(self, value):
        alpha = float(value) / float(100)
        try:
            if self.coloristhere:

                for i in range(0, len(self.normEnergy)):
                    self.color[i] = hot(self.normEnergy[i], alpha)

            if value >= 98:

                self.plot.setGLOptions('translucent')

            else:

                self.plot.setGLOptions('additive')
        except AttributeError:
            QtGui.QMessageBox.about(self, "Error",
                                    "Must load a xyz file first.")

    def viewAllAreas(self, viewAll, xPlaneLE, yPlaneLE, zPlaneLE):
        if viewAll.isChecked():

            xPlaneLE.setEnabled(False)
            yPlaneLE.setEnabled(False)
            zPlaneLE.setEnabled(False)

            for i in range(0, len(self.pos)):
                self.size[i] = .5

        else:

            xPlaneLE.setEnabled(True)
            yPlaneLE.setEnabled(True)
            zPlaneLE.setEnabled(True)

    def changeViewAreas(self, plotAlreadyThere, xPlaneLE, yPlaneLE, zPlaneLE):
        if not plotAlreadyThere:
            QtGui.QMessageBox.about(self, "Error",
                                    "Must load a xyz file first.")

        xPlaneArea = self.parseAreaInput(xPlaneLE, self.xMaxPos)
        yPlaneArea = self.parseAreaInput(yPlaneLE, self.yMaxPos)
        zPlaneArea = self.parseAreaInput(zPlaneLE, self.zMaxPos)

        visualizeThese = []
        for i in range(0, len(self.pos)):
            for x in range(0, len(xPlaneArea)):
                for y in range(0, len(yPlaneArea)):
                    for z in range(0, len(zPlaneArea)):
                        self.size[i] = 0
                        if ((self.pos[i][0] == xPlaneArea[x])
                                and (self.pos[i][1] == yPlaneArea[y])
                                and (self.pos[i][2] == zPlaneArea[z])):
                            visualizeThese.append(i)

        for j in range(0, len(visualizeThese)):
            self.size[visualizeThese[j]] = .5

    def parseAreaInput(self, planeArea, maxPos):
        planeAreaLE = planeArea
        planeArea = str(planeArea.text())
        planeArea = planeArea.split(",")

        temp1 = []
        temp2 = []

        for i in range(0, len(planeArea)):
            if "-" in planeArea[i]:

                temp = planeArea[i].split("-")
                foo = int(temp[0])
                bar = int(temp[1])
                temp1 = range(foo, bar + 1)
                planeArea.extend(temp1)
                temp2.append(planeArea[i])

        for i in range(0, len(temp2)):
            planeArea.remove(temp2[i])

        if not planeArea[0]:
            planeArea = range(0, maxPos)
            planeAreaLE.setText("0-%i" % maxPos)
        else:
            planeArea = map(int, planeArea)
            planeArea.sort()

        return planeArea

    def processData(self, xyzData, energy, pos, begin, end):
        self.xyzData[begin:end] = xyzData[begin:end]
        self.energy[begin:end] = energy[begin:end]
        self.pos[begin:end] = pos[begin:end]
        self.num += 1
        print(self.num, "/", self.numThreads)
        self.progress.setValue(self.num)
        # self.show()
        if self.num == self.numThreads:
            energy = [float(i) for i in self.energy] # This is for python3 compatibility
            minEnergy = min(energy)
            maxEnergy = max(energy)
            # self.normEnergy = map(lambda x:(x - minEnergy)/(maxEnergy - minEnergy), energy)
            # self.progress.close()
            self.normEnergy = divide(
                subtract(energy, minEnergy), subtract(maxEnergy, minEnergy))
            self.color = hot(self.normEnergy)
            maxPos = self.pos[self.previousDataSize - 1]
            self.xMaxPos = int(maxPos[0])
            self.yMaxPos = int(maxPos[1])
            self.zMaxPos = int(maxPos[2])
            # self.xPlaneLabel.setText("X-Plane: Max %i" % self.xMaxPos)
            # self.yPlaneLabel.setText("Y-Plane: Max %i" % self.yMaxPos)
            # self.zPlaneLabel.setText("Z-Plane: Max %i" % self.zMaxPos)
            self.plot = gl.GLScatterPlotItem(
                pos=self.pos, size=self.size, color=self.color, pxMode=False)
            self.plotWidget.addItem(self.plot)
            self.plotAlreadyThere = True
