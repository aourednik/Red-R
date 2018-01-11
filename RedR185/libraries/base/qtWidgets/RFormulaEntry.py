## RFormula; provides a toolkit for editing R formulas where an R funciton may need a formulas

from redRGUI import widgetState

from libraries.base.qtWidgets.groupBox import groupBox
from libraries.base.qtWidgets.button import button
from libraries.base.qtWidgets.listBox import listBox
from libraries.base.qtWidgets.widgetBox import widgetBox
from libraries.base.qtWidgets.comboBox import comboBox
from libraries.base.qtWidgets.lineEdit import lineEdit
from libraries.base.qtWidgets.widgetLabel import widgetLabel
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import redRi18n
_ = redRi18n.get_(package = 'base')
class RFormulaEntry(widgetState):
    def __init__(self, widget, label = _('Formula Entry'), displayLabel=True, includeInReports=True):
        # make a widgetBox to hold everything
        widgetState.__init__(self,widget,label,includeInReports)
        
        box = groupBox(self.controlArea,label=label)

        ## add the elements to the box
        #place the command keys
        self.buttonsBox = groupBox(box, label = _("Formula Commands"))
        self.plusButton = button(self.buttonsBox, _("And (+)"), callback = self.plusButtonClicked)
        self.plusButton.setEnabled(False)
        self.colonButton = button(self.buttonsBox, _("Interacting With (:)"), callback = self.colonButtonClicked)
        self.colonButton.setEnabled(False)
        self.starButton = button(self.buttonsBox, _("Together and Interacting (*)"), callback = self.starButtonClicked)
        self.starButton.setEnabled(False)
        button(self.buttonsBox, _('Clear'), self.clearFormula)
        self.elementsListBox = listBox(self.buttonsBox, label = _('Elements'), callback = self.FormulaEntryElementSelected)
        self.elementsListBox.setEnabled(True)
        
        # place the formula line edit
        self.modelBox = groupBox(box, label = _("Model Formula"), orientation = 'horizontal')
        self.extrasBox = widgetBox(self.modelBox)
        self.outcomeVariable = comboBox(self.modelBox, label = _('Outcome (f(x)):'))
        widgetLabel(self.modelBox, ' = ')
        self.modelLineEdit = lineEdit(self.modelBox, label = _('model'), displayLabel=False)
        self.label = label
    def clear(self):
        self.elementsListBox.clear()
        self.outcomeVariable.clear()
        self.clearFormula()
    def clearFormula(self):
        self.modelLineEdit.clear()
        #self.elementsListBox.clear()
        #self.outcomeVariable.clear()
        self.updateEnabled(1)
    def addItems(self, items):
        self.clearFormula()
        self.elementsListBox.clear()
        self.outcomeVariable.addItem('')
        for item in items:
            self.outcomeVariable.addItem(item)
        self.elementsListBox.addItems(items)
        
    def updateEnabled(self, pos):
        # 1 is the beginning state of the widget, 0 is the state after an element is selected
        self.elementsListBox.setEnabled(pos)
        self.plusButton.setEnabled(not pos)
        self.colonButton.setEnabled(not pos)
        self.starButton.setEnabled(not pos)
    def FormulaEntryElementSelected(self):
        self.modelLineEdit.setText(unicode(self.modelLineEdit.text()) + unicode(self.elementsListBox.currentItem().text()))
        self.updateEnabled(0)
        
    def plusButtonClicked(self):
        self.modelLineEdit.setText(unicode(self.modelLineEdit.text()) + ' + ')
        self.updateEnabled(1)
        
    def colonButtonClicked(self):
        self.modelLineEdit.setText(unicode(self.modelLineEdit.text()) + ' : ')
        self.updateEnabled(1)
        
    def starButtonClicked(self):
        self.modelLineEdit.setText(unicode(self.modelLineEdit.text()) + ' * ')
        self.updateEnabled(1)
        
    def Formula(self):
        return (unicode(self.outcomeVariable.currentText()), unicode(self.modelLineEdit.text())) # returns the left and right of the formula.  Users are expected to insert the ~ where appropriate.
    def getSettings(self):
        itemsText = []
        for item in self.elementsListBox.items():
           itemsText.append(unicode(item.text()))
                
        r = {'current':self.outcomeVariable.currentIndex(), 
        'buttonState': self.elementsListBox.isEnabled(), 'listBoxItems':itemsText}
        
        return r
        #items = []
        #for item in self.elementsListBox.items():
    def loadSettings(self, data):
        try:
            self.elementsListBox.addItems(data['listBoxItems'])
            self.outcomeVariable.addItems(data['listBoxItems'])
            self.updateEnabled(data['buttonState'])
            self.outcomeVariable.setCurrentIndex(data['current'])
        except:
            print _("Loading of RFormulaEntry encountered an error.")
        
    def update(self, items):
        
        self.outcomeVariable.update(items)
        self.elementsListBox.update(items)
            
    def getReportText(self, fileDir):
        (a,b) = self.Formula()
        return {self.widgetName:{'includeInReports': self.includeInReports, 'text':a + ' = ' + b}}
        