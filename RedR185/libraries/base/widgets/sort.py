"""
<name>Sort</name>
<tags>Data Manipulation</tags>
"""
from OWRpy import *
import redRGUI 
from libraries.base.signalClasses.RDataFrame import RDataFrame as redRRDataFrame

from libraries.base.qtWidgets.lineEdit import lineEdit
from libraries.base.qtWidgets.widgetBox import widgetBox
from libraries.base.qtWidgets.button import button
from libraries.base.qtWidgets.radioButtons import radioButtons
from libraries.base.qtWidgets.comboBox import comboBox
from libraries.base.qtWidgets.checkBox import checkBox
from libraries.base.qtWidgets.commitButton import commitButton as redRCommitButton
import redRi18n
_ = redRi18n.get_(package = 'base')
class sort(OWRpy): 
    globalSettingsList = ['commit']
    def __init__(self, parent=None, signalManager=None):
        OWRpy.__init__(self)
        self.setRvariableNames(["sort"])
        self.data = {}
         
        self.RFunctionParam_x = ''
        self.inputs.addInput('id0', _('Data Tabel'), redRRDataFrame, self.processx)

        self.outputs.addOutput('id0', _('Sorted Data Table'), redRRDataFrame)

        self.standardTab = widgetBox(self.controlArea)
        self.options =  checkBox(self.standardTab,label=_('Options'),
        buttons = [_("Decreasing"), _('NA Last')], orientation='horizontal')
        # self.standardTab.layout().setAlignment(self.options,Qt.AlignLeft)
        
        self.sortingColumn1 = comboBox(self.standardTab, label = _('First Column to Sort:'))
        self.sortingColumn2 = comboBox(self.standardTab, label = _('Second Column to Sort:'))
        self.sortingColumn3 = comboBox(self.standardTab, label = _('Third Column to Sort:'))
        
        self.commit = redRCommitButton(self.bottomAreaRight, _("Commit"), callback = self.commitFunction,
        processOnInput=True)

    def processx(self, data):
        if data:
            self.RFunctionParam_x=data.getData()
            colNames = self.R('colnames('+self.RFunctionParam_x+')',wantType='list')
            colNames.insert(0,'')
            self.sortingColumn1.update(colNames)
            self.sortingColumn2.update(colNames)
            self.sortingColumn3.update(colNames)
            if self.commit.processOnInput():
                self.commitFunction()
        else:
            self.RFunctionParam_x=''
    def commitFunction(self):
        if unicode(self.RFunctionParam_x) == '': return
        if self.sortingColumn1.currentText() =='':
            return
        injection = []

        injection.append('%s$%s' % (self.RFunctionParam_x, self.sortingColumn1.currentText()))
        if self.sortingColumn2.currentText() !='':
            injection.append('%s$%s' % (self.RFunctionParam_x, self.sortingColumn2.currentText()))
        if self.sortingColumn3.currentText() !='':
            injection.append('%s$%s' % (self.RFunctionParam_x, self.sortingColumn3.currentText()))
            
            
        if _('Decreasing') in self.options.getChecked():
            string = 'decreasing=TRUE'
            injection.append(string)
        else:
            injection.append('decreasing = FALSE')
        if _('NA Last') in self.options.getChecked():
            injection.append('na.last = TRUE')
        inj = ','.join(injection)

        self.R(self.Rvariables['sort']+'<-%s[order(%s),]' % (self.RFunctionParam_x, inj), wantType = 'NoConversion')
        newData = redRRDataFrame(data = self.Rvariables["sort"]) 
        
        self.rSend("id0", newData)
