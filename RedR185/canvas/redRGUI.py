from PyQt4.QtCore import *
from PyQt4.QtGui import *
import math, glob 
import redREnviron

import os.path
import imp
import redRi18n
# def _(a):
    # return a
_ = redRi18n.Coreget_()
class qtWidgetBox(QWidget):
    def __init__(self,widget):
        QWidget.__init__(self,widget)
        if widget and widget.layout():
            widget.layout().addWidget(self)
        self.setLayout(QVBoxLayout())
        self.layout().setSpacing(0)
        self.layout().setMargin(0)
        self.layout().setAlignment(Qt.AlignTop | Qt.AlignLeft)

       
class widgetState:
    def __init__(self,widget,widgetName,includeInReports,**args):
        
        self.controlArea = qtWidgetBox(widget)
        #print widgetName,self.controlArea
        if hasattr(self,'getReportText'):
            self.controlArea.getReportText = self.getReportText
        else:
            self.controlArea.getReportText = self.getReportTextDefault
        
        self.includeInReports=includeInReports
        
        if not widgetName:
            # print '#########widget Name is required############'
            raise RuntimeError(_('#########widget Name is required############'))

        self.widgetName = widgetName
    
    def hide(self):
        self.controlArea.hide()
    def show(self):
        self.controlArea.show()
    def setDisabled(self,e):
        self.controlArea.setDisabled(e)
    def setEnabled(self,e):
        self.controlArea.setEnabled(e)
        
    def getReportTextDefault(self,fileDir):
        # print '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'
        # print _('self'), self, self.widgetName
        children = self.children()
        # print children
        if len(children) ==0:
            return False
            
        reportData = {}
        for i in children:
            if isinstance(i, qtWidgetBox):
                d = i.getReportText(fileDir)
                if type(d) is dict:
                    reportData.update(d)
                # dd = []
                # if type(d) is dict:
                    # for x in d.items():
                        # x['includeInReports'] = i.includeInReports
                        # dd.append(x)
                    # reportData = reportData + dd
                # elif d:
                    # d['includeInReports'] = i.includeInReports
                    # reportData.append(d)
        
        return reportData
    
    def getDefaultState(self):
        r = {'enabled': self.controlArea.isEnabled(),'hidden': self.controlArea.isHidden()}
        return r
    def setDefaultState(self,data):
        # print _(' in wdiget state')
        self.controlArea.setEnabled(data['enabled'])
        self.controlArea.setHidden(data['hidden'])
    def getSettings(self):
        pass
    def loadSettings(self,data):
        pass
    
    def layout(self):
        return self.controlArea.layout()
    def setEnabled(self,b):
        self.controlArea.setEnabled(b)
        


# def forname(modname, classname):
    # ''' Returns a class of "classname" from module "modname". '''
    # module = __import__(modname)
    # classobj = getattr(module, classname)
    # return classobj

# current_module = __import__(__name__)
qtWidgets = []

def registerQTWidgets():   
    for package in os.listdir(redREnviron.directoryNames['libraryDir']): 
        if not (os.path.isdir(os.path.join(redREnviron.directoryNames['libraryDir'], package)) 
        and os.path.isfile(os.path.join(redREnviron.directoryNames['libraryDir'],package,'package.xml'))):
            continue
        try:
            directory = os.path.join(redREnviron.directoryNames['libraryDir'],package,'qtWidgets')
            for filename in glob.iglob(os.path.join(directory,  "*.py")):
                if os.path.isdir(filename) or os.path.islink(filename):
                    continue
                guiClass = os.path.basename(filename).split('.')[0]
                qtWidgets.append(guiClass)
        except:
           import redRLog
           redRLog.log(redRLog.REDRCORE, redRLog.ERROR,redRLog.formatException())


# def separator(widget, width=8, height=8):
    # sep = QWidget(widget)
    # if widget.layout(): widget.layout().addWidget(sep)
    # sep.setFixedSize(width, height)
    # return sep

    
# def rubber(widget):
    # widget.layout().addStretch(100)
