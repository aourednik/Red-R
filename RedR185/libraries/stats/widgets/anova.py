"""
<name>Generic ANOVA</name>
<description>Performed ANOVA on any model or data received.  This can result in errors if inappropriate models are supplied.</description>
<tags>Advanced Stats</tags>
<icon>stats.png</icon>
"""
from OWRpy import * 
import redRGUI
from libraries.stats.signalClasses.RLMFit import RLMFit as redRRLMFit
from libraries.base.qtWidgets.textEdit import textEdit
from libraries.base.qtWidgets.button import button
from libraries.base.qtWidgets.groupBox import groupBox
from libraries.base.qtWidgets.commitButton import commitButton as redRCommitButton

class anova(OWRpy): 
    globalSettingsList = ['commit']
    def __init__(self, parent=None, signalManager=None):
        OWRpy.__init__(self)
        self.RFunctionParam_object = ''
        self.saveSettingsList.extend(['RFunctionParam_object'])
        self.inputs.addInput('id0', 'object', 'All', self.processobject)

        
        box = groupBox(self.controlArea, "Output")
        self.commit = redRCommitButton(self.bottomAreaRight, "Commit", callback = self.commitFunction,
        processOnInput=True)
        self.RoutputWindow = textEdit(box,label='R Output', displayLabel=False)
        
    def onLoadSavedSession(self):
        self.commitFunction()
        
    def processobject(self, data):
        if data:
            self.RFunctionParam_object=data.getData()
            if self.commit.processOnInput():
                self.commitFunction()
        else: self.RFunctionParam_object = ''
    def commitFunction(self):
        if self.RFunctionParam_object == '': return
        self.R('txt<-capture.output('+'anova(object='+unicode(self.RFunctionParam_object)+'))')
        self.RoutputWindow.clear()
        tmp = self.R('paste(txt, collapse ="\n")')
        self.RoutputWindow.insertPlainText(tmp)

