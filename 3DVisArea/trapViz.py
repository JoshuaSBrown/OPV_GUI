#!/usr/bin/env python

import sys
from PyQt4 import QtGui, QtCore
import pyqtgraph.examples
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from numpy import *
from matplotlib.cm import *
import itertools
from worker import Worker


class trapViz(QtGui.QWidget):

    mysignal = QtCore.pyqtSignal(list, bool)

    def __init__(self):
        super(trapViz, self).__init__()

    def loadTrapFile(self, trapChargeIdCB, plotWidget):
        self.trapChargeIdCB = trapChargeIdCB
        self.plotWidget = plotWidget
        trapFileName = QtGui.QFileDialog.getOpenFileName(self, 'Load Trap File', '.')
        self.worker = Worker(trapFileName, self.mysignal, ".trap")
        self.worker.start()
        self.mysignal.connect(self.printData)
        # try:
        #     with open(trapFileName) as trapFile:
        #         trapData = trapFile.readlines()
        # except IOError:
        #     return

        # if not ".trap" in trapFileName:
        #     QtGui.QMessageBox.about(self, "Error", "Not a Trap File")
        #     return

    def printData(self, trapData, mybool):
        if not mybool:
            QtGui.QMessageBox.about(self, "Error",
                                    "Not a .xyz File or is currupted")
            return
        dataLen = len(trapData)

        self.pos = empty((dataLen, 3))
        self.size = empty((dataLen))
        self.color = empty((dataLen, 4))

        chargeIdColorCode = {

                0: (1, 0, 0, 1), # Red
                1: (1, .5, 0, 1), # Orange
                2: (1, 1, 0, 1), # Yellow
                3: (.5, 1, 0, 1), # Spring Green
                4: (0, 1, 0, 1), # Green
                5: (0, 1, .5, 1), # Turquoise
                6: (0, 1, 1, 1), # Cyan
                7: (0, .5, 1, 1), # Ocean
                8: (0, 0, 1, 1), # Blue
                9: (.5, 0, 1, 1), # Violet
                10: (1, 0, 1, 1), # Magenta
                11: (1, 0, .5, 1), # Raspberry

                }


        idList = []
        self.chargeIdDic = {}
        self.trapDataDic = {}
        self.plotDic = {}

        for i, j in enumerate(trapData):
            temp = trapData[i].split(' ')

            if (len(temp) == 2):
                currentKey = temp[0]
                self.trapDataDic.setdefault(temp[0], [])
                if currentKey not in idList:
                    idList.append(currentKey)
            else:
                self.trapDataDic[currentKey].append(temp)


        for k,v in self.trapDataDic.iteritems():

            dataLen = len(v)

            self.pos = empty((dataLen,3))
            self.size = empty((dataLen))
            self.color = empty((dataLen,4))

            for i,j in enumerate(v):

                self.pos[i] = tuple(v[i][0:3])
                self.size[i] = .5
                self.color[i] = chargeIdColorCode[int(k)]

            self.plotDic[k] = gl.GLScatterPlotItem(pos=self.pos, size=self.size, color=self.color, pxMode=False)

        idList.sort()
        self.trapChargeIdCB.setEnabled(True)
        self.trapChargeIdCB.addItems(["View All"])
        self.trapChargeIdCB.addItems(idList)
        self.trapChargeIdCB.setCurrentIndex(0)

        maxPos = self.pos[dataLen - 1]

        xMaxPos = int(maxPos[0])
        yMaxPos = int(maxPos[1])
        zMaxPos = int(maxPos[2])



        for k,v in self.plotDic.iteritems():
            self.plotWidget.addItem(self.plotDic[k])

        self.plotAlreadyThere = True
        self.previousDataSize = dataLen

    def selectTrapChargeID(self, plotWidget):

        chargeID = str(self.trapChargeIdCB.currentText())
        if chargeID != "View All":
            for k,v in self.plotDic.iteritems():
                try:
                    plotWidget.removeItem(self.plotDic[k])
                    print "removed: ", k, self.plotDic[k]
                except ValueError:
                    pass

        for k,v in self.plotDic.iteritems():
            if k == chargeID:
                print "added: ", k, self.plotDic[k]
                plotWidget.addItem(self.plotDic[k])
        """

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

        """
