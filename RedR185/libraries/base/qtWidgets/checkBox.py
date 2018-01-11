from redRGUI import widgetState
from libraries.base.qtWidgets.widgetBox import widgetBox
from libraries.base.qtWidgets.groupBox import groupBox
from OrderedDict import OrderedDict
import redRReports,redRLog

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import redRi18n
_ = redRi18n.get_(package = 'base')
class checkBox(widgetState,QWidget):
    def __init__(self,widget,label = None, displayLabel= True, includeInReports=True,
    buttons = None,toolTips = None, setChecked=None,
    orientation='vertical',callback = None):
        
        if toolTips and len(toolTips) != len(buttons):
            raise RuntimeError(_('Number of buttons and toolTips must be equal'))
 
        QWidget.__init__(self,widget)
        widgetState.__init__(self,widget,label,includeInReports)
        
        self.controlArea.layout().setAlignment(Qt.AlignTop | Qt.AlignLeft)

        self.controlArea.layout().addWidget(self)

        if displayLabel:
            self.box = groupBox(self.controlArea,label=label,orientation=orientation)
            # self.layout().addWidget(self.box)
        else:
            self.box = widgetBox(self.controlArea,orientation=orientation)
        
        # if orientation=='vertical':
            # self.box.setSizePolicy(QSizePolicy(QSizePolicy.Preferred,
            # QSizePolicy.MinimumExpanding))
        # else:
            # self.box.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding,
            # QSizePolicy.Preferred))
            
        self.label = label
        self.items = OrderedDict()
        self.buttons = QButtonGroup(self.box)
        self.buttons.setExclusive(False)
        if buttons:
            self.addButtons(buttons)

        # if buttons:
            # for i,b in zip(range(len(buttons)),buttons):
                # w = QCheckBox(b,self.box)
                # if toolTips:
                    # w.setToolTip(toolTips[i])
                # self.buttons.addButton(w,i)
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
        w = QCheckBox(text)
        if toolTip:
            w.setToolTip(toolTip)
        self.buttons.addButton(w,self.items.keys().index(id))
        self.box.layout().addWidget(w)
                    
    def setSizePolicy(self, h,w):
        # self.controlArea.setSizePolicy(h,w)
        # QWidget.setSizePolicy(self,h,w)
        self.box.setSizePolicy(h,w)
            
    def setChecked(self,ids):
        for i in self.buttons.buttons():
            id = self.buttons.id(i)
            if unicode(self.items.keys()[id]) in ids: i.setChecked(True)
            else: i.setChecked(False)
    
    def checkAll(self):
        for i in self.buttons.buttons():
            i.setChecked(True)
    def uncheckAll(self):
        for i in self.buttons.buttons():
            i.setChecked(False)
        
    def getChecked(self):
        return self.getCheckedItems().values()
        # checked = []
        # for i in self.buttons.buttons():
            # if i.isChecked(): checked.append(unicode(i.text()))
        # return checked
    def getCheckedIds(self):
        return self.getCheckedItems().keys()
        # checked = []
        # for i in self.buttons.buttons():
            # if i.isChecked(): checked.append(self.items.keys()[i.id()])
        # return checked
        
    def getCheckedItems(self):
        checked = {}
        for i in self.buttons.buttons():
            id = self.buttons.id(i)
            if i.isChecked(): checked[self.items.keys()[id]] = self.items[self.items.keys()[id]]
        return checked
        
    def getUnchecked(self):
        unChecked = []
        for i in self.buttons.buttons():
            if not i.isChecked(): unChecked.append(unicode(i.text()))
        return unChecked
    
    def buttonAt(self,ind):
        return unicode(self.buttons.button(ind).text())
                
    def getSettings(self):
        #print _('radioButtons getSettings') + self.getChecked()
        r = {'items':self.items, 'checked': self.getCheckedIds()}
        return r
    def loadSettings(self,data):
        #print _('radioButtons loadSettings') + data
        #self.addButtons(data['items'])
        self.setChecked(data['checked'])
        
    def getReportText(self, fileDir):
        selected = self.getChecked()

        if len(selected):
            text='Checked: ' + ', '.join(selected)
        else:
            text= _('Nothing Checked')
        r = {self.widgetName:{'includeInReports': self.includeInReports, 'text': text}}
        # print '@@@@@@@@@@@@@@@@@@@@@@@', r
        #t = 'The following items were checked in %s:\n\n%s\n\n' % (self.label, self.getChecked())
        return r

