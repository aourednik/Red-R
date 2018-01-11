"""
<name>t.test</name>
<author>Generated using Widget Maker written by Kyle R. Covington</author>
<description>Performs a t-test.</description>
<RFunctions>stats:t.test</RFunctions>
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

class RedRt_test(OWRpy): 
    settingsList = []
    def __init__(self, parent=None, signalManager=None):
        OWRpy.__init__(self)
        self.setRvariableNames(["t.test"])
        self.data = {}
        self.RFunctionParam_y = ''
        self.RFunctionParam_x = ''
        self.inputs.addInput("y", "y", signals.RVector.RVector, self.processy)
        self.inputs.addInput("x", "x", signals.RVector.RVector, self.processx)
        self.outputs.addOutput("t.test Output","t.test Output", signals.RModelFit.RModelFit)
        
        
        self.RFunctionParampaired_radioButtons = redRradioButtons(self.controlArea, label = "paired:", buttons = ["TRUE","FALSE"], setChecked = "FALSE", orientation = 'horizontal')
        self.RFunctionParamalternative_checkBox = redRradioButtons(self.controlArea, label = "alternative:", buttons = ["two.sided", "less", "greater"], setChecked = "two.sided", orientation = 'horizontal')
        self.RFunctionParamvar_equal_radioButtons = redRradioButtons(self.controlArea, label = "var_equal:", buttons = ["TRUE","FALSE"], setChecked = "FALSE", orientation = 'horizontal')
        self.RFunctionParamconf_level_lineEdit = redRlineEdit(self.controlArea, label = "conf_level:", text = '0.95')
        self.RFunctionParammu_lineEdit = redRlineEdit(self.controlArea, label = "mu:", text = '')
        redRCommitButton(self.bottomAreaRight, "Commit", callback = self.commitFunction)
        self.RoutputWindow = redRtextEdit(self.controlArea, label = "R Output Window")
    def processy(self, data):
        if not self.require_librarys(["stats"]):
            self.status.setText('R Libraries Not Loaded.')
            return
        if data:
            self.RFunctionParam_y=data.getData()
            #self.data = data
            self.commitFunction()
        else:
            self.RFunctionParam_y=''
    def processx(self, data):
        if not self.require_librarys(["stats"]):
            self.status.setText('R Libraries Not Loaded.')
            return
        if data:
            self.RFunctionParam_x=data.getData()
            #self.data = data
            self.commitFunction()
        else:
            self.RFunctionParam_x=''
    def commitFunction(self):
        if unicode(self.RFunctionParam_y) == '': return
        if unicode(self.RFunctionParam_x) == '': return
        injection = []
        if unicode(self.RFunctionParammu_lineEdit.text()) != '':
            string = ',mu='+unicode(self.RFunctionParammu_lineEdit.text())+''
            injection.append(string)
        ## make commit function for self.RFunctionParampaired_radioButtons
        injection.append(',paired = '+unicode(self.RFunctionParampaired_radioButtons.getChecked()))
        ## make commit function for self.RFunctionParamalternative_checkBox
        injection.append(',alternative = \"'+unicode(self.RFunctionParamalternative_checkBox.getChecked())+'\"')
        ## make commit function for self.RFunctionParamvar_equal_radioButtons
        injection.append(',var.equal ='+unicode(self.RFunctionParamvar_equal_radioButtons.getChecked()))
        if unicode(self.RFunctionParamconf_level_lineEdit.text()) != '':
            string = ',conf.level='+unicode(self.RFunctionParamconf_level_lineEdit.text())+''
            injection.append(string)
        inj = ''.join(injection)
        self.R(self.Rvariables['t.test']+'<-t.test(y='+unicode(self.RFunctionParam_y)+',x='+unicode(self.RFunctionParam_x)+inj+')')
        self.R('txt<-capture.output('+self.Rvariables['t.test']+')')
        self.RoutputWindow.clear()
        tmp = self.R('paste(txt, collapse ="\n")')
        self.RoutputWindow.insertPlainText(tmp)