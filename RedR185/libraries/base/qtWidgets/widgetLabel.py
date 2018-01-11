from redRGUI import widgetState
from libraries.base.qtWidgets.widgetBox import widgetBox as redRWidgetBox

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import redRi18n
_ = redRi18n.get_(package = 'base')
class widgetLabel(QLabel,widgetState):
    def __init__(self,widget,label = '', icon=None, wordWrap=False):
        widgetState.__init__(self,widget, _('widgetLabel'),includeInReports=False)
        QLabel.__init__(self,self.controlArea)
        # if icon:
            # icon = QIcon(icon)
            # box = redRWidgetBox(widget,orientation='horizontal')
            # box.layout().addWidget(icon)
            # box.layout().addWidget(self)
        # else:
        self.controlArea.layout().addWidget(self)
        if icon:
            label = "<img style='margin-left:5px' src=\"%s\" /> %s" % (icon, label)
        self.setText(label)
        self.setWordWrap(wordWrap)
    def text(self):
        return unicode(QLabel.text(self))
    def getSettings(self):
        # print _('in widgetLabel getSettings')
        r = {'text':self.text()}
        # print r
        return r
    def loadSettings(self,data):
        # print _('in widgetLabel loadSettings')
        # print data
        self.setText(data['text'])
        

