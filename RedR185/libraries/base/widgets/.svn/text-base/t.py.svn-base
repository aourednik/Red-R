"""
<name>Transpose</name>
<tags>Data Manipulation</tags>
"""
from OWRpy import * 

from libraries.base.signalClasses.RDataFrame import RDataFrame as redRRDataFrame
from libraries.base.signalClasses.RMatrix import RMatrix as redRRMatrix

from libraries.base.qtWidgets.button import button
from libraries.base.qtWidgets.checkBox import checkBox as redRCheckBox
import redRi18n
_ = redRi18n.get_(package = 'base')
class t(OWRpy): 
    globalSettingsList = ['commit']
    def __init__(self, parent=None, signalManager=None):
        OWRpy.__init__(self)
        self.setRvariableNames(["t"])
        self.RFunctionParam_x = ''
        self.data={}
        
        
        self.inputs.addInput('id0', _('Input Data Table or Matrix'), [redRRDataFrame, redRRMatrix], self.processx)

        self.outputs.addOutput('id0', _('Transposed Data Table'), redRRDataFrame)

        self.commit = redRCommitButton(self.bottomAreaRight, _("Commit"), callback = self.commitFunction,
        processOnInput=True)
    def processx(self, data):
        if data:
            self.RFunctionParam_x=data.getData()
            self.data = data
            if self.commit.processOnInput():
                self.commitFunction()
    def commitFunction(self):
        if self.x == '': return
        
        self.R(self.Rvariables['t']+'<-as.data.frame(t(x='+unicode(self.RFunctionParam_x)+'))', wantType = 'NoConversion')
        
        newData = redRRDataFrame(data = self.Rvariables['t'])
        newData.dictAttrs = self.data.dictAttrs.copy()
        self.rSend("id0", newData)
