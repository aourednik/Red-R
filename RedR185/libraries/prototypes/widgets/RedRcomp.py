"""
<name>Raw to Compositional Data</name>
<author>By Serge-Etienne Parent, firstly generated using Widget Maker written by Kyle R. Covington</author>
<description></description>
<RFunctions>compositions</RFunctions>
<tags>Compositions</tags>
<icon>raw2comp.png</icon>
<outputWidgets>plotting_plot, base_rViewer</outputWidgets>
"""
from OWRpy import * 
from libraries.base.qtWidgets.lineEdit import lineEdit as redRlineEdit 
from libraries.base.qtWidgets.radioButtons import radioButtons as redRradioButtons 
from libraries.base.qtWidgets.comboBox import comboBox as redRcomboBox 
from libraries.base.qtWidgets.checkBox import checkBox as redRcheckBox 
from libraries.base.qtWidgets.textEdit import textEdit as redRtextEdit 
import libraries.base.signalClasses as signals

class RedRcomp(OWRpy): 
    settingsList = []
    
    def __init__(self, parent=None, signalManager=None):
        OWRpy.__init__(self)
        
        self.data = {}
        self.setRvariableNames(['acomp', 'rcomp', 'aplus', 'rplus'])
        self.RFunctionParam_X = ''
        self.inputs.addInput("X", "X", signals.RDataFrame.RDataFrame, self.processX)
        self.outputs.addOutput("acomp Output","acomp Output", signals.RMatrix.RMatrix)
        self.outputs.addOutput("rcomp Output","rcomp Output", signals.RMatrix.RMatrix)		
        self.outputs.addOutput("rplus Output","rplus Output", signals.RMatrix.RMatrix)
        self.outputs.addOutput("aplus Output","aplus Output", signals.RMatrix.RMatrix)		
        self.compositionType = redRradioButtons(self.controlArea, label = "Composition Type:", buttons = ['acomp', 'rcomp', 'aplus', 'rplus'], setChecked = "acomp", orientation='horizontal') # choose composition type
        
        self.RFunctionParamparts_lineEdit = redRlineEdit(self.controlArea, label = "parts:", text = '')
        self.RFunctionParamtotal_lineEdit = redRlineEdit(self.controlArea, label = "total:", text = '1')
        redRCommitButton(self.bottomAreaRight, "Commit", callback = self.commitFunction)

        
    def processX(self, data):
        if not self.require_librarys(["compositions"]):
            self.status.setText('R Libraries Not Loaded.')
            return
        if data:
            self.RFunctionParam_X=data.getData()
            #self.data = data
            self.commitFunction()
        else:
            self.RFunctionParam_X=''
    def commitFunction(self):
        if str(self.RFunctionParam_X) == '': return
        injection = []
        if str(self.RFunctionParamparts_lineEdit.text()) != '':
            string = 'parts='+str(self.RFunctionParamparts_lineEdit.text())+''
            injection.append(string)
        if str(self.RFunctionParamtotal_lineEdit.text()) != '':
            string = 'total='+str(self.RFunctionParamtotal_lineEdit.text())+''
            injection.append(string)
        inj = ','.join(injection)
        if self.compositionType.getChecked() =='acomp':
            self.R(self.Rvariables['acomp']+'<-acomp(X='+str(self.RFunctionParam_X)+','+inj+')')
            newData = signals.RMatrix.RMatrix(data = self.Rvariables["acomp"], checkVal = False) 
            self.rSend("acomp Output", newData)
			self.rSend('rcomp Output', None)
			self.rSend('aplus Output', None)
			self.rSend('rplus Output', None)
        elif self.compositionType.getChecked() =='rcomp':
            self.R(self.Rvariables['rcomp']+'<-rcomp(X='+str(self.RFunctionParam_X)+','+inj+')')
            newData = signals.RMatrix.RMatrix(data = self.Rvariables["rcomp"], checkVal = False)
            self.rSend("rcomp Output", newData)
			self.rSend('acomp Output', None)
			self.rSend('aplus Output', None)
			self.rSend('rplus Output', None)
        elif self.compositionType.getChecked() =='aplus':
            self.R(self.Rvariables['aplus']+'<-aplus(X='+str(self.RFunctionParam_X)+','+inj+')')
            newData = signals.RMatrix.RMatrix(data = self.Rvariables["aplus"], checkVal = False)
            self.rSend("aplus Output", newData)
			self.rSend('acomp Output', None)
			self.rSend('rcomp Output', None)
			self.rSend('rplus Output', None)
        else:
            self.R(self.Rvariables['rplus']+'<-rplus(X='+str(self.RFunctionParam_X)+','+inj+')')
            newData = signals.RMatrix.RMatrix(data = self.Rvariables["rplus"], checkVal = False)
            self.rSend("rplus Output", newData)		
			self.rSend('acomp Output', None)
			self.rSend('rcomp Output', None)
			self.rSend('aplus Output', None)