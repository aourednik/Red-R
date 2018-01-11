"""
<name>Cast</name>
<author>Generated using Widget Maker written by Kyle R. Covington</author>
<description></description>
<RFunctions>reshape:cast</RFunctions>
<tags>Reshape</tags>
<icon></icon>
"""
from OWRpy import * 
from libraries.base.qtWidgets.lineEdit import lineEdit as redRlineEdit 
from libraries.base.qtWidgets.radioButtons import radioButtons as redRradioButtons 
from libraries.base.qtWidgets.comboBox import comboBox as redRcomboBox 
from libraries.base.qtWidgets.checkBox import checkBox as redRcheckBox 
from libraries.base.qtWidgets.textEdit import textEdit as redRtextEdit 
import libraries.base.signalClasses as signals

class RedRcast(OWRpy): 
    settingsList = []
    def __init__(self, parent=None, signalManager=None):
        OWRpy.__init__(self)
        self.setRvariableNames(["cast"])
        self.data = {}
        self.require_librarys(["reshape"])
        self.RFunctionParam_data = ''
        self.inputs.addInput("data", "Molten Data", signals.RDataFrame.RDataFrame, self.processdata)
        self.outputs.addOutput("cast Output","Reshaped Data", signals.RDataFrame.RDataFrame)
        
        self.RFunctionParamformula_listBox = redRListBox(self.controlArea, label = "Reshape Variables:")
        self.RFunctionParamformula_listBox.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.RFunctionParamfun_aggregate_lineEdit = redRcomboBox(self.controlArea, label = "Aggregating Function:", items = ['NULL', 'mean', 'median', 'mode', 'range'])
        redRCommitButton(self.bottomAreaRight, "Commit", callback = self.commitFunction)
        self.RoutputWindow = redRtextEdit(self.controlArea, label = "R Output Window")
    def processdata(self, data):
        
        if data:
            self.RFunctionParam_data=data.getData()
            #self.data = data
            self.RFunctionParamformula_listBox.update(self.R('names('+self.RFunctionParam_data+')'))
            self.commitFunction()
        else:
            self.RFunctionParam_data=''
    def commitFunction(self):
        if unicode(self.RFunctionParam_data) == '': return
        injection = []
        if len(self.RFunctionParamformula_listBox.selectedItems()) > 1:
            string = ',formula='+'~'.join([unicode(i.text()) for i in self.RFunctionParamformula_listBox.selectedItems()]) #unicode(self.RFunctionParamformula_comboBox.currentText())+''
            injection.append(string)
        elif len(self.RFunctionParamformula_listBox.selectedItems()) == 1:
            string = ',formula=...~'+unicode(self.RFunctionParamformula_listBox.selectedItems()[0].text()) #unicode(self.RFunctionParamformula_comboBox.currentText())+''
            injection.append(string)
        if unicode(self.RFunctionParamfun_aggregate_lineEdit.currentText()) != '':
            string = ',fun.aggregate='+unicode(self.RFunctionParamfun_aggregate_lineEdit.currentText())+''
            injection.append(string)
        inj = ''.join(injection)
        self.R(self.Rvariables['cast']+'<-cast(data='+unicode(self.RFunctionParam_data)+inj+')')
        self.R('txt<-capture.output('+self.Rvariables['cast']+')')
        self.RoutputWindow.clear()
        tmp = self.R('paste(txt, collapse ="\n")')
        self.RoutputWindow.insertPlainText('This is your data:\n\n'+tmp)
        newData = signals.RDataFrame.RDataFrame(data = 'as.data.frame('+self.Rvariables['cast']+')', parent = 'as.data.frame('+self.Rvariables['cast']+')')
        self.rSend('cast Output', newData)