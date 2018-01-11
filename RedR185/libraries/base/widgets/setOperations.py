"""
<name>Set Operations</name>
<tags>Data Manipulation</tags>
<icon>datatable.png</icon>
"""

from OWRpy import * 
import redRGUI 
from libraries.base.signalClasses.RVector import RVector as redRRVector
from libraries.base.signalClasses.RList import RList as redRRList

from libraries.base.qtWidgets.button import button
from libraries.base.qtWidgets.checkBox import checkBox as redRCheckBox
from libraries.base.qtWidgets.widgetBox import widgetBox
from libraries.base.qtWidgets.groupBox import groupBox
from libraries.base.qtWidgets.listBox import listBox
from libraries.base.qtWidgets.radioButtons import radioButtons
from libraries.base.qtWidgets.textEdit import textEdit
import redRi18n
_ = redRi18n.get_(package = 'base')
class setOperations(OWRpy): 
    globalSettingsList = ['commit']

    def __init__(self, parent=None, signalManager=None):
        OWRpy.__init__(self)
        self.setRvariableNames(["intersect"])
        self.dataA = None
        self.dataB = None
        
        self.inputs.addInput('id0', _('Input Data A'), redRRList, self.processA)
        self.inputs.addInput('id1', _('Input Data B'), redRRList, self.processB)

        self.outputs.addOutput('id0', _('intersect Output'), redRRVector)
        
        box = widgetBox(self.controlArea,orientation = 'vertical')
        dataSetBox = widgetBox(box,orientation = 'horizontal')
        #pickA = groupBox(dataSetBox, "Dataset A:")
        self.colA = listBox(dataSetBox, label = _('Input Data A'), callback = self.onSelect)
        
        #pickB = groupBox(dataSetBox, "Dataset B:")
        self.colB = listBox(dataSetBox, label = _('Input Data B'), callback = self.onSelect)

        self.resultInfo = textEdit(box,label=_('Results'), displayLabel=False,includeInReports=False,
        editable=False, alignment=Qt.AlignHCenter)
        self.resultInfo.setMaximumWidth(170)
        self.resultInfo.setMaximumHeight(25)
        self.resultInfo.setMinimumWidth(170)
        self.resultInfo.setMinimumHeight(25)
        #box.layout().setAlignment(self.resultInfo,Qt.AlignHCenter)
        self.resultInfo.hide()
        self.type = radioButtons(self.bottomAreaLeft,  label = _("Perform"), 
        buttons = [_('Intersect'), _('Union'), _('Set Difference'), _('Set Equal')],setChecked=_('Intersect'),
        orientation='horizontal',callback=self.onTypeSelect)
        
        commitBox = widgetBox(self.bottomAreaRight,orientation = 'horizontal')
        self.bottomAreaRight.layout().setAlignment(commitBox, Qt.AlignBottom)

        self.commit = redRCommitButton(commitBox, _("Commit"), callback = self.commitFunction, processOnChange=True, processOnInput=True)
    
    def onSelect(self):
        if self.commit.processOnChange():
            self.commitFunction()
    def onTypeSelect(self):
        self.resultInfo.setPlainText('')
        if self.type.getChecked() == _('Set Equal'):
            self.resultInfo.show()
        else:
            self.resultInfo.hide()
        
        if self.commit.processOnChange():
            self.commitFunction()
            
    def processA(self, data):
        #print 'processA'
        if not data:
            self.colA.update([])
            return 
            
        self.dataA = data.getData()
        colsA = self.R('names('+self.dataA+')',wantType='list')
        self.colA.update(colsA)
        
        if self.commit.processOnInput():
            self.commitFunction()
    def processB(self, data):
        if not data:
            self.colB.update([])
            return 
        self.dataB = data.getData()
        colsB = self.R('names('+self.dataB+')',wantType='list') 

        self.colB.update(colsB)

        if self.commit.processOnInput():
            self.commitFunction()
    def commitFunction(self):
        if self.dataA and self.dataB:
            h = self.R('intersect(names('+self.dataA+'), names('+self.dataB+'))',wantType='list')
        else: 
            return
            
        if self.colA.selectedItems():
            nameA = self.colA.selectedItems()[0].text()
        else:
            nameA = None
        if self.colB.selectedItems():
            nameB = self.colB.selectedItems()[0].text()
        else:
            nameB = None
            
        if self.type.getChecked() == _('Intersect'):
            func = 'intersect'
        elif self.type.getChecked() == _('Union'):
            func = 'union'
        elif self.type.getChecked() == _('Set Difference'):
            func = 'setdiff'
        elif self.type.getChecked() == _('Set Equal'):
            func = 'setequal'
        else:
            return 
            
        if nameA and nameB:
            self.R(self.Rvariables['intersect']+'<-%s(y=%s[["%s"]],x=%s[["%s"]])' 
            % (func, self.dataA,nameA,self.dataB,nameB), wantType = 'NoConversion')
        elif len(h) ==1:
            self.R(self.Rvariables['intersect']+'<-%s(y=%s[["%s"]],x=%s[["%s"]])' 
            % (func, self.dataA,h[0],self.dataB,h[0]), wantType = 'NoConversion')
        else:
            return
            
        if self.type.getChecked() == _('Set Equal'):
            eq = self.R(self.Rvariables['intersect'])
            if eq:
                self.resultInfo.setPlainText('%s is equal to %s' % (nameA, nameB))
            else:
                self.resultInfo.setPlainText('%s is not equal to %s' % (nameA, nameB))
        else:
            newData = redRRVector(data = self.Rvariables["intersect"])
            self.rSend("id0", newData)
    
