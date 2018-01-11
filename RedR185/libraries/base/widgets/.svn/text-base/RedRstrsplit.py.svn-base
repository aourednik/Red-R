"""
<name>strsplit</name>
<tags>Prototypes</tags>
"""
from OWRpy import * 
import redRGUI 
import libraries.base.signalClasses as signals
from libraries.base.signalClasses.RVector import RVector as redRRVector
from libraries.base.signalClasses.RList import RList as redRRList
from libraries.base.signalClasses.RDataFrame import RDataFrame as redRDataFrame
from libraries.base.qtWidgets.lineEdit import lineEdit
from libraries.base.qtWidgets.radioButtons import radioButtons
from libraries.base.qtWidgets.button import button
import redRi18n
_ = redRi18n.get_(package = 'base')
class RedRstrsplit(OWRpy): 
    settingsList = []
    def __init__(self, parent=None, signalManager=None):
        OWRpy.__init__(self)
        self.setRvariableNames(["strsplit", "dataframe"])
        self.data = {}
        self.RFunctionParam_x = ''
        self.inputs.addInput('id0', _('Input Data'), redRRVector, self.processx)

        self.outputs.addOutput('id0', _('strsplit Output'), redRRList)
        self.outputs.addOutput('id1', _('strsplit Vector'), redRRVector)
        self.outputs.addOutput('dataframe', _('Data Table'), redRDataFrame)

        
        self.RFunctionParamsplit_lineEdit =  lineEdit(self.controlArea,  label = _("Split Text Using:"), text = '')
        self.RFunctionParamfixed_radioButtons =  radioButtons(self.controlArea,  label = _("fixed:"), buttons = [_('Use text exactly'), _('Use text as expression (Advanced)')], setChecked = _('Use text exactly'), orientation = 'horizontal')
        self.RFunctionParamextended_radiButtons =  radioButtons(self.controlArea,  label = _("Extend Expressions:"), buttons = [_('Yes'), _('No')], setChecked = _('No'), orientation = 'horizontal')
        self.RFunctionParamperl_radioButtons =  radioButtons(self.controlArea,  label = _("Use Perl Expressions:"), buttons = [_('Yes'), _('No')], setChecked = _('No'), orientation = 'horizontal')
        self.RFunctionParamunlist_radioButtons = radioButtons(self.controlArea, label = _('Convert to RVector'), buttons = [_('Send only the list'), _('Send list and vector')], setChecked = _('Send list and vector'), orientation = 'horizontal')
        redRCommitButton(self.bottomAreaRight, _("Commit"), callback = self.commitFunction)
    def processx(self, data):
        if not self.require_librarys(["base"]):
            self.status.setText('R Libraries Not Loaded.')
            return
        if data:
            self.RFunctionParam_x=data.getData()
            #self.data = data
            self.commitFunction()
        else:
            self.RFunctionParam_x=''
    def commitFunction(self):
        if unicode(self.RFunctionParam_x) == '': 
            self.status.setText(_('No Data to Split'))
            return
        if unicode(self.RFunctionParamsplit_lineEdit.text()) == '':
            self.status.setText(_('No string to split on'))
            return
        injection = []
        if unicode(self.RFunctionParamfixed_radioButtons.getChecked()) == _('Yes'):
            string = 'fixed=TRUE'
            injection.append(string)
        else:
            string = 'fixed=FALSE'
            injection.append(string)
        if unicode(self.RFunctionParamextended_radiButtons.getChecked()) == _('Yes'):
            string = 'extended=TRUE'
            injection.append(string)
        else:
            string = 'extended=FALSE'
            injection.append(string)
        if unicode(self.RFunctionParamsplit_lineEdit.text()) != '':
            string = 'split='+unicode(self.RFunctionParamsplit_lineEdit.text())+''
            injection.append(string)
        if unicode(self.RFunctionParamperl_radioButtons.getChecked()) == _('Yes'):
            string = 'perl=TRUE'
            injection.append(string)
        else:
            string = 'perl=FALSE'
            injection.append(string)
        inj = ','.join(injection)
        self.R(self.Rvariables['strsplit']+'<-strsplit(x= as.character('+unicode(self.RFunctionParam_x)+') ,'+inj+')', wantType = 'NoConversion')
        newData = redRRList(data = self.Rvariables["strsplit"]) # moment of variable creation, no preexisting data set.  To pass forward the data that was received in the input uncomment the next line.
        #newData.copyAllOptinoalData(self.data)  ## note, if you plan to uncomment this please uncomment the call to set self.data in the process statemtn of the data whose attributes you plan to send forward.
        self.rSend("id0", newData)
        
        if unicode(self.RFunctionParamunlist_radioButtons.getChecked()) == _('Send list and vector'):
            newData = redRRVector(data = 'unlist('+self.Rvariables['strsplit']+')')
            self.rSend("id1", newData)
            
        ## convert to a data frame
        self.R(
        """
        for(i in 1:length(%s)){
            if(length(%s[[i]]) == 0){
                %s[[i]] = c('','')
            }
        }
        """ % (self.Rvariables['strsplit'], self.Rvariables['strsplit'], self.Rvariables['strsplit']),
        wantType = 'NoConversion',
        silent = True)
        self.R(self.Rvariables['dataframe']+'<-t(data.frame('+self.Rvariables['strsplit']+'))', wantType = 'NoConversion')
        newDataFrame = redRDataFrame(data = self.Rvariables['dataframe'], parent = self.Rvariables['dataframe'], checkVal = False)
        self.rSend('dataframe', newDataFrame)
        
