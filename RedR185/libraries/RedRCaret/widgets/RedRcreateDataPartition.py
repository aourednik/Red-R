"""
<name>Partition/Resample/Fold (Caret)</name>
<author>Generated using Widget Maker written by Kyle R. Covington</author>
<description>Creates a data partition, a resample of the data or a fold depending on the selections in the function box.  Partition, partitions the data into groups, resample generates a bootstrap resampling of the data and folds generates an evenly split dataset across the number of folds.</description>
<RFunctions>caret:createDataPartition</RFunctions>
<tags>Classification Regression, Prototypes</tags>
<icon></icon>
"""
from OWRpy import * 
from libraries.base.qtWidgets.lineEdit import lineEdit as redRlineEdit 
from libraries.base.qtWidgets.radioButtons import radioButtons as redRradioButtons 
from libraries.base.qtWidgets.comboBox import comboBox as redRcomboBox 
from libraries.base.qtWidgets.checkBox import checkBox as redRcheckBox 
from libraries.base.qtWidgets.textEdit import textEdit as redRtextEdit 
import libraries.base.signalClasses as signals

class RedRcreateDataPartition(OWRpy): 
    settingsList = []
    def __init__(self, parent=None, signalManager=None):
        OWRpy.__init__(self)
        self.require_librarys(["caret"])
        self.setRvariableNames(["createDataPartition", 'dataOutputList'])
        self.data = {}
        self.RFunctionParam_y = ''
        self.inputs.addInput("y", "Input Vector List", signals.RDataFrame.RDataFrame, self.processy)
        self.outputs.addOutput("createDataPartition Output","Partition/Resample/Fold List", signals.RList.RList)
        self.outputs.addOutput("dataOutputList", "Data Output List \n(Subsets of data that matches the partitioning)", signals.RList.RList)
        
        self.ListElementCombo = redRcomboBox(self.controlArea, label = 'List Element (Vector):')
        self.functionCombo = redRcomboBox(self.controlArea, label = 'Function:', items = ['Partition', 'Resample', 'Fold'])
        self.RFunctionParamp_spinBox = redRSpinBox(self.controlArea, label = "Percentage (Partition):", value = 50, min = 1, max = 100)
        #self.RFunctionParamlist_radioButtons = redRradioButtons(self.controlArea, label = "list:", buttons = ["TRUE"], setChecked = "")
        self.RFunctionParamgroups_spinBox = redRSpinBox(self.controlArea, label = "Number of Quantiles (Partition on Numeric Data):", value = 5, min = 1)
        self.RFunctionParamtimes_spinBox = redRSpinBox(self.controlArea, label = "Number of Partitions (Partition and Resample):", value = 1, min = 1, toolTip = 'Typically higher values are set for resampling because one wants to generate several resamples at once.')
        self.RFunctionParam_folds_spinBox = redRSpinBox(self.controlArea, label = "Number of Folds (Folds):", value = 10, min = 1)
        redRCommitButton(self.bottomAreaRight, "Commit", callback = self.commitFunction)
        self.RoutputWindow = redRtextEdit(self.controlArea, label = "R Output Window")
    def processy(self, data):
        
        if data:
            self.RFunctionParam_y=data.getData()
            self.ListElementCombo.update(self.R('names('+self.RFunctionParam_y+')'))
            #self.data = data
            #self.commitFunction()
        else:
            self.RFunctionParam_y=''
    def commitFunction(self):
        if unicode(self.RFunctionParam_y) == '': return
        if unicode(self.ListElementCombo.currentText()) == '': return
        if self.R('class('+self.RFunctionParam_y+'$'+unicode(self.ListElementCombo.currentText())+')') not in ['factor', 'numeric', 'character', 'logical']: return
        if self.R('length('+self.RFunctionParam_y+'$'+unicode(self.ListElementCombo.currentText())+')') < int(self.RFunctionParamgroups_spinBox.value()): return
        injection = []
        if unicode(self.functionCombo.currentText()) == 'Partition':
            function = 'createDataPartition'
            string = ',p='+unicode(float(self.RFunctionParamp_spinBox.value())/100)+''
            injection.append(string)
            string = ',groups='+unicode(self.RFunctionParamgroups_spinBox.value())+''
            injection.append(string)
            string = ',times='+unicode(self.RFunctionParamtimes_spinBox.value())+''
            injection.append(string)
        elif unicode(self.functionCombo.currentText()) == 'Resample':
            function = 'createResample'
            string = ',times='+unicode(self.RFunctionParamtimes_spinBox.value())+''
            injection.append(string)
        elif unicode(self.functionCombo.currentText()) == 'Fold':
            function = 'createFolds'
            injection.append(', k = '+unicode(self.RFunctionParam_folds_spinBox.value()))
        inj = ''.join(injection)
        self.R(self.Rvariables['createDataPartition']+'<-'+function+'(y='+self.RFunctionParam_y+'$'+unicode(self.ListElementCombo.currentText())+inj+')')
        self.R('txt<-capture.output('+self.Rvariables['createDataPartition']+')')
        self.RoutputWindow.clear()
        tmp = self.R('paste(txt, collapse ="\n")')
        self.RoutputWindow.insertPlainText(tmp)
        newData = signals.RList.RList(data = self.Rvariables["createDataPartition"]) # moment of variable creation, no preexisting data set.  To pass forward the data that was received in the input uncomment the next line.
        #newData.copyAllOptinoalData(self.data)  ## note, if you plan to uncomment this please uncomment the call to set self.data in the process statemtn of the data whose attributes you plan to send forward.
        self.rSend("createDataPartition Output", newData)
        self.R(self.Rvariables['dataOutputList']+'<-list()', wantType = 'NoConversion')
        for i in range(self.R('length('+self.Rvariables['createDataPartition']+')')):
            ## make a new sub data table for each of the partition levels
            if unicode(self.functionCombo.currentText()) == 'Partition':
                self.R('%s$Training_%s<-%s[%s[[%s]],]' % (self.Rvariables['dataOutputList'], unicode(i+1), self.RFunctionParam_y, self.Rvariables['createDataPartition'], unicode(i+1)))
                self.R('%s$Test_%s<-%s[-%s[[%s]],]' % (self.Rvariables['dataOutputList'], unicode(i+1), self.RFunctionParam_y, self.Rvariables['createDataPartition'], unicode(i+1)))
            else:
                self.R('%s$Sample_%s<-%s[-%s[[%s]],]' % (self.Rvariables['dataOutputList'], unicode(i+1), self.RFunctionParam_y, self.Rvariables['createDataPartition'], unicode(i+1)))
        
        newDataOutputList = signals.RList.RList(data = self.Rvariables['dataOutputList'])
        self.rSend("dataOutputList", newDataOutputList)