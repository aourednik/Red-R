# treeWidget.  implementation of a QTreeWidget for redRGUI

from redRGUI import widgetState
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from libraries.base.qtWidgets.treeWidgetItem import treeWidgetItem
from libraries.base.qtWidgets.widgetBox import widgetBox
from libraries.base.qtWidgets.widgetLabel import widgetLabel

import redRi18n
_ = redRi18n.get_(package = 'base')
class treeWidget(QTreeWidget, widgetState):
    def __init__(self, widget, label = None, displayLabel=False, includeInReports=True, 
    orientation='vertical', toolTip = None, callback = None):
        
        widgetState.__init__(self,widget,label,includeInReports)

        QTreeWidget.__init__(self, self.controlArea)
        
        if displayLabel:
            self.hb = widgetBox(self.controlArea,orientation=orientation)
            widgetLabel(self.hb, label)
            if width != -1:
                sb = widgetBox(self.hb)
                sb.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.hb.layout().addWidget(self)
        else:
            self.controlArea.layout().addWidget(self)

        if toolTip: self.setToolTip(toolTip)
        if callback:
            QObject.connect(self, SIGNAL('currentItemChanged(QTreeWidgetItem*, QTreeWidgetItem*)'), callback)
    def setHeaderLabels(self, labels):
        self.labels = labels
        QTreeWidget.setHeaderLabels(self, labels)
   
    def getSettings(self):
        r = {}
        r['headerLabels'] = self.labels
        r['itemSettings'] = []
        for item in self.items():
            try:
                r.append(item.getSettings())
            except:
                continue
        return r

    def loadSettings(self,data):
        try:
            self.setHeaderLabels(data['headerLabels'])
            for item in data['itemSettings']:
                try:
                    newItem = treeWidgetItem()
                    newItem.loadSettings(item)
                    self.addTopLevelItem(newItem)
                except:
                    continue
        except:
            print _('Exception during setting assignment.')
