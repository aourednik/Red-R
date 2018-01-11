from redRGUI import widgetState
from libraries.base.qtWidgets.widgetBox import widgetBox
from libraries.base.qtWidgets.groupBox import groupBox

import redRReports,redRLog
from OrderedDict import OrderedDict

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import redRi18n
_ = redRi18n.get_(package = 'base')
class radioButtons(widgetState,QWidget):
    def __init__(self,widget,label=None, displayLabel=True, includeInReports=True,
    buttons=None,toolTips = None, setChecked = None,
    orientation='vertical',callback = None, **args):
        
        QWidget.__init__(self,widget)
        widgetState.__init__(self,widget,label,includeInReports,**args)
        
        self.controlArea.layout().setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.label = label
        

        if displayLabel:
            self.box = groupBox(self.controlArea,label=label,orientation=orientation)
            self.controlArea.layout().addWidget(self.box)
        else:
            self.box = widgetBox(self.controlArea,orientation=orientation)

        # if orientation=='vertical':
            # self.box.setSizePolicy(QSizePolicy(QSizePolicy.Preferred,
            # QSizePolicy.MinimumExpanding))
        # else:
            # self.box.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding,
            # QSizePolicy.Preferred))
        
        self.items = OrderedDict()
        self.buttons = QButtonGroup(self.box)
        if buttons:
            self.addButtons(buttons)

        # for i,b in zip(range(len(buttons)),buttons):
            # w = QRadioButton(b)
            # if toolTips:
                # w.setToolTip(toolTips[i])
            # self.buttons.addButton(w)
            # self.box.layout().addWidget(w)

        if callback:
            QObject.connect(self.buttons, SIGNAL('buttonClicked(int)'), callback)

        if setChecked:
            self.setChecked(setChecked)
    
    def addButtons(self,buttons):
        if type(buttons) in [dict,OrderedDict]:
            for k,v in buttons.items():
                self.addButton(k,v)
        elif type(buttons) in [list]:
            if len(buttons) > 0 and type(buttons[0]) is tuple:
                for k,v in buttons:
                    self.addButton(k,v)
            else:
                for v in buttons:
                    self.addButton(v,v)

            # redRLog.log(redRLog.REDRCORE,redRLog.DEBUG,_('In radioButtons should not use list'))
        else:
            raise Exception(_('In radioButtons, addButtons takes a list, dict or OrderedDict'))

    def addButton(self,id, text,toolTip=None):
        self.items[id] = text
        w = QRadioButton(text)
        if toolTip:
            w.setToolTip(toolTip)
        self.buttons.addButton(w,self.items.keys().index(id))
        self.box.layout().addWidget(w)
        
    def setChecked(self,id):
        buttons = self.buttons.buttons()
        try:
            self.buttons.button(self.items.keys().index(id)).setChecked(True)
        except:
            pass
        # for i in self.buttons.buttons():
            # if i.text() == id: i.setChecked(True)
            # else: i.setChecked(False)
    def getCheckedItem(self):
        buttonId = self.buttons.checkedId()
        if buttonId == -1:return
        return {self.items.keys()[buttonId]: self.items[self.items.keys()[buttonId]]}
    def getChecked(self):
        buttonId = self.buttons.checkedId()
        if buttonId == -1:return
        return self.items[self.items.keys()[buttonId]]
        
        # if button == 0 or button == None or button.isEnabled()==False: return 0
        # else: return unicode(button.text())
    def getCheckedId(self):
        buttonId = self.buttons.checkedId()
        if buttonId == -1:return
        return self.items.keys()[buttonId]
        
    def setSizePolicy(self, h,w):
        # self.controlArea.setSizePolicy(h,w)
        # QWidget.setSizePolicy(self,h,w)
        self.box.setSizePolicy(h,w)
    
    def disable(self,buttons):
        for i in self.buttons.buttons():
            if i.text() in buttons: i.setDisabled(True)

    def enable(self,buttons):
        for i in self.buttons.buttons():
            if i.text() in buttons: i.setEnabled(True)
    
    def getSettings(self):
        #print _('radioButtons getSettings') + self.getChecked()
        r = {'items':self.items, 'checked': self.getCheckedId()}
        return r
    def loadSettings(self,data):
        #print _('radioButtons loadSettings') + data
        #self.addButtons(data['items'])
        self.setChecked(data['checked'])
        
    def getReportText(self, fileDir):
        r = {self.widgetName:{'includeInReports': self.includeInReports, 'text': self.getChecked()}}
        return r


