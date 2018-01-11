"""
<name>Linear Model</name>
<tags>Parametric</tags>
<icon>stats.png</icon>
"""
from OWRpy import * 
import redRGUI
from libraries.plotting.signalClasses.RPlotAttribute import RPlotAttribute as redRRPlotAttribute
from libraries.stats.signalClasses.RLMFit import RLMFit as redRRLMFit
from libraries.base.signalClasses.RDataFrame import RDataFrame as redRRDataFrame
from libraries.base.qtWidgets.RFormulaEntry import RFormulaEntry
from libraries.base.qtWidgets.lineEdit import lineEdit
from libraries.base.qtWidgets.groupBox import groupBox
from libraries.base.qtWidgets.button import button
from libraries.base.qtWidgets.widgetBox import widgetBox
from libraries.base.qtWidgets.commitButton import commitButton as redRCommitButton

class lm(OWRpy): 
    globalSettingsList = ['commit']
    def __init__(self, parent=None, signalManager=None):
        OWRpy.__init__(self, wantGUIDialog = 1)
        self.setRvariableNames(["lm"])
        self.RFunctionParam_formula = ""
        self.RFunctionParam_data = ''
        self.modelFormula = ''
        self.processingComplete = 0
        
        self.inputs.addInput('id0', 'data', redRRDataFrame, self.processdata)

        self.outputs.addOutput('id0', 'lm Output', redRRLMFit)
        self.outputs.addOutput('id1', 'lm plot attribute', redRRPlotAttribute)

        
        #GUI
        
        box = widgetBox(self.GUIDialog, orientation = 'horizontal')
        paramBox = groupBox(self.GUIDialog, 'Parameters')
        formulaBox = widgetBox(self.controlArea)
        self.RFunctionParam_subset = lineEdit(paramBox, 'NULL', label = "subset:")
        self.RFunctionParam_qr = lineEdit(paramBox, 'TRUE', label = "qr:")

        self.RFunctionParam_singular_ok = lineEdit(paramBox, 'TRUE', label = "singular_ok:")
        self.RFunctionParam_y = lineEdit(paramBox, 'FALSE', label = "y:")
        self.RFunctionParam_weights = lineEdit(paramBox, "", label = "weights:")
        self.RFunctionParam_offset = lineEdit(paramBox, "", label = "offset:")
        self.RFunctionParam_contrasts = lineEdit(paramBox, "NULL", label = "contrasts:")
        self.RFunctionParam_x = lineEdit(paramBox, "FALSE", label = "x:")
        self.RFunctionParam_model = lineEdit(paramBox, "TRUE", label = "model:")
        self.RFunctionParam_method = lineEdit(paramBox, "qr", label = "method:")
        
        #start formula entry section

        buttonsBox = widgetBox(formulaBox, "Commands")
        self.formulEntry = RFormulaEntry(buttonsBox,label='Formula',displayLabel=False)
        
        
        self.commit = redRCommitButton(self.bottomAreaRight, "Commit", callback = self.commitFunction,
        processOnInput=True)
        #self.processButton.setEnabled(False)
        self.status.setText('Data Not Connected Yet')
    def processdata(self, data):
        if data:
            self.RFunctionParam_data=data.getData()
            names = self.R('colnames('+self.RFunctionParam_data+')')
            self.formulEntry.update(names)
            self.status.setText('Data Connected')
            if self.commit.processOnInput():
                self.commitFunction()

        else:
            self.formulEntry.clear()
            self.RFunctionParam_data = ''
            self.status.setText('Data Connection Failed. Please Reconnect')
    def commitFunction(self):
        if self.RFunctionParam_data == '': 
            self.status.setText('No data')
            return
        if self.formulEntry.Formula()[0] == '' or self.formulEntry.Formula()[1] == '':
            self.status.setText('Please select valid formula parameters')
            return
        self.RFunctionParam_formula = self.formulEntry.Formula()[0] + ' ~ ' + self.formulEntry.Formula()[1]

        
        self.R(self.Rvariables['lm']+'<-lm(data='+unicode(self.RFunctionParam_data)+',subset='+unicode(self.RFunctionParam_subset.text())+',qr='+unicode(self.RFunctionParam_qr.text())+',formula='+unicode(self.RFunctionParam_formula)+',singular_ok='+unicode(self.RFunctionParam_singular_ok.text())+',y='+unicode(self.RFunctionParam_y.text())+',weights='+unicode(self.RFunctionParam_weights.text())+',offset='+unicode(self.RFunctionParam_offset.text())+',contrasts='+unicode(self.RFunctionParam_contrasts.text())+',x='+unicode(self.RFunctionParam_x.text())+',model='+unicode(self.RFunctionParam_model.text())+',method="'+unicode(self.RFunctionParam_method.text())+'")')
        newData = redRRLMFit(data = self.Rvariables['lm'])
        self.rSend("id0", newData)
        
        newPlotAtt = redRRPlotAttribute(data = 'abline('+self.Rvariables['lm']+')')
        self.rSend("id1", newPlotAtt)
        
    def getReportText(self, fileDir):
        return 'Generates a linear model fit to attached data and a linear model plot attribute.  The data fit was generated based on the following formula:\n\n%s\n\nOther parameters are as follows:\n\n%s\n\n' % (self.formulEntry.Formula()[0] + ' ~ ' + self.formulEntry.Formula()[1], '(data='+unicode(self.RFunctionParam_data)+',subset='+unicode(self.RFunctionParam_subset.text())+',qr='+unicode(self.RFunctionParam_qr.text())+',formula='+unicode(self.RFunctionParam_formula)+',singular_ok='+unicode(self.RFunctionParam_singular_ok.text())+',y='+unicode(self.RFunctionParam_y.text())+',weights='+unicode(self.RFunctionParam_weights.text())+',offset='+unicode(self.RFunctionParam_offset.text())+',contrasts='+unicode(self.RFunctionParam_contrasts.text())+',x='+unicode(self.RFunctionParam_x.text())+',model='+unicode(self.RFunctionParam_model.text())+',method="'+unicode(self.RFunctionParam_method.text())+'")')
        
