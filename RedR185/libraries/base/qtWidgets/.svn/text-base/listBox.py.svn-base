from redRGUI import widgetState
from libraries.base.qtWidgets.widgetBox import widgetBox
from libraries.base.qtWidgets.groupBox import groupBox
from libraries.base.qtWidgets.widgetLabel import widgetLabel
import redRReports,redRLog
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from OrderedDict import OrderedDict
import redRi18n
_ = redRi18n.get_(package = 'base')
class listBox(QListWidget,widgetState):
    def __init__(self, widget, value=None, label=None, displayLabel=True, includeInReports=True, 
    orientation='vertical', selectionMode=QAbstractItemView.SingleSelection,
    enableDragDrop = 0, dragDropCallback = None, dataValidityCallback = None, sizeHint = None, 
    callback=None, toolTip = None, items = None, *args):
        
        widgetState.__init__(self,widget,label,includeInReports)
        QListWidget.__init__(self, *args)
        self.label = label
        self.widget = self.controlArea
        if displayLabel:
            self.hb = groupBox(self.controlArea,label=label,orientation=orientation)
            
        else:
            self.hb = widgetBox(self.controlArea,orientation=orientation)
            
        self.hb.layout().addWidget(self)
        self.ogValue = value
        self.ogLabels = label
        self.enableDragDrop = enableDragDrop
        self.dragDopCallback = dragDropCallback
        self.dataValidityCallback = dataValidityCallback
        if not sizeHint:
            self.defaultSizeHint = QSize(150,100)
        else:
            self.defaultSizeHint = sizeHint
        self.setSelectionMode(selectionMode)
        if enableDragDrop:
            self.setDragEnabled(1)
            self.setAcceptDrops(1)
            self.setDropIndicatorShown(1)
            #self.setDragDropMode(QAbstractItemView.DragDrop)
            
            self.dragStartPosition = 0
        if toolTip:
            self.setToolTip(toolTip)
        
        self.listItems = OrderedDict()
        if items:
            self.addItems(items)
        
        if callback:
            QObject.connect(self, SIGNAL('itemClicked(QListWidgetItem*)'), callback)



    def getItems(self):
        return self.listItems

    def addItem(self,id,item):
        QListWidget.addItem(self,item)
        self.listItems[id] = item
    def addItems(self,items):
        if type(items) in [dict,OrderedDict]:
            for k,v in items.items():
                self.addItem(k,v)
        elif type(items) in [list]:
            if len(items) > 0 and type(items[0]) is tuple:
                for k,v in items:
                    self.addItem(k,v)
            else:
                for v in items:
                    self.addItem(v,v)
            # redRLog.log(redRLog.REDRCORE,redRLog.DEBUG,_('In listBox should not use list'))
        else:
            raise Exception(_('In listBox, addItems takes a list, dict or OrderedDict'))

    def setSelectedIds(self,ids):
        for x in ids:
            try:
                self.item(self.listItems.keys().index(x)).setSelected(True)
            except:
                pass
                
    def update(self, items):
        current = self.selectedIds()
        self.clear()
        self.addItems(items)
        self.setSelectedIds(current)
        

    def clear(self):
        QListWidget.clear(self)
        self.items = OrderedDict()

    def invertSelection(self):
        for i in range(self.count()):
            if self.isItemSelected(self.item(i)):
                self.item(i).setSelected(False)
            else:
                self.item(i).setSelected(True)
    
    def selectionCount(self):
        return len(self.selectedIndexes())
    def currentSelection(self):
            return self.selectedItems().values()
    def selectedItems(self):
        items = {}
        for x in self.selectedIndexes():
            items[self.listItems.keys()[x.row()]] = self.listItems.values()[x.row()]
        return items
    def selectedIds(self):
        ids = []
        for x in self.selectedIndexes():
            ids.append(self.listItems.keys()[x.row()])
        return ids
    
    def sizeHint(self):
        return self.defaultSizeHint
    def startDrag(self, supportedActions):
        if not self.enableDragDrop: return

        drag = QDrag(self)
        mime = QMimeData()

        if not self.ogValue:
            selectedItems = [i for i in range(self.count()) if self.item(i).isSelected()]
        else:
            selectedItems = getdeepattr(self.widget, self.ogValue, default = [])

        mime.setText(unicode(selectedItems))
        mime.source = self
        drag.setMimeData(mime)
        drag.start(Qt.MoveAction)

    def dragEnterEvent(self, ev):
        if not self.enableDragDrop: return
        if self.dataValidityCallback: return self.dataValidityCallback(ev)

        if ev.mimeData().hasText():
            ev.accept()
        else:
            ev.ignore()
    def dragMoveEvent(self, ev):
        if not self.enableDragDrop: return
        if self.dataValidityCallback: return self.dataValidityCallback(ev)

        if ev.mimeData().hasText():
            ev.setDropAction(Qt.MoveAction)
            ev.accept()
        else:
            ev.ignore()

    def dropEvent(self, ev):
        if not self.enableDragDrop: return
        if ev.mimeData().hasText():
            item = self.itemAt(ev.pos())
            if item:
                index = self.indexFromItem(item).row()
            else:
                index = self.count()

            source = ev.mimeData().source
            selectedItemIndices = eval(unicode(ev.mimeData().text()))

            if self.ogLabels != None and self.ogValue != None:
                allSourceItems = getdeepattr(source.widget, source.ogLabels, default = [])
                selectedItems = [allSourceItems[i] for i in selectedItemIndices]
                allDestItems = getdeepattr(self.widget, self.ogLabels, default = [])

                if source != self:
                    setattr(source.widget, source.ogLabels, [item for item in allSourceItems if item not in selectedItems])   # TODO: optimize this code. use the fact that the selectedItemIndices is a sorted list
                    setattr(self.widget, self.ogLabels, allDestItems[:index] + selectedItems + allDestItems[index:])
                    setattr(source.widget, source.ogValue, [])  # clear selection in the source widget
                else:
                    items = [item for item in allSourceItems if item not in selectedItems]
                    if index < len(allDestItems):
                        while index > 0 and index in getdeepattr(self.widget, self.ogValue, default = []):      # if we are dropping items on a selected item, we have to select some previous unselected item as the drop target
                            index -= 1
                        destItem = allDestItems[index]
                        index = items.index(destItem)
                    else:
                        index = max(0, index - len(selectedItems))
                    setattr(self.widget, self.ogLabels, items[:index] + selectedItems + items[index:])
                setattr(self.widget, self.ogValue, range(index, index+len(selectedItems)))
            else:       # if we don't have variables ogValue and ogLabel
                if source != self:
                    self.insertItems(source.selectedItems())
                    for index in selectedItemIndices[::-1]:
                        source.takeItem(index)
                else:
                    if index < self.count():
                        while index > 0 and self.item(index).isSelected():      # if we are dropping items on a selected item, we have to select some previous unselected item as the drop target
                            index -= 1
                    items = [source.item(i) for i in selectedItemIndices]
                    for ind in selectedItemIndices[::-1]:
                        source.takeItem(ind)
                        if ind <= index: index-= 1
                    for item in items[::-1]:
                        self.insertItem(index, item)
                    self.clearSelection()
                    for i in range(index, index+len(items)):
                        self.item(i).setSelected(1)

            if self.dragDopCallback:        # call the callback
                self.dragDopCallback()
            ev.setDropAction(Qt.MoveAction)
            ev.accept()
            
            ## whatever all of this does we need to execute the function to update the items
            self.updateRedRItems()
        else:
            ev.ignore()

    def updateRedRItems(self):
        ## we go through all of the items and remake the items OrderedDict
        newDict = OrderedDict()
        for r in range(self.count()):
            t = unicode(self.itemAt(r).text())  # get the text of the item
            if t not in self.listItems.values():
                newDict[t] = t
            else:
                for i, ov in self.listItems.items():
                    if ov == t:
                        newDict[i] = ov
        self.listItems = newDict
    def getSettings(self):
        print 'saving list box'
        r = {'items':self.items, 'selected':self.selectedIds()}
        print r
        return r
    def loadSettings(self,data):
        print _('loading list box')
        print data
        self.clear()
        self.addItems(data['items'])
        self.setSelectedIds(data['selected'])


    def getReportText(self, fileDir):
        items = self.getItems()
        selected = self.currentSelection()
        new = []
        
        for x in items:
            if x in selected:
                new.append([_('Selected'), x])
            else:
                new.append([_('Not Selected'),x])
        #print new
        text = redRReports.createTable(new,columnNames=[_('Selection'),_('Option')])
        # if text != '':
            # text += '\nSelected text has * in front'
        
        r = {self.widgetName:{'includeInReports': self.includeInReports, 'text': text}}

        return r