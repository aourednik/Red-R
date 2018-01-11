from PyQt4.QtCore import *
from PyQt4.QtGui import *
from libraries.base.signalClasses.RDataFrame import *
class ShapeDataFrame(RDataFrame):
    def __init__(self, data, parent = None, checkVal = True):
        RDataFrame.__init__(self, data = data, parent = parent, checkVal = False)
        
    def convertToClass(self, valClass):
        if valClass == ShapeDataFrame:
            return self
        else:
            return RDataFrame.convertToClass(self, valClass)