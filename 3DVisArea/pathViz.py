#!/usr/bin/env python

import sys
from PyQt4 import QtGui, QtCore
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from numpy import *
from matplotlib.cm import *
import itertools
from worker import Worker


class pathViz(QtGui.QWidget):

    mysignal = QtCore.pyqtSignal(list, bool)

    def __init__(self):
        super(pathViz, self).__init__()

        # add init here

    def loadPathFile(self, plotWidget, chargeIdCB):

        self.plotWidget = plotWidget
        widgetItems = self.plotWidget.items
        prevPlot = []

        if len(widgetItems) > 3:
            for i in range(3, len(widgetItems)):
                prevPlot.append(widgetItems[i])

        # print prevPlot

        # try:
        #     self.plotWidget.removeItem(prevPlot)
        #  catch:
        #     pass

        self.chargeIdCB = chargeIdCB
        pathFileName = QtGui.QFileDialog.getOpenFileName(
            self, 'Load Path File', '../Data')

        self.worker = Worker(pathFileName, self.mysignal, ".path")
        self.worker.start()
        self.mysignal.connect(self.printData)
        # try:
        #     with open(pathFileName) as pathFile:
        #         pathData = pathFile.readlines()
        # except IOError:
        #     return

        # if ".path" not in pathFileName:
        #     QtGui.QMessageBox.about(self, "Error", "Not a Path File")
        #     return

    def printData(self, pathData, mybool):

        if not mybool:
            QtGui.QMessageBox.about(self, "Error",
                                    "Not a .path File or is currupted")
            return

        dataLen = len(pathData)

        self.pos = empty((dataLen, 3))
        self.size = empty((dataLen))
        self.color = empty((dataLen, 4))

        chargeIdColorCode = {
            0: (1, 0, 0, .5),  # Red
            1: (1, .5, 0, .5),  # Orange
            2: (1, 1, 0, .5),  # Yellow
            3: (.5, 1, 0, .5),  # Spring Green
            4: (0, 1, 0, .5),  # Green
            5: (0, 1, .5, .5),  # Turquoise
            6: (0, 1, 1, .5),  # Cyan
            7: (0, .5, 1, .5),  # Ocean
            8: (0, 0, 1, .5),  # Blue
            9: (.5, 0, 1, .5),  # Violet
            10: (1, 0, 1, .5),  # Magenta
            11: (1, 0, .5, .5),  # Raspberry
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

        self.plot = gl.GLScatterPlotItem(
            pos=self.pos, size=self.size, color=self.color, pxMode=False)
        self.plotWidget.addItem(self.plot)
        self.plotAlreadyThere = True
        self.previousDataSize = dataLen

    def selectPathChargeID(self, chargeIdCB):

        chargeID = chargeIdCB.currentText()

        print(chargeID)

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

    def changeShape(self, shapeCB):

        if shapeCB.currentText() == "Square":
            transSlider.blockSignals(True)
            self.plot.setGLOptions('additive')

        else:
            self.plot.setGLOptions('additive')
            transSlider.blockSignals(False)
