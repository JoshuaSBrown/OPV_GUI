from PyQt4 import QtCore


class Worker(QtCore.QThread):

    def __init__(self, file, sig):
        super(Worker, self).__init__()
        self.file = file
        self.sig = sig

    def run(self):
        xyzData = list()
        if ".xyz" not in self.file:
            self.sig.emit(xyzData, False)
            return

        try:
            with open(self.file) as xyzFile:
                xyzData = xyzFile.readlines()
        except IOError:
            self.sig.emit(xyzData, False)
            return
        self.sig.emit(xyzData, True)
        # print(xyzData)
        # return xyzData
