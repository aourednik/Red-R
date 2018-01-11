"""
<name>eigen</name>
<tags>Prototypes</tags>
"""
from OWRpy import * 
import redRGUI 

from libraries.base.signalClasses.RDataFrame import RDataFrame as redRRDataFrame
from libraries.base.signalClasses.RMatrix import RMatrix as redRRMatrix
from libraries.base.signalClasses.RList import RList as redRRList

from libraries.base.qtWidgets.button import button
from libraries.base.qtWidgets.radioButtons import radioButtons
import redRi18n
_ = redRi18n.get_(package = 'base')
class RedReigen(OWRpy): 
    settingsList = []
    def __init__(self, parent=None, signalManager=None):
        OWRpy.__init__(self)
        self.setRvariableNames(["eigen"])
        self.data = {}
        self.RFunctionParam_x = ''
        self.inputs.addInput('id0', _('Input Data'), redRRMatrix, self.processx)

        self.outputs.addOutput('id0', _('Eigen Output'), redRRList)

        
        self.RFunctionParamsymmetric_radioButtons =  radioButtons(self.controlArea,  label = _("symmetric:"), buttons = [_('Yes'), _('No')], setChecked = _('Yes'))
        self.RFunctionParamonly_values_radioButtons =  radioButtons(self.controlArea,  label = _("only_values:"), buttons = [_('Yes'), _('No')], setChecked = _('Yes'))
        self.RFunctionParamEISPACK_radioButtons =  radioButtons(self.controlArea,  label = _("EISPACK:"), buttons = [_('Yes'), _('No')], setChecked = _('Yes'))
        button(self.bottomAreaRight, _("Commit"), callback = self.commitFunction)
    def processx(self, data):
        if not self.require_librarys(["base"]):
            self.status.setText(_('R Libraries Not Loaded.'))
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
        if unicode(self.RFunctionParamsymmetric_radioButtons.text()) == _('Yes'):
            string = 'symmetric=TRUE'
            injection.append(string)
        else:
            string = 'symmetric=FALSE'
            injection.append(string)
        if unicode(self.RFunctionParamonly_values_radioButtons.text()) == _('Yes'):
            string = 'only.values=TRUE'
            injection.append(string)
        else:
            string = 'only.values=FALSE'
            injection.append(string)
        if unicode(self.RFunctionParamEISPACK_radioButtons.text()) == _('Yes'):
            string = 'EISPACK=TRUE'
            injection.append(string)
        else:
            string = 'EISPACK=FALSE'
            injection.append(string)
        inj = ','.join(injection)
        self.R(self.Rvariables['eigen']+'<-eigen(x='+unicode(self.RFunctionParam_x)+','+inj+')', wantType = 'NoConversion')
        newData = signals.redRRList(data = self.Rvariables["eigen"]) # moment of variable creation, no preexisting data set.  To pass forward the data that was received in the input uncomment the next line.
        #newData.copyAllOptinoalData(self.data)  ## note, if you plan to uncomment this please uncomment the call to set self.data in the process statemtn of the data whose attributes you plan to send forward.
        self.rSend("id0", newData)
