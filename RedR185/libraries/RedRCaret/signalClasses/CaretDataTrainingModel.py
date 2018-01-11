## RArbitraryList signal, all list signals inherit from this

from libraries.base.signalClasses.RArbitraryList import *

class CaretDataTrainingModel(RArbitraryList):
    convertFromList = [UnstructuredDict, StructuredDict]
    convertToList = [RVariable, UnstructuredDict, RArbitraryList]
    
    def __init__(self, data, parent, checkVal):
        RArbitraryList.__init__(self, data = data, parent = parent, checkVal = False)
        if checkVal and self.getClass_data() != 'list':
            raise Exception
            
    def convertFromClass(self, signal):
        return RArbitraryList.convertFromClass(self, signal)
        
    def convertToClass(self, varClass):
        if varClass == CaretDataTrainingModel:
            return self
        else:
            return RArbitraryList.convertToClass(self, varClass)
            