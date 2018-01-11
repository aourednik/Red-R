## python filter table

from redRGUI import widgetState
import os.path, log
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
class pyDataTable(widgetState, QTableView):
    def __init__(self,widget,label=None, displayLabel=True, includeInReports=True, data=None, 
    editable=False, sortable=True, filterable=False,
    selectionBehavior=QAbstractItemView.SelectRows, 
    selectionMode = QAbstractItemView.NoSelection, 
    showResizeButtons = True,
    onFilterCallback = None,
    callback=None):
        
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


        self.data = None
        self.filteredData = None
        self.sortIndex = None
        self.criteriaList = {}
        self.parent = widget
        self.tm=None
        self.sortable=sortable
        self.editable=editable
        self.filterable=filterable
        self.onFilterCallback = onFilterCallback
        self.setSelectionBehavior(selectionBehavior)

        self.setAlternatingRowColors(True)
        
        if selectionMode != -1:
            self.setSelectionMode(selectionMode)
    
        if data:
            self.setTable(data)

        if editable:
            self.horizontalHeader().hide()
            self.verticalHeader().hide()
            
        # if sortable:
            # self.horizontalHeader().setSortIndicatorShown(True)
            # self.horizontalHeader().setSortIndicator(-1,0)
        if filterable or sortable:
            #self.horizontalHeader().setClickable(True)
            QObject.connect(self.horizontalHeader(), SIGNAL('sectionClicked (int)'), self.headerClicked)
            # self.horizontalHeader().setContextMenuPolicy(Qt.CustomContextMenu)
            # self.horizontalHeader().customContextMenuRequested.connect(self.headerClicked)

        
        if callback:
            QObject.connect(self, SIGNAL('clicked (QModelIndex)'), callback)
    def setTable(self, data):
        ## data is of the Unstructured Dict object type.  This gives access to the keys object
        
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
            
    def getSettings(self):
        # print '############################# getSettings'
        r = {
        'data': self.data
        }
        
        if self.sortIndex:
            r['sortIndex'] = self.sortIndex
        
        # print r
        return r
    def loadSettings(self,data):
        # print '############################# loadSettings'
        # print data
        if not data['data']: return 

        self.data = data['data']
        self.setTable(self.data)
        
class MyTableModel(QAbstractTableModel):   # a table model based on the filterTable table model but centered around data in the UnstructuredDict signal class.
    def __init__(self,data,parent, filteredOn = [], editable=False,
    filterable=False,sortable=False): 

        self.range = 500
        self.parent =  parent
        self.sortable = sortable
        self.editable = editable
        self.filterable = filterable
        self.filteredOn = filteredOn
        QAbstractTableModel.__init__(self,parent) 
        self.initData(data)
        
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
        
    def initData(self,data):
        self.data = data
        self.orgdata = data
        self.nrow = max([len(a) for a in self.data.getData().values()])
        self.ncol = len(self.data.keys)
        
        # self.currentRange = self.getRange(0,0)
        
        # self.arraydata = self.R('as.matrix(%s[%d:%d,%d:%d])' % (self.Rdata,
        # self.currentRange['rstart'],
        # self.currentRange['rend'],
        # self.currentRange['cstart'],
        # self.currentRange['cend']
        # ),
        # wantType = 'listOfLists',silent=True)

        # self.colnames = self.data.keys  #self.R('colnames(as.data.frame(' +Rdata+ '))', wantType = 'list',silent=True)
        # self.rownames = self.R('rownames(as.data.frame(' +Rdata+'))', wantType = 'list',silent=True)
        # if len(self.rownames) ==0: self.rownames = [1]
        # print self.rownames, self.rowCount(self)
        # print self.colnames

        # if self.arraydata == [[]]:
            # toAppend= ['' for i in xrange(self.columnCount(self))]
            # self.arraydata = [toAppend]
        # print 'self.arraydata' , self.arraydata
        
    def rowCount(self, parent): 
        return self.nrow
        #return len(self.arraydata)
    def columnCount(self, parent): 
        return self.ncol
        #return len(self.arraydata[0])
 
    def data(self, index, role): 
        # print _('in data')
        if not index.isValid(): 
            return QVariant() 
        elif role != Qt.DisplayRole: 
            return QVariant() 
        elif not self.data or self.data == None:
            return QVariant()
        # print self.currentRange['rstart'], index.row(), self.currentRange['rend'], self.currentRange['cstart'], index.column(), self.currentRange['cend']
        
        # if (
            # (self.currentRange['cstart'] + 100 > index.column() and self.currentRange['cstart'] !=1) or 
            # (self.currentRange['cend'] - 100 < index.column() and self.currentRange['cend'] != self.ncol) or 
            # (self.currentRange['rstart'] + 100 > index.row() and self.currentRange['rstart'] !=1) or 
            # (self.currentRange['rend'] - 100 < index.row() and self.currentRange['rend'] != self.nrow)
        # ):
            
            
            # self.currentRange = self.getRange(index.row(), index.column())
            
            # self.arraydata = self.R('as.matrix(%s[%d:%d,%d:%d])' % (self.Rdata,
            # self.currentRange['rstart'],
            # self.currentRange['rend'],
            # self.currentRange['cstart'],
            # self.currentRange['cend']
            # ),
            # wantType = 'list',silent=True)
        # if len(self.arraydata) == 0 or len(self.arraydata[0]) == 0:
            # return QVariant()
        #log.log(10, 5, 3, 'Filter table R data is %s' % self.Rdata)
        
        rowInd = index.row()
        colInd = self.data.keys[index.column()]
        
        return QVariant(self.data.getData()[colInd][rowInd]) 

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
        return
        if self.editable: return
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        #print 'adfasfasdfasdfas', self.R('class(%s)' % self.orgRdata)
        # if order == Qt.DescendingOrder:
            # self.Rdata = '%s[order(%s[,%d],decreasing=TRUE),]' % (self.orgRdata,self.orgRdata,Ncol+1)
        # else:
            # self.Rdata = '%s[order(%s[,%d]),]' % (self.orgRdata,self.orgRdata,Ncol+1)
            
        # self.colnames = self.R('colnames(as.data.frame(' +self.Rdata+ '))', wantType = 'list')#, silent=True)
        # self.rownames = self.R('rownames(as.data.frame(' +self.Rdata+'))', wantType = 'list')#, silent=True)
        # self.nrow = self.R('nrow(as.matrix(%s))' % self.Rdata)#, silent=True)
        # self.ncol = self.R('ncol(as.matrix(%s))' % self.Rdata)#, silent=True)
        
        # self.arraydata = self.R('as.matrix(as.matrix(%s)[%d:%d,%d:%d])' % (self.Rdata,
        # self.currentRange['rstart'],
        # self.currentRange['rend'],
        # self.currentRange['cstart'],
        # self.currentRange['cend']
        # ),
        # wantType = 'listOfLists',silent=False)

        # self.emit(SIGNAL("layoutChanged()"))


    def delete(self):
        sip.delete(self)  