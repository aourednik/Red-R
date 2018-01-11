"""
<name>ANOVA</name>
<author>Generated using Widget Maker written by Kyle R. Covington</author>
<RFunctions>stats:aov</RFunctions>
<tags>Parametric</tags>
<icon>stats.png</icon>
"""
from OWRpy import * 
import redRGUI 
from libraries.base.signalClasses.RDataFrame import RDataFrame as redRRDataFrame
from libraries.base.signalClasses.RModelFit import RModelFit as redRRModelFit
from libraries.base.qtWidgets.RFormulaEntry import RFormulaEntry
from libraries.base.qtWidgets.lineEdit import lineEdit
from libraries.base.qtWidgets.tabWidget import tabWidget
from libraries.base.qtWidgets.button import button
from libraries.base.qtWidgets.textEdit import textEdit
class aov(OWRpy): 
    settingsList = []
    def __init__(self, parent=None, signalManager=None):
        OWRpy.__init__(self)
        self.setRvariableNames(["aov"])
        self.data = {}
        self.RFunctionParam_data = ''
        self.saveSettingsList.extend(['data', 'RFunctionParam_data'])
        self.inputs.addInput('id0', 'data', redRRDataFrame, self.processdata)

        self.outputs.addOutput('id0', 'aov Output', redRRModelFit)

        
        box = tabWidget(self.controlArea)
        self.standardTab = box.createTabPage(name = "Standard")
        self.advancedTab = box.createTabPage(name = "Advanced")
        self.RFunctionParamcontrasts_lineEdit =  lineEdit(self.advancedTab,  label = "contrasts:", text = 'NULL')
        self.RFunctionParamformula_formulaEntry =  RFormulaEntry(self.standardTab)
        self.RFunctionParamqr_lineEdit =  lineEdit(self.advancedTab,  label = "qr:", text = 'TRUE')
        self.RFunctionParamprojections_lineEdit =  lineEdit(self.advancedTab,  label = "projections:", text = 'FALSE')
        redRCommitButton(self.bottomAreaRight, "Commit", callback = self.commitFunction)
        self.RoutputWindow = textEdit(self.controlArea, label = "R Output Window")
    def processdata(self, data):
        
        if data:
            self.removeWarning()
            self.RFunctionParam_data=data.getData()
            #self.data = data.copy()
            self.RFunctionParamformula_formulaEntry.update(self.R('names('+self.RFunctionParam_data+')'))
            self.commitFunction()
        else:
            self.RFunctionParam_data=''
            self.RFunctionParamformula_formulaEntry.clear()
    def commitFunction(self):
        if unicode(self.RFunctionParam_data) == '': 
            self.setWarning(id = 'NoData', text = 'No Data connected or data is blank')
            return
        formula = self.RFunctionParamformula_formulaEntry.Formula()
        if formula[0] == '' or formula[1] == '': 
            self.status.setText('Formula Not Entered Correctly')
            return
        injection = []
        string = 'formula='+formula[0]+ ' ~ '+formula[1]
        injection.append(string)
        if unicode(self.RFunctionParamcontrasts_lineEdit.text()) != '':
            string = 'contrasts='+unicode(self.RFunctionParamcontrasts_lineEdit.text())+''
            injection.append(string)
        if unicode(self.RFunctionParamqr_lineEdit.text()) != '':
            string = 'qr='+unicode(self.RFunctionParamqr_lineEdit.text())+''
            injection.append(string)
        if unicode(self.RFunctionParamprojections_lineEdit.text()) != '':
            string = 'projections='+unicode(self.RFunctionParamprojections_lineEdit.text())+''
            injection.append(string)
        inj = ','.join(injection)
        self.R(self.Rvariables['aov']+'<-aov(data='+unicode(self.RFunctionParam_data)+','+inj+')')
        self.R('txt<-capture.output(summary('+self.Rvariables['aov']+'))')
        self.RoutputWindow.clear()
        tmp = self.R('paste(txt, collapse ="\n")')
        self.RoutputWindow.insertPlainText(tmp)
        newData = redRRModelFit(data = self.Rvariables["aov"]) # moment of variable creation, no preexisting data set.  To pass forward the data that was received in the input uncomment the next line.
        #newData.copyAllOptinoalData(self.data)  ## note, if you plan to uncomment this please uncomment the call to set self.data in the process statemtn of the data whose attributes you plan to send forward.
        self.rSend("id0", newData)
    def getReportText(self, fileD):
        text = 'Performed ANOVA analysis on the attached data.  The following parameters were used:\n\n'
        formula = self.RFunctionParamformula_formulaEntry.Formula()
        if formula[0] == '' or formula[1] == '': 
            self.setWarning(id = 'BadFormula', text = 'Formula not entered correctly')
        injection = []
        string = 'formula='+formula[0]+ ' ~ '+formula[1]
        injection.append(string)
        if unicode(self.RFunctionParamcontrasts_lineEdit.text()) != '':
            string = 'contrasts='+unicode(self.RFunctionParamcontrasts_lineEdit.text())+''
            injection.append(string)
        if unicode(self.RFunctionParamqr_lineEdit.text()) != '':
            string = 'qr='+unicode(self.RFunctionParamqr_lineEdit.text())+''
            injection.append(string)
        if unicode(self.RFunctionParamprojections_lineEdit.text()) != '':
            string = 'projections='+unicode(self.RFunctionParamprojections_lineEdit.text())+''
            injection.append(string)
        inj = '\n\n'.join(injection)
        text += inj
        text += '\n\nThe following is a summary of the output:\n\n'
        text += unicode(self.RoutputWindow.toPlainText())+'\n\n'
        return text
