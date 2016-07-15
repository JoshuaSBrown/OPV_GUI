#!/usr/local/bin/python

import sys
from PyQt4 import QtGui, QtCore
import pyqtgraph.examples
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from numpy import *
from matplotlib.cm import *
import itertools

class percViz(QtGui.QWidget):
    def __init__(self):
        super(percViz, self).__init__()