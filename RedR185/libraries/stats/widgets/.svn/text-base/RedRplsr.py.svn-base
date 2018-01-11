"""
<name>plsr</name>
<author>Generated using Widget Maker written by Kyle R. Covington</author>
<description>Beginning module for the pls package to generate a model fit.</description>
<RFunctions>pls:plsr</RFunctions>
<tags>Prototypes</tags>
<icon></icon>
"""
from OWRpy import * 
import redRGUI 
import libraries.base.signalClasses as signals

from libraries.base.qtWidgets.comboBox import comboBox
from libraries.base.qtWidgets.lineEdit import lineEdit
from libraries.base.qtWidgets.radioButtons import radioButtons
from libraries.base.qtWidgets.button import button
class RedRplsr(OWRpy): 
    settingsList = []
    def __init__(self, parent=None, signalManager=None):
        OWRpy.__init__(self)
        self.setRvariableNames(["plsr"])
        self.data = {}
        self.RFunctionParam_data = ''
        self.inputs.addInput('id0', 'data', redRRDataFrame, self.processdata)

        self.outputs.addOutput('id0', 'plsr Output', redRRModelFit)

        
        self.RFunctionParamformula_lineEdit = lineEdit(self.controlArea, label = "formula:", text = '')
        self.RFunctionParamscale_radioButtons = radioButtons(self.controlArea, label = "Scale the data:", buttons = ['TRUE', 'FALSE'], setChecked = 'FALSE', orientation = 'horizontal')
        self.RFunctionParammethod_lineEdit = lineEdit(self.controlArea, label = "method:", text = '')
        self.RFunctionParamncomp_lineEdit = lineEdit(self.controlArea, label = "ncomp:", text = '10')
        self.RFunctionParamvalidation_comboBox = comboBox(self.controlArea, label = "validation:", items = ["none","CV","LOO"])
        redRCommitButton(self.bottomAreaRight, "Commit", callback = self.commitFunction)
    def processdata(self, data):
        if not self.require_librarys(["pls"]):
            self.status.setText('R Libraries Not Loaded.')
            return
        if data:
            self.RFunctionParam_data=data.getData()
            #self.data = data
            self.commitFunction()
        else:
            self.RFunctionParam_data=''
    def commitFunction(self):
        if unicode(self.RFunctionParam_data) == '': return
        if unicode(self.RFunctionParamformula_lineEdit.text()) == '':
            self.status.setText('No Formula')
            return
        injection = []
        if unicode(self.RFunctionParamformula_lineEdit.text()) != '':
            string = 'formula='+unicode(self.RFunctionParamformula_lineEdit.text())+''
            injection.append(string)
        ## make commit function for self.RFunctionParamscale_checkBox
        if unicode(self.RFunctionParamscale_radioButtons.getChecked()) == 'TRUE':
            injection.append('scale = TRUE')
        else:
            injection.append('scale = FALSE')
        if unicode(self.RFunctionParammethod_lineEdit.text()) != '':
            string = 'method='+unicode(self.RFunctionParammethod_lineEdit.text())+''
            injection.append(string)
        if unicode(self.RFunctionParamncomp_lineEdit.text()) != '':
            string = 'ncomp='+unicode(self.RFunctionParamncomp_lineEdit.text())+''
            injection.append(string)
        string = 'validation=\''+unicode(self.RFunctionParamvalidation_comboBox.currentText())+'\''
        injection.append(string)
        inj = ','.join(injection)
        self.R(self.Rvariables['plsr']+'<-plsr(data='+unicode(self.RFunctionParam_data)+',model = TRUE, x = TRUE, y = TRUE,'+inj+')')
        newData = signals.redRRModelFit(data = self.Rvariables["plsr"]) # moment of variable creation, no preexisting data set.  To pass forward the data that was received in the input uncomment the next line.
        #newData.copyAllOptinoalData(self.data)  ## note, if you plan to uncomment this please uncomment the call to set self.data in the process statemtn of the data whose attributes you plan to send forward.
        self.rSend("id0", newData)
