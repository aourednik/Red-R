"""
<name>predict</name>
<author>Generated using Widget Maker written by Kyle R. Covington</author>
<description></description>
<RFunctions>caret:predict</RFunctions>
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

class RedRpredict(OWRpy): 
    settingsList = []
    def __init__(self, parent=None, signalManager=None):
        OWRpy.__init__(self)
        self.setRvariableNames(["predict", 'tempData'])
        self.data = {}
        self.RFunctionParam_object = ''
        self.RFunctionParam_newData = ''
        self.inputs.addInput("object", "object", signals.RModelFit.RModelFit, self.processobject)
        self.inputs.addInput("newData", "newData", [signals.RArbitraryList.RArbitraryList, signals.RDataFrame.RDataFrame], self.processnewData)
        self.outputs.addOutput("predict Output","predict Output", signals.RModelFit.RModelFit)
        
        self.testData = redRcomboBox(self.controlArea, label = 'Test Data:')
        self.classLabels = redRcomboBox(self.controlArea, label = 'Class Labels:')
        redRCommitButton(self.bottomAreaRight, "Commit", callback = self.commitFunction)
        self.RoutputWindow = redRtextEdit(self.controlArea, label = "R Output Window")
    def processobject(self, data):
        
        if data:
            
            self.RFunctionParam_object=data.getData()
            
            self.commitFunction()
        else:
            self.RFunctionParam_object=''
    def processnewData(self, data):
        if data:
            if self.R('class('+data.getData()+')') == 'data.frame':
                self.R(self.Rvariables['tempData']+'<-list(TrainingData = '+data.getData()+')', wantType = 'NoConversion')
                self.RFunctionParam_newData = self.Rvariables['tempData']
            else:
                self.RFunctionParam_newData=data.getData()
            self.testData.update(self.R('names('+self.RFunctionParam_newData+')'))
            self.classLabels.update([''] + self.R('names('+self.RFunctionParam_newData+'[[1]])'))
        else:
            self.RFunctionParam_newData=''
    def commitFunction(self):
        if unicode(self.RFunctionParam_object) == '': return
        if unicode(self.RFunctionParam_newData) == '': 
            self.R(self.Rvariables['predict']+'<-predict.train(object='+unicode(self.RFunctionParam_object)+')')
        else:
            newData = '%s[[\'%s\']]' % (self.RFunctionParam_newData, unicode(self.testData.currentText()))
            if unicode(self.classLabels.currentText()) != '':
                newData = newData+'[, !names('+newData+') %in% c(\''+unicode(self.classLabels.currentText())+'\')]'
            
            self.R(self.Rvariables['predict']+'<-extractPrediction(models=list('+unicode(self.RFunctionParam_object)+'),testX='+newData+')')
        self.R('txt<-c(capture.output(summary('+self.Rvariables['predict']+')), capture.output('+self.Rvariables['predict']+'))')
        self.RoutputWindow.clear()
        tmp = self.R('paste(txt, collapse ="\n")')
        self.RoutputWindow.insertPlainText(tmp)
        new = signals.RModelFit.RModelFit(data = self.Rvariables['predict'])
        self.rSend('predict Output', new)