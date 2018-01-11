### Python Structured Dictionary Class.  Contains python dictionary objects and can be the parent class of other classes, even R classes.
### Dict must be a dictionary of lists and the lists must be of the same length.

from libraries.base.signalClasses.UnstructuredDict import *

class StructuredDict(UnstructuredDict):
    convertToList = [BaseRedRVariable, UnstructuredDict]
    convertFromList = []
    def __init__(self, data, parent = None, keys = None, checkVal = True):
        
        UnstructuredDict.__init__(self, data = data, parent = parent, keys = keys, checkVal = False)
        
        
        if checkVal:
            self.length = len(data[data.keys()[0]]) # the length of the first element
            if type(data) not in [dict]:
                raise Exception, 'Data not of dict type'
            
            for key in data.keys():
                if type(data[key]) not in [list]:
                    raise Exception, 'Data in '+unicode(key)+' not of list type'
                if len(data[key]) != self.length:
                    print data
                    raise Exception, 'Data in '+unicode(key)+' not of same length as data in first key.'
                        
            if keys and len(keys) != len(self.data.keys()):
                print 'WARNING! Key length not same as keys.  Ignoring keys.'
                self.keys = self.data.keys()
            elif keys:
                self.keys = keys
            else:
                self.keys = self.data.keys()
        else:
            self.keys = None
            self.length = None
    def getKeys(self):
        return self.keys
    def transpose(self):
        ## transpose the structured data
        
        newDict = {}
        newKeys = []
        if 'row_names' in self.data:
            for name in self.data['row_names']:
                newDict[name] = []
                newKeys.append(name)
        else:
            for i in range(len(self.data[self.data.keys()[0]])):
                newDict[unicode(i+1)] = []
                newKeys.append(unicode(i+1))
        if not self.keys or self.keys == None:
            keys = self.data.keys()
        else:
            keys = self.keys
        for i in range(len(self.data[self.data.keys()[0]])):
            for key in keys:
                newDict[newKeys[i]].append(self.data[key][i])
                
        newData = StructuredDict(data = newDict, parent = self, keys = newKeys)
        return newData
            
    def convertToClass(self, varClass):
        if varClass == BaseRedRVariable:
            return self
        elif varClass == UnstructuredDict:
            return self
        elif varClass == StructuredDict:
            return self
        else:
            raise Exception
            
    def getDims_data(self):
        return (len(self.data.keys()), self.length)