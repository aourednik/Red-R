"""
<name>Reshape Data</name>
<tags>Data Manipulation</tags>
"""
from OWRpy import * 
import redRGUI 
from libraries.base.signalClasses.RDataFrame import RDataFrame as redRRDataFrame
from libraries.base.qtWidgets.comboBox import comboBox
from libraries.base.qtWidgets.lineEdit import lineEdit
from libraries.base.qtWidgets.listBox import listBox
from libraries.base.qtWidgets.button import button
from libraries.base.qtWidgets.widgetBox import widgetBox
import redRi18n
_ = redRi18n.get_(package = 'base')
class Melt_DF(OWRpy): 
    globalSettingsList = ['commit']
    def __init__(self, parent=None, signalManager=None):
        OWRpy.__init__(self)
        self.setRvariableNames(["melt.data.frame", "melt.data.frame.cm"])
        self.RFunctionParam_data = ''
        self.data = {}
        self.inputs.addInput('id0', _('data'), redRRDataFrame, self.processdata)

        self.outputs.addOutput('id0', _('melt.data.frame Output'), redRRDataFrame)

        
        box = widgetBox(self.controlArea, _("Widget Box"))
        self.RFunctionParam_na_rm = comboBox(box, label = _("Remove NA:"), items = [_('Yes'), _('No')])
        self.RFunctionParam_measure_var = listBox(box, label = _("Result Variable:"), toolTip = _('The column that contains the result or the measurement that the data should be melted around.'))
        self.RFunctionParam_measure_var.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.RFunctionParam_id_var = listBox(box, label = _("Groupings:"), toolTip = _('The columns indicating the groupings of the data.'))
        self.RFunctionParam_id_var.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.RFunctionParam_variable_name = lineEdit(box, label = _("New Group Name:"), toolTip = _('The name of the new column that the groupings will be put into.'))
        self.commit = redRCommitButton(self.bottomAreaRight, _("Commit"), callback = self.commitFunction, 
        processOnInput=True)
    
    def RWidgetReload(self):
        self.commitFunction()
    def processdata(self, data):
        if data:
            if not self.require_librarys(['reshape']):
                self.status.setText(_('R Libraries Not Loaded.'))
                return
            self.RFunctionParam_data=data.getData()
            self.data = data
            colnames = self.R('colnames('+self.RFunctionParam_data+')')
            self.RFunctionParam_measure_var.update(colnames)
            self.RFunctionParam_id_var.update(colnames)
            if self.commit.processOnInput():
                self.commitFunction()
        else:
            self.RFunctionParam_measure_var.clear()
            self.RFunctionParam_id_var.clear()
    def commitFunction(self):
        if not self.require_librarys(['reshape']):
            self.status.setText(_('R Libraries Not Loaded.'))
            return
        if self.RFunctionParam_na_rm == 0: pna = 'TRUE'
        else: pna = 'FALSE'
        if self.RFunctionParam_data == '': return
        mvItem = self.RFunctionParam_measure_var.selectedItems()
        try:
            mvStr = []
            for item in mvItem:
                mvStr.append(unicode(item.text()))
            mvStr = ', measure.var = c(\''+'\',\''.join(mvStr)+'\')'
            if mvStr == ', measure.var = c(\'\')':
                mvStr = ''
        except:
            mvStr = ''
        ivItem = self.RFunctionParam_id_var.selectedItems()
        try:
            ivStr = []
            for item in ivItem:
                ivStr.append(unicode(ivItem.text()))
            ivStr = ', id.var = c(\''+'\',\''.join(ivStr)+'\')'
            if ivStr == ', id.var = c(\'\')': ivStr = ''
        except:
            ivStr = ''
        self.R('OldRownames<-rownames('+unicode(self.RFunctionParam_data)+')', wantType = 'NoConversion')
        self.R(self.Rvariables['melt.data.frame']+'<-melt.data.frame(data=cbind('+unicode(self.RFunctionParam_data)+', OldRownames),na.rm='+unicode(pna)+mvStr+',variable.name="'+unicode(self.RFunctionParam_variable_name.text())+'"'+ivStr+')', wantType = 'NoConversion')
        self.R('rm(OldRownames)', wantType = 'NoConversion')
        # copy the signals class and send the newData
        newData = redRRDataFrame(data = self.Rvariables['melt.data.frame'])
        newData.dictAttrs = self.data.dictAttrs.copy()
        self.rSend("id0", newData)
        