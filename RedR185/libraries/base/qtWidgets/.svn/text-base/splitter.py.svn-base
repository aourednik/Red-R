## splitter Widget.  This widget provides a way to resize widgets within a main area.  To keep things working we won't allow widgets to be added to the splitter but will instead return areas into which widgets can be added using the conventional methods.

from redRGUI import widgetState
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from libraries.base.qtWidgets.widgetBox import widgetBox
import redRi18n
_ = redRi18n.get_(package = 'base')
class splitter(QSplitter, widgetState):
    def __init__(self, widget = None, orientation = 'horizontal'):
        widgetState.__init__(self,widget, 'splitter',includeInReports=False)
        QSplitter.__init__(self, widget)
        
        self.controlArea.layout().addWidget(self)
        
        if orientation == 'horizontal':
            self.setOrientation(Qt.Horizontal)
        else:
            self.setOrientation(Qt.Vertical)
            
    def widgetArea(self, orientation = 'horizontal', margin = -1):
        newWidgetBox = widgetBox(None, orientation = orientation, margin = margin)
        self.addWidget(newWidgetBox)
        return newWidgetBox
    def getSettings(self):
        r = {'sizes': self.sizes}
        return r
        
    def loadSettings(self, r):
        self.setSizes(r['sizes'])
        