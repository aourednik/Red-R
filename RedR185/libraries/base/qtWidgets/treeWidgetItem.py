# treeWidgetItem. implementation of the QTreeWidgetItem class

from redRGUI import widgetState
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import redRi18n
_ = redRi18n.get_(package = 'base')
class treeWidgetItem(QTreeWidgetItem):
    def __init__(self, widget = None, stringList = None, toolTip = None, flags=None):
        #widgetState.__init__(self,widget, _('treeWidgetItem'),includeInReports=False)
        if stringList:
            QTreeWidgetItem.__init__(self, stringList)
        else:
            QTreeWidgetItem.__init__(self)
            
        if widget:
            widget.addTopLevelItem(self)
            
        if toolTip:
            self.setToolTip(toolTip)
        if flags:
            self.setFlags(flags);
            
    def text(self,col):
        return str(QTreeWidgetItem.text(self,col))
    
    # def setData(self,col,role,val):
        # print col,role,val
        # QTreeWidgetItem.setData(self,col,role,val)
        
    def getSettings(self):
        r = {}
        r['text'] = []
        for i in range(self.columnCount()):
            try:
                r['text'].append(self.text(i))
            except:
                r['text'].append(None)
            
        r['childSettings'] = []
        for i in range(self.childCount()):
            r['childSettings'].append(self.child(i).getSettings())
        return r
    def loadSettings(self, data):
        try:
            ## set the text
            for i in range(len(data['text'])):
                try:
                    if data['text'][i]:
                        self.setText(i, data['text'][i])
                except:
                    continue
        except Exception as inst:
            print inst, _('Error setting text')
        ## load the child items
        try:
            if len(data['childSettings']) > 0:
                for i in range(len(data['childSettings'])):
                    try:    
                        newItem = treeWidgetItem()
                        newItem.loadSettings(data['childSettings'][i])
                        self.addChild(newItem)
                    except:
                        continue
        except Exception as inst:
            print inst, _('Exception occured in loading child items.')
