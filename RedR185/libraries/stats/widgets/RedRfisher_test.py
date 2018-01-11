"""
<name>Fisher Exact Test</name>
<tags>Stats</tags>
"""
from OWRpy import * 
import redRGUI 
from libraries.base.signalClasses.RMatrix import RMatrix as redRRMatrix

from libraries.base.qtWidgets.comboBox import comboBox
from libraries.base.qtWidgets.lineEdit import lineEdit
from libraries.base.qtWidgets.checkBox import checkBox
from libraries.base.qtWidgets.button import button
from libraries.base.qtWidgets.textEdit import textEdit
from libraries.base.qtWidgets.commitButton import commitButton as redRCommitButton

class RedRfisher_test(OWRpy): 
    globalSettingsList = ['commit']
    def __init__(self, parent=None, signalManager=None):
        OWRpy.__init__(self)
        self.setRvariableNames(["fisher.test"])
        self.data = {}
        self.RFunctionParam_x = ''
        self.inputs.addInput('id0', 'x', redRRMatrix, self.processx)

        
        self.RFunctionParamB_lineEdit = lineEdit(self.controlArea, label = "Number of Replicates for Monte Carlo:", text = '2000')
        self.RFunctionParamhybrid_checkBox = checkBox(self.controlArea, label = "Hybrid Probabilities:", buttons = ['FALSE', 'TRUE'], setChecked = 'FALSE')
        self.RFunctionParamsimulate_p_value_lineEdit = checkBox(self.controlArea, label = "simulate_p_value:", buttons = ['FALSE,TRUE'], setChecked = 'FALSE')
        self.RFunctionParamconf_level_lineEdit = lineEdit(self.controlArea, label = "Confidence Level:", text = '0.95')
        self.RFunctionParamconf_int_lineEdit = checkBox(self.controlArea, label = "Calculate Confidence Interval:", buttons = ['TRUE','FALSE'], setChecked = 'TRUE')
        self.RFunctionParamalternative_comboBox = comboBox(self.controlArea, label = "Alternative Hypothesis:", items = ["two.sided","greater","less"])
        self.RFunctionParamor_lineEdit = lineEdit(self.controlArea, label = "Odds Ratio:", text = '1')
        redRCommitButton(self.bottomAreaRight, "Commit", callback = self.commitFunction)
        self.RoutputWindow = textEdit(self.controlArea, label = "R Output Window")
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
        if unicode(self.RFunctionParam_x) == '': return
        injection = []
        # if unicode(self.RFunctionParamcontrol_lineEdit.text()) != '':
            # string = 'control='+unicode(self.RFunctionParamcontrol_lineEdit.text())+''
            # injection.append(string)
        if unicode(self.RFunctionParamB_lineEdit.text()) != '':
            string = 'B='+unicode(self.RFunctionParamB_lineEdit.text())+''
            injection.append(string)
        injection.append('hybrid ='+ unicode(self.RFunctionParamhybrid_checkBox.getChecked()))
        injection.append('simulate.p.value='+unicode(self.RFunctionParamsimulate_p_value_lineEdit.getChecked()))
        if unicode(self.RFunctionParamconf_level_lineEdit.text()) != '':
            string = 'conf.level='+unicode(self.RFunctionParamconf_level_lineEdit.text())+''
            injection.append(string)
        injection.append('conf.int='+unicode(self.RFunctionParamconf_int_lineEdit.text()))
        string = 'alternative='+unicode(self.RFunctionParamalternative_comboBox.currentText())+''
        injection.append(string)
        if unicode(self.RFunctionParamor_lineEdit.text()) != '':
            string = 'or='+unicode(self.RFunctionParamor_lineEdit.text())+''
            injection.append(string)
        inj = ','.join(injection)
        self.R(self.Rvariables['fisher.test']+'<-fisher.test(x='+unicode(self.RFunctionParam_x)+','+inj+')')
        self.R('txt<-capture.output('+self.Rvariables['fisher.test']+')')
        self.RoutputWindow.clear()
        tmp = self.R('paste(txt, collapse ="\n")')
        self.RoutputWindow.insertHtml('<br><pre>'+tmp+'</pre>')
