"""
<name>Preprocess (Caret)</name>
<author>Generated using Widget Maker written by Kyle R. Covington</author>
<description></description>
<RFunctions>caret:preProcess</RFunctions>
<tags>Prototypes</tags>
<icon></icon>
"""
from OWRpy import * 
from libraries.base.qtWidgets.lineEdit import lineEdit as redRlineEdit 
from libraries.base.qtWidgets.radioButtons import radioButtons as redRradioButtons 
from libraries.base.qtWidgets.comboBox import comboBox as redRcomboBox 
from libraries.base.qtWidgets.checkBox import checkBox as redRcheckBox 
from libraries.base.qtWidgets.textEdit import textEdit as redRtextEdit 
import libraries.base.signalClasses as signals

class RedRpreProcess(OWRpy): 
    settingsList = []
    def __init__(self, parent=None, signalManager=None):
        OWRpy.__init__(self)
        self.require_librarys(["caret"])
        self.setRvariableNames(["preProcess", 'preProcess_values'])
        self.data = {}
        self.RFunctionParam_x = ''
        self.inputs.addInput("x", "x", signals.RList.RList, self.processx)
        self.outputs.addOutput("preProcess Output","preProcess Output", signals.RModelFit.RModelFit)
        self.outputs.addOutput('preProcess_values', 'Processed Values', signals.RList.RList)
        
        self.trainingElement = redRcomboBox(self.controlArea, lable = 'Training Dataset:')
        self.RFunctionParamthresh_spinBox = redRSpinBox(self.controlArea, label = "Threshold (PCA):", value = 95, min = 1, max = 99)
        self.RFunctionParammethod_listBox = redRListBox(self.controlArea, label = "Method:", items = ["center","scale","pca","spatilaSign"], toolTip = 'Select the options to be applied to the data.  If nothing is selected then center and scale will be applied by default')
        for i in range(self.RFunctionParammethod_listBox.count()):
            if unicode(self.RFunctionParammethod_listBox.item(i).text()) in ['center', 'scale']:
                self.RFunctionParammethod_listBox.setItemSelected(self.RFunctionParammethod_listBox.item(i), True)
            
        redRCommitButton(self.bottomAreaRight, "Commit", callback = self.commitFunction)
    def processx(self, data):
        if data:
            self.RFunctionParam_x=data.getData()
            #self.data = data
            self.trainingElement.update(self.R('names('+self.RFunctionParam_x+')'))
            self.commitFunction()
        else:
            self.RFunctionParam_x=''
    def commitFunction(self):
        if unicode(self.RFunctionParam_x) == '': return
        
        injection = []
        #if unicode(self.RFunctionParamthresh_lineEdit.text()) != '':
        string = ',thresh='+unicode(float(self.RFunctionParamthresh_spinBox.value())/100)+''
        injection.append(string)
        if len(self.RFunctionParammethod_listBox.selectedItems()) > 0:
            string = ',method= c("'+'","'.join([unicode(i.text()) for i in self.RFunctionParammethod_listBox.selectedItems()])+'")'
            injection.append(string)
        inj = ''.join(injection)
        self.R(self.Rvariables['preProcess']+'<-preProcess(x='+unicode(self.RFunctionParam_x)+'$'+unicode(self.trainingElement.currentText())+inj+')')
        self.R(self.Rvariables['preProcess_values']+'<-list()')
        names = self.R('names('+self.RFunctionParam_x+')')
        for i in names:
            self.R('%s$processed_%s<-predict(%s, %s$%s)' % (self.Rvariables['preProcess_values'], i, self.Rvariables['preProcess'], self.RFunctionParam_x, i), wantType = 'NoConversion')
        newData = signals.RModelFit.RModelFit(data = self.Rvariables["preProcess"]) # moment of variable creation, no preexisting data set.  To pass forward the data that was received in the input uncomment the next line.
        #newData.copyAllOptinoalData(self.data)  ## note, if you plan to uncomment this please uncomment the call to set self.data in the process statemtn of the data whose attributes you plan to send forward.
        self.rSend("preProcess Output", newData)
        newData_values = signals.RList.RList(data = self.Rvariables['preProcess_values'])
        self.rSend('preProcess_values', newData_values)