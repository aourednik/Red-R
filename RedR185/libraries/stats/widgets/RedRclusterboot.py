"""
<name>clusterboot</name>
<author>Generated using Widget Maker written by Kyle R. Covington</author>
<description></description>
<RFunctions>fpc:clusterboot</RFunctions>
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

class RedRclusterboot(OWRpy): 
    settingsList = []
    def __init__(self, parent=None, signalManager=None):
        OWRpy.__init__(self)
        self.setRvariableNames(["clusterboot"])
        self.data = {}
        self.require_librarys(["fpc"])
        self.RFunctionParam_data = ''
        self.inputs.addInput("data", "data", signals.RMatrix.RMatrix, self.processdata)
        self.outputs.addOutput("clusterboot Output","clusterboot Output", signals.RArbitraryList.RArbitraryList)
        
        self.RFunctionParamdistances_lineEdit = redRlineEdit(self.controlArea, label = "distances:", text = '')
        self.RFunctionParamB_lineEdit = redRlineEdit(self.controlArea, label = "B:", text = '100')
        self.RFunctionParamjittertuning_lineEdit = redRlineEdit(self.controlArea, label = "jittertuning:", text = '0.05')
        self.RFunctionParamclustermethod_lineEdit = redRlineEdit(self.controlArea, label = "clustermethod:", text = '')
        self.RFunctionParamdissolution_lineEdit = redRlineEdit(self.controlArea, label = "dissolution:", text = '0.5')
        self.RFunctionParammultipleboot_lineEdit = redRlineEdit(self.controlArea, label = "multipleboot:", text = 'TRUE')
        self.RFunctionParambscompare_lineEdit = redRlineEdit(self.controlArea, label = "bscompare:", text = 'FALSE')
        self.RFunctionParamshowplots_lineEdit = redRlineEdit(self.controlArea, label = "showplots:", text = 'FALSE')
        self.RFunctionParamnoisetuning_lineEdit = redRlineEdit(self.controlArea, label = "noisetuning:", text = '0.0')
        self.RFunctionParambootmethod_lineEdit = redRlineEdit(self.controlArea, label = "bootmethod:", text = '')
        self.RFunctionParamrecover_lineEdit = redRlineEdit(self.controlArea, label = "recover:", text = '0.75')
        self.RFunctionParamsubtuning_lineEdit = redRlineEdit(self.controlArea, label = "subtuning:", text = '')
        self.RFunctionParamseed_lineEdit = redRlineEdit(self.controlArea, label = "seed:", text = 'NULL')
        self.RFunctionParamnoisemethod_lineEdit = redRlineEdit(self.controlArea, label = "noisemethod:", text = 'FALSE')
        redRCommitButton(self.bottomAreaRight, "Commit", callback = self.commitFunction)
    def processdata(self, data):

        if data:
            self.RFunctionParam_data=data.getData()
            #self.data = data
            self.commitFunction()
        else:
            self.RFunctionParam_data=''
    def commitFunction(self):
        if unicode(self.RFunctionParam_data) == '': return
        injection = []
        if unicode(self.RFunctionParamdistances_lineEdit.text()) != '':
            string = ',distances='+unicode(self.RFunctionParamdistances_lineEdit.text())+''
            injection.append(string)
        if unicode(self.RFunctionParamB_lineEdit.text()) != '':
            string = ',B='+unicode(self.RFunctionParamB_lineEdit.text())+''
            injection.append(string)
        if unicode(self.RFunctionParamjittertuning_lineEdit.text()) != '':
            string = ',jittertuning='+unicode(self.RFunctionParamjittertuning_lineEdit.text())+''
            injection.append(string)
        if unicode(self.RFunctionParamclustermethod_lineEdit.text()) != '':
            string = ',clustermethod='+unicode(self.RFunctionParamclustermethod_lineEdit.text())+''
            injection.append(string)
        if unicode(self.RFunctionParamdissolution_lineEdit.text()) != '':
            string = ',dissolution='+unicode(self.RFunctionParamdissolution_lineEdit.text())+''
            injection.append(string)
        if unicode(self.RFunctionParammultipleboot_lineEdit.text()) != '':
            string = ',multipleboot='+unicode(self.RFunctionParammultipleboot_lineEdit.text())+''
            injection.append(string)
        if unicode(self.RFunctionParambscompare_lineEdit.text()) != '':
            string = ',bscompare='+unicode(self.RFunctionParambscompare_lineEdit.text())+''
            injection.append(string)
        if unicode(self.RFunctionParamshowplots_lineEdit.text()) != '':
            string = ',showplots='+unicode(self.RFunctionParamshowplots_lineEdit.text())+''
            injection.append(string)
        if unicode(self.RFunctionParamnoisetuning_lineEdit.text()) != '':
            string = ',noisetuning='+unicode(self.RFunctionParamnoisetuning_lineEdit.text())+''
            injection.append(string)
        if unicode(self.RFunctionParambootmethod_lineEdit.text()) != '':
            string = ',bootmethod='+unicode(self.RFunctionParambootmethod_lineEdit.text())+''
            injection.append(string)
        if unicode(self.RFunctionParamrecover_lineEdit.text()) != '':
            string = ',recover='+unicode(self.RFunctionParamrecover_lineEdit.text())+''
            injection.append(string)
        if unicode(self.RFunctionParamsubtuning_lineEdit.text()) != '':
            string = ',subtuning='+unicode(self.RFunctionParamsubtuning_lineEdit.text())+''
            injection.append(string)
        if unicode(self.RFunctionParamseed_lineEdit.text()) != '':
            string = ',seed='+unicode(self.RFunctionParamseed_lineEdit.text())+''
            injection.append(string)
        if unicode(self.RFunctionParamnoisemethod_lineEdit.text()) != '':
            string = ',noisemethod='+unicode(self.RFunctionParamnoisemethod_lineEdit.text())+''
            injection.append(string)
        inj = ''.join(injection)
        self.R(self.Rvariables['clusterboot']+'<-clusterboot(data='+unicode(self.RFunctionParam_data)+inj+')')
        newData = signals.RArbitraryList.RArbitraryList(data = self.Rvariables["clusterboot"], checkVal = False) # moment of variable creation, no preexisting data set.  To pass forward the data that was received in the input uncomment the next line.
        #newData.copyAllOptinoalData(self.data)  ## note, if you plan to uncomment this please uncomment the call to set self.data in the process statemtn of the data whose attributes you plan to send forward.
        self.rSend("clusterboot Output", newData)