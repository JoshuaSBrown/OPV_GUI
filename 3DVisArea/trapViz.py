#!/usr/local/bin/python

import sys
from PyQt4 import QtGui, QtCore
import pyqtgraph.examples
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from numpy import *
from matplotlib.cm import *
import itertools

class trapViz(QtGui.QWidget):
    def __init__(self):
        super(trapViz, self).__init__()