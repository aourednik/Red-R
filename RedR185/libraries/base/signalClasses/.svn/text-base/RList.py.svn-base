from libraries.base.signalClasses.RVariable import *
from libraries.base.signalClasses.UnstructuredDict import *
from libraries.base.signalClasses.StructuredDict import *
from libraries.base.signalClasses.RArbitraryList import *
import time
class RList(RArbitraryList, UnstructuredDict):
    convertFromList = [UnstructuredDict, StructuredDict]
    convertToList = [RVariable, UnstructuredDict, RArbitraryList]
    def __init__(self, data, parent = None, checkVal = True):
        RArbitraryList.__init__(self, data = data, parent = parent, checkVal = False)
        if checkVal and self.getClass_data() != 'list':
            raise Exception
        self.newDataID = unicode(time.time()).replace('.', '_')
    def convertFromClass(self, signal):
        if isinstance(signal, UnstructuredDict):
            return self._convertFromUnstructuredDict(signal)
        elif isinstance(signal, StructuredDict):
            return self._convertFromStructuredDict(signal)
            
    def _convertFromStructuredDict(self, signal):
        newVar = self.assignR('RListConversion_'+self.newDataID, signal.getData())
        return RList(data = 'as.list('+newVar+')')
    def _convertFromUnstructuredDict(self, signal):
        newVar = self.assignR('RListConversion_'+self.newDataID, signal.getData())
        return RList(data = 'as.list('+newVar+')')
    def convertToClass(self, varClass):
        if varClass == RVariable:
            return self._convertToVariable()
        elif varClass == BaseRedRVariable:
            return self._convertToVariable()
        elif varClass == RList:
            return self
        elif varClass == RArbitraryList:
            return self
        elif varClass == UnstructuredDict:
            return self._convertToUnstructuredDict()
        else:
            raise Exception
    def _convertToUnstructuredDict(self):
        return UnstructuredDict(data = self.R(self.getData(), wantType = 'dict'))
    def _convertToVariable(self):
        return self
    def _fullOutput(self, subsetting = ''):
        text = self._simpleOutput()+'\n\n'
        text += 'R Data Variable Value: '+self.getAttrOutput_data('data', subsetting)+'\n\n'
        text += 'R Data Variable Size: '+unicode(self.getLength_data())+' Elements\n\n'
        text += 'R Parent Variable Name: '+self.parent+'\n\n'
        text += 'R Parent Variable Value: '+self.getAttrOutput_data('parent', subsetting)+'\n\n'
        text += 'Class Dictionary: '+unicode(self.dictAttrs)+'\n\n'
        return text
        
        
    def names_call(self):
        return 'names('+self.data+')'
    def names_data(self):
        return self.R(self.names_call(), silent = True)
    def getLength_call(self):
        return 'length('+self.data+')'
    def getLength_data(self):
        return self.R(self.length_call(), silent = True)
    def getItem_call(self, item):
        if type(item) in [int, float, long]:
            item = int(item)
            return self.data+'[['+unicode(item)+']]'
        elif type(item) in [str]:
            return self.data+'[[\''+unicode(item)+'\']]'
        elif type(item) in [list]:
            newItemList = []
            for i in item:
                if type(i) in [int, float, long]:
                    newItemList.append(unicode(int(i)))
                elif type(i) in [str]:
                    newItemList.append('\"'+unicode(i)+'\"')
            return self.data+'[[c('+unicode(newItemList)[1:-1]+')]]'
        else:
            return self.data #just return all of the data and hope the widget picks up from there
    def getItem_data(self, item):
        call = self.getItem_call(item)
        if call != None:
            return self.R(call, silent = True) # should return a subsetted dictionary (dict)
        else:
            print 'No data to return'
            return {}
            
    def getDims_call(self):
        return 'dim('+self.data+')'
        
    def getDims_data(self):
        output = self.R(self.getDims_call(), wantType = 'list', silent = True)
        if output != None:
            return output
        else: return [0, 0]
    def getNames_call(self):
        return 'names('+self.data+')'
    def getNames_data(self):
        output = self.R(self.getNames_call(), wantType = 'list', silent = True)
        if output != None:
            return output
        else:
            return range(1, self.getDims_data()[0])