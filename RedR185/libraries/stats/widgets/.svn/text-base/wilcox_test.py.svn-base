"""
<name>Wilcoxon Test</name>
<tags>Non Parametric</tags>
<icon>stats.png</icon>
"""
from OWRpy import * 
import redRGUI
from libraries.base.signalClasses.RVariable import RVariable as redRRVariable
from libraries.base.signalClasses.RVector import RVector as redRRVector

from libraries.base.qtWidgets.textEdit import textEdit
from libraries.base.qtWidgets.button import button
from libraries.base.qtWidgets.commitButton import commitButton as redRCommitButton

class wilcox_test(OWRpy): 
    globalSettingsList = ['commit']
    def __init__(self, parent=None, signalManager=None):
        OWRpy.__init__(self)
        self.setRvariableNames(["wilcox.test"])
         
        self.RFunctionParam_x = ''
        self.RFunctionParam_y = ''
        self.inputs.addInput('id0', 'x', redRRVector, self.processx)
        self.inputs.addInput('id1', 'y', redRRVector, self.processy)

        self.outputs.addOutput('id0', 'wilcox.test Output', redRRVariable)

        

        self.commit = redRCommitButton(self.bottomAreaRight, "Commit", callback = self.commitFunction,
        processOnInput=True)
        self.RoutputWindow = textEdit(self.controlArea,label='R Output', displayLabel=False)
        
    def processx(self, data):
        if data:
            self.RFunctionParam_x=data.getData()
            self.status.setText('X data set to %s' % self.RFunctionParam_x)
            if self.commit.processOnInput():
                self.commitFunction()
    def processy(self, data):
        if data:
            self.RFunctionParam_y=data.getData()
            if self.commit.processOnInput():
                self.commitFunction()
    def commitFunction(self):
        if self.RFunctionParam_x == '': 
            self.status.setText('No X data available')
            return
        injection = []
        if self.RFunctionParam_y != '':
            injection.append(unicode('y='+unicode(self.RFunctionParam_y)))
        inj = ','.join(injection)
        self.R('txt<-capture.output('+self.Rvariables['wilcox.test']+'<-wilcox.test(x='+unicode(self.RFunctionParam_x)+','+inj+'))')
        self.RoutputWindow.clear()
        tmp = self.R('paste(txt, collapse ="\n")')
        self.RoutputWindow.insertHtml('<br><pre>'+tmp+'</pre>')
        self.rSend("id0", {"data":self.Rvariables["wilcox.test"]})
    def getReportText(self, fileDir):
        text = 'The wilkox test was performed on the incoming data X and Y.  A summary of the results is listed below:\n\n'
        text += unicode(self.RoutputWindow.toPlainText())+'\n\n'
        return text
