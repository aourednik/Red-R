### RedR-Savepoint Widget.  Allows the user to connect data and treat this as a save point.  the outputs will not be removed even if the upstream widgets are deleted.

"""
<name>Red-R Save Point</name>
<tags>R</tags>
"""
import redRi18n
_ = redRi18n.get_(package = 'base')
from OWRpy import * 
from libraries.base.qtWidgets.textEdit import textEdit
from libraries.base.qtWidgets.button import button
from libraries.base.qtWidgets.groupBox import groupBox
from libraries.base.qtWidgets.widgetLabel import widgetLabel
from libraries.base.qtWidgets.commitButton import commitButton as redRCommitButton
class redRSavePoint(OWRpy):
    def __init__(self, parent=None, signalManager=None):
        OWRpy.__init__(self)
        self.setRvariableNames(['saveData'])
        self.inputObject = None
        self.outputObject = None
        self.inputs.addInput('id0', _('Input Object'), 'All', self.processobject)
        self.outputs.addOutput('id0', _('Output Object'), 'All')
        self.outputs.propogateNone = self.newPropNone  ## this is here to stop the propogation of None when a None is received.
        widgetLabel(self.controlArea, _('This widget acts as a save point for analyses so that data is not lost when upstream widgets are removed.  You can use this to help manage memory in your schemas by deleting upstream data (making the schema smaller) yet retaining the analyses.'), wordWrap = True)
        redRCommitButton(self.bottomAreaRight, label = _("Commit"), callback = self.commitFunction)
        self.RoutputWindow = textEdit(self.controlArea, label = _('Input Object'))
        self.RoutputWindow2 = textEdit(self.controlArea, label = _('Output Object'))
        #box.layout().addWidget(self.RoutputWindow)
    def newPropNone(self, ask = False):
        pass
    def onLoadSavedSession(self):
        self.commitFunction()
    def processobject(self, data):
        if data:
            self.inputObject=data
        else: self.inputObject = None
        self.RoutputWindow.setText(unicode(self.inputObject))
        self.commitFunction()
    def commitFunction(self):
        if self.inputObject == None: 
            self.status.setText(_('Input Does not Exist'))
            return
        print 'Setting output'
        ## set a new variable in R which is a copy of the old variable.
        self.R(self.Rvariables['saveData']+'<-'+self.inputObject.getData())
        self.outputObject = self.inputObject.copy()
        self.outputObject.data = self.Rvariables['saveData']
        self.outputObject.parent = self.Rvariables['saveData']
        self.RoutputWindow2.setText(unicode(self.outputObject))
        self.rSend('id0', self.outputObject)    

