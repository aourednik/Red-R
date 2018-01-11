"""
<name>Row Filtering</name>
<tags>Subsetting</tags>
<icon>filter.png</icon>
"""

from OWRpy import *
import redRGUI
from libraries.base.signalClasses.RDataFrame import RDataFrame as redRRDataFrame
from libraries.base.signalClasses.RVector import RVector as redRRVector


from libraries.base.qtWidgets.filterTable import filterTable
from libraries.base.qtWidgets.button import button
from libraries.base.qtWidgets.widgetLabel import widgetLabel
from libraries.base.qtWidgets.widgetBox import widgetBox
from libraries.base.qtWidgets.checkBox import checkBox as redRCheckBox
import redRi18n
_ = redRi18n.get_(package = 'base')
class rowFilter(OWRpy):
    globalSettingsList = ['commitOnInput']
    def __init__(self, parent=None, signalManager = None):
        OWRpy.__init__(self)
        self.data = None
        self.orriginalData = '' # a holder for data that we get from a connection
        self.currentDataTransformation = '' # holder for data transformations ex: ((data[1:5,])[,1:3])[1:2,]
        self.dataParent = None
        
        self.currentRow = 0
        self.currentColumn = 0
        self.rowNameSelectionCriteria = ''
        self.criteriaList = {}
        
        self.setRvariableNames(['dataExplorer'])
        self.criteriaDialogList = []
        self.inputs.addInput('id0', _('Data Table'), redRRDataFrame, self.processData)
 
        self.outputs.addOutput('id0', _('Data Table'), redRRDataFrame)

        
        ######## GUI ############
        
        self.tableArea = widgetBox(self.controlArea)
        self.table = filterTable(self.controlArea, sortable=True,label=_('Data Table'),displayLabel=False,
        filterable=True,selectionMode = QAbstractItemView.NoSelection,onFilterCallback=self.onFilter)
        
        self.commitOnInput = redRCheckBox(self.bottomAreaRight, label=_('Commit'), displayLabel=False,
        buttons = [_('Commit on Filter')],
        toolTips = [_('On filter send data forward.')])
        redRCommitButton(self.bottomAreaRight, _("Commit"), callback = self.commitSubset)
        
    def processData(self, data):
        if not data: 
            self.table.clear()
            return
        self.dataParent = data

        self.data  = data.getData()
        self.table.setRTable(self.data)
        
    def onFilter(self):
        if _('Commit on Filter') in self.commitOnInput.getChecked():
            self.commitSubset()

    def commitSubset(self):
        filteredData = self.table.getFilteredData()
        newData = redRRDataFrame(data = filteredData, parent = self.dataParent.getData())

        self.rSend('id0', newData)
   
