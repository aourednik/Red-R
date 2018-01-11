"""
<name>Kruskal</name>
<description>Performs the Kruskal Walis test on data.</description>
<author>Generated using Widget Maker written by Kyle R. Covington</author>

<icon>stats.png</icon>
<tags>Non Parametric</tags>
<RFunctions>stats:kruskal.test</RFunctions>
"""
from OWRpy import * 
import redRGUI 
from libraries.base.signalClasses.RVariable import RVariable as redRRVariable
from libraries.base.qtWidgets.RFormulaEntry import RFormulaEntry
from libraries.base.qtWidgets.button import button
from libraries.base.qtWidgets.textEdit import textEdit
class kruskal_test(OWRpy): 
    settingsList = []
    def __init__(self, parent=None, signalManager=None):
        OWRpy.__init__(self)
         
        self.RFunctionParam_data = ''
        self.inputs.addInput('id0', 'data', redRRVariable, self.processdata)


        self.RFunctionParamformula =  RFormulaEntry(self.controlArea)
        redRCommitButton(self.bottomAreaRight, "Commit", callback = self.commitFunction)
        self.RoutputWindow = textEdit(self.controlArea, label = "RoutputWindow")
    def processdata(self, data):
        if not self.require_librarys(["stats"]):
            self.status.setText('R Libraries Not Loaded.')
            return
        self.RoutputWindow.clear()
        self.status.setText('New data recieved')
        if data:
            self.RFunctionParam_data=data.getData()
            self.data = data
            self.RFunctionParamformula.update(self.R('colnames('+self.RFunctionParam_data+')'))
            self.commitFunction()
        else:
            self.RFunctionParam_data = ''
            self.RFunctionParamformula.clear()
    def commitFunction(self):
        if unicode(self.RFunctionParam_data) == '': 
            self.status.setText('No data')
            return
        formulaOutput = self.RFunctionParamformula.Formula()
        if formulaOutput == None or formulaOutput[0] == '' or formulaOutput[1] == '': 
            self.status.setText('Bad formula construction')
            return
        injection = []
        string = formulaOutput[0]+ ' ~ ' + formulaOutput[1]
        injection.append(string)

        inj = ','.join(injection)
        self.R('txt<-capture.output(kruskal.test('+inj+', data='+unicode(self.RFunctionParam_data)+'))')
        self.RoutputWindow.clear()
        tmp = self.R('paste(txt, collapse ="\n")')
        self.RoutputWindow.insertHtml('<pre>'+tmp+'</pre>')
        self.status.setText('Data sent')
    def getReportText(self, fileDir):
        text = 'Perform a kruskal test of the attached data.  A summary of the output is below:\n\n'
        text += unicode(self.RoutputWindow.toPlainText())+'\n\n'
        return text
