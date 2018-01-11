"""
<name>Row or Column Selection</name>
<tags>Subsetting</tags>
<icon>Subset.png</icon>
"""

from OWRpy import *
import redRGUI
from libraries.base.signalClasses.RDataFrame import RDataFrame as redRRDataFrame
from libraries.base.signalClasses.RList import RList as redRRList
from libraries.base.signalClasses.RVector import RVector as redRRVector
from libraries.base.qtWidgets.radioButtons import radioButtons
from libraries.base.qtWidgets.checkBox import checkBox
from libraries.base.qtWidgets.comboBox import comboBox
from libraries.base.qtWidgets.button import button
from libraries.base.qtWidgets.commitButton import commitButton
from libraries.base.qtWidgets.groupBox import groupBox
from libraries.base.qtWidgets.widgetLabel import widgetLabel
from libraries.base.qtWidgets.separator import separator
from libraries.base.qtWidgets.listBox import listBox
from libraries.base.qtWidgets.widgetBox import widgetBox
import redRi18n
_ = redRi18n.get_(package = 'base')
class rowcolPicker(OWRpy): 
       
    globalSettingsList = ['subsetButton']

    def __init__(self, parent=None, signalManager=None):
        OWRpy.__init__(self) #initialize the widget
        self.dataClass = None
        self.dataParent = None
        self.setRvariableNames(['rowcolSelector', 'rowcolSelectorNot'])
        self.SubsetByAttached = 0
        
        self.inputs.addInput('id0', _('Data Table'), redRRDataFrame, self.setWidget)
        self.inputs.addInput('id1', _('Subsetting Vector'), redRRList, self.setSubsettingVector)

        
        self.outputs.addOutput('id0', _('Selected Items'), redRRDataFrame)
        self.outputs.addOutput('id1', _('Non-selected Items'), redRRDataFrame)

        
        #set the gui

        area = widgetBox(self.controlArea,orientation='horizontal')       
        options = widgetBox(area, orientation = 'vertical')
        
        self.rowcolBox = radioButtons(options, label=_('Select On'), buttons=[_('Column'),_('Row')], setChecked= _('Column'),
        callback=self.rowcolButtonSelected,orientation='horizontal')
        
        self.sendSection = checkBox(options,label=_('Create subset from:'), displayLabel=True,
        buttons=[_('Selected'),_('Not Selected')],
        setChecked = [_('Selected')],
        orientation='horizontal')
        

        # toolTips = [_("Select True to send data from the Data slot where the selections that you made are True."),
        # _("Select False to send data from the Not Data slot that are not the selections you made.")])
        
        
        self.invertButton = button(options, _("Invert Selection"), callback=self.invertSelection)
      
        separator(options,height=15)

        self.subsetBox = groupBox(options,label=_('Subset by'))
        self.subsetColumn = comboBox(self.subsetBox,label=_("Column:"), orientation='vertical',items=[_('Select')])
        self.subOnAttachedButton = button(self.subsetBox, _("Subset by column"), callback=self.subOnAttached)
        self.subsetBox.setDisabled(True)
        
        separator(options,height=20)

        info = widgetBox(options)
        options.layout().setAlignment(info,Qt.AlignBottom)
        self.infoBox = widgetLabel(info)
        separator(info,height=15)
        self.selectionInfoBox = widgetLabel(info)
        mainArea = widgetBox(area,orientation='vertical')
        self.attributes = listBox(mainArea, label=_('Select'),callback=self.onSelect)
        self.attributes.setSelectionMode(QAbstractItemView.ExtendedSelection)
        
        self.subsetButton = commitButton(mainArea, _("Subset on Selection"), callback=self.subset,
        processOnChange=True, processOnInput=True,alignment=Qt.AlignRight)
        
    def onSelect(self):
        count = self.attributes.selectionCount()
        self.selectionInfoBox.setText(_('# %(ITEMTYPE)ss selected: %(NUMBERSELECTED)s') % {'ITEMTYPE':self.rowcolBox.getChecked(), 'NUMBERSELECTED':unicode(count)})
        if self.subsetButton.processOnChange():
            self.subset()
    def setWidget(self, data):
        if data:
            self.data = data.getData()
            self.dataParent = data
            self.rowcolButtonSelected()
            dims = data.getDims_data()
            self.infoBox.setText(_('# Rows: %(ROWS)s\n# Columns: %(COLS)s') % {'ROWS':unicode(dims[0]), 'COLS':unicode(dims[1])})
            if self.subsetButton.processOnInput():
                self.subset()
        else:
            self.data = ''
            self.dataParent = None
            self.attributes.clear()
    def invertSelection(self):
        self.attributes.invertSelection()
        self.onSelect()
    def rowcolButtonSelected(self): #recall the GUI setting the data if data is selected
        # print self.rowcolBox.getChecked()
        # if self.dataParent:
        if not self.dataParent: return
        if self.rowcolBox.getChecked() == _('Row'): #if we are looking at rows
            r =  self.R('rownames('+self.data+')', wantType = 'list')
            if type(r) == list:
                self.attributes.update(r)

        elif self.rowcolBox.getChecked() == _('Column'): # if we are looking in the columns
            c =  self.R('colnames('+self.data+')', wantType = 'list')
            if type(c) == list:
                self.attributes.update(c)

        else: #by exclusion we haven't picked anything yet
            self.status.setText(_('You must select either Row or Column to procede'))
    def setSubsettingVector(self, data):
        if data == None: 
            self.subsetBox.setEnabled(False)
            self.ssv = ''
            self.subsetColumn.clear()
            return       
            
        self.subsetBox.setEnabled(True)

        self.ssv = data.getData()
        self.subsetColumn.clear()
        
        self.subsetColumn.addItems(self.R('names(as.list('+data.getData()+'))', wantType = 'list'))
        self.ssvdata = data
        
    def subOnAttached(self):
        if self.data == None or self.data == '': return
                
        col=unicode(self.subsetColumn.currentText())
        
        if self.rowcolBox.getChecked() == _('Row'):
            if _("Selected") in self.sendSection.getChecked():
                self.R(self.Rvariables['rowcolSelector']+'<-as.data.frame('+self.data+'[rownames('+self.data+')'+' %in% '+self.ssv+'[["'+col+'"]],,drop = FALSE])', wantType = 'NoConversion')
                newData = redRRDataFrame(data = self.Rvariables['rowcolSelector'])
                self.rSend('id0', newData)
            if _("Not Selected") in self.sendSection.getChecked():
                self.R(self.Rvariables['rowcolSelectorNot']+'<-as.data.frame('+self.data+'[!rownames('+self.data+')'+' %in% '+self.ssv+'[["'+col+'"]],,drop = FALSE])', wantType = 'NoConversion')
                newDataNot = redRRDataFrame(data = self.Rvariables['rowcolSelectorNot'])
                self.rSend('id1', newDataNot)
        elif self.rowcolBox.getChecked() == 'Column':
            if _("Selected") in self.sendSection.getChecked():
                self.R(self.Rvariables['rowcolSelector']+'<-as.data.frame('+self.data+'[,colnames('+self.data+')'+
            ' %in% '+self.ssv+'[[\''+col+'\']],drop = FALSE])', wantType = 'NoConversion')
                newData = redRRDataFrame(data = self.Rvariables['rowcolSelector'])
                self.rSend('id0', newData)
            if _("Not Selected") in self.sendSection.getChecked():
                self.R(self.Rvariables['rowcolSelectorNot']+'<-as.data.frame('+self.data+'[,!colnames('+self.data+')'+
            ' %in% '+self.ssv+'[[\''+col+'\']],drop = FALSE])', wantType = 'NoConversion')
                newDataNot = redRRDataFrame(data = self.Rvariables['rowcolSelectorNot'])
                self.rSend('id1', newDataNot)
        self.SubsetByAttached = 1
    def subset(self): # now we need to make the R command that will handle the subsetting.
        if self.data == None or self.data == '': 
            self.status.setText(_("Connect data before processing"))
            return
        
        selectedDFItems = []
        for name in self.attributes.selectedItems():
            selectedDFItems.append('"'+unicode(name.text())+'"') # get the text of the selected items
        
        
        if self.rowcolBox.getChecked() == _('Row'):
            if _("Selected") in self.sendSection.getChecked():
                self.R(self.Rvariables['rowcolSelector']+'<-as.data.frame('+self.data+'[rownames('+self.data+')'+' %in% c('+','.join(selectedDFItems)+')'+',,drop = FALSE])', wantType = 'NoConversion')
                newData = redRRDataFrame(data = self.Rvariables['rowcolSelector'])
                self.rSend('id0', newData)
            else:
                self.rSend('id0', None)
            if _("Not Selected") in self.sendSection.getChecked():
                self.R(self.Rvariables['rowcolSelectorNot']+'<-as.data.frame('+self.data+'[!rownames('+self.data+') %in% c('+','.join(selectedDFItems)+'),,drop = FALSE])', wantType = 'NoConversion')
                newDataNot = redRRDataFrame(data = self.Rvariables['rowcolSelectorNot'])
                self.rSend('id1', newDataNot)
            else:
                self.rSend('id1', None)
        elif self.rowcolBox.getChecked() == _('Column'):
            if _("Selected") in self.sendSection.getChecked():
                self.R(self.Rvariables['rowcolSelector']+'<-as.data.frame('+self.data+'[,colnames('+self.data+')'+' %in% c('+','.join(selectedDFItems)+')'+',drop = FALSE])', wantType = 'NoConversion')
                newData = redRRDataFrame(data = self.Rvariables['rowcolSelector'])
                self.rSend('id0', newData)
            else:
                self.rSend('id0', None)
            if _("Not Selected") in self.sendSection.getChecked():
                self.R(self.Rvariables['rowcolSelectorNot']+'<-as.data.frame('+self.data+'[,!colnames('+self.data+')'+' %in% c('+','.join(selectedDFItems)+'),drop = FALSE])', wantType = 'NoConversion')
                newDataNot = redRRDataFrame(data = self.Rvariables['rowcolSelectorNot'])
                self.rSend('id1', newDataNot)
            else:
                self.rSend('id1', None)
        self.SubsetByAttached = 0
    def loadCustomSettings(self,settings):
        # print '######################\n'*5
        # import pprint
        # pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(settings)
        
        selected = []
        print settings['sendSection']['redRGUIObject']['checked']
        if 'True' in settings['sendSection']['redRGUIObject']['checked']:
            selected.append('Selected')

        if 'False' in settings['sendSection']['redRGUIObject']['checked']:
            selected.append('Not Selected')
        # print selected
        self.sendSection.setChecked(selected)
