"""
<name>Test For Correlation (Single)</name>
<author>Generated using Widget Maker written by Kyle R. Covington</author>
<RFunctions>stats:cor.test</RFunctions>
<tags>Parametric</tags>
<icon>stats.png</icon>
"""
from OWRpy import * 
import redRGUI 
from libraries.base.signalClasses.RVector import RVector as redRRVector
from libraries.base.qtWidgets.textEdit import textEdit
from libraries.base.qtWidgets.button import button
class cor_test(OWRpy): 
    settingsList = []
    def __init__(self, parent=None, signalManager=None):
        OWRpy.__init__(self)
        self.setRvariableNames(["cor.test"])
        self.data = {}
        self.RFunctionParam_y = ''
        self.RFunctionParam_x = ''
        self.inputs.addInput('id0', 'y', redRRVector, self.processy)
        self.inputs.addInput('id1', 'x', redRRVector, self.processx)

        redRCommitButton(self.bottomAreaRight, "Commit", callback = self.commitFunction)
        self.RoutputWindow = textEdit(self.controlArea, label = "RoutputWindow")
    def processy(self, data):
        if not self.require_librarys(["stats"]):
            self.status.setText('R Libraries Not Loaded.')
            return
        if data:
            self.RFunctionParam_y=data.getData()
            #self.data = data
            self.commitFunction()
        else:
            self.RFunctionParam_y=''
    def processx(self, data):
        if not self.require_librarys(["stats"]):
            self.status.setText('R Libraries Not Loaded.')
            return
        if data:
            self.RFunctionParam_x=data.getData()
            #self.data = data
            self.commitFunction()
        else:
            self.RFunctionParam_x=''
    def commitFunction(self):
        if unicode(self.RFunctionParam_y) == '': return
        if unicode(self.RFunctionParam_x) == '': return
        injection = []
        inj = ','.join(injection)
        self.R(self.Rvariables['cor.test']+'<-cor.test(y=as.numeric(as.character('+unicode(self.RFunctionParam_y)+')),x=as.numeric(as.character('+unicode(self.RFunctionParam_x)+')),'+','+inj+')')
        self.R('txt<-capture.output('+self.Rvariables['cor.test']+')')
        self.RoutputWindow.clear()
        tmp = self.R('paste(txt, collapse ="\n")')
        self.RoutputWindow.insertHtml('<br><pre>'+tmp+'</pre>')
    def getReportText(self, fileDir):
        text = 'Correlations were performed on the attached data vectors.  A summary of the results are below:\n\n'
        text += unicode(self.RoutputWindow.toPlainText())+'\n\n'
        return text
