"""
<name>Fast Discrete Fourier Transform</name>
<tags>Stats</tags>
<icon></icon>
"""
from OWRpy import * 
import redRGUI 
from libraries.base.signalClasses.RMatrix import RMatrix as redRRMatrix

from libraries.base.qtWidgets.button import button
from libraries.base.qtWidgets.radioButtons import radioButtons
from libraries.base.qtWidgets.checkBox import checkBox as redRCheckBox
from libraries.base.qtWidgets.commitButton import commitButton as redRCommitButton

class RedRfft(OWRpy): 
    globalSettingsList = ['commit']
    def __init__(self, parent=None, signalManager=None):
        OWRpy.__init__(self)
        self.setRvariableNames(["fft"])
        self.data = {}
        self.RFunctionParam_z = ''
        self.isNumeric = False
        self.inputs.addInput('id0', 'z', redRRMatrix, self.processz)

        self.outputs.addOutput('id0', 'fft Output', redRRMatrix)

        
        self.RFunctionParaminverse_radioBox = radioButtons(self.controlArea, 
        label = "inverse:", buttons = ["Yes","No"], setChecked = "No")
        
        self.commit = redRCommitButton(self.bottomAreaRight, "Commit", callback = self.commitFunction,
        processOnInput=True)

    def processz(self, data):
        if data:
            self.RFunctionParam_z=data.getData()
            if not self.R('is.numeric(%s)' % self.RFunctionParam_z, silent=True):
                self.status.setText('Data Must be Numeric')
                self.commitButton.setDisabled(True)
                return
            else:
                self.commitButton.setEnabled(True)
                self.status.setText('')
            if self.commit.processOnInput():
                self.commitFunction()
        else:
            self.RFunctionParam_z=''
    def commitFunction(self):
        if unicode(self.RFunctionParam_z) == '': return
        injection = []
        if unicode(self.RFunctionParaminverse_radioBox.getChecked()) == 'Yes':
            injection.append('inverse = TRUE')
        else:
            injection.append('inverse = FALSE')
        inj = ','.join(injection)
        self.R(self.Rvariables['fft']+'<-fft(z='+unicode(self.RFunctionParam_z)+','+inj+')')
        newData = redRRMatrix(data = self.Rvariables["fft"]) # moment of variable creation, no preexisting data set.  To pass forward the data that was received in the input uncomment the next line.
        #newData.copyAllOptinoalData(self.data)  ## note, if you plan to uncomment this please uncomment the call to set self.data in the process statemtn of the data whose attributes you plan to send forward.
        self.rSend("id0", newData)
