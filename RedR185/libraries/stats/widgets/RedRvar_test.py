"""
<name>F Test</name>
<RFunctions>stats:var.test</RFunctions>
<tags>Stats</tags>
"""
from OWRpy import * 
import redRGUI 
from libraries.base.signalClasses.RVector import RVector as redRRVector

from libraries.base.qtWidgets.comboBox import comboBox
from libraries.base.qtWidgets.lineEdit import lineEdit
from libraries.base.qtWidgets.button import button
from libraries.base.qtWidgets.textEdit import textEdit
from libraries.base.qtWidgets.commitButton import commitButton as redRCommitButton

class RedRvar_test(OWRpy): 
    globalSettingsList = ['commit']
    def __init__(self, parent=None, signalManager=None):
        OWRpy.__init__(self)
        self.setRvariableNames(["var.test"])
        self.data = {}
        self.RFunctionParam_y = ''
        self.RFunctionParam_x = ''
        self.inputs.addInput('id0', 'y', redRRVector, self.processy)
        self.inputs.addInput('id1', 'x', redRRVector, self.processx)

        
        self.RFunctionParamalternative_comboBox = comboBox(self.controlArea, label = "alternative:", items = ["two.sided","less","greater"])
        self.RFunctionParamratio_lineEdit = lineEdit(self.controlArea, label = "ratio:", text = '1')
        self.RFunctionParamconf_level_lineEdit = lineEdit(self.controlArea, label = 'Confidence Interval:', text = '0.95')
        self.commit = redRCommitButton(self.bottomAreaRight, "Commit", callback = self.commitFunction,
        processOnInput=True)
        self.RoutputWindow = textEdit(self.controlArea, label = "RoutputWindow")
    def processy(self, data):
        if not self.require_librarys(["stats"]):
            self.status.setText('R Libraries Not Loaded.')
            return
        if data:
            self.RFunctionParam_y=data.getData()
            if self.commit.processOnInput():
                self.commitFunction()
        else:
            self.RFunctionParam_y=''
    def processx(self, data):
        if not self.require_librarys(["stats"]):
            self.status.setText('R Libraries Not Loaded.')
            return
        if data:
            self.RFunctionParam_x=data.getData()
            if self.commit.processOnInput():
                self.commitFunction()
        else:
            self.RFunctionParam_x=''
    def commitFunction(self):
        if unicode(self.RFunctionParam_y) == '': return
        if unicode(self.RFunctionParam_x) == '': return
        injection = []
        string = 'alternative='+unicode(self.RFunctionParamalternative_comboBox.currentText())+''
        injection.append(string)
        if unicode(self.RFunctionParamratio_lineEdit.text()) != '':
            string = 'ratio='+unicode(self.RFunctionParamratio_lineEdit.text())+''
            injection.append(string)
        if unicode(self.RFunctionParamconf_level_lineEdit.text()) != '':
            try:
                float(self.RFunctionParamconf_level_lineEdit.text())
                string = 'conf.level = '+unicode(self.RFunctionParamconf_level_lineEdit.text())
                injection.append(string)
            except:
                self.status.setText('Confidence Interval not a number')
        inj = ','.join(injection)
        self.R(self.Rvariables['var.test']+'<-var.test(y='+unicode(self.RFunctionParam_y)+',x='+unicode(self.RFunctionParam_x)+','+inj+')')
        self.R('txt<-capture.output('+self.Rvariables['var.test']+')')
        self.RoutputWindow.clear()
        tmp = self.R('paste(txt, collapse ="\n")')
        self.RoutputWindow.insertHtml('<br><pre>'+tmp+'</pre>')
