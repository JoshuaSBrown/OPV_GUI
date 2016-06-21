#!/usr/local/bin/python
"""

OPV GUI
Written by Soo Park 2016 for Shaheen Group @ CU Boulder
Contact: soo.park@colorado.edu

"""

import sys
from PyQt4 import QtGui, QtCore
from OpenGL.GL import *
from PyQt4.QtOpenGL import *
import pyqtgraph.examples
import pyqtgraph

class MainWindow(QtGui.QWidget):
    
    def __init__(self):
        super(MainWindow, self).__init__()
        #pyqtgraph.examples.run()
        
        pyqtgraph.plot(x=[0,1,2,4], y=[4,5,9,6])

def main():

    app = QtGui.QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
