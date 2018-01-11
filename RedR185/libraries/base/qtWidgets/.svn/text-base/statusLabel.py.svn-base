from redRGUI import widgetState
from libraries.base.qtWidgets.widgetBox import widgetBox as redRWidgetBox
from libraries.base.qtWidgets.widgetLabel import widgetLabel as redRwidgetLabel

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import redRi18n
_ = redRi18n.get_(package = 'base')
class statusLabel(QLabel,widgetState):
    def __init__(self,widget,label = '', wordWrap=True):
        widgetState.__init__(self, widget, 'statusLabel',includeInReports=False)
        QLabel.__init__(self,self.controlArea)
        # if icon:
            # icon = QIcon(icon)
            # box = redRWidgetBox(widget,orientation='horizontal')
            # box.layout().addWidget(icon)
            # box.layout().addWidget(self)
        # else:
        #widget.layout().addWidget(self)
        
        box = redRWidgetBox(self.controlArea,orientation='horizontal')
        
        self.controlArea.layout().addWidget(box)
        box.layout().addWidget(self)
        
        #self.statusIndicator = redRwidgetLabel(box,label='aaaaa  ')
        #widget.layout().addWidget(self.statusIndicator)
        self.status = 0
        self.setText(label)
        self.setWordWrap(wordWrap)
        
    def getSettings(self):
        # print _('in widgetLabel getSettings')
        r = {'text':self.text(),'status':self.status}
        print r
        return r
    def loadSettings(self,data):
        # print _('in widgetLabel loadSettings')
        print data
        self.setText(data['text'])
        self.setStatus(data['status'])
    def getReportText(self, fileDir):
        return ''
        
    def setText(self, string,color=None):
        # self.setStyleSheet("QLabel { background-color: #ffff00 }")
        #string = '<table><tr><td class="indicator">aaaaa</td><td>%s</td></tr></table>' % string
        if color:
            self.setStyleSheet("QLabel { background-color: %s }" % color)
            
        QLabel.setText(self, string)
        qApp.processEvents()    
    def setStatus(self, statusInt):
        self.status = statusInt
        if statusInt == 0: ## No valid data
            self.setText(_('No Data To Process'))
        elif statusInt == 1: ## New data not processed
            self.setText(_('New Data Received, Not Processed'),'#ffff00')
        elif statusInt == 2: ## data sent
            self.setText(_('Data Processed And Sent'),'#00ff00')
        elif statusInt == 3: ## Error
            self.setText(_('Error'),'#ff0000')
        elif statusInt == 4: ## Data Processing    
            self.setText(_('Data Processing...'),'#ffff00')
        elif statusInt == 5: ## Data Processing Complete
            self.setText(_('Data Processing Complete'),'#ffff00')
        

        qApp.processEvents()    