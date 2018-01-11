from redRGUI import widgetState
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import redRi18n
_ = redRi18n.get_(package = 'base')
class separator(QWidget,widgetState):
    def __init__(self,widget,width=8, height=8):
        widgetState.__init__(self, widget, 'separator',includeInReports=False)
        QWidget.__init__(self,self.controlArea)
        self.controlArea.layout().addWidget(self)       
        self.setFixedSize(width, height)


