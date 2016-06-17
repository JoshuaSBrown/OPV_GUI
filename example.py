#!/usr/local/bin/python


import sys
import yaml
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
        self.primaryLayout.addWidget(self.loadButton)
        self.primaryLayout.addWidget(self.scrollArea)
        
        index = 0
        config = self.parseConfig()
        
        for key1, val1 in config.iteritems():
            for param in val1:
                #print param
                for key2, val2 in param.iteritems():
                    
                    if len(val2) == 1:
                        
                        self.paramName = QtGui.QLabel(key2)
                        self.secondaryLayout.addWidget(self.paramName, index, 0)

                        self.lineEdit = QtGui.QLineEdit()
                        self.secondaryLayout.addWidget(self.lineEdit, index, 1)
                    
                    else:
                        
                        # Parameter Names
                        self.paramName = QtGui.QLabel(key2)
                        self.secondaryLayout.addWidget(self.paramName, index, 0)

                        # Combo Box for options
                        self.comboBox = QtGui.QComboBox()
                        for order, items in enumerate(val2):
                            if order > 0:
                                self.comboBox.addItems(str(items))
                                self.secondaryLayout.addWidget(self.comboBox, index, 1)
                    
                    index = index + 1

        self.setLayout(self.primaryLayout)
        self.resize(300, 600)
        self.center()
        self.setWindowTitle('OPV GUI')
        self.show()

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
