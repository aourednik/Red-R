from libraries.base.signalClasses.RDataFrame import *
import time
class RMatrix(RDataFrame):
    convertFromList = [RDataFrame, StructuredDict]
    convertToList = [RDataFrame, StructuredDict, UnstructuredDict, RVariable, RList]
    def __init__(self, data, parent = None, checkVal = True):
        RDataFrame.__init__(self, data = data, parent = parent, checkVal = False)
        if checkVal and self.getClass_data() not in ['matrix', 'numeric', 'complex']:
            raise Exception('not a Matrix.') # there this isn't the right kind of data for me to get !!!!!

        self.RDataFrameSignal = None
        self.RListSignal = None
        self.StructuredDictSignal = None
        self.newDataID = unicode(time.time()).replace('.', '_')
        self.matrix = None
        
    def convertFromClass(self, signal):
        if isinstance(signal, RDataFrame):
            return self._convertFromRDataFrame(signal)
        elif isinstance(signal, StructuredDict):
            return self._convertFromStructuredDict(signl)
            
    def _convertFromStructuredDict(self, signal):
        self.assignR('matrixConversion'+self.newDataID, signal.getData())
        return RMatrix(data = 'as.matrix('+'matrixConversion'+self.newDataID+')')
    def _convertFromRDataFrame(self, signal):
        #self.R('matrix_'+self.newDataID+'<-apply(data.matrix('+signal.getData()+'),2, as.numeric)', wantType = 'NoConversion')
        if not self.matrix:
            self.matrix = RMatrix(data = 'data.matrix('+signal.getData()+')')
            return RMatrix(data = 'data.matrix('+signal.getData()+')')
        else:
            return self.matrix
    def convertToClass(self, varClass):
        if varClass == RVariable:
            return self._convertToVariable()
        elif varClass == RDataFrame:
            return self._convertToRDataFrame()
        elif varClass == RList:
            return self._convertToRList()
        elif varClass == RMatrix:
            return self
        elif varClass == StructuredDict:
            return self._convertToStructuredDict()
        elif varClass == UnstructuredDict:
            return self._convertToStructuredDict()
        else:
            raise Exception
        
    def _convertToStructuredDict(self):
        if not self.StructuredDictSignal:
            data = self.R('as.data.frame('+self.data+')', wantType = 'dict')
            keys = ['row_names']
            keys += self.R('colnames(as.data.frame('+self.data+'))', wantType = 'list')
            rownames = self.R('rownames('+self.data+')', wantType = 'list')
            if rownames[0] in [None, 'NULL', 'NA']:
                rownames = [unicode(i+1) for i in range(len(data[data.keys()[0]]))]
            data['row_names'] = rownames
            self.StructuredDictSignal = StructuredDict(data = data, parent = self, keys = keys)
            return self.StructuredDictSignal
        else:
            return self.StructuredDictSignal
    def _convertToRDataFrame(self):
        if not self.RDataFrameSignal:
            self.RDataFrameSignal = RDataFrame(data = 'as.data.frame('+self.data+')', parent = self.parent)
            self.RDataFrameSignal.dictAttrs = self.dictAttrs.copy()
            return self.RDataFrameSignal
        else:
            return self.RDataFrameSignal
    def _convertToRList(self):
        if not self.RListSignal:
            self.RListSignal = RList(data = 'as.list(as.data.frame('+self.data+'))')
            self.RListSignal.dictAttrs = self. dictAttrs.copy()
            return self.RListSignal
        else:
            return self.RListSignal
    def deleteSignal(self):
        self.R('if(exists("matrixConversion'+self.newDataID+'")){rm(matrixConversion'+self.newDataID+')}', wantType = 'NoConversion')