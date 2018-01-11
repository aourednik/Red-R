"""
<name>List Selection</name>
<tags>Subsetting</tags>
"""

from OWRpy import *
import redRGUI
from libraries.base.signalClasses.RDataFrame import RDataFrame as redRRDataFrame
from libraries.base.signalClasses.RVector import RVector as redRRVector
from libraries.base.signalClasses.RList import RList as redRRList
from libraries.base.signalClasses.RMatrix import RMatrix as redRRMatrix
from libraries.base.signalClasses.RVariable import RVariable as redRRVariable
from libraries.base.signalClasses.RArbitraryList import RArbitraryList as redRRArbitraryList

from libraries.base.qtWidgets.listBox import listBox
from libraries.base.qtWidgets.groupBox import groupBox
from libraries.base.qtWidgets.widgetLabel import widgetLabel
from libraries.base.qtWidgets.button import button as RedRButton
from libraries.base.qtWidgets.checkBox import checkBox as redRCheckBox
import redRi18n
_ = redRi18n.get_(package = 'base')
class ListSelector(OWRpy):
    globalSettingsList= ['commit']
    def __init__(self, parent=None, signalManager=None):
        OWRpy.__init__(self)
        
        #self.selection = 0
        self.setRvariableNames(['listelement'])
        self.data = None
        
        self.inputs.addInput('id0', _('R List'), [redRRList, redRRArbitraryList] , self.process)

        self.outputs.addOutput('id0', _('R Data Frame'), redRRDataFrame)
        self.outputs.addOutput('id1', _('R Vector'), redRRVector)
        self.outputs.addOutput('id2', _('R List'), redRRList)
        self.outputs.addOutput('id3', _('R Variable'), redRRVariable)
        self.outputs.addOutput('id4', _('R Matrix'), redRRMatrix)

        
        #GUI
        #box = groupBox(self.controlArea, "List Data")
        
        self.names = listBox(self.controlArea, label=_("List of Data"), displayLabel=True,
        callback = self.selectionChanged)
        self.infoa = widgetLabel(self.controlArea, '')
        
        self.commit = redRCommitButton(self.bottomAreaRight, _("Commit"), callback = self.sendSelection,
        processOnChange=True, processOnInput=True)

        
    def process(self, data):
        self.data = None
        
        if data:
            self.data = data.getData()
            names = self.R('names('+self.data+')', wantType = 'list')
            print unicode(names)
            if names == None:
                names = range(1, self.R('length('+self.data+')')+1)
                print names
            self.names.update(names)
            if self.commit.processOnInput():
                self.sendSelection()
        else:
            self.names.clear()
            for signal in self.outputs.outputIDs():
                self.rSend(signal, None)
          
    def selectionChanged(self):
        if self.commit.processOnChange():
            self.sendSelection()
        
    def sendSelection(self):
        #print self.names.selectedItems()[0]
        if self.data == None: 
            self.status.setText('No data to process')
            return
        name = unicode(self.names.row(self.names.currentItem())+1)
        self.Rvariables['listelement'] = self.data+'[['+name+']]'
        # use signals converter in OWWidget to convert to the signals class
        myclass = self.R('class('+self.Rvariables['listelement']+')')
        print myclass
        if myclass == 'data.frame':
            
            newData = redRRDataFrame(data = self.Rvariables['listelement'], parent = self.Rvariables['listelement'])
            self.rSend("id0", newData)
            #self.infoa.setText('Sent Data Frame')
            slot = 'Data Frame'
        elif myclass == 'list':
            newData = redRRList(data = self.Rvariables['listelement'])
            self.rSend("id2", newData)
            #self.infoa.setText('Sent List')
            slot = 'List'
        elif myclass in ['vector', 'character', 'factor', 'logical', 'numeric', 'integer', ['POSIXt', 'POSIXct']]:
            newData = redRRVector(data = self.Rvariables['listelement'])
            self.rSend("id1", newData)
            #self.infoa.setText('Sent Vector')
            slot = 'Vector'
        elif myclass in ['matrix']:
            newData = redRRMatrix(data = self.Rvariables['listelement'])
            self.rSend("id4", newData)
            #self.infoa.setText('Sent Matrix')
            slot = 'Matrix'
        else:
            newData = redRRVariable(data = self.Rvariables['listelement'])
            self.rSend("id3", newData)
            slot = 'R Variable'
        
        self.infoa.setText(_('Sent %(NAME)s as %(SLOT)s') % {'NAME':name, 'SLOT':slot})