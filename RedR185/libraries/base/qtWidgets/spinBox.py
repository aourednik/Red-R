import redRGUI
from redRGUI import widgetState
from libraries.base.qtWidgets.widgetBox import widgetBox
from libraries.base.qtWidgets.widgetLabel import widgetLabel

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import redRi18n
_ = redRi18n.get_(package = 'base')
class spinBox(QDoubleSpinBox ,widgetState):
    def __init__(self, widget, label=None, displayLabel=True, includeInReports=True, value=None, 
    orientation='horizontal', decimals=0, max = None, min = None, callback=None, toolTip = None, *args):
        
        self.widget = widget
        
        widgetState.__init__(self,widget,label,includeInReports)
        QDoubleSpinBox.__init__(self)
        self.setDecimals(decimals)
        self.label = label
        if displayLabel:
            self.hb = widgetBox(self.controlArea,orientation=orientation)
            widgetLabel(self.hb, label)
            self.hb.layout().addWidget(self)
        else:
            self.controlArea.layout().addWidget(self)
        
        if max:
            self.setMaximum(int(max))
        if min:
            self.setMinimum(int(min))
        if toolTip:
            self.setToolTip(unicode(toolTip))
        self.setWrapping(True) # we always allow the spin box to wrap around
        if value:
            self.setValue(value)
        if callback:
            QObject.connect(self, SIGNAL('valueChanged(double)'), callback)
        
    def getSettings(self):
        value = self.value()
        prefix = self.prefix()
        suffix = self.suffix()
        singleStep = self.singleStep()
        min = self.minimum()
        max = self.maximum()
        r = {'value':value, 'prefix':prefix, 'suffix':suffix, 'singleStep':singleStep, 'max':max, 'min':min}
        return r
    def loadSettings(self,data):
        try:
            self.setValue(data['value'])
            self.setPrefix(data['prefix'])
            self.setSuffix(data['suffix'])
            self.setMaximum(data['max'])
            self.setMinimum(data['min'])
            self.setSingleStep(data['singleStep'])
        except:
            print _('Error occured in Spin Box loading')
            import traceback,sys
            print '-'*60
            traceback.print_exc(file=sys.stdout)
            print '-'*60
    def update(self, min, max):
        value = self.value()
        self.setMaximum(max)
        self.setMinimum(min)
        if value >= min and value <= max:
            self.setValue(value)
    def getReportText(self, fileDir):
        return {self.widgetName:{'includeInReports': self.includeInReports, 'text': str(self.value())}}
        
        
