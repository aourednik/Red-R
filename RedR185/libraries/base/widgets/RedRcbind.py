"""
<name>cbind</name>
<RFunctions>base:cbind</RFunctions>
"""
from OWRpy import * 
import redRGUI 
from libraries.base.signalClasses.RDataFrame import RDataFrame as redRRDataFrame

from libraries.base.qtWidgets.lineEdit import lineEdit
from libraries.base.qtWidgets.widgetBox import widgetBox
from libraries.base.qtWidgets.checkBox import checkBox
from libraries.base.qtWidgets.button import button
import redRi18n
_ = redRi18n.get_(package = 'base')
class RedRcbind(OWRpy): 
    globalSettingsList = ['commit']
    def __init__(self, parent=None, signalManager=None):
        OWRpy.__init__(self)
        self.setRvariableNames(["cbind"])
        self.data = {}
        self.RFunctionParam_a = ''
        self.RFunctionParam_b = ''
        self.inputs.addInput('id0', _('Input Data A'), redRRDataFrame, self.processa)
        self.inputs.addInput('id1', _('Input Data B'), redRRDataFrame, self.processb)

        self.outputs.addOutput('id0', _('Output Data'), redRRDataFrame)

        
        self.RFunctionParamdeparse_level_lineEdit = lineEdit(self.controlArea, label = _("deparse_level:"), text = '1')
        
        buttonBox = widgetBox(self.controlArea,orientation='horizontal',alignment=Qt.AlignRight)
        self.commit = redRCommitButton(buttonBox, _("Commit"), callback = self.commitFunction, processOnInput=True)
        
        
    def processa(self, data):
        if not self.require_librarys(["base"]):
            self.status.setText(_('R Libraries Not Loaded.'))
            return
        if data:
            self.RFunctionParam_a=data.getData()
            #self.data = data
            if self.commit.processOnInput():
                self.commitFunction()
                
        else:
            self.RFunctionParam_a=''
    def processb(self, data):
        if not self.require_librarys(["base"]):
            self.status.setText(_('R Libraries Not Loaded.'))
            return
        if data:
            self.RFunctionParam_b=data.getData()
            #self.data = data
            if self.commit.processOnInput():
                self.commitFunction()
        else:
            self.RFunctionParam_b=''
    def commitFunction(self):
        if unicode(self.RFunctionParam_a) == '': return
        if unicode(self.RFunctionParam_b) == '': return
        injection = []
        if unicode(self.RFunctionParamdeparse_level_lineEdit.text()) != '':
            string = 'deparse.level='+unicode(self.RFunctionParamdeparse_level_lineEdit.text())+''
            injection.append(string)
        inj = ','.join(injection)
        self.R(self.Rvariables['cbind']+'<-cbind('+unicode(self.RFunctionParam_a)+','+unicode(self.RFunctionParam_b)+','+inj+')', wantType = 'NoConversion')
        newData = redRRDataFrame(data = self.Rvariables["cbind"]) # moment of variable creation, no preexisting data set.  To pass forward the data that was received in the input uncomment the next line.
        #newData.copyAllOptinoalData(self.data)  ## note, if you plan to uncomment this please uncomment the call to set self.data in the process statemtn of the data whose attributes you plan to send forward.
        self.rSend("id0", newData)
