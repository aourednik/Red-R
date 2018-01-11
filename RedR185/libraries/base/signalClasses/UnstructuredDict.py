### Python Dictionary Class.  Contains python dictionary objects and can be the parent class of other classes, even R classes.

from signals import BaseRedRVariable

class UnstructuredDict(BaseRedRVariable):
    convertToList = [BaseRedRVariable]
    convertFromList = []
    def __init__(self, data, parent = None, keys = None, checkVal = True):
        BaseRedRVariable.__init__(self, data = data, parent = parent, checkVal = False)
        
        if checkVal:
            if type(data) not in [dict]:
                raise Exception, 'Data not of dictionary class'
            if keys:
                if len(keys) != len(self.data.keys()):
                    print 'WARNING! Key length not same as keys.  Ignoring keys.'
                    self.keys = self.data.keys()
                else:
                    self.keys = keys
            else:
                self.keys = self.data.keys()
        else:
            self.keys = None
    def getItem(self, name):
        #gets a required item from the signal, this does not query the dictAttrs but could return it.
        try:
            attr = getattr(self, name)
            return attr
        except:
            return None
    def convertToClass(self, varClass):
        if varClass == BaseRedRVariable:
            return self
        elif varClass == UnstructuredDict:
            return self
        else:
            raise Exception
