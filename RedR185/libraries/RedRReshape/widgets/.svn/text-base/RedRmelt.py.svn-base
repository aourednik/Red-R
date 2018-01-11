"""
<name>Melt Data</name>
<author>Generated using Widget Maker written by Kyle R. Covington</author>
<description>Generates a molten set of data.  The function Cast can be used to recast the data into a new shape.</description>
<RFunctions>reshape:melt</RFunctions>
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

class RedRmelt(OWRpy): 
    settingsList = []
    def __init__(self, parent=None, signalManager=None):
        OWRpy.__init__(self)
        self.setRvariableNames(["melt"])
        self.require_librarys(["reshape"])
        self.data = {}
        self.RFunctionParam_data = ''
        self.inputs.addInput("data", "Data Table", signals.RDataFrame.RDataFrame, self.processdata)
        self.outputs.addOutput("melt Output","Molten Data", signals.RDataFrame.RDataFrame)
        
        self.RFunctionParamna_rm_radioButtons = redRradioButtons(self.controlArea, label = "Remove NA's:", buttons = ["TRUE","FALSE"], setChecked = "TRUE")
        self.RFunctionParammeasure_vars_comboBox = redRcomboBox(self.controlArea, label = "Measure Variables (Values):")
        self.RFunctionParamvariable_name_lineEdit = redRlineEdit(self.controlArea, label = "New Variable Column Name:", text = 'variable')
        self.RFunctionParamid_vars_listBox = redRListBox(self.controlArea, label = "id_vars:")
        self.RFunctionParamid_vars_listBox.setSelectionMode(QAbstractItemView.ExtendedSelection)
        redRCommitButton(self.bottomAreaRight, "Commit", callback = self.commitFunction)
        self.RoutputWindow = redRtextEdit(self.controlArea, label = "R Output Window")
    def processdata(self, data):
        if data:
            self.RFunctionParam_data=data.getData()
            #self.data = data
            self.RFunctionParammeasure_vars_comboBox.update(self.R('names('+self.RFunctionParam_data+')'))
            self.RFunctionParamid_vars_listBox.update(self.R('names('+self.RFunctionParam_data+')'))
            
            self.commitFunction()
        else:
            self.RFunctionParam_data=''
    def commitFunction(self):
        if unicode(self.RFunctionParam_data) == '': return
        injection = []
        ## make commit function for self.RFunctionParamna_rm_radioButtons
        injection.append(',na.rm = '+unicode(self.RFunctionParamna_rm_radioButtons.getChecked()))
        string = ',measure.vars= "'+unicode(self.RFunctionParammeasure_vars_comboBox.currentText())+'"'
        injection.append(string)
        if unicode(self.RFunctionParamvariable_name_lineEdit.text()) != '':
            string = ',variable_name="'+unicode(self.RFunctionParamvariable_name_lineEdit.text())+'"'
            injection.append(string)
        if len(self.RFunctionParamid_vars_listBox.selectedItems()) > 0:
            string = ',id.vars= c("'+'","'.join([unicode(i.text()) for i in self.RFunctionParamid_vars_listBox.selectedItems()])+'")'   #unicode(self.RFunctionParamid_vars_comboBox.currentText())+''
            injection.append(string)
        inj = ''.join(injection)
        self.R(self.Rvariables['melt']+'<-melt(data='+unicode(self.RFunctionParam_data)+inj+')')
        self.R('txt<-capture.output('+self.Rvariables['melt']+')')
        self.RoutputWindow.clear()
        tmp = self.R('paste(txt, collapse ="\n")')
        self.RoutputWindow.insertPlainText('This is your data:\n\n'+tmp)
        newData = signals.RDataFrame.RDataFrame(data = self.Rvariables['melt'], parent = self.Rvariables['melt'])
        self.rSend('melt Output', newData)