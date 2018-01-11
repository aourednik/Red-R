from redRGUI import widgetState
import os.path, redRLog
import redREnviron, redRReports
from libraries.base.qtWidgets.widgetBox import widgetBox
from libraries.base.qtWidgets.groupBox import groupBox
from libraries.base.qtWidgets.button import button
from libraries.base.qtWidgets.widgetLabel import widgetLabel
from libraries.base.qtWidgets.scrollArea import scrollArea
from libraries.base.qtWidgets.lineEdit import lineEdit
from libraries.base.qtWidgets.checkBox import checkBox


from RSession import Rcommand
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sip
import redRi18n
_ = redRi18n.get_(package = 'base')

class filterTable(widgetState, QTableView):
    def __init__(self,widget,label=None, displayLabel=True, includeInReports=True, Rdata=None, 
    editable=False, sortable=True, filterable=False,
    selectionBehavior=QAbstractItemView.SelectRows, 
    selectionMode = QAbstractItemView.ExtendedSelection, 
    showResizeButtons = True,
    onFilterCallback = None,
    callback=None,
    selectionCallback=None):
        
        widgetState.__init__(self,widget,label,includeInReports)
        
        if displayLabel:
            mainBox = groupBox(self.controlArea,label=label, orientation='vertical')
        else:
            mainBox = widgetBox(self.controlArea,orientation='vertical')
        self.label = label
        
        QTableView.__init__(self,self.controlArea)
        mainBox.layout().addWidget(self)
        box = widgetBox(mainBox,orientation='horizontal')
        leftBox = widgetBox(box,orientation='horizontal')
        if filterable:
            self.clearButton = button(leftBox,label=_('Clear All Filtering'), callback=self.clearFiltering)
        self.dataInfo = widgetLabel(leftBox,label='',wordWrap=False) 
        box.layout().setAlignment(leftBox, Qt.AlignLeft)

        
        if showResizeButtons:
            resizeColsBox = widgetBox(box, orientation="horizontal")
            resizeColsBox.layout().setAlignment(Qt.AlignRight)
            box.layout().setAlignment(resizeColsBox, Qt.AlignRight)
            widgetLabel(resizeColsBox, label = _("Resize columns: "))
            button(resizeColsBox, label = "+", callback=self.increaseColWidth, 
            toolTip = _("Increase the width of the columns"), width=30)
            button(resizeColsBox, label = "-", callback=self.decreaseColWidth, 
            toolTip = _("Decrease the width of the columns"), width=30)
            button(resizeColsBox, label = _("Resize To Content"), callback=self.resizeColumnsToContents, 
            toolTip = _("Set width based on content size"))

        
        self.R = Rcommand
        self.Rdata = None
        self.filteredData = None
        self.sortIndex = None
        self.criteriaList = {}
        self.parent = widget
        self.tm=None
        self.sortable=sortable
        self.editable=editable
        self.filterable=filterable
        self.onFilterCallback = onFilterCallback
        self.selectionCallback = selectionCallback
        self.selections = QItemSelection()
        self.working = False

        self.setHorizontalHeader(myHeaderView(self))
        self.setSelectionBehavior(selectionBehavior)
        self.setAlternatingRowColors(True)
        
        if selectionMode != -1:
            self.setSelectionMode(selectionMode)
    
        if Rdata:
            self.setRTable(Rdata)

        if editable:
            self.horizontalHeader().hide()
            self.verticalHeader().hide()
            
        # if sortable:
            # self.horizontalHeader().setSortIndicatorShown(True)
            # self.horizontalHeader().setSortIndicator(-1,0)
        if filterable or sortable:
            self.horizontalHeader().setClickable(True)
            # QObject.connect(self.horizontalHeader(), SIGNAL('sectionClicked (int)'), self.selectColumn)
            self.horizontalHeader().setContextMenuPolicy(Qt.CustomContextMenu)
            self.horizontalHeader().customContextMenuRequested.connect(self.headerClicked)

            
        if callback:
            QObject.connect(self, SIGNAL('clicked (QModelIndex)'), callback)
    def selectColumn(self,val):
        print 'selectColumn#############################', val

    def cellSelection(self,newSelected,oldSelected):
        # print 'cellSelection ################', newSelected, oldSelected
        #print self.selectionModel().selectedColumns()#, self.selectionModel().selectedRows() 
        self.selections.merge(newSelected,QItemSelectionModel.Select)
        self.selections.merge(oldSelected,QItemSelectionModel.Deselect)
        inds = self.selections.indexes()
        
        if self.working:
            return 
        self.working = True
        rows = []
        cols = []
        if len(self.selectionModel().selectedColumns()) > 0:
            for x in self.selectionModel().selectedColumns():
                cols.append(str(x.column()+1))
            tmpData = '%s[,c(%s)]' % (self.Rdata, ','.join(cols))
        elif len(self.selectionModel().selectedRows()) > 0:
            for x in self.selectionModel().selectedRows():
                cols.append(str(x.row()+1))
            tmpData = '%s[c(%s),]' % (self.Rdata, ','.join(rows))
        else:
            for ind in inds:
                #print _('new'), ind.row(),ind.column()
                rows.append(str(ind.row()+1))
                cols.append(str(ind.column()+1))

            self.R('rowInd <- c(' + ','.join(rows) + ')',silent=True)
            self.R('colInd <- c(' + ','.join(cols) + ')',silent=True)
            
            self.R('tmpData <- apply(cbind(rowInd,colInd),1,FUN=function(x) {%s[x[1],x[2]]})' % self.Rdata, silent=True)
            tmpData = 'tmpData'
            
        self.selectionCallback(tmpData)
        self.working = False
        
    def setRTable(self,data, setRowHeaders = 1, setColHeaders = 1,filtered=False):
        # print _('in setRTable'), data
        if self.R('class(%s)' %data, silent=True) != 'data.frame':
            data = 'as.data.frame(%s)' %data
        #self.Rdata = Rdata
        if not filtered:
            self.Rdata = data
            self.filteredData = data
            self.criteriaList = {}
            filteredCols = []
            
        else:
            filteredCols = self.criteriaList.keys()
        total = self.R('nrow(%s)' % self.Rdata,silent=True)        
        if self.filterable:
            filtered = self.R('nrow(%s)' % data,silent=True)
            self.dataInfo.setText(_('Showing %d of %d rows.') % (filtered,total))
        else:
            self.dataInfo.setText(_('Showing %d rows.') % (total))

        self.tm = MyTableModel(data,self,editable=self.editable, 
        filteredOn = filteredCols, filterable=self.filterable,sortable=self.sortable)
        self.setModel(self.tm)
    
    def setModel(self, model):
        QTableView.setModel(self, model)
        if self.selectionCallback:
            self.connect(self.selectionModel(),  
                         SIGNAL("selectionChanged(QItemSelection, QItemSelection)"),  
                         self.cellSelection) 

    def resizeColumnsToContents(self):
        QTableView.resizeColumnsToContents(self)
        for i in range(self.tm.columnCount(self)):
            if self.columnWidth(i) > 600:
                self.setColumnWidth(i,600)

    def increaseColWidth(self):        
        for col in range(self.tm.columnCount(self)):
            w = self.columnWidth(col)
            self.setColumnWidth(col, w + 10)

    def decreaseColWidth(self):
        for col in range(self.tm.columnCount(self)):
            w = self.columnWidth(col)
            minW = self.sizeHintForColumn(col)
            self.setColumnWidth(col, max(w - 10, minW))

    def columnCount(self):
        if self.tm:
            return self.tm.columnCount(self)
        else:
            return 0
    
    def rowCount(self):
        if self.tm:
            return self.tm.rowCount(self)
        else:
            return 0
    
    def copy(self):
        selection = self.selectionModel() #self.table = QAbstractItemView
        indexes = selection.selectedIndexes()

        columns = indexes[-1].column() - indexes[0].column() + 1
        rows = len(indexes) / columns
        textTable = [[""] * columns for i in xrange(rows)]

        for i, index in enumerate(indexes):
         textTable[i % rows][i / rows] = unicode(self.tm.data(index,Qt.DisplayRole).toString()) #self.model = QAbstractItemModel 

         qApp.clipboard().setText("\n".join(("\t".join(i) for i in textTable)))
    
    def keyPressEvent(self, event):
        if event.matches(QKeySequence.Copy):
            self.copy()
        else:
            QTableView.keyPressEvent(self,event)

    def addRows(self,count,headers=None):
        self.tm.insertRows(self.tm.rowCount(self),count,headers=headers)
    def addColumns(self,count,headers=None):
        self.tm.insertColumns(self.tm.columnCount(self),count,headers)
    def clear(self):
        self.setRTable('matrix("")')
        self.criteriaList = {}
    def headerClicked(self,val):
        
        selectedCol = self.horizontalHeader().logicalIndexAt(val) + 1
        self.createMenu(selectedCol)
    
    def getData(self,row,col):
        if not self.tm: return False
        return self.tm.data(self.tm.createIndex(row,col),Qt.DisplayRole).toString()
    def createMenu(self, selectedCol):
        #print selectedCol, pos
        # print _('in createMenu'), self.criteriaList

        globalPos = QCursor.pos() #self.mapToGlobal(pos)
        self.menu = QDialog(None,Qt.Popup)
        self.menu.setLayout(QVBoxLayout())
        if self.sortable:
            box = widgetBox(self.menu,orientation='horizontal')
            box.layout().setAlignment(Qt.AlignLeft)
            button(box,label='A->Z',callback= lambda: self.sort(selectedCol,Qt.AscendingOrder))
            widgetLabel(box,label=_('Ascending Sort'))
            box = widgetBox(self.menu,orientation='horizontal')
            box.layout().setAlignment(Qt.AlignLeft)
            button(box,label='Z->A',callback= lambda: self.sort(selectedCol,Qt.DescendingOrder))
            widgetLabel(box,label=_('Descending Sort'))
            # qmenu = QMenu(self.menu)
            # self.menu.layout().addWidget(qmenu)
            # a = QAction('A->Z',self.menu)
            # qmenu.addAction(a)
            # self.menu.addAction(a)

        if not self.filterable:
            self.menu.move(globalPos)
            self.menu.show()
            return
        
        if self.sortable:
            hr = QFrame(self.menu)
            hr.setFrameStyle( QFrame.Sunken + QFrame.HLine );
            hr.setFixedHeight( 12 );
            self.menu.layout().addWidget(hr)
    
        
        clearButton = button(self.menu,label=_('Clear Filter'),
        callback=lambda col=selectedCol: self.createCriteriaList(col,self.menu,action='clear'))
        self.menu.layout().setAlignment(clearButton,Qt.AlignHCenter)
        clearButton.hide()
        
        self.numericLabel = widgetLabel(self.menu,label=_('Enter a value for one of these critera:'))
        self.numericLabel.hide()
        self.stringLabel = widgetLabel(self.menu,label=_('Enter a value for one of these critera (case sensitive):'))
        self.stringLabel.hide()
        
        self.factorLabel = widgetLabel(self.menu,label=_('Select Levels:'))
        self.factorLabel.hide()
        
        
        if selectedCol in self.criteriaList.keys():
            clearButton.show()
        
        self.optionsBox = widgetBox(self.menu)
        self.optionsBox.layout().setAlignment(Qt.AlignTop)
        
        colClass = self.R('class(%s[,%d])' % (self.Rdata,selectedCol),silent=True)
        
        if colClass in ['factor','logical']:
            self.factorLabel.show()
            
            if selectedCol in self.criteriaList.keys():
                checked = self.criteriaList[selectedCol]['value']
            else:
                checked = []
            if colClass =='logical':
                levels = ['TRUE','FALSE']
            else:
                levels = self.R('levels(%s[,%d])' % (self.Rdata,selectedCol),wantType='list', silent=True)
                
            if len(levels) > 1:
                levels.insert(0,_('Check All'))
            scroll = scrollArea(self.optionsBox,spacing=1)
            
            c = checkBox(scroll,label=_('Levels'),displayLabel=False, buttons=levels,setChecked = checked)
            scroll.setWidget(c.controlArea)
            
            QObject.connect(c.buttons, SIGNAL('buttonClicked (int)'), lambda val : self.factorCheckBox(val,self.optionsBox))
    
        elif colClass in ['integer','numeric']:
            self.numericLabel.show()
            self.options = [_('Equals'), _('Does Not Equal'),_('Greater Than'),_('Greater Than Or Equal To'), 
            _('Less Than'), _('Less Than or Equal To'), 'Between\n(2 numbers comma\nseparated, inclusive)', 
            'Not Between\n(2 numbers comma\nseparated)']
            for x in self.options:
                if selectedCol in self.criteriaList and self.criteriaList[selectedCol]['method'] == _('Numeric ') + x:
                    e = lineEdit(self.optionsBox,label=x,text=self.criteriaList[selectedCol]['value'])
                else:
                    e = lineEdit(self.optionsBox,label=x)
                self.connect(e, SIGNAL("textEdited(QString)"),
                lambda val, col=selectedCol,field=x : self.clearOthers(val,self.optionsBox,field))
    
        elif colClass in ['character']:
            self.stringLabel.show()
            self.options = [_('Equals'), _('Does Not Equal'),_('Begins With'),_('Ends With'), 
            _('Contains'), _('Does Not Contain')]
            for x in self.options:
                if selectedCol in self.criteriaList and self.criteriaList[selectedCol]['method'] == _('String ') + x:
                    e = lineEdit(self.optionsBox,label=x,text=self.criteriaList[selectedCol]['value'])
                else:
                    e = lineEdit(self.optionsBox,label=x)
                self.connect(e, SIGNAL("textEdited(QString)"),
                lambda val, col=selectedCol,field=x : self.clearOthers(val,self.optionsBox,field))
            
        buttonBox = widgetBox(self.optionsBox,orientation='horizontal')
        buttonBox.layout().setAlignment(Qt.AlignRight)
        okButton = button(buttonBox,label=_('OK'),
        callback=lambda col=selectedCol: self.createCriteriaList(col,self.optionsBox,action=_('OK')))
        okButton.setDefault (True)
        button(buttonBox,label=_('Cancel'),
        callback=lambda col=selectedCol: self.createCriteriaList(col,self.optionsBox,action='cancel'))
        
        self.menu.move(globalPos)
        self.menu.show()
    def factorCheckBox(self,val,menu):
        if val != 0: return
        checkbox = menu.findChildren(checkBox)[0]
        if checkbox.buttonAt(0) != _('Check All'): return
        #print checkbox.getChecked(), _('Check All') in checkbox.getChecked()
        if _('Check All') in checkbox.getChecked():
            checkbox.checkAll()
        else: 
            checkbox.uncheckAll()
        
    def clearOthers(self,val, menu, field):
        # print '##############', val, field
        for label,value in zip(menu.findChildren(QLabel),menu.findChildren(QLineEdit)):
            if label.text() != field:
                value.setText('')

    def clearFiltering(self):
        self.criteriaList = {}
        # self.horizontalHeader().setSortIndicator(-1,order)
        self.filter()
        
    def createCriteriaList(self,col,menu,action):
        #print 'in filter@@@@@@@@@@@@@@@@@@@@@@@@@@', col,action
        #print self.criteriaList
        if action=='cancel':
            self.menu.hide()
            return
        colClass = self.R('class(%s[,%d])' % (self.Rdata,col),silent=True)
        if action =='clear':
            del self.criteriaList[col]
        elif action=='OK':
            if colClass in ['integer','numeric']:
                for label,value in zip(menu.findChildren(QLabel),menu.findChildren(QLineEdit)):
                    if value.text() != '':
                        # print label.text(),value.text()
                        self.criteriaList[col] = {'column':col, "method": _('Numeric ') + unicode(label.text()), "value": unicode(value.text())}
            elif colClass in ['character']:
                for label,value in zip(menu.findChildren(QLabel),menu.findChildren(QLineEdit)):
                    if value.text() != '':
                        # print label.text(),value.text()
                        self.criteriaList[col] = {'column':col, "method": _('String ') + unicode(label.text()), "value": unicode(value.text())}
            elif colClass in ['factor','logical']:
                checks = menu.findChildren(checkBox)[0].getChecked()
                if _('Check All') in checks:
                    checks.remove(_('Check All'))
                if len(checks) != 0:
                    self.criteriaList[col] = {'column':col, "method": colClass, "value": checks}
                else:
                    del self.criteriaList[col]
            
        #print _('criteriaList'), self.criteriaList
        self.menu.hide()
        self.filter()
    
    def filter(self):
        filters  = []
        for col,criteria in self.criteriaList.items():
            #print _('in loop'), col,criteria['method']
            if _('Numeric Equals') == criteria['method']:
                filters.append('%s[,%s] == %s' % (self.Rdata,col,criteria['value']))
            elif _('Numeric Does Not Equal') == criteria['method']:
                filters.append('%s[,%s] != %s' % (self.Rdata,col,criteria['value']))
            elif _('Numeric Greater Than') == criteria['method']:
                filters.append('%s[,%s] > %s' % (self.Rdata,col,criteria['value']))
            elif _('Numeric Greater Than Or Equal To') == criteria['method']:
                filters.append('%s[,%s] >= %s' % (self.Rdata,col,criteria['value']))
            elif _('Numeric Less Than') == criteria['method']:
                filters.append('%s[,%s] < %s' % (self.Rdata,col,criteria['value']))
            elif _('Numeric Less Than or Equal To') == criteria['method']:
                filters.append('%s[,%s] <= %s' % (self.Rdata,col,criteria['value']))
            elif 'Numeric Between\n(2 numbers comma\nseparated, inclusive)' == criteria['method']:
                (start,comma,stop) = criteria['value'].partition(',')
                if start !='' and stop !='' or comma == ',':
                    filters.append('%s[,%s] >= %s & %s[,%s] <= %s' % (self.Rdata,col,start,self.Rdata,col,stop))
            elif 'Numeric Not Between\n(2 numbers comma\nseparated)' == criteria['method']:
                (start,comma, stop) = criteria['value'].partition(',')
                if start !='' and stop !='' or comma == ',':
                    filters.append('%s[,%s] < %s | %s[,%s] > %s' % (self.Rdata,col,start,self.Rdata,col,stop))

            elif _('String Equals') == criteria['method']:
                filters.append('%s[,%s] == "%s"' % (self.Rdata,col,criteria['value']))
            elif _('String Does Not Equal') == criteria['method']:
                filters.append('%s[,%s] != "%s"' % (self.Rdata,col,criteria['value']))
            elif _('String Begins With') == criteria['method']:
                filters.append('grepl("^%s",%s[,%s])' % (criteria['value'],self.Rdata,col))
            elif _('String Ends With') == criteria['method']:
                filters.append('grepl("%s$",%s[,%s])' % (criteria['value'],self.Rdata,col))
            elif _('String Contains') == criteria['method']:
                filters.append('grepl("%s",%s[,%s])' % (criteria['value'],self.Rdata,col))
            elif _('String Does Not Contain') == criteria['method']:
                filters.append('!grepl("%s",%s[,%s])' % (criteria['value'],self.Rdata,col))
            
            
            elif criteria['method'] in ['logical','factor']:
                f= '","'.join([unicode(x) for x in criteria['value']])
                filters.append(self.Rdata+'[,'+unicode(col)+'] %in% as.factor(c("'+f+'"))')
            #elif 'logical' == critera['method']:
            
       # print 'filters:', filters
        self.filteredData = '%s[%s,,drop = F]' % (self.Rdata,' & '.join(filters))
        #print 'string:', self.filteredData
        self.setRTable(self.filteredData,filtered=True)
        if self.onFilterCallback:
            self.onFilterCallback()
             
    def getFilteredData(self):
        try:
            return self.tm.Rdata
        except:
            return None
    def sort(self,col,order):
        #self.tm.sort(col-1,order)
        self.sortByColumn(col-1, order)
        self.horizontalHeader().setSortIndicator(col-1,order)
        self.menu.hide()
        self.sortIndex = [col-1,order]
        
        
    def getSettings(self):
        # print '############################# getSettings'
        r = {
        'Rdata': self.Rdata,
        'filteredData':self.filteredData,
        'criteriaList': self.criteriaList,
        'selection':[[i.row(),i.column()] for i in self.selectedIndexes()]
        }
        
        if self.sortIndex:
            r['sortIndex'] = self.sortIndex
        
        # print r
        return r
    def startProgressBar(self, title,text,max):
        progressBar = QProgressDialog()
        progressBar.setCancelButtonText(QString())
        progressBar.setWindowTitle(title)
        progressBar.setLabelText(text)
        progressBar.setMaximum(max)
        progressBar.setValue(0)
        progressBar.show()
        return progressBar
    def loadSettings(self,data):
        print _('loadSettings for a filter table')
        # print data
        if not data['Rdata']: return 
        progressBar = self.startProgressBar(_('Filter Table Loading'), _('Loading Fiter Table'), 50)
        self.Rdata = data['Rdata']
        self.criteriaList = data['criteriaList']
        print 'filtering data on the following criteria %s' % unicode(self.criteriaList)
        self.filter()

        if 'sortIndex' in data.keys():
            self.sortByColumn(data['sortIndex'][0],data['sortIndex'][1])
        selModel = self.selectionModel()
        # print selModel
        if 'selection' in data.keys() and len(data['selection']):
            if len(data['selection']) > 1000:
                mb = QMessageBox.question(None, _('Setting Selection'), _('There are more than 1000 selections to set for %s,\ndo you want to discard them?\nSetting may take a very long time.') % self.label, QMessageBox.Yes, QMessageBox.No)
                if mb.exec_() == QMessageBox.No:
                
                    progressBar.setLabelText(_('Loading Selections'))
                    progressBar.setMaximum(len(data['selection']))
                    progressBar.setValue(0)
                    val = 0
                    for i in data['selection']:
                        selModel.select(self.tm.createIndex(i[0],i[1]),QItemSelectionModel.Select)
                        val += 1
                        progressBar.setValue(val)
        progressBar.hide()
        progressBar.close()
     
    def delete(self):
        sip.delete(self)
    def getReportText(self, fileDir):
        if self.getFilteredData():
            limit = min(self.tm.rowCount(self),50)
            # import time
            # start = time.time()
            # print 'start'
            data = self.R('as.matrix(%s[1:%d,])'% (self.getFilteredData(),limit))
            # print 'stop', time
            colNames = self.R('colnames(%s)' % self.getFilteredData())
            # text = redRReports.createTable(data, columnNames = colNames)
            return {self.widgetName:{'includeInReports': self.includeInReports, 'type':'table', 
            'data':data,'colNames': colNames,
            'numRowLimit': limit}}

        else:
            return {self.widgetName:{'includeInReports': self.includeInReports, 'text':''}}
        


class MyTableModel(QAbstractTableModel): 
    def __init__(self,Rdata,parent, filteredOn = [], editable=False,
    filterable=False,sortable=False): 

        self.working = False
        self.range = 500
        self.parent =  parent
        self.R = Rcommand
        self.sortable = sortable
        self.editable = editable
        self.filterable = filterable
        self.filteredOn = filteredOn
        QAbstractTableModel.__init__(self,parent) 
        self.initData(Rdata)
        self.filter_delete = QIcon(os.path.join(redREnviron.directoryNames['picsDir'],'filter_delete.gif'))
        self.filter_add = QIcon(os.path.join(redREnviron.directoryNames['picsDir'],'filter_add.gif'))
        
    def flags(self,index):
        if self.editable:
            return (Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled)
        else:
            return (Qt.ItemIsSelectable | Qt.ItemIsEnabled)
 
    def getRange(self,row,col):
        r = {}
        if row-self.range < 0:
            r['rstart'] = 1
        else:
            r['rstart'] = row-self.range
        
        
        if row+self.range > self.nrow:
            r['rend'] = self.nrow
        else:
            r['rend'] = row+self.range
        
        
        if col-self.range < 0:
            r['cstart'] = 1
        else:
            r['cstart'] = col-self.range
        
        #print 'cend: ', row+self.range,  self.nrow        
        if col+self.range > self.ncol:
            r['cend'] = self.ncol
        else:
            r['cend'] = col+self.range
        
        return r
        
    def initData(self,Rdata):
        self.Rdata = Rdata
        self.orgRdata = Rdata
        self.nrow = self.R('nrow(%s)' % self.Rdata,silent=True)
        self.ncol = self.R('ncol(%s)' % self.Rdata,silent=True)
        
        self.currentRange = self.getRange(0,0)
        
        self.arraydata = self.R('as.matrix(%s[%d:%d,%d:%d])' % (self.Rdata,
        self.currentRange['rstart'],
        self.currentRange['rend'],
        self.currentRange['cstart'],
        self.currentRange['cend']
        ),
        wantType = 'listOfLists',silent=True)
        
        # print _('self.arraydata loaded')

        self.colnames = self.R('colnames(as.data.frame(' +Rdata+ '))', wantType = 'list',silent=True)
        self.rownames = self.R('rownames(as.data.frame(' +Rdata+'))', wantType = 'list',silent=True)
        if len(self.rownames) ==0: self.rownames = [1]
        # print self.rownames, self.rowCount(self)
        # print self.colnames

        if self.arraydata == [[]]:
            toAppend= ['' for i in xrange(self.columnCount(self))]
            self.arraydata = [toAppend]
        # print 'self.arraydata' , self.arraydata
        
    def rowCount(self, parent): 
        return self.nrow
        #return len(self.arraydata)
    def columnCount(self, parent): 
        return self.ncol
        #return len(self.arraydata[0])
 
    def data(self, index, role): 
        # print _('in data')
        # if self.working == True:
            # return QVariant()
        # self.working = True
        if not index.isValid(): 
            return QVariant() 
        elif role != Qt.DisplayRole: 
            return QVariant() 
        elif not self.Rdata or self.Rdata == None:
            return QVariant()
        # print self.currentRange['rstart'], index.row(), self.currentRange['rend'], self.currentRange['cstart'], index.column(), self.currentRange['cend']
        
        if (
            (self.currentRange['cstart'] + 100 > index.column() and self.currentRange['cstart'] !=1) or 
            (self.currentRange['cend'] - 100 < index.column() and self.currentRange['cend'] != self.ncol) or 
            (self.currentRange['rstart'] + 100 > index.row() and self.currentRange['rstart'] !=1) or 
            (self.currentRange['rend'] - 100 < index.row() and self.currentRange['rend'] != self.nrow)
        ):

            self.currentRange = self.getRange(index.row(), index.column())
            if not self.working:
                self.working = True
                self.arraydata = self.R('as.matrix(%s[%d:%d,%d:%d])' % (self.Rdata,
            self.currentRange['rstart'],
            self.currentRange['rend'],
            self.currentRange['cstart'],
            self.currentRange['cend']
            ),
            wantType = 'list',silent=True)
                self.working = False
                
            else: self.arraydata = []
        if len(self.arraydata) == 0 or len(self.arraydata[0]) == 0:
            return QVariant()
        #redRLog.log(redRLog.REDRCORE, redRLog.DEBUG, 'Filter table R data is %s' % self.Rdata)
        
        rowInd = index.row() - self.currentRange['rstart'] + 1
        colInd = index.column() - self.currentRange['cstart'] + 1
        # self.working = False
        return QVariant(self.arraydata[rowInd][colInd]) 

    def headerData(self, col, orientation, role):
        # print _('in headerData'), col, orientation, role
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.colnames[col])
        elif orientation == Qt.Horizontal and role == Qt.DecorationRole and (self.filterable or self.sortable):
            # print _('DecorationRole')
            if col+1 in self.filteredOn:
                # print self.filter_delete
                return QVariant(self.filter_delete)
            else:
                # print self.filter_add
                return QVariant(self.filter_add)
                
            #return QVariant(icon)
        elif orientation == Qt.Vertical and role == Qt.DisplayRole:     
            return QVariant(self.rownames[col])
        return QVariant()
    

    def sort(self, Ncol, order):
        if self.editable: return
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        #print 'adfasfasdfasdfas', self.R('class(%s)' % self.orgRdata)
        if order == Qt.DescendingOrder:
            self.Rdata = '%s[order(%s[,%d],decreasing=TRUE),]' % (self.orgRdata,self.orgRdata,Ncol+1)
        else:
            self.Rdata = '%s[order(%s[,%d]),]' % (self.orgRdata,self.orgRdata,Ncol+1)
            
        self.colnames = self.R('colnames(as.data.frame(' +self.Rdata+ '))', wantType = 'list')#, silent=True)
        self.rownames = self.R('rownames(as.data.frame(' +self.Rdata+'))', wantType = 'list')#, silent=True)
        self.nrow = self.R('nrow(as.matrix(%s))' % self.Rdata)#, silent=True)
        self.ncol = self.R('ncol(as.matrix(%s))' % self.Rdata)#, silent=True)
        
        self.arraydata = self.R('as.matrix(as.matrix(%s)[%d:%d,%d:%d])' % (self.Rdata,
        self.currentRange['rstart'],
        self.currentRange['rend'],
        self.currentRange['cstart'],
        self.currentRange['cend']
        ),
        wantType = 'listOfLists',silent=False)

        self.emit(SIGNAL("layoutChanged()"))


    def delete(self):
        sip.delete(self)  
  

class myHeaderView(QHeaderView):
    def __init__(self,parent):
        QHeaderView.__init__(self,Qt.Horizontal,parent)
    
