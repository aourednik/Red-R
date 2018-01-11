"""
<name>Percentile Classifier</name>
<tags>Data Classification</tags>
"""
from OWRpy import * 
import redRGUI 
from libraries.base.signalClasses.RDataFrame import RDataFrame as redRRDataFrame
from libraries.base.qtWidgets.spinBox import spinBox
from libraries.base.qtWidgets.lineEdit import lineEdit
from libraries.base.qtWidgets.listBox import listBox
from libraries.base.qtWidgets.button import button
from libraries.base.qtWidgets.textEdit import textEdit
import redRi18n
_ = redRi18n.get_(package = 'base')
class percentileClassifier(OWRpy): 
    globalSettingsList = ['commitButton']
    def __init__(self, parent=None, signalManager=None):
        OWRpy.__init__(self)
        self.setRvariableNames(["percentileClassifier_df", "percentileClassifier", 'percentileClassifier_cm'])
        self.data = ''
        self.dataParent = None
        self.inputs.addInput('id0', _('Data Frame'), redRRDataFrame, self.processData)

        self.outputs.addOutput('id0', _('Data Frame'), redRRDataFrame)

        
        ### GUI ###
        self.colNames_listBox = listBox(self.controlArea, label = _('Column Names:'),callback=self.onChange)
        self.colNames_listBox.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.percentile_spinBox = spinBox(self.controlArea, label= _('Percentile Cutoff Selector:'), min = 0, max = 100, callback=self.onChange)
        self.percentile_lineEdit = lineEdit(self.controlArea, label = _('Percentile Cutoff:'), toolTip = _('Input multiple cutoffs in the form; a, b, c.  Where a, b, and c are cutoffs.\nThis takes the place of the Percentile Cutoff Selector if not blank.'))
        self.outputWindow = textEdit(self.controlArea, label = _('Output Summary'))
        
        self.commitButton = redRCommitButton(self.bottomAreaRight, _("Commit"), callback = self.commit,
        processOnInput=True,processOnChange=True)
        
    def onChange(self):
        if self.commitButton.processOnChange():
            self.commit()
    def processData(self, data):
        if data:
            self.data = data.getData()
            self.dataParent = data
            redRLog.log(redRLog.REDRCORE, redRLog.DEBUG, str(self.R('colnames('+self.data+')', wantType = 'list')))
            self.colNames_listBox.update(self.R('colnames('+self.data+')', wantType = 'list'))
            self.outputWindow.clear()
            if self.commitButton.processOnInput():
                self.commit()
        else:
            self.data = ''
            self.dataParent = {}
        
        
        
    def commit(self):
        # set a column where the classes are either greater than or less than the xth percentile of the selected column
        self.outputWindow.clear()
        if self.data == '': 
            self.outputWindow.insertHtml(_('No data to work with'))
            return
        if self.dataParent == {}: 
            self.outputWindow.insertHtml(_('No data to work with'))
            return
        items = self.colNames_listBox.selectedItems()
        if len(items) == 0: 
            self.outputWindow.insertHtml(_('No items selected in the Column Names box'))
            return
        percentile = [unicode(self.percentile_spinBox.value())]
        if unicode(self.percentile_lineEdit.text()) not in ['', ' ']:
            lineText = unicode(self.percentile_lineEdit.text())
            lineText.replace(' ', '')
            percentile = lineText.split(',')
        self.R(self.Rvariables['percentileClassifier_df']+'<-'+self.data, wantType = 'NoConversion')
        self.outputWindow.insertHtml(_('<table class="reference" cellspacing="0" border="1" width="100%"><tr><th align="left" width="50%">New Column Name</th><th align="left" width="50%">Number above percentile</th></tr>'))
        for percent in percentile:
            if int(percent) == 0 or int(percent) == 100: continue
            for item in items:
                
                column = unicode(item.text())
                length = self.R('length(na.omit('+self.data+'[,\''+column+'\']))')
                
                self.R(self.Rvariables['percentileClassifier_df'] + '$' + column+'_'+unicode(percent).strip(' ')+'percentile' + '<- !is.na(' + self.Rvariables['percentileClassifier_df'] +'$'+column+ ') & ' + self.Rvariables['percentileClassifier_df'] + '$'+column+' > sort('+self.Rvariables['percentileClassifier_df']+'$'+column+')['+unicode(percent).strip(' ')+'/100*'+unicode(length)+']', wantType = 'NoConversion')
                self.outputWindow.insertHtml('<tr><td width="50%">' + column+'_'+unicode(percent)+'percentile</td><td width="50%">'+unicode(self.R('sum(as.numeric('+self.Rvariables['percentileClassifier_df'] + '$' + column+'_'+unicode(percent).strip(' ')+'percentile))'))+'</td></tr>')
        self.outputWindow.insertHtml('</table>')
        newData = self.dataParent.copy()
        newData.data = self.Rvariables['percentileClassifier_df']
        self.rSend("id0", newData)