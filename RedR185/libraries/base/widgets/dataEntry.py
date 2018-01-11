"""
<name>Data Entry</name>
<tags>Data Input</tags>
<icon>readfile.png</icon>
"""

import redRGUI
from OWRpy import *
from libraries.base.signalClasses.RDataFrame import RDataFrame as redRRDataFrame
from libraries.base.qtWidgets.table import table
from libraries.base.qtWidgets.pyDataTable import pyDataTable as pyDataTable
from libraries.base.qtWidgets.button import button
from libraries.base.qtWidgets.groupBox import groupBox
from libraries.base.qtWidgets.lineEdit import lineEdit
import redRi18n
_ = redRi18n.get_(package = 'base')
class dataEntry(OWRpy):
    
    def __init__(self, parent=None, signalManager=None):
        OWRpy.__init__(self)

        self.rowCount = 1
        self.colCount = 1
        self.maxRow = 0 # sets the most extreme row and cols
        self.maxCol = 0
        self.classes = None
        self.savedData = None
        self.setRvariableNames(['table', 'table_cm'])
        
        self.inputs.addInput('id0', _('Data Table'), redRRDataFrame, self.processDF)

        self.outputs.addOutput('id0', _('Data Table'), redRRDataFrame)
        #GUI.
        
        redRCommitButton(self.bottomAreaRight, _('Commit'), self.commitTable)

        self.columnDialog = QDialog(self)
        self.columnDialog.setLayout(QVBoxLayout())
        self.columnDialog.hide()
        self.columnNameLineEdit = lineEdit(self.columnDialog, label = _('Column Name:'))
        button(self.columnDialog, _('Commit'), callback = self.commitNewColumn)
        button(self.bottomAreaRight, _("Add Column"), callback = self.columnDialog.show)
        
        box = groupBox(self.controlArea, label = _("Table"), 
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred))
        #self.splitCanvas.addWidget(box)
        

        self.dataTable = pyDataTable(box,label=_('Data Entry'),displayLabel=False,
        data = None)
        
        self.connect(self.dataTable, SIGNAL("cellClicked(int, int)"), self.cellClicked) # works OK
        self.connect(self.dataTable, SIGNAL("cellChanged(int, int)"), self.itemChanged)
        self.connect(self.dataTable, SIGNAL('sectionClicked (int)'), self.headerClicked)
        self.resize(700,500)
        self.move(300, 25)
    def headerClicked(self, index):
        globalPos = QCursor.pos() #self.mapToGlobal(pos)
        self.menu = QDialog(None,Qt.Popup)
        self.menu.setLayout(QVBoxLayout())
        box = widgetBox(self.menu, orientation = 'horizontal')
        name = lineEdit(box, label = _('New Name (Overrides Current Value)'), callback = self.menu.accept)
        equation = lineEdit(box, label = _('Equation (Overrides Current Values)'), callback = self.menu.accept)
        remove = button(box, label = _('Remove Column'), callback = lambda: self.removeColumn(index))
        done = button(box, label = _('Done'), callback = self.menu.accept)
        res = self.menu.exec_()
        if res == Qt.Accept:
            if unicode(equation.text()) != '':
                self.calculateEquation(current = , equation = unicode(equation.text()))
            if unicode(name.text()) != '':
                self.resetName(current = , new = unicode(name.text()))
            
    def resetName(self, current, new):
        self.data.getData()[new] = self.data.getData()[current].copy()
        del self.data.getData()[current]
        for i in range(len(self.data.keys)):
            if self.data.keys[i] == current:
                self.data.keys.remove(i)
                self.data.keys.insert(i, new)
        self.table.setTable(self.data)
        self.rSend('id0', self.data)
    def calculateEquation(self, current, equation):
        self.data.getData()[current] = []
        ## parse equation  ([Sepal.length] * [Sepal.width])
        import re
        import math
        ekeys = re.findall(r'\[\w+\]', equation)
        dekeys = [t.replace('[', '').replace(']', '') for t in ekeys]
        for i in range(max([len(a) for a in self.data.getData().values()])):
            tempe = e
            for w in ekeys:
                tempe = tempe.replace(w, 'self.data.getData()[\'%s\'][%s]' % (w.replace('[', '').replace(']', ''), str(i)))
            try:
                self.data.getData()[current].append(eval(tempe))
            except:
                self.data.getData()[current].append(None)
        self.table.setTable(self.data)
        self.rSend('id0', self.data)
    def commitNewColumn(self):
        labels = []
        for i in range(self.dataTable.columnCount()):
            item = self.dataTable.horizontalHeaderItem(i)
            
            if item:
                labels.append(item.text())
        labels.append(unicode(self.columnNameLineEdit.text()))
        self.dataTable.setColumnCount(self.dataTable.columnCount()+1)
        self.dataTable.setHorizontalHeaderLabels(labels)
        self.colCount = self.dataTable.columnCount()
        self.columnNameLineEdit.clear()
        self.columnDialog.hide()
    def processDF(self, data):
        if data:
            self.data = data.copy()
            self.populateTable()
        else:
            return
    def populateTable(self):
        self.dataTable.setTable(self.data)
        self.connect(self.dataTable, SIGNAL("cellClicked(int, int)"), self.cellClicked) # works OK
        self.connect(self.dataTable, SIGNAL("cellChanged(int, int)"), self.itemChanged)
        self.connect(self.dataTable, SIGNAL('sectionClicked (int)'), self.headerClicked)
    def cellClicked(self, row, col):
        print unicode(row), unicode(col)
        pass

    def onCellFocus(self, currentRow, currentCol, tb):
        if len(tb) == 0: return
        print 'cell on focus'
        item = tb.item(currentRow, currentCol)
        tb.editItem(item)
    
    def itemChanged(self, row, col):
        if row == self.rowCount-1: #bump up the number of cells to keep up with the needs of the table
            self.dataTable.setRowCount(self.rowCount+1)
            self.rowCount += 1
        if row > self.maxRow: self.maxRow = row #update the extremes of the row and cols
        if col > self.maxCol: self.maxCol = col
        self.data.getData()[self.data.keys[col]][row] = 
        self.dataTable.setCurrentCell(row+1, col)

    def commitTable(self):
        #run through the table and make the output
        try:
            trange = self.dataTable.selectedRanges()[0]
        except:
            trange = None
        if trange and trange.leftColumn() == trange.rightColumn() and trange.topRow() == trange.bottomRow():
            rowi = range(0, self.maxRow+1)
            coli = range(0, self.maxCol+1)
        else:
            rowi = range(trange.topRow(), trange.bottomRow())
            coli = range(trange.leftColumn(), trange.rightColumn()+1)
            
       
        rownames = {}  
        colnames = {}        
        #if 'Use Row Headers' in self.rowHeaders.getChecked():
            
        for i in rowi:
            item = self.dataTable.item(i, coli[0])
            if item != None:
                thisText = item.text()
            else: thisText = unicode(i)
            if thisText == None or thisText == '':
                thisText = unicode(i)
                
            rownames[unicode(i)] = (unicode(thisText))
        coli = coli[1:] #index up the cols

       # if 'Use Column Headers' in self.rowHeaders.getChecked():
        for j in coli:
            item = self.dataTable.horizontalHeaderItem(j)
            if item != None:
                thisText = item.text()
            else: thisText = '"'+unicode(j)+'"'
            if thisText == None or thisText == '':
                thisText = '"'+unicode(j)+'"'
            thisText = thisText.split(' ')[0]
            colnames[unicode(j)] = (unicode(thisText))

        rinsertion = []
        
        for j in coli:
            element = ''
            if colnames:
                element += colnames[unicode(j)]+'='
            # if self.classes:
                # element += self.classes[j-1][0]
            element += 'c('
            inserts = []
            for i in rowi:

                tableItem = self.dataTable.item(i,j)
                if tableItem == None:
                    inserts.append('NA')
                else:
                    try: #catch if the element can be coerced to numeric in the table
                        float(tableItem.text()) #will fail if can't be coerced to int 
                        inserts.append(unicode(tableItem.text()))
                    except:
                        if tableItem.text() == 'NA': 
                            inserts.append(unicode(tableItem.text()))
                            print 'set NA'
                        elif tableItem.text() == '1.#QNAN': 
                            inserts.append('NA') #if we read in some data
                            print 'set QNAN to NA'
                        else: 
                            inserts.append('"'+unicode(tableItem.text())+'"')
                            print unicode(tableItem.text())+' set as text'

            insert = ','.join(inserts)
            element += insert+')'
            if self.classes:
                element += self.classes[j-1][1]
            rinsertion.append(element)
            
        rinsert = ','.join(rinsertion)

        if len(rownames) > 0:
            rname = []
            for i in rowi:
                if rownames[unicode(i)] in rname:
                    rname.append(rownames[unicode(i)]+'_at_'+unicode(i))
                else:
                    rname.append(rownames[unicode(i)])
            rnf = '","'.join(rname)
            rinsert += ', row.names =c("'+rnf+'")' 
        self.R(self.Rvariables['table']+'<-data.frame('+rinsert+')', wantType = 'NoConversion')
        
        # make a new data table, we copy the dictAttrs from the incoming table but nothing more, as a patch for cm managers we also remove the cm from the dictAttrs if one exists
        
        self.newData = redRRDataFrame(data = self.Rvariables['table'], parent = self.Rvariables['table'])
        
        self.rSend("id0", self.newData)
        self.processDF(self.newData)  ## a good way to ensure loading and saving.
        

            