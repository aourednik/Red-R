from redRGUI import widgetState
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import os.path
import redRi18n
_ = redRi18n.get_(package = 'base')
class button(QPushButton,widgetState):
    def __init__(self,widget,label, callback = None, disabled=0, icon=None, 
    toolTip=None, width = None, height = None,alignment=Qt.AlignLeft, toggleButton = False):

        if icon and (not label or label == ''):
            widgetState.__init__(self,widget,os.path.basename(icon),includeInReports=False)
        else:
            widgetState.__init__(self,widget,label,includeInReports=False)
            
        if icon:
            QPushButton.__init__(self,QIcon(icon), label,self.controlArea)
        else:
            QPushButton.__init__(self,label,self.controlArea)

        self.controlArea.layout().addWidget(self)
        if alignment:
            self.controlArea.layout().setAlignment(self, alignment)
        
        if icon or width == -1:
            pass
        elif width: 
            self.setFixedWidth(width)
        elif len(label)*7+5 < 50:
            self.setFixedWidth(50)
        else:
            self.setFixedWidth(len(label)*7+5)
            
        if height:
            self.setFixedHeight(height)
        self.setDisabled(disabled)
        
        if toolTip:
            self.setToolTip(toolTip)
            
        if toggleButton:
            self.setCheckable(True)
            
        if callback:
            QObject.connect(self, SIGNAL("clicked()"), callback)
            
    def getSettings(self):
        pass
    def loadSettings(self,data):
        pass

