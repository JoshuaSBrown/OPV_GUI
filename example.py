#!/usr/local/bin/python


import sys
import yaml
from PyQt4 import QtGui, QtCore

class MainWindow(QtGui.QWidget):
    
    def __init__(self):
        super(MainWindow, self).__init__()
       
        self.layout = QtGui.QGridLayout()
        index = 0
        config = self.parseConfig()
        for key1, val1 in config.iteritems():
            for param in val1:
                print param
                for key2, val2 in param.iteritems():
                    if len(val2) == 1:
                        print "Not Combo Box"
                    else:
                        print "Combo Box"
                        
                        # Parameter Names
                        self.paramName = QtGui.QLabel(key2)
                        self.layout.addWidget(self.paramName, index, 0)

                        # Combo Box for options
                        self.comboBox = QtGui.QComboBox()
                        for order, items in enumerate(val2):
                            if order > 0:
                                self.comboBox.addItems(str(items))
                                self.layout.addWidget(self.comboBox, index, 1)
                    index = index + 1

        self.setLayout(self.layout)
        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle('OPV GUI')
    
    def parseConfig(self):

        with open("config.yaml", 'r') as config:
            configFile = yaml.load(config)
            prettyConfigFile = yaml.dump(configFile, default_flow_style = False)
            #print prettyConfigFile
            return configFile

def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()    
