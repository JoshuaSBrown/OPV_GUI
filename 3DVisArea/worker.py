from PyQt4 import QtCore


class Worker(QtCore.QThread):
    def __init__(self, file, sig, fType):
        super(Worker, self).__init__()
        self.file = file
        self.sig = sig
        self.fType = fType

    def run(self):
        xyzData = list()
        try:
            with open(self.file) as xyzFile:
                xyzData = xyzFile.readlines()
        except IOError:
            self.sig.emit(xyzData, False)
            return
        self.sig.emit(xyzData, True)
        # print(xyzData)
        # return xyzData


class Slave(QtCore.QThread):
    def __init__(self, xyzData, energy, begin, end, pos, sig):
        super(Slave, self).__init__()
        self.xyzData = xyzData
        self.energy = energy
        self.begin = begin
        self.end = end
        self.pos = pos
        self.sig = sig

    def run(self):
        for i in range(self.begin, self.end):
            self.xyzData[i] = self.xyzData[i].split('\t')
            # self.xyzData[i] = self.xyzData[i].split('\t')
            # print self.xyzData[i]
            del self.xyzData[i][0]  # delete "C"
            self.pos[i] = tuple(self.xyzData[i][0:3])
            self.energy[i] = self.xyzData[i][3]
            # progress.setText(str(i) + "/" + str(dataLen))
        self.sig.emit(self.xyzData, self.energy, self.pos, self.begin,
                      self.end)

def clearBox(plotWidget):
    items = plotWidget.items
    for i in range(3, len(items)):
        plotWidget.removeItem(items[i])
