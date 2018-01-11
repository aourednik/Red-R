"""
<name>Data Entry2</name>
<description>A table input data entry into a data.frame.</description>
<tags>Prototypes</tags>
<RFunctions>base:data.frame</RFunctions>
<icon>readfile.png</icon>
<priority>20</priority>
"""

import redRGUI
from OWRpy import *
from libraries.base.signalClasses.RDataFrame import RDataFrame as redRRDataFrame
from libraries.base.qtWidgets.checkBox import checkBox
from libraries.base.qtWidgets.button import button
from libraries.base.qtWidgets.groupBox import groupBox
from libraries.base.qtWidgets.Rtable import Rtable
from libraries.base.qtWidgets.table import table
from libraries.base.qtWidgets.lineEdit import lineEdit
class dataEntry2(OWRpy):
    
    def __init__(self, parent=None, signalManager=None):
        OWRpy.__init__(self, wantGUIDialog = 1)

        self.rowCount = 1
        self.colCount = 1
        self.maxRow = 0 # sets the most extreme row and cols
        self.maxCol = 0
        self.classes = None
        self.savedData = None
        self.setRvariableNames(['table', 'table_cm'])
        
        self.inputs.addInput('Data Table', 'Data Table', redRRDataFrame, self.processDF)
        self.outputs.addOutput('Data Table', 'Data Table', redRRDataFrame) # trace problem with outputs
        #GUI.
        
        
        box = groupBox(self.GUIDialog, label = "Options")
        redRCommitButton(self.bottomAreaRight, 'Commit', self.commitTable)
        self.rowHeaders = checkBox(box, label= 'Table Annotations', buttons=['Use Row Headers', 'Use Column Headers'])
        #self.colHeaders = checkBox(box, label=None, buttons=['Use Column Headers'])
        self.rowHeaders.setChecked(['Use Row Headers', 'Use Column Headers'])
        #self.colHeaders.setChecked(['Use Column Headers'])
        self.customClasses = button(box, 'Use Custom Column Classes', callback = self.setCustomClasses)
        button(box, 'Clear Classes', callback = self.clearClasses)
        
        self.columnDialog = QDialog()
        self.columnDialog.setLayout(QVBoxLayout())
        self.columnDialog.hide()
        self.columnNameLineEdit = lineEdit(self.columnDialog, label = 'Column Name:')
        button(self.columnDialog, 'Commit', callback = self.commitNewColumn)
        button(self.bottomAreaRight, "Add Column", callback = self.addColumn)
        button(self.bottomAreaRight, "Add Row", callback = self.addRow)
        box = groupBox(self.controlArea, label = "Table", 
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred))
        #self.splitCanvas.addWidget(box)
        

        #self.R(self.Rvariables['table'] + '<- matrix("",nrow=10,ncol=10)', wantType = 'NoConversion')
        self.dataTable = table(box, label = 'Data Table', rows = 10, columns = 10)
        # if self.dataTable.columnCount() < 1:
            # self.dataTable.setColumnCount(1)
            # self.dataTable.setHorizontalHeaderLabels(['Rownames'])
        # if self.dataTable.rowCount() < 1:
            # self.dataTable.setRowCount(1)
        # self.dataTable.setHorizontalHeaderLabels(['Rownames'])
        
        self.connect(self.dataTable, SIGNAL("cellClicked(int, int)"), self.cellClicked) # works OK
        self.connect(self.dataTable, SIGNAL("cellChanged(int, int)"), self.itemChanged)
        self.window = QDialog(self)
        self.window.setLayout(QVBoxLayout())
        self.classTable = table(self.window, label = 'Data Table', rows = self.maxCol, columns = 2)
        self.resize(700,500)
        self.move(300, 25)
    
    def addRow(self):
        self.dataTable.addRows(1)
    def addColumn(self):
        self.dataTable.addColumns(1)
        
    def commitNewColumn(self):
        labels = []
        for i in range(self.colCount):
            item = self.dataTable.horizontalHeaderItem(i)
            labels.append(item.text())
        labels.append(unicode(self.columnNameLineEdit.text()))
        self.dataTable.setColumnCount(self.colCount+1)
        self.dataTable.setHorizontalHeaderLabels(labels)
        self.colCount += 1
        self.columnNameLineEdit.clear()
        self.columnDialog.hide()
        
    def processDF(self, data):
        if not data: return
        self.data = data.getData()
        self.savedData = data
        self.dataTable.setRTable(self.data)
        # pythonData = self.R('cbind(rownames = '+self.savedData.getRownames_call()+','+self.data+')')
        # self.dataTable.setTable(pythonData)
        dims = self.R('dim('+self.data+')', wantType = 'list')
        self.colCount = dims[1]+1
        self.rowCount = dims[0]
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
            #self.dataTable.setRowCount(self.rowCount+1)
            self.addRow()
            self.rowCount += 1
        if row > self.maxRow: self.maxRow = row #update the extremes of the row and cols
        if col > self.maxCol: self.maxCol = col
        #self.dataTable.setCurrentCell(row+1, col)

    def setCustomClasses(self):
        self.classTable = table(self.window, rows = self.maxCol, columns = 2)
        for j in range(1, self.colCount+1):
            cb = QComboBox()
            item = self.dataTable.item(0, j)
            if item == None:
                newitem = QTableWidgetItem(unicode('NA'))
            else:
                newitem = QTableWidgetItem(unicode(item.text()))
            cb.addItems(['Default', 'Factor', 'Numeric', 'Character'])
            self.classTable.setCellWidget(j-1, 1, cb)
            newitem.setToolTip(unicode('Set the data type for column '+unicode(newitem.text())))
            self.classTable.setItem(j-1, 0, newitem)
            
        button(self.window, 'Set Classes', callback = self.setClasses)
        button(self.window, 'Clear Classes', callback = self.clearClasses)
        self.window.show()
    def clearClasses(self):
        self.classes = None
        self.window.hide()
        
    def setClasses(self):
        if self.classTable.rowCount() != self.maxCol:
            print self.classTable.rowCount()
            print self.maxCol
            self.window.hide()
            self.setCustomClasses()
            return
        else:
            self.classes = []
            for j in range(0, self.classTable.rowCount()):
                txt = self.classTable.cellWidget(j,1)
                ct = txt.currentText()
                if ct == 'Default':
                    self.classes.append(('', ''))
                elif ct == 'Factor':
                    self.classes.append(('as.factor(', ')'))
                elif ct == 'Numeric':
                    self.classes.append(('as.numeric(', ')'))
                elif ct == 'Character':
                    self.classes.append(('as.character(', ')'))
        self.window.hide()
        self.status.setText('Classes Set')
    def commitTable(self):
        #run through the table and make the output
        
        #self.dataTable.getData()
        
        trange = self.dataTable.selectedRanges()[0]
        
        #redRLog.log(redRLog.REDRCORE, redRLog.DEBUG, ','.join([str(a) for a in trange.leftColumn(), trange.rightColumn(), trange.topRow(), trange.bottomRow()]))
        if trange.leftColumn() == trange.rightColumn() and trange.topRow() == trange.bottomRow():
            rowi = range(0, self.maxRow+1)
            coli = range(0, self.maxCol+1)
        else:

            rowi = range(trange.topRow(), trange.bottomRow()+1)
            coli = range(trange.leftColumn(), trange.rightColumn()+1)
            
        if self.dataTable.item(rowi[0], coli[0]) == None: 
            #redRLog.log(redRLog.REDRCORE, redRLog.DEBUG, 'Setting row and col headers to true')
            self.rowHeaders.setChecked(['Use Row Headers', 'Use Column Headers'])
            #self.rowHeaders.setChecked(['Use Column Headers'])
        rownames = {}
        colnames = {}
        if 'Use Row Headers' in self.rowHeaders.getChecked():
            #redRLog.log(redRLog.REDRCORE, redRLog.DEBUG, 'Using Row headers')
            for i in rowi:
                item = self.dataTable.item(i, coli[0])
                if item != None:
                    thisText = item.text()
                else: thisText = unicode(i)
                if thisText == None or thisText == '':
                    thisText = unicode(i)
                    
                rownames[unicode(i)] = unicode(thisText)
            coli = coli[1:] #index up the cols

        if 'Use Column Headers' in self.rowHeaders.getChecked():
            #redRLog.log(redRLog.REDRCORE, redRLog.DEBUG, 'Using col headers')
            for j in coli:
                item = self.dataTable.item(rowi[0], j)
                if item != None:
                    thisText = item.text()
                else: thisText = '"'+unicode(j)+'"'
                if thisText == None or thisText == '':
                    thisText = '"'+unicode(j)+'"'
                thisText = thisText.split(' ')[0]
                colnames[unicode(j)] = (unicode(thisText))
            #redRLog.log(redRLog.REDRCORE, redRLog.DEBUG, unicode(colnames))
            rowi = rowi[1:]
        rinsertion = []
        
        for j in coli:
            element = ''
            if colnames:
                element += colnames[unicode(j)]+'='
            if self.classes:
                element += self.classes[j-1][0]
            element += 'c('
            inserts = []
            for i in rowi:
                #redRLog.log(redRLog.REDRCORE, redRLog.DEBUG, 'inserting data in cell i %s, j %s' % (i, j))
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
        
        self.rSend('Data Table', self.newData)
    def loadCustomSettings(self,settings=None):
        print settings
        if settings and 'newData' in settings.keys():
            if self.newData != None:
                self.processDF(self.newData)
            