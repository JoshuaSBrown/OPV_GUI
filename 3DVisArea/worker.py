from PyQt4 import QtCore


class Worker(QtCore.QThread):
    def __init__(self, file, sig, fType):
        super(Worker, self).__init__()
        self.file = file
        self.sig = sig
        self.fType = fType

    def run(self):
        xyzData = list()
        if self.fType not in self.file:
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
