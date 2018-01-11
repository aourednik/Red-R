"""
<name>findCorrelation</name>
<author>Generated using Widget Maker written by Kyle R. Covington</author>
<description></description>
<RFunctions>caret:findCorrelation</RFunctions>
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

class RedRfindCorrelation(OWRpy): 
    settingsList = []
    def __init__(self, parent=None, signalManager=None):
        OWRpy.__init__(self)
        self.require_librarys(["caret"])
        self.setRvariableNames(["findCorrelation"])
        self.data = {}
        self.RFunctionParam_x = ''
        self.RFunctionParam_data = ''
        #self.inputs.addInput("x", "Correlation Matrix", signals.RMatrix.RMatrix, self.processx)
        self.inputs.addInput("data", "Data Table / Sample List", [signals.RDataFrame.RDataFrame, signals.RList.RList], self.processdata)
        self.outputs.addOutput("findCorrelation Output","Reduced Data Table", signals.RDataFrame.RDataFrame)
        self.outputs.addOutput("findCorrelation Output List", "Reduced Data List", signals.RList.RList)
        
        self.trainingData = redRComboBox(self.controlArea, label = 'Training Data')
        self.classLabels = redRComboBox(self.controlArea, label = 'Classes')
        self.nearZero = redRRadioButtons(self.controlArea, label = 'Remove Near Zero Variance Predictors?', buttons = ['Yes', 'No'], setChecked = 'Yes', callback = self.nzvShowHide)
        
        self.nzvBox = redRWidgetBox(self.controlArea)
        self.freqCut = redRLineEdit(self.nzvBox, label = 'Frequency Cut:', text = '95/5')
        self.uniqueCut = redRLineEdit(self.nzvBox, label = 'Unique Cut:', text = '10')
        
        
        self.RFunctionParamcutoff_spinBox = redRSpinBox(self.controlArea, label = "Max Correlation Coef (/100):", min = 1, max = 99, value = 90)
        redRCommitButton(self.bottomAreaRight, "Commit", callback = self.commitFunction)
        self.RoutputWindow = redRtextEdit(self.controlArea, label = "R Output Window")
    def nzvShowHide(self):
        if unicode(self.nearZero.getChecked()) == 'Yes':
            self.nzvBox.show()
        else:
            self.nzvBox.hide()
    
    def processdata(self, data):
        if data:
            self.RFunctionParam_data=data.getData()
            self.dataClass = self.R('class('+self.RFunctionParam_data+')')
            if self.dataClass == 'list':
                self.trainingData.update(self.R('names('+self.RFunctionParam_data+')'))
                self.classLabels.update(self.R('names('+self.RFunctionParam_data+'[[1]])'))  ## update to the names of the first data frame (they should all be the same.)
            else:
                self.classLabels.update(self.R('names('+self.RFunctionParam_data+')'))
                self.trainingData.clear()
            #self.data = data
            #self.commitFunction()
        else:
            self.RFunctionParam_data=''
    def commitFunction(self):
        if unicode(self.RFunctionParam_x) == '': return
        if unicode(self.RFunctionParam_data) == '': return
        injection = []
        #if unicode(self.RFunctionParamcutoff_spinBox.value()) != '':
        string = ',cutoff='+unicode(float(self.RFunctionParamcutoff_spinBox.value())/100)+''
        injection.append(string)
        inj = ''.join(injection)
        nzvInjection = []
        nzvInjection.append(',freqCut = '+unicode(self.freqCut.text()))
        nzvInjection.append(',uniqueCut = '+unicode(self.uniqueCut.text()))
        nzvInj = ''.join(nzvInjection)
        if self.dataClass == 'list':
            if unicode(self.nearZero.getChecked()) == 'Yes':
                self.R('%s<-nearZeroVar(%s, %s)' % (self.Rvariables['nearZero'], unicode(self.RFunctionParam_x)+'[[\"'+unicode(self.trainingData.currentText())+'\"]][, -'+unicode(self.classLabels.currentText())+']', nzvInj))
                self.R('tempCor<-cor(%s)' % unicode(self.RFunctionParam_x)+'[[\"'+unicode(self.trainingData.currentText())+'\"]][,-'+self.Rvariables['nearZero']+']')
                self.R(self.Rvariables['findCorrelation']+'<-findCorrelation(x=tempCor'+inj+')')
                remove = 'c(%s, %s)' % (self.Rvariables['findCorrelation'], self.Rvariables['nearZero'])
            else:
                self.R('tempCor<-cor(%s)' % unicode(self.RFunctionParam_x)+'[[\"'+unicode(self.trainingData.currentText())+'\"]]')
                self.R(self.Rvariables['findCorrelation']+'<-findCorrelation(x=tempCor'+inj+')')
                remove = self.Rvariables['findCorrelation']
            ## need to remove the findCorrelation from all of the class objects
            self.R(self.Rvariables['findCorrelationOutput']+'<-list()', wantType = 'NoConversion')
            for i in range(self.R('length('+self.RFunctionParam_data+')')):
                self.R(self.Rvariables['findCorrelationOutput']+'[['+unicode(i+1)+']]<-'+self.RFunctionParam_data+'[['+unicode(i + 1)+']][, -'+remove+']')
            newData = signals.RList.RList(data = self.Rvariables['findCorrelationOutput'])
            self.rSend("findCorrelation Output List", newData)
            self.rSend("findCorrelation Output", None)
        if self.dataClass == 'data.frame':
            if unicode(self.nearZero.getChecked()) == 'Yes':
                self.R('%s<-nearZeroVar(%s, %s)' % (self.Rvariables['nearZero'], unicode(self.RFunctionParam_x), nzvInj))
                self.R('tempCor<-cor(%s)' % unicode(self.RFunctionParam_x)+'[,-'+self.Rvariables['nearZero']+']')
                self.R(self.Rvariables['findCorrelation']+'<-findCorrelation(x=tempCor'+inj+')')
                remove = 'c(%s, %s)' % (self.Rvariables['findCorrelation'], self.Rvariables['nearZero'])
            else:
                self.R('tempCor<-cor(%s)' % unicode(self.RFunctionParam_x))
                self.R(self.Rvariables['findCorrelation']+'<-findCorrelation(x=tempCor'+inj+')')
                remove = self.Rvariables['findCorrelation']
            self.R(self.Rvariables['findCorrelationOutput']+'<-'+self.RFunctionParam_data+'[, -'+remove+']', wantType = 'NoConversion')
            newData = signals.RDataFrame.RDataFrame(data = self.Rvariables['findCorrelationOutput'], parent = self.Rvariables['findCorrelationOutput'])
            self.rSend("findCorrelation Output", newData)
            self.rSend("findCorrelation Output List", None)
        self.RoutputWindow.clear()
        self.RoutputWindow.insertPlainText('Removed %s samples from the data.' % self.R('length('+self.Rvariables['findCorrelation']+')'))