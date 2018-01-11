"""
<name>Principal Component</name>
<icon>stats.png</icon>
<tags>Parametric</tags>
"""
from OWRpy import * 
import OWGUI 
import redRGUI 
from libraries.base.signalClasses.RDataFrame import RDataFrame as redRRDataFrame
from libraries.base.signalClasses.RMatrix import RMatrix as redRRMatrix
from libraries.base.signalClasses.RModelFit import RModelFit as redRRModelFit
import libraries.base.signalClasses as signals
from libraries.base.qtWidgets.button import button
from libraries.base.qtWidgets.checkBox import checkBox
from libraries.base.qtWidgets.commitButton import commitButton as redRCommitButton

class prcomp(OWRpy): 
    globalSettingsList = ['commit']
    def __init__(self, parent=None, signalManager=None):
        OWRpy.__init__(self)
        self.setRvariableNames(["prcomp"])
         
        self.RFunctionParam_x = ''
        self.inputs.addInput('id0', 'x', redRRDataFrame, self.processx)

        self.outputs.addOutput('id0', 'prcomp Output', redRRModelFit)
        self.outputs.addOutput('id1', 'Scaled Data', redRRMatrix)
        self.options = checkBox(self.controlArea, label = 'Options:', buttons = ['Center', 'Scale'])
        self.options.setChecked(['Center', 'Scale'])

        self.commit = redRCommitButton(self.bottomAreaRight, "Commit", callback = self.commitFunction,
        processOnInput=True)
    def processx(self, data):
        if data:
            self.RFunctionParam_x=data.getData()
            if self.commit.processOnInput():
                self.commitFunction()
        else:
            self.RFunctionParam_x = ''
    def commitFunction(self):
        if unicode(self.RFunctionParam_x) == '': return
        injection = []
        if 'Center' in self.options.getChecked():
            injection.append('center = TRUE')
        else:
            injection.append('center = FALSE')
        if 'Scale' in self.options.getChecked():
            injection.append('scale = TRUE')
        else:
            injection.append('scale = FALSE')
        inj = ','.join(injection)
        self.R(self.Rvariables['prcomp']+'<-prcomp(x=data.matrix('+unicode(self.RFunctionParam_x)+'), '+inj+')')
        
        newPRComp = redRRModelFit(data = self.Rvariables['prcomp'])
        self.rSend("id0", newPRComp)
        newPRCompMatrix = redRRMatrix(data = self.Rvariables['prcomp']+'$x')
        self.rSend("id1", newPRCompMatrix)
    def getReportText(self, fileDir):
        text = 'This widget generates principal component fits to data and sends that fit and the resulting matrix of components to downstream widgets.  Please see the .rrs file or other output for more informaiton.\n\n'
        return text
