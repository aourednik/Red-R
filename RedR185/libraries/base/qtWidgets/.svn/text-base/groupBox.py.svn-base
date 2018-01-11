from redRGUI import widgetState
from libraries.base.qtWidgets.separator import separator

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import redRi18n
_ = redRi18n.get_(package = 'base')
class groupBox(QGroupBox,widgetState):
    def __init__(self,widget, label = None, displayLabel=True, includeInReports=True,
    orientation='vertical', addSpace=False, 
    sizePolicy = None, margin = -1, spacing = -1, flat = 0,alignment=Qt.AlignTop):        
        if label:
            widgetState.__init__(self,widget,label,includeInReports)
        else:
            widgetState.__init__(self,widget,_('Group Box'),includeInReports)
        
        if displayLabel:
            QGroupBox.__init__(self,label)
        else:
            QGroupBox.__init__(self)
       
        self.label = label
        self.controlArea.layout().addWidget(self)
        
        self.controlArea.layout().setAlignment(alignment)            

        try:
            if isinstance(orientation, QLayout):
                self.setLayout(orientation)
            elif orientation == 'horizontal' or not orientation:
                self.setLayout(QHBoxLayout())
            else:
                self.setLayout(QVBoxLayout())
        except:
            self.setLayout(QVBoxLayout())
            
        if self.layout() == 0 or self.layout() == None:
            self.setLayout(QVBoxLayout())

        if spacing == -1: spacing = 8
        self.layout().setSpacing(spacing)
        if margin != -1:
            self.layout().setMargin(margin)
        if widget:
            if addSpace and isinstance(addSpace, int):
                separator(self.controlArea, 0, addSpace)
            elif addSpace:
                separator(self.controlArea)
        
        if sizePolicy:
            self.setSizePolicy(sizePolicy)
        

    def layout(self):
        return QGroupBox.layout(self)
    
    def delete(self):
        
        # itemRange = self.layout().count()
        # for i in range(0, itemRange):
            # item = self.layout().itemAt(i)
            # if item.widget:
                # try:
                    # item.widget.delete()
                # except: pass
            # sip.delete(item)
        sip.delete(self)
        

