"""
<name>Summary</name>
<tags>R</tags>
"""
from OWRpy import * 
import redRGUI 
from libraries.base.signalClasses.RVariable import RVariable as redRRVariable
from libraries.base.qtWidgets.button import button
from libraries.base.qtWidgets.checkBox import checkBox
from libraries.base.qtWidgets.textEdit import textEdit
import redRi18n
_ = redRi18n.get_(package = 'base')
class summary(OWRpy): 
    globalSettingsList = ['commit']
    def __init__(self, parent=None, signalManager=None):
        OWRpy.__init__(self)
        self.setRvariableNames(["summary"])
        self.data = {}
         
        self.RFunctionParam_object = ''
        self.inputs.addInput('id0', _('R Variable Object'), redRRVariable, self.processobject)
        
        self.commit = redRCommitButton(self.bottomAreaRight, _('Commit'), callback = self.commitFunction,
        processOnInput=True)
        
        self.RoutputWindow = textEdit(self.controlArea, label = _("RoutputWindow"))
    def processobject(self, data):
        if not self.require_librarys(["base"]):
            self.status.setText(_('R Libraries Not Loaded.'))
            return
        if data:
            self.RFunctionParam_object=data.getData()
            self.data = data
            if self.commit.processOnInput():
                self.commitFunction()
        else:
            self.RFunctionParam_object=''
    def commitFunction(self):
        if unicode(self.RFunctionParam_object) == '': return
        self.R('txt<-capture.output(summary(object='+unicode(self.RFunctionParam_object)+'))', wantType = 'NoConversion')
        self.RoutputWindow.clear()
        tmp = self.R('paste(txt, collapse ="\n")')
        self.RoutputWindow.insertHtml('<br><pre>'+tmp+'</pre>')

