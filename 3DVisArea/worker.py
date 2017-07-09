from PyQt4 import QtCore


class Worker(QtCore.QThread):
    def __init__(self, file, sig, xPlaneLabel, yPlaneLabel, zPlaneLabel):
        super(Worker, self).__init__()
        self.file = file
        self.sig = sig
        self.xPlaneLabel = xPlaneLabel
        self.yPlaneLabel = yPlaneLabel
        self.zPlaneLabel = zPlaneLabel

    def run(self):
        xyzData = list()
        if ".xyz" not in self.file:
            self.sig.emit(xyzData, False, self.xPlaneLabel, self.yPlaneLabel,
                          self.zPlaneLabel)
            return

        try:
            with open(self.file) as xyzFile:
                xyzData = xyzFile.readlines()
        except IOError:
            self.sig.emit(xyzData, False, self.xPlaneLabel, self.yPlaneLabel,
                          self.zPlaneLabel)
            return
        self.sig.emit(xyzData, True, self.xPlaneLabel, self.yPlaneLabel,
                      self.zPlaneLabel)
        # print(xyzData)
        # return xyzData
