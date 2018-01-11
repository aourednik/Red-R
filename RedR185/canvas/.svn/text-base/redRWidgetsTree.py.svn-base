# Author: Gregor Leban (gregor.leban@fri.uni-lj.si) modifications by Kyle R Covington and Anup Parikh
# Description:
#    tab for showing widgets and widget button class
#
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import os.path, sys
from string import strip, count, replace
import orngDoc, orngRegistry, redRObjects
import OWGUIEx, redRSaveLoad, redRStyle
import redREnviron, redRLog
import xml.dom.minidom
# from libraries.base.qtWidgets.SearchDialog import SearchDialog as redRSearchDialog
# from libraries.base.qtWidgets.lineEditHint import lineEditHint as redRlineEditHint

# we have to use a custom class since QLabel by default ignores the mouse
# events if it is showing text (it does not ignore events if it's showing an icon)
import redRi18n
# def _(a):
    # return a
_ = redRi18n.Coreget_()

class OrangeLabel(QLabel):
    def mousePressEvent(self, e):
        pos = self.mapToParent(e.pos())
        ev = QMouseEvent(e.type(), pos, e.button(), e.buttons(), e.modifiers())
        self.parent().mousePressEvent(ev)

    def mouseMoveEvent(self, e):
        pos = self.mapToParent(e.pos())
        ev = QMouseEvent(e.type(), pos, e.button(), e.buttons(), e.modifiers())
        self.parent().mouseMoveEvent(ev)

    def mouseReleaseEvent(self, e):
        pos = self.mapToParent(e.pos())
        ev = QMouseEvent(e.type(), pos, e.button(), e.buttons(), e.modifiers())
        self.parent().mouseReleaseEvent(ev)



class WidgetButtonBase():
    def __init__(self, name, widgetInfo, widgetTabs, canvasDlg):
        self.shiftPressed = 0
        self.name = name
        self.widgetInfo = widgetInfo
        self.widgetTabs = widgetTabs
        self.canvasDlg = canvasDlg

    def clicked(self, rightClick = False, pos = None):
        win = self.canvasDlg.schema
        if pos:
            pos = win.mapFromGlobal(pos)
            win.addWidget(self.widgetInfo, pos.x(), pos.y())
        else:
            win.addWidget(self.widgetInfo)
        if (rightClick or self.shiftPressed):
            import orngCanvasItems
            if isinstance(rightClick, orngCanvasItems.CanvasWidget):
                win.addLine(rightClick, win.widgets[-1])
            elif len(win.widgets) > 1:
                win.addLine(win.widgets[-2], win.widgets[-1])
        
        #return win.widgets[-1]
    def setCompatible(self, widget):
        ## the goal of this is to set the background to a color (light blue?) if the selected canvas widget has connected to the canvas widget before.
        connectingWidgets = log.getHistory(widget.widgetInfo.fileName)
        if self.widgetInfo.fileName in connectingWidgets:
            self.setBackgroundColor(Qt.blue)
        else:
            self.setBackgroundColor(Qt.white)
        
class WidgetButton(QFrame, WidgetButtonBase):
    def __init__(self, tab, name, widgetInfo, widgetTabs, canvasDlg, buttonType = 2, size=30):
        QFrame.__init__(self)
        WidgetButtonBase.__init__(self, name, widgetInfo, widgetTabs, canvasDlg)

        self.buttonType = buttonType
        self.iconSize = size
        self.setLayout(buttonType == WB_TOOLBOX and QHBoxLayout() or QVBoxLayout())
        self.pixmapWidget = QLabel(self)

        self.textWidget = OrangeLabel(self)
        if buttonType == WB_TABBAR_NO_TEXT:
            self.textWidget.hide()

        self.layout().setMargin(3)
        if buttonType != WB_TOOLBOX:
            self.layout().setSpacing(0)
            
        self.icon = QIcon(widgetInfo.icon)
        self.pixmapWidget.setPixmap(self.icon.pixmap(self.iconSize, self.iconSize))
        self.pixmapWidget.setScaledContents(1)
        self.pixmapWidget.setFixedSize(QSize(self.iconSize, self.iconSize))

        #split long names into two lines
        buttonName = name
        if self.buttonType == WB_TABBAR_TEXT:
            numSpaces = count(buttonName, " ")
            if numSpaces == 1: buttonName = replace(buttonName, " ", "<br>")
            elif numSpaces > 1:
                mid = len(buttonName)/2; i = 0
                found = 0
                while "<br>" not in buttonName:
                    if buttonName[mid + i] == " ": buttonName = buttonName[:mid + i] + "<br>" + buttonName[(mid + i + 1):]
                    elif buttonName[mid - i] == " ": buttonName = buttonName[:mid - i] + "<br>" + buttonName[(mid - i + 1):]
                    i+=1
            else:
                buttonName += "<br>"

        self.layout().addWidget(self.pixmapWidget)
        self.layout().addWidget(self.textWidget)

        if self.buttonType != WB_TOOLBOX:
            self.textWidget.setText("<div align=\"center\">" + buttonName + "</div>")
            self.layout().setAlignment(self.pixmapWidget, Qt.AlignHCenter)
            self.layout().setAlignment(self.textWidget, Qt.AlignHCenter)
        else:
            self.textWidget.setText(name)
        self.setToolTip(widgetInfo.tooltipText)


    # we need to handle context menu event, otherwise we get a popup when pressing the right button on one of the icons
    def contextMenuEvent(self, ev):
        ev.accept()

    def mouseMoveEvent(self, e):
        ### Semaphore "busy" is needed for some widgets whose loading takes more time, e.g. Select Data
        ### Since the active window cannot change during dragging, we wouldn't have to remember the window; but let's leave the code in, it can't hurt
        schema = self.canvasDlg.schema
        if hasattr(self, "busy"):
            return
        self.busy = 1

        inside = schema.canvasView.rect().contains(schema.canvasView.mapFromGlobal(self.mapToGlobal(e.pos())) - QPoint(50,50))
        p = QPointF(schema.canvasView.mapFromGlobal(self.mapToGlobal(e.pos()))) + QPointF(schema.canvasView.mapToScene(QPoint(0, 0)))

        dinwin, widget = getattr(self, "widgetDragging", (None, None))
        if dinwin and (dinwin != schema or not inside):
             dinwin.removeWidget(widget)
             delattr(self, "widgetDragging")
             #dinwin.canvasView.scene().update()

        if inside:
            #print 'I\'m inside'
            if not widget:
                #print 'I\'m adding a widget!!!'
                widget = schema.addWidget(self.widgetInfo, p.x(), p.y())
                self.widgetDragging = schema, widget

            # in case we got an exception when creating a widget instance
            if widget == None:
                delattr(self, "busy")
                return

            widget.setCoords(p.x() - widget.rect().width()/2, p.y() - widget.rect().height()/2)

            import orngCanvasItems
            items = schema.canvas.collidingItems(widget)
            widget.invalidPosition = widget.selected = (schema.canvasView.findItemTypeCount(items, orngCanvasItems.CanvasWidget) > 0)

        delattr(self, "busy")

    def mousePressEvent(self, e):
        self.setFrameShape(QFrame.StyledPanel)
        self.layout().setMargin(self.layout().margin()-2)

        
    def mouseReleaseEvent(self, e):
        self.layout().setMargin(self.layout().margin()+2)
        self.setFrameShape(QFrame.NoFrame)
        dinwin, widget = getattr(self, "widgetDragging", (None, None))
        self.shiftPressed = e.modifiers() & Qt.ShiftModifier
        if widget:
            if widget.invalidPosition:
                dinwin.removeWidget(widget)
                dinwin.canvasView.scene().update()
            elif self.shiftPressed and len(dinwin.widgets) > 1:
                dinwin.addLine(dinwin.widgets[-2], dinwin.widgets[-1])
            delattr(self, "widgetDragging")
        
        # we say that we clicked the button only if we released the mouse inside the button
        if e.pos().x() >= 0 and e.pos().x() < self.width() and e.pos().y() > 0 and e.pos().y() < self.height():
            self.clicked(e.button() == Qt.RightButton)

    def wheelEvent(self, ev):
        if self.parent() and self.buttonType != WB_TOOLBOX:
            hs = self.parent().tab.horizontalScrollBar()
            hs.setValue(min(max(hs.minimum(), hs.value()-ev.delta()), hs.maximum()))
        else:
            QFrame.wheelEvent(self, ev)


class WidgetTreeItem(QTreeWidgetItem, WidgetButtonBase):
    def __init__(self, parent, name, widgetInfo, tabs, canvasDlg):
        QTreeWidgetItem.__init__(self, parent)
        WidgetButtonBase.__init__(self, name, widgetInfo, tabs, canvasDlg)
        
        self.setIcon(0, QIcon(widgetInfo.icon))
        self.setText(0, name)
        self.setToolTip(0, widgetInfo.tooltipText)
    
    def adjustSize(self):
        pass


       
class WidgetScrollArea(QScrollArea):
    def wheelEvent(self, ev):
        hs = self.horizontalScrollBar()
        hs.setValue(min(max(hs.minimum(), hs.value()-ev.delta()), hs.maximum()))

class widgetSuggestions(QTreeWidget):
    def __init__(self, parent,canvasDlg):
        
        self.canvasDlg = canvasDlg
        QTreeWidget.__init__(self, parent)
        parent.layout().addWidget(self)
        self.setHeaderLabels([_('Suggested Widgets')])
        QObject.connect(self, SIGNAL('itemClicked (QTreeWidgetItem *,int)'), lambda action: self.activateSuggestWidget(action))
        self.hide()
        
    def activateSuggestWidget(self, action):
        newwidget = self.canvasDlg.schema.addWidget(action.widgetInfo)
        if self.suggestingWidget:
            self.canvasDlg.schema.addLine(self.suggestingWidget, redRObjects.getWidgetByIDActiveTabOnly(newwidget))
        

class WidgetTree(QTreeWidget):
    def __init__(self, parent, canvasDlg, widgetRegistry, *args):
        self.canvasDlg = canvasDlg
        self.widgetInfo = widgetRegistry
        self.allWidgets = []
        self.tabDict = {}
        self.tabs = []

        QTreeWidget.__init__(self, parent)
        parent.layout().addWidget(self)
        
        self.setMouseTracking(1)
        self.setHeaderHidden(1)
        self.mousePressed = 0
        self.mouseRightClick = 0
        self.connect(self, SIGNAL("itemClicked (QTreeWidgetItem *,int)"), self.itemClicked)
        self.setStyleSheet(""" QTreeView::item {padding: 2px 0px 2px 0px} """)          # show items a little bit apart from each other

        # this is needed otherwise the document window will sometimes strangely lose focus and the output window will be focused
        self.setFocusPolicy(Qt.ClickFocus)   
        self.createWidgetTabs(widgetRegistry)            
        
        # iconSize = redRStyle.iconSizeList[redREnviron.settings["toolbarIconSize"]]
        # self.setIconSize(QSize(iconSize, iconSize))
       
        
        # must make a widget container to hold the search area and the widget tree
        # self.containerWidget = QWidget()
        # tmpBoxLayout = QBoxLayout(QBoxLayout.TopToBottom, self.containerWidget)
        #self.widgetSuggestEdit = OWGUIEx.lineEditHint(self, None, None, useRE = 0, caseSensitive = 0, matchAnywhere = 1, autoSizeListWidget = 1, callback = self.callback)
        # self.widgetSuggestEdit = SearchBox(None, callback = self.callback)
        # self.widgetSuggestEdit.caseSensitive = 0
        # self.widgetSuggestEdit.matchAnywhere = 1
        # self.widgetSuggestEdit.autoSizeListWidget = 1
        
        # self.widgetSuggestEdit.setItems([QListWidgetItem(action.icon(), action.widgetInfo.name) for action in self.actions])
        # self.widgetSuggestEdit.addItems([QListWidgetItem(action.icon(), action.templateInfo.name) for action in self.templateActions])
        #self.favoritesTree = MyTreeWidget(canvasDlg, self) # tree that will contain a set of favorite widgets that the user will set
        #tmpBoxLayout.insertWidget(0, CanvasPopup)
        
        # tmpBoxLayout.insertWidget(0, self.widgetSuggestEdit)
        # tmpBoxLayout.insertWidget(1, self.treeWidget)
            
        #tmpBoxLayout.insertWidget(2, self.favoritesTree)
        
        # self.setWidget(self.containerWidget)
        
#        self.treeWidget.setRootIsDecorated(0) 
        #self.setWidget(OWGUIEx.lineEditHint(self, None, None, useRE = 0, caseSensitive = 0, matchAnywhere = 1, autoSizeListWidget = 1))
    def mousePressEvent(self, e):
        QTreeWidget.mousePressEvent(self, e)
        self.mousePressed = 1
        self.shiftPressed = bool(e.modifiers() & Qt.ShiftModifier)
        self.mouseRightClick = e.button() == Qt.RightButton
        
    def mouseReleaseEvent(self, e):
        QTreeWidget.mouseReleaseEvent(self, e)
        dinwin, widget = getattr(self, "widgetDragging", (None, None))
        self.shiftPressed = bool(e.modifiers() & Qt.ShiftModifier)
        if widget:
            if widget.invalidPosition:
                dinwin.removeWidget(widget)
                dinwin.canvasView.scene().update()
            elif self.shiftPressed and len(dinwin.widgets) > 1:
                dinwin.addLine(dinwin.widgets[-2], dinwin.widgets[-1])
            delattr(self, "widgetDragging")
           
        self.mousePressed = 0
        
    def itemClicked(self, item, column):
        if isinstance(item, WidgetTreeFolder):
            return
        win = self.canvasDlg.schema
        win.addWidget(item.widgetInfo)
        if (self.mouseRightClick or self.shiftPressed) and len(win.widgets) > 1:
            win.addLine(win.widgets[-2], win.widgets[-1])
    def clear(self):
        self.allWidgets = []
        self.tabDict = {}
        self.tabs = []
        QTreeWidget.clear(self)
        
    def createWidgetTabs(self, widgetRegistry):
        
        iconSize = redRStyle.iconSizeList[redREnviron.settings["toolbarIconSize"]]
        self.setIconSize(QSize(iconSize, iconSize))

        mainTabs = widgetRegistry['tags']
        treeXML = mainTabs.childNodes[0]
        #print treeXML.childNodes
        redREnviron.settings['widgetXML'] = mainTabs
        for itab in treeXML.childNodes:
            if itab.nodeName == 'group': #picked a group element
                
                tab = self.insertWidgetTab(unicode(itab.getAttribute('name')), 1) # a QTreeWidgetItem
                
                #print _('inserted tab ')+unicode(itab.getAttribute('name'))
                self.insertChildTabs(itab, tab, widgetRegistry)
                
                self.insertWidgets(itab.getAttribute('name'), tab, widgetRegistry)

                if hasattr(tab, "adjustSize"):
                    tab.adjustSize()
        
        # return the list of tabs and their status (shown/hidden)
    
    def insertChildTabs(self, itab, tab, widgetRegistry):
        try:
            
            if itab.hasChildNodes(): subTabs = itab.childNodes
            else: return
            
            for child in subTabs:
                if child.nodeName == 'group': # we found another group
                    childTab = WidgetTreeFolder(tab, unicode(child.getAttribute('name')))
                    
                    childTab.widgets = []
                    childTab.setChildIndicatorPolicy(QTreeWidgetItem.DontShowIndicatorWhenChildless)
                    self.insertChildTabs(child, childTab, widgetRegistry)
                    self.insertWidgets(child.getAttribute('name'), childTab, widgetRegistry)
                    
        except Exception as inst: #subtabs don't exist
            redRLog.log(redRLog.REDRCORE, redRLog.ERROR, redRLog.formatException())
            print inst
            return
                
    def insertWidgets(self, itab, tab, widgetRegistry):
        #print 'Widget Registry is \n\n' + unicode(widgetRegistry) + '\n\n'
        widgets = None
        try:
            for wName in widgetRegistry['widgets'].keys():
                widgetInfo = widgetRegistry['widgets'][wName]
                try:
                    if unicode(itab) in widgetInfo.tags: # add the widget
                        button = WidgetTreeItem(tab, widgetInfo.name, widgetInfo, self, self.canvasDlg)
                        if button not in tab.widgets:
                            tab.widgets.append(button)
                        self.allWidgets.append(button)
                            
                except Exception as inst: 
                    redRLog.log(redRLog.REDRCORE, redRLog.ERROR, redRLog.formatException())
                    print inst
                    pass
        except:
            redRLog.log(redRLog.REDRCORE, redRLog.ERROR, redRLog.formatException())
            pass

        
    def insertWidgetTab(self, name, show = 1):
        if self.tabDict.has_key(name):
            self.tabDict[name].setHidden(not show)
            return self.tabDict[name]
        
        item = WidgetTreeFolder(self, name)
        item.widgets = []
        self.tabDict[name] = item

        if not show:
            item.setHidden(1)
        if redREnviron.settings.has_key("treeItemsOpenness") and redREnviron.settings["treeItemsOpenness"].has_key(name):
             item.setExpanded(redREnviron.settings["treeItemsOpenness"][name])
        elif not redREnviron.settings.has_key("treeItemsOpenness") and self.topLevelItemCount() == 1:
            item.setExpanded(1)
        self.tabs.append((name, 2*int(show), item))

        return item

    def callback(self):
        text = unicode(self.widgetSuggestEdit.text())
        if '.rrts' in text: ## this is a template, we should load this and not add the widget
            for action in self.templateActions:
                if action.templateInfo.name == text:
                    redRSaveLoad.loadTemplate(action.templateInfo.file)
                    return
        else: ## if there isn't a .rrts in the filename then we should proceed as normal
            for action in self.actions: # move through all of the actions in the actions list
                if action.widgetInfo.name == text: # find the widget (action) that has the correct name, note this finds the first instance.  Widget names must be unique   ??? should we allow multiple widgets with the same name ??? probably not.
                    self.widgetInfo = action.widgetInfo
                    #print action.widgetInfo, _('Widget info')
                    self.canvasDlg.schema.addWidget(action.widgetInfo) # add the correct widget to the schema
                    
                    self.widgetSuggestEdit.clear()  # clear the line edit for the next widget
                    return

class WidgetTreeFolder(QTreeWidgetItem):
    def __init__(self, parent, name):
        QTreeWidgetItem.__init__(self, parent, [name])
#        item.setChildIndicatorPolicy(item.ShowIndicator)
    
    def mousePressEvent(self, e):
        self.treeItem.setExpanded(not self.treeItem.isExpanded())
         
                

