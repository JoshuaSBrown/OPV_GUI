#!/usr/local/bin/python
""" 

OPV GUI
Written by Soo Park 2016 for Shaheen Group @ CU Boulder
Contact: soo.park@colorado.edu

"""

import sys
import yaml
import re
from PyQt4 import QtGui, QtCore

class MainWindow(QtGui.QWidget):
    
    def __init__(self):
        super(MainWindow, self).__init__()
       
       	self.primaryLayout = QtGui.QVBoxLayout()
        self.secondaryLayout = QtGui.QGridLayout()
        
        self.scrollArea = QtGui.QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QtGui.QWidget(self.scrollArea)
        self.scrollAreaWidgetContents.setLayout(self.secondaryLayout)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        
        self.loadButton = QtGui.QPushButton("Load")
        self.loadButton.clicked.connect(self.loadFile)
       
        self.saveButton = QtGui.QPushButton("Save")
        self.saveButton.clicked.connect(self.saveFile)

        self.primaryLayout.addWidget(self.loadButton)
        self.primaryLayout.addWidget(self.saveButton)
        self.primaryLayout.addWidget(self.scrollArea)
        
        self.paramDic = []
        index = 0
        config = self.parseConfig()
        
        for key1, val1 in config.iteritems():
            for param in val1:
                #print param
                for key2, val2 in param.iteritems():
                    
                    if len(val2) == 1:
                        
                        self.paramName = QtGui.QLabel(key2)
                        self.paramName.setToolTip(val2[0])
                        self.secondaryLayout.addWidget(self.paramName, index, 0)

                        self.lineEdit = QtGui.QLineEdit()
                        self.lineEdit.setToolTip(val2[0])
                        self.secondaryLayout.addWidget(self.lineEdit, index, 1)
                        
                        self.paramObjects = []
                        self.paramObjects.append(self.paramName)
                        self.paramObjects.append(self.lineEdit)
                        self.paramDic.append(self.paramObjects)

                    else:
                        
                        #print key2, val2
                        self.paramName = QtGui.QLabel(key2)
                        self.paramName.setToolTip(val2[0])
                        self.secondaryLayout.addWidget(self.paramName, index, 0)

                        self.comboBox = QtGui.QComboBox()
                       
                        for index2 in range(0, len(val2)):
                            if index2 > 0:
                                
                                self.comboBox.addItems(str(val2[index2]))
                                self.comboBox.setCurrentIndex(-1)
                                self.comboBox.setToolTip(val2[0])
                                self.secondaryLayout.addWidget(self.comboBox, index, 1)

                        self.paramObjects = []
                        self.paramObjects.append(self.paramName)
                        self.paramObjects.append(self.comboBox)
                        self.paramDic.append(self.paramObjects)
                               

                        if key2 == "method":
                            
                            self.comboBox.currentIndexChanged.connect(lambda: self.methodParamSetup())
                            

                    index = index + 1
   
        # testing purposes
        #for index3, value3 in enumerate(self.paramDic):
        #    print self.paramDic[index3][0].text()

        self.setLayout(self.primaryLayout)
        self.resize(300, 600)
        self.center()
        self.setWindowTitle('OPV GUI')
        self.show()

    def methodParamSetup(self):
        
        method = self.paramDic[0][1].currentText()
        method = int(method)
        
        if method == 0:
           
            self.paramDic[74][1].setText("0.0")
            self.paramDic[74][1].setEnabled(False)

            self.paramDic[75][1].setText("0.0")
            self.paramDic[75][1].setEnabled(False)

            self.paramDic[76][1].setText("0.0")
            self.paramDic[76][1].setEnabled(False)

            self.paramDic[48][1].clear()
            self.paramDic[48][1].setEnabled(True)

        else:

            self.paramDic[48][1].setText("0")
            self.paramDic[48][1].setEnabled(False)

            self.paramDic[74][1].clear()
            self.paramDic[74][1].setEnabled(True)

            self.paramDic[75][1].clear()
            self.paramDic[75][1].setEnabled(True)

            self.paramDic[76][1].clear()
            self.paramDic[76][1].setEnabled(True)
    
    def loadFile(self):

        loadFileName = QtGui.QFileDialog.getOpenFileName(self, 'Load file', '/Users/soorinpark/Documents/School/ShaheenGroup/OPV_GUI')
    
    def saveFile(self):

        period = 0
        elec = 0
        end = 0
        xon = 0
        yon = 0
        zon = 0
        xyz = 0

        for index, value in enumerate(self.paramDic):
            
            # X
            if (self.paramDic[index][0].text() == "PeriodicX" and self.paramDic[index][1].currentText() == "1"):
                print "1", self.paramDic[index][1].currentText()
                period = 1
            if (self.paramDic[index][0].text() == "XElecOn" and self.paramDic[index][1].currentText() == "1"):
                print "2", self.paramDic[index][1].currentText()
                elec = 1
                xon = 1
            if (self.paramDic[index][0].text() == "EndX" and self.paramDic[index][1].currentText() == "0"):
                print "3", self.paramDic[index][1].currentText()
                end = 1
                xyz = "X"

            # Y
            if (self.paramDic[index][0].text() == "PeriodicY" and self.paramDic[index][1].currentText() == "1"):
                print "1", self.paramDic[index][1].currentText()
                period = 1
            if (self.paramDic[index][0].text() == "YElecOn" and self.paramDic[index][1].currentText() == "1"):
                print "2", self.paramDic[index][1].currentText()
                elec = 1
                yon = 1
            if (self.paramDic[index][0].text() == "EndY" and self.paramDic[index][1].currentText() == "0"):
                print "3", self.paramDic[index][1].currentText()
                end = 1
                xyz = "Y"

            # Z
            if (self.paramDic[index][0].text() == "PeriodicZ" and self.paramDic[index][1].currentText() == "1"):
                print "1", self.paramDic[index][1].currentText()
                period = 1
            if (self.paramDic[index][0].text() == "ZElecOn" and self.paramDic[index][1].currentText() == "1"):
                print "2", self.paramDic[index][1].currentText()
                elec = 1
                zon = 1
            if (self.paramDic[index][0].text() == "EndZ" and self.paramDic[index][1].currentText() == "0"):
                print "3", self.paramDic[index][1].currentText()
                end = 1
                xyz = "Z"

        if (period == 1 and elec == 1 and end == 1):
            QtGui.QMessageBox.about(self, "Warning", "Periodic%s = 1, %sElecOn = 1, therefore End%s cannot be 0. Please go back and edit End%s." % (xyz, xyz, xyz, xyz))
            return 


        if (period == 0 and elec == 0 and end == 0):
            QtGui.QMessageBox.about(self, "Warning", "At least one set of electrodes (*ElecOn) must be on")
            return


        saveFileName = QtGui.QFileDialog.getSaveFileName(self, 'Save File', '/Users/soorinpark/Documents/School/ShaheenGroup/OPV_GUI', selectedFilter='*.txt')
        #saveFile = open(saveFileName, 'w')

        with open(saveFileName, 'a') as saveFile:
            for index, value in enumerate(self.paramDic):
                #print self.paramDic[index][0].text(), self.paramDic[index][1].text()
                try:

                    data = self.paramDic[index][0].text() + " " + self.paramDic[index][1].text()
                    print data
                    saveFile.write(data)
                   
                except AttributeError:
                        
                    data = self.paramDic[index][0].text() + " " + self.paramDic[index][1].currentText() 
                    print data
                    saveFile.write(data)
                    

    def parseConfig(self):

        with open("config.yaml", 'r') as config:
            configFile = yaml.load(config)
            prettyConfigFile = yaml.dump(configFile, default_flow_style = False)
            #print prettyConfigFile
            return configFile
            
    def center(self):
        
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()    
