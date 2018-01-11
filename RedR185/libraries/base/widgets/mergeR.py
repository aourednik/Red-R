"""
<name>Merge</name>
<tags>Data Manipulation</tags>
<icon>merge2.png</icon>
"""

from OWRpy import *
import redRGUI
from libraries.base.signalClasses.RDataFrame import RDataFrame as redRRDataFrame

from libraries.base.qtWidgets.listBox import listBox
from libraries.base.qtWidgets.button import button
from libraries.base.qtWidgets.checkBox import checkBox
from libraries.base.qtWidgets.widgetBox import widgetBox
from libraries.base.qtWidgets.groupBox import groupBox
from libraries.base.qtWidgets.widgetLabel import widgetLabel
from libraries.base.qtWidgets.radioButtons import radioButtons
import redRi18n
_ = redRi18n.get_(package = 'base')
class mergeR(OWRpy):
    globalSettingsList = ['commit']

    def __init__(self, parent=None, signalManager=None):
        OWRpy.__init__(self)
        
        # self.dataParentA = {}
        # self.dataParentB = {}
        self.dataA = ''
        self.dataB = ''
        
        
        self.inputs.addInput('id0', _('Dataset A'), redRRDataFrame, self.processA)
        self.inputs.addInput('id1', _('Dataset B'), redRRDataFrame, self.processB)

        self.outputs.addOutput('id0', _('Merged'), redRRDataFrame)

        #default values        
        self.colAsel = None
        self.colBsel = None
        #self.forceMergeAll = 0 #checkbox value for forcing merger on all data, default is to remove instances from the rows or cols.
        
        #set R variable names
        self.setRvariableNames(['merged'])
                
        #GUI
        box = widgetBox(self.controlArea,orientation='horizontal')
    
        self.colA = listBox(box, label=_('Columns to Merge From A'), callback = self.setcolA)
        self.colB = listBox(box, label=_('Columns to Merge From B'),  callback = self.setcolB)
        

        self.sortOption = checkBox(self.bottomAreaLeft, label=_('Sort by Selected Column'), displayLabel=False, 
        buttons = [_('Sort by Selected Column')], 
        toolTips = [_('logical. Should the results be sorted on the by columns?')])
        self.rownamesOption = checkBox(self.bottomAreaLeft, label = _('Include Row Names in Merge'), displayLabel = False, buttons = [_('Include Row in Merge')], toolTips = [_('This will include the row names in the data after merge.')], setChecked = [_('Include Row in Merge')])
        self.sortOption.layout().setAlignment(Qt.AlignLeft)
        
        self.mergeOptions = radioButtons(self.bottomAreaCenter,label=_('Type of merge'), displayLabel=False,
        buttons=['A+B','B+A','AB'],setChecked='A+B',
        orientation='horizontal')
        
        self.mergeOptions.layout().setAlignment(Qt.AlignCenter) 
        
        self.commit = redRCommitButton(self.bottomAreaRight, _('Commit'), callback = self.run, 
        processOnChange=True,processOnInput=True)
        
    def processA(self, data):
        #print 'processA'
        if not data:
            self.colA.clear()
            return 
        self.dataA = unicode(data.getData())
        self.dataParentA = data
        colsA = self.R('colnames('+self.dataA+')') #collect the sample names to make the differential matrix
        
        if type(colsA) is str:
            colsA = [colsA]
        colsA.insert(0, 'Rownames')
        self.colA.update(colsA)

        if self.commit.processOnInput():
            self.run()
        
    def processB(self, data):
        #print 'processB'
        if not data:
            self.colB.clear()
            return 
        self.dataB = unicode(data.getData())
        self.dataParentB = data
        colsB = self.R('colnames('+self.dataB+')') #collect the sample names to make the differential matrix
        if type(colsB) is str:
            colsB = [colsB]
        colsB.insert(0, 'Rownames')
        self.colB.update(colsB)
                
        if self.commit.processOnInput():
            self.run()
    
    def run(self):
        if self.dataA == '': return
        if self.dataB == '': return
        
        if len(self.colA.selectedItems()) == 0 or len(self.colB.selectedItems()) == 0:
            self.status.setText(_('Please make valid column selections'))
            return
        if self.dataA != '' and self.dataB != '':
            h = self.R('intersect(colnames('+self.dataA+'), colnames('+self.dataB+'))')
        else: h = None
        
        # make a temp variable that is the combination of the parent frame and the cm for the parent.
        if self.mergeOptions.getChecked() =='A+B':
            options = 'all.x=T'
        elif self.mergeOptions.getChecked() =='B+A':
            options = 'all.y=T'
        else:
            options = '' #'all.y=T, all.x=T'
        if _('Sort by Selected Column') in self.sortOption.getChecked():
            options += ', sort=TRUE'
            
        if self.colAsel == None and self.colBsel == None and type(h) is str: 
            self.colA.setCurrentRow( self.R('which(colnames('+self.dataA+') == "' + h + '")-1'))
            self.colB.setCurrentRow( self.R('which(colnames('+self.dataB+') == "' + h + '")-1'))
            
            self.R(self.Rvariables['merged']+'<-merge('+self.dataA+', '+self.dataB+','+options+')', wantType = 'NoConversion')
            self.sendMe()
        elif self.colAsel and self.colBsel:
            if self.colAsel == 'Rownames': cas = '0'
            else: cas = self.colAsel
            if self.colBsel == 'Rownames': cbs = '0'
            else: cbs = self.colBsel
            
            if 'Include Row in Merge' in self.rownamesOption.getChecked():
                self.R(self.Rvariables['merged']+'<-merge(cbind('+self.dataA+', RownamesA = rownames('+self.dataA+')), cbind('+self.dataB+', RownamesB = rownames('+self.dataB+')), by.x='+cas+', by.y='+cbs+','+options+')', wantType = 'NoConversion')
            else:
                self.R(self.Rvariables['merged']+'<-merge('+self.dataA+', '+self.dataB+', by.x='+cas+', by.y='+cbs+','+options+')', wantType = 'NoConversion')
            # if self.colAsel == 'Rownames':
                # self.R('rownames('+self.Rvariables['merged']+')<-rownames('+self.dataA+')', wantType = 'NoConversion')
            self.sendMe()

    def sendMe(self,kill=False):
            newDataAll = redRRDataFrame(data = self.Rvariables['merged'])
            newDataAll.dictAttrs = self.dataParentB.dictAttrs.copy()
            newDataAll.dictAttrs.update(self.dataParentA.dictAttrs)
            self.rSend("id0", newDataAll)
    
    def setcolA(self):
        try:
            self.colAsel = '\''+unicode(self.colA.selectedItems()[0].text())+'\''
            if self.colAsel == '\'Rownames\'':
                self.colAsel = '0'
        except: return
        if self.commit.processOnChange():
            self.run()
    def setcolB(self):
        try:
            self.colBsel = '\''+unicode(self.colB.selectedItems()[0].text())+'\''
            if self.colBsel == '\'Rownames\'':
                self.colBsel = '0'
        except: return
        if self.commit.processOnChange():
            self.run()
