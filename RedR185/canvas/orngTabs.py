# Author: Gregor Leban (gregor.leban@fri.uni-lj.si) modifications by Kyle R Covington and Anup Parikh
# Description:
#    tab for showing widgets and widget button class
#
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import os.path, sys
from string import strip, count, replace
import orngDoc, orngRegistry, redRObjects
#from orngSignalManager import InputSignal, OutputSignal
import OWGUIEx, redRSaveLoad, redRStyle
import OWGUIEx, redRSaveLoad
import redREnviron, redRLog
import xml.dom.minidom
from libraries.base.qtWidgets.SearchDialog import SearchDialog as redRSearchDialog
from libraries.base.qtWidgets.lineEditHint import lineEditHint as redRlineEditHint
import redRi18n
# def _(a):
    # return a
_ = redRi18n.Coreget_()
WB_TOOLBOX = 0
WB_TREEVIEW = 1
WB_TABBAR_NO_TEXT = 2
WB_TABBAR_TEXT = 3

# we have to use a custom class since QLabel by default ignores the mouse
# events if it is showing text (it does not ignore events if it's showing an icon)
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
            #print 'I\_('m inside')
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


class MyTreeWidget(QTreeWidget):
    def __init__(self, canvasDlg, parent = None):
        QTreeWidget.__init__(self, parent)
        self.canvasDlg = canvasDlg
        self.setMouseTracking(1)
        self.setHeaderHidden(1)
        self.mousePressed = 0
        self.mouseRightClick = 0
        self.connect(self, SIGNAL("itemClicked (QTreeWidgetItem *,int)"), self.itemClicked)
        self.setStyleSheet(""" QTreeView::item {padding: 2px 0px 2px 0px} """)          # show items a little bit apart from each other

        
    ####  DEPRICATED   #####
        
    # def mouseMoveEvent(self, e):
        # if not self.mousePressed:   # this is needed, otherwise another widget in the tree might get selected while we drag the icon to the canvas
            # QTreeWidget.mouseMoveEvent(self, e)
        ## Semaphore "busy" is needed for some widgets whose loading takes more time, e.g. Select Data
        ## Since the active window cannot change during dragging, we wouldn't have to remember the window; but let's leave the code in, it can't hurt
        # schema = self.canvasDlg.schema
        # if hasattr(self, "busy"):
            # return
        # self.busy = 1

        # inside = schema.canvasView.rect().contains(schema.canvasView.mapFromGlobal(self.mapToGlobal(e.pos())) - QPoint(50,50))
        # p = QPointF(schema.canvasView.mapFromGlobal(self.mapToGlobal(e.pos()))) + QPointF(schema.canvasView.mapToScene(QPoint(0, 0)))

        # dinwin, widget = getattr(self, "widgetDragging", (None, None))
        # if dinwin and not inside:
             # dinwin.removeWidget(widget)
             # delattr(self, "widgetDragging")
             # dinwin.canvasView.scene().update()

        # if inside:
            # if not widget and self.selectedItems() != [] and isinstance(self.selectedItems()[0], WidgetTreeItem):
                # widget = schema.addWidget(self.selectedItems()[0].widgetInfo, p.x(), p.y())
                # self.widgetDragging = schema, widget

            ###in case we got an exception when creating a widget instance
            # if widget == None:
                # delattr(self, "busy")
                # return

            # widget.setCoords(p.x() - widget.rect().width()/2, p.y() - widget.rect().height()/2)
            # schema.canvasView.scene().update()

            # import orngCanvasItems
            # items = schema.canvas.collidingItems(widget)
            # widget.invalidPosition = widget.selected = (schema.canvasView.findItemTypeCount(items, orngCanvasItems.CanvasWidget) > 0)

        # delattr(self, "busy")
        
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
         
class WidgetScrollArea(QScrollArea):
    def wheelEvent(self, ev):
        hs = self.horizontalScrollBar()
        hs.setValue(min(max(hs.minimum(), hs.value()-ev.delta()), hs.maximum()))

class WidgetListBase:
    def __init__(self, canvasDlg, widgetInfo):
        self.canvasDlg = canvasDlg
        self.widgetInfo = widgetInfo
        self.allWidgets = []
        self.tabDict = {}
        self.tabs = []
    def createFavoriteWidgetTabs(self, widgetRegistry, widgetDir, picsDir, defaultPic):
        # populate the favorites widget, we will want to repopulate this when a widget is added
        
        try:
            ffile = os.path.abspath(redREnviron.directoryNames['redRDir'] + '/tagsSystem/favorites.xml')
            f = open(ffile, 'r')
        except: # there was an exception, the user might not have the favorites file, we need to make one and set a default settings 
            redRLog.log(redRLog.REDRCORE, redRLog.ERROR, redRLog.formatException())
            self.insertFavoriteWidgetTab(_('Favorites'), 1) # make a favorites tab
            return
            
        favTabs = xml.dom.minidom.parse(f)
        f.close()
        treeXML = favTabs.childNodes[0] # everything is contained within the Favorites
        #print _('Favorites') + unicode(treeXML.childNodes)
            
        #loop to make the catagories
        for node in treeXML.childNodes: # put the child nodes into the widgets
            if node.nodeName == 'group':
                tab = self.insertFavoriteWidgetTab(unicode(node.getAttribute('name')), 1)
                self.insertFavoriteChildTabs(node, tab, widgetRegistry)
                
                self.insertFavoriteWidgets(node, tab, widgetRegistry)

                if hasattr(tab, "adjustSize"):
                    tab.adjustSize()

    def insertFavoriteChildTabs(self, node, tab, widgetRegistry):
        try:
            if node.hasChildNodes(): subTabs = node.childNodes
            else: return
            
            for child in subTabs:
                if child.nodeName == 'group': # we found another group
                    childTab = WidgetTreeFolder(tab, unicode(child.getAttribute('name')))
                    childTab.widgets = []
                    childTab.setChildIndicatorPolicy(QTreeWidgetItem.DontShowIndicatorWhenChildless)
                    self.insertFavoriteChildTabs(child, childTab, widgetRegistry)
                    self.insertFavoriteWidgets(child, childTab, widgetRegistry)
                
        except: #subtabs don't exist
            redRLog.log(redRLog.REDRCORE, redRLog.ERROR, redRLog.formatException())
            return
            
    def insertFavoriteWidgets(self, node, tab, widgetRegistry):
        widgets = None
        #print unicode(widgetRegistry.keys())
        
        for (tabName, show) in [(name, 1) for name in widgetRegistry.keys()]:
            #print widgetRegistry[tabName].keys()
            for wName in widgetRegistry[tabName].keys(): #wName will be a collection of widget names as they appear in the tree
                #print wName
                awidgets = {} # not sure what this does yet
                for subNode in node.childNodes: # what are the child nodes
                    if subNode.nodeName == 'description':
                        subNodeAtt = ''
                        for subNode2 in subNode.childNodes:
                            if subNode2.nodeType == node.TEXT_NODE:
                                subNodeAtt = subNodeAtt + subNode2.data
                        subNodeAtt = unicode(subNodeAtt)
                        subNodeAtt = subNodeAtt.replace(' ', '')
                        #print subNodeAtt.strip()
                        widgetNames = subNodeAtt.split(',')
                        #print unicode(widgetNames)
                        if wName.replace(' ', '') in widgetNames: # add the widget
                            if tabName not in awidgets.keys(): awidgets[tabName] = {}
                            awidgets[tabName][wName] = widgetRegistry[tabName][wName]
                            #print _('made it past the awidgets stage')
                            #print unicode(awidgets[tabName].items())
                            (name, widgetInfo) = awidgets[tabName].items()[0]
                            (priority, name, widgetInfo) = (int(widgetInfo.priority), name, widgetInfo)
                            #print unicode((priority, name, widgetInfo)) + _('made it to 7894')
                            #print unicode(widgetInfo)
                            if isinstance(self, WidgetTree):
                                #print unicode(tab)
                                button = WidgetTreeItem(tab, name, widgetInfo, self, self.canvasDlg)
                                
                            else:
                                button = WidgetButton(tab, name, widgetInfo, self, self.canvasDlg, widgetTypeList, iconSize)
                                for k in range(priority/1000 - exIndex):
                                    tab.layout().addSpacing(10)
                                exIndex = priority / 1000
                                tab.layout().addWidget(button)
                            if button not in tab.widgets:
                                tab.widgets.append(button)
                            self.allWidgets.append(button)
                        
    def createWidgetTabs(self, widgetRegistry, widgetDir, picsDir, defaultPic):
        #print unicode(widgetRegistry) + _(' widget registry')
        self.widgetDir = widgetDir
        self.picsDir = picsDir
        self.defaultPic = defaultPic
        widgetTypeList = redREnviron.settings["widgetListType"]
        size = min(len(redRStyle.iconSizeList)-1, redREnviron.settings["toolbarIconSize"])
        iconSize = redRStyle.iconSizeList[size]
        
        # find tab names that are not in widgetTabList
        
        # tfile = os.path.abspath(redREnviron.directoryNames['redRDir'] + '/tagsSystem/tags.xml')
        # f = open(tfile, 'r')
        #print unicode(f)
        
        #mainTabs = xml.dom.minidom.parse(f)
        mainTabs = widgetRegistry['tags']
        # f.close()
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
            return
                
    def insertWidgets(self, itab, tab, widgetRegistry):
        #print 'Widget Registry is \n\n' + unicode(widgetRegistry) + '\n\n'
        widgets = None
        try:
            for wName in widgetRegistry['widgets'].keys():
                widgetInfo = widgetRegistry['widgets'][wName]
                try:
                    if unicode(itab.replace(' ', '')) in widgetInfo.tags: # add the widget
                        button = WidgetTreeItem(tab, widgetInfo.name, widgetInfo, self, self.canvasDlg)
                        if button not in tab.widgets:
                            tab.widgets.append(button)
                        self.allWidgets.append(button)
                            
                except Exception as inst: 
                    redRLog.log(redRLog.REDRCORE, redRLog.ERROR, redRLog.formatException())
                    pass
        except:
            redRLog.log(redRLog.REDRCORE, redRLog.ERROR, redRLog.formatException())

class WidgetTabs(WidgetListBase, QTabWidget):
    def __init__(self, canvasDlg, widgetInfo, *args):
        WidgetListBase.__init__(self, canvasDlg, widgetInfo)
        apply(QTabWidget.__init__, (self,) + args)

    def insertWidgetTab(self, name, show = 1):
        if self.tabDict.has_key(name):
            if show: self.tabDict[name].tab.show()
            else:    self.tabDict[name].tab.hide()
            return self.tabDict[name]
        
        tab = WidgetScrollArea(self)
        tab.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        tab.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        widgetSpace = QWidget(self)
        widgetSpace.setLayout(QHBoxLayout())
        widgetSpace.layout().setSpacing(0)
        widgetSpace.layout().setMargin(0)
        widgetSpace.tab = tab
        widgetSpace.widgets = []
        tab.setWidget(widgetSpace)

        self.tabDict[name] = widgetSpace

        if show:
            self.addTab(tab, name)
            self.tabs.append((name, 2, widgetSpace))
        else:
            tab.hide()
            self.tabs.append((name, 0, widgetSpace))

        return widgetSpace


class WidgetTree(WidgetListBase, QDockWidget):
    def __init__(self, canvasDlg, widgetInfo, *args):
        WidgetListBase.__init__(self, canvasDlg, widgetInfo)
        QDockWidget.__init__(self)
        self.setObjectName('widgetDock')
        self.actions = categoriesPopup.allActions
        self.templateActions = categoriesPopup.templateActions
        self.treeWidget = MyTreeWidget(canvasDlg, self)
        self.treeWidget.setFocusPolicy(Qt.ClickFocus)    # this is needed otherwise the document window will sometimes strangely lose focus and the output window will be focused
        self.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable | QDockWidget.DockWidgetClosable)

        
        # must make a widget container to hold the search area and the widget tree
        self.containerWidget = QWidget()
        tmpBoxLayout = QBoxLayout(QBoxLayout.TopToBottom, self.containerWidget)
        #self.widgetSuggestEdit = OWGUIEx.lineEditHint(self, None, None, useRE = 0, caseSensitive = 0, matchAnywhere = 1, autoSizeListWidget = 1, callback = self.callback)
        self.widgetSuggestEdit = SearchBox(None, callback = self.callback)
        self.widgetSuggestEdit.caseSensitive = 0
        self.widgetSuggestEdit.matchAnywhere = 1
        self.widgetSuggestEdit.autoSizeListWidget = 1
        
        self.widgetSuggestEdit.setItems([QListWidgetItem(action.icon(), action.widgetInfo.name) for action in self.actions])
        self.widgetSuggestEdit.addItems([QListWidgetItem(action.icon(), action.templateInfo.name) for action in self.templateActions])
        #self.favoritesTree = MyTreeWidget(canvasDlg, self) # tree that will contain a set of favorite widgets that the user will set
        #tmpBoxLayout.insertWidget(0, CanvasPopup)
        
        tmpBoxLayout.insertWidget(0, self.widgetSuggestEdit)
        tmpBoxLayout.insertWidget(1, self.treeWidget)
        self.suggestButtonsList = QTreeWidget()
        self.suggestButtonsList.setHeaderLabels([_('Suggested Widgets')])
        tmpBoxLayout.insertWidget(2, self.suggestButtonsList)
        QObject.connect(self.suggestButtonsList, SIGNAL('itemClicked (QTreeWidgetItem *,int)'), lambda action: self.activateSuggestWidget(action))
        self.suggestButtonsList.hide()
            
        #tmpBoxLayout.insertWidget(2, self.favoritesTree)
        
        self.setWidget(self.containerWidget)
        
        iconSize = redRStyle.iconSizeList[redREnviron.settings["toolbarIconSize"]]
        self.treeWidget.setIconSize(QSize(iconSize, iconSize))
#        self.treeWidget.setRootIsDecorated(0) 
        #self.setWidget(OWGUIEx.lineEditHint(self, None, None, useRE = 0, caseSensitive = 0, matchAnywhere = 1, autoSizeListWidget = 1))
        
    def activateSuggestWidget(self, action):
        #print action
        #print action.widgetInfo
        newwidget = self.canvasDlg.schema.addWidget(action.widgetInfo)
        if self.suggestButtonsList.suggestingWidget:
            self.canvasDlg.schema.addLine(self.suggestButtonsList.suggestingWidget, redRObjects.getWidgetByIDActiveTabOnly(newwidget))
    def insertWidgetTab(self, name, show = 1):
        if self.tabDict.has_key(name):
            self.tabDict[name].setHidden(not show)
            return self.tabDict[name]
        
        item = WidgetTreeFolder(self.treeWidget, name)
        item.widgets = []
        self.tabDict[name] = item

        if not show:
            item.setHidden(1)
        if redREnviron.settings.has_key("treeItemsOpenness") and redREnviron.settings["treeItemsOpenness"].has_key(name):
             item.setExpanded(redREnviron.settings["treeItemsOpenness"][name])
        elif not redREnviron.settings.has_key("treeItemsOpenness") and self.treeWidget.topLevelItemCount() == 1:
            item.setExpanded(1)
        self.tabs.append((name, 2*int(show), item))

        return item
    def insertFavoriteWidgetTab(self, name, show = 1):  # currently depricated but would add a favorites widget tab into the favorites widget dropdown.
        if self.tabDict.has_key(name):
            self.tabDict[name].setHidden(not show)
            return self.tabDict[name]
        
        item = WidgetTreeFolder(self.favoritesTree, name)
        item.widgets = []
        self.tabDict[name] = item

        if not show:
            item.setHidden(1)
        if redREnviron.settings.has_key("treeItemsOpenness") and redREnviron.settings["treeItemsOpenness"].has_key(name):
             item.setExpanded(redREnviron.settings["treeItemsOpenness"][name])
        elif not redREnviron.settings.has_key("treeItemsOpenness") and self.favoritesTree.topLevelItemCount() == 1:
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
         
                

# button that contains the name of the widget category. 
# when clicked it shows or hides the widgets in the category
class WidgetTreeButton(QPushButton):
    def __init__(self, treeItem, name, parent):
        QPushButton.__init__(self, name, parent)
        self.treeItem = treeItem
        
    def mousePressEvent(self, e):
        self.treeItem.setExpanded(not self.treeItem.isExpanded())

class WidgetToolBox(WidgetListBase, QDockWidget):
    def __init__(self, canvasDlg, widgetInfo, *args):
        WidgetListBase.__init__(self, canvasDlg, widgetInfo)
        QDockWidget.__init__(self, "Widgets")
        self.toolbox = MyQToolBox(redREnviron.settings["toolboxWidth"], self)
        self.toolbox.setFocusPolicy(Qt.ClickFocus)    # this is needed otherwise the document window will sometimes strangely lose focus and the output window will be focused
        self.toolbox.layout().setSpacing(0)
        self.setWidget(self.toolbox)


    def insertWidgetTab(self, name, show = 1):
        if self.tabDict.has_key(name):
            if show: self.tabDict[name].scrollArea.show()
            else:    self.tabDict[name].scrollArea.hide()
            return self.tabDict[name]
        
        sa = QScrollArea(self.toolbox)
        sa.setBackgroundRole(QPalette.Base)
        tab = QFrame(self)
        tab.scrollArea = sa
        tab.widgets = []
        sa.setWidget(tab)
        sa.setWidgetResizable(0)
        sa.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        tab.setBackgroundRole(QPalette.Base)
        tab.setLayout(QVBoxLayout())
        tab.layout().setMargin(0)
        tab.layout().setSpacing(0)
        tab.layout().setContentsMargins(6, 6, 6, 6)
        self.tabDict[name] = tab

        if show:
            self.toolbox.addItem(sa, name)
            self.tabs.append((name, 2, tab))
        else:
            sa.hide()
            self.tabs.append((name, 0, tab))

        return tab


class MyQToolBox(QToolBox):
    def __init__(self, size, parent):
        QToolBox.__init__(self, parent)
        self.desiredSize = size

    def sizeHint(self):
        return QSize(self.desiredSize, 100)


class CanvasWidgetAction(QWidgetAction):
    def __init__(self, parent, actions):
        QWidgetAction.__init__(self, parent)
        self.parent = parent
        self.actions = actions
        
        self.widgetSuggestEdit = SearchBox(None, callback = self.callback)
        self.widgetSuggestEdit.caseSensitive = 0
        self.widgetSuggestEdit.matchAnywhere = 1
        self.widgetSuggestEdit.autoSizeListWidget = 1
        
        self.widgetSuggestEdit.setItems([QListWidgetItem(action.icon(), action.widgetInfo.name) for action in actions]) # sets the icon and the names of the widgets that are available when we start to type.  In this case actions are the widgets
        self.widgetSuggestEdit.setStyleSheet(""" QLineEdit { background: #fffff0; border: 1px solid orange} """)
        self.widgetSuggestEdit.listWidget.setStyleSheet(""" QListView { background: #fffff0; } QListView::item {padding: 3px 0px 3px 0px} QListView::item:selected { color: white; background: blue;} """)
        self.widgetSuggestEdit.listWidget.setIconSize(QSize(16,16)) 
        self.setDefaultWidget(self.widgetSuggestEdit)
        
    def callback(self):
        text = unicode(self.widgetSuggestEdit.text())
        for action in self.actions:
            if action.widgetInfo.name == text:
                self.widgetInfo = action.widgetInfo
                self.parent.setActiveAction(self)
                self.activate(QAction.Trigger)
                QApplication.sendEvent(self.widgetSuggestEdit, QKeyEvent(QEvent.KeyPress, Qt.Key_Enter, Qt.NoModifier))
                return
        

class CanvasPopup(QMenu):
    def __init__(self, canvasDlg):
        QMenu.__init__(self, canvasDlg)
        self.allActions = []
        self.templateActions = []
        self.widgetActionNameList = []
        self.catActions = []
        self.quickActions = []
        self.candidates = []
        self.canvasDlg = canvasDlg
        cats = redRObjects.widgetRegistry()
        self.suggestDict = {} #dict([(widget.name, widget) for widget in reduce(lambda x,y: x+y, [cat.values() for cat in cats.values()])]) ## gives an error in linux
        self.suggestItems = [QListWidgetItem(QIcon(widget.info), widget.name) for widget in self.suggestDict.values()]
        self.categoriesYOffset = 0
                
    def showEvent(self, ev):
        QMenu.showEvent(self, ev)
#        if self.actions() != []:
#            self.actions()[0].defaultWidget().setFocus()
        if self.actions() != []:
            self.actions()[0].defaultWidget().setFocus()
        
    
    def addWidgetSuggest(self):
        actions = [action for action in self.allActions if action.isEnabled()]
        self.addAction(CanvasWidgetAction(self, actions))
        self.addSeparator()
        
    def showAllWidgets(self):
        for cat in self.catActions:
            cat.setEnabled(True)
        for act in self.allActions:
            act.setEnabled(True)
            
    def selectActions(self, actClassesAttr, widgetClasses):
        for cat in self.catActions:
            cat.setEnabled(False)
            
        for act in self.allActions:
            if getattr(act.widgetInfo, actClassesAttr) & widgetClasses:
                act.setEnabled(True)
                act.category.setEnabled(True)
            else: 
                act.setEnabled(False)

    def updateWidgesByOutputs(self, widgetInfo):
        #self.selectActions("outputClasses", widgetInfo.inputClasses)
        pass
    def updateWidgetsByInputs(self, widgetInfo):
        #self.selectActions("inputClasses", widgetInfo.outputClasses)
        pass
    def updatePredictedWidgets(self, widgets, actClassesAttr, ioClasses=None):
        self.candidates = []
        for widget in widgets:
            if ioClasses == None:
                self.candidates.append(widget)
            else:
                # filter widgets by allowed signal 
                # added = False
                # for category, show in redREnviron.settings["WidgetTabs"]:
                    # if not show or not self.canvasDlg.widgetRegistry.has_key(category):
                        # continue
    
                    # for candidate in self.canvasDlg.widgetRegistry[category]:
                        # if widget.strip().lower() == candidate.strip().lower():
                            # if getattr(self.canvasDlg.widgetRegistry[category][candidate], actClassesAttr) & ioClasses:
                                # self.candidates.append(candidate)
                                # added = True
                    # if added:
                        # break
                self.candidates.append(widget)
        self.candidates = self.candidates[:3]
        
    def updateMenu(self):
        self.clear()
        self.addWidgetSuggest()
        for c in self.candidates:
            for category, show in redREnviron.settings["WidgetTabs"]:
                if not show or not redRObjects.widgetRegistry().has_key(category):
                    continue
                
                if c in redRObjects.widgetRegistry()[category]:
                    widgetInfo = redRObjects.widgetRegistry()[category][c]
                    
                    icon = QIcon(widgetInfo.icon)
                    act = self.addAction(icon, widgetInfo.name)
                    act.widgetInfo = widgetInfo
                    self.quickActions.append(act)
                    break
        self.categoriesYOffset = self.sizeHint().height()
        self.addSeparator()
        for m in self.catActions:
            self.addMenu(m)
            
    
        

def constructCategoriesPopup(canvasDlg):
    global categoriesPopup
    categoriesPopup = CanvasPopup(canvasDlg)
    categoriesPopup.setStyleSheet(""" QMenu { background-color: #fffff0; selection-background-color: blue; } QMenu::item:disabled { color: #dddddd } QMenu::separator {height: 1px; background: #dddddd; margin-left: 3px; margin-right: 4px;}""")
    
    
    # tfile = os.path.abspath(redREnviron.directoryNames['redRDir'] + '/tagsSystem/tags.xml')
    # f = open(tfile, 'r')
    # mainTabs = xml.dom.minidom.parse(f)
    # f.close() 
    mainTabs = redRObjects.widgetRegistry()['tags']
    treeXML = mainTabs.childNodes[0]
    #print treeXML.childNodes
    
    for itab in treeXML.childNodes:
        if itab.nodeName == 'group': #picked a group element
            catmenu = categoriesPopup.addMenu(unicode(itab.getAttribute('name')))
            categoriesPopup.catActions.append(catmenu) # put the catmenu in the categoriespopup
            insertChildActions(canvasDlg, catmenu, categoriesPopup, itab)
            insertWidgets(canvasDlg, catmenu, categoriesPopup, unicode(itab.getAttribute('name'))) 
    # print redREnviron.settings["WidgetTabs"]
    try:
        for category, show in redREnviron.settings["WidgetTabs"]:
            if not show or not redRObjects.widgetRegistry().has_key(category):
                continue
            catmenu = categoriesPopup.addMenu(category)
            categoriesPopup.catActions.append(catmenu)
            #print canvasDlg.widgetRegistry[category]
            for widgetInfo in sorted(redRObjects.widgetRegistry()[category].values(), key=lambda x:x.priority):
                icon = QIcon(widgetInfo.icon)
                act = catmenu.addAction(icon, widgetInfo.name)
                
                act.widgetInfo = widgetInfo
                act.category = catmenu
                #categoriesPopup.allActions.append(act)
    except Exception as inst:
        redRLog.log(redRLog.REDRCORE, redRLog.ERROR,redRLog.formatException())
    
    ### Add the templates to the popup, these should be actions with a function that puts a templates icon and loads the template
    for template in redRObjects.widgetRegistry()['templates']:
        try:
            icon = QIcon(os.path.join(redREnviron.directoryNames['picsDir'], 'Default.png'))
            act = catmenu.addAction(icon, template.name)
            act.templateInfo = template
            categoriesPopup.templateActions.append(act)
        except Exception as inst:
            redRLog.log(redRLog.REDRCORE, redRLog.ERROR,redRLog.formatException())
    #categoriesPopup.allActions += widgetRegistry['templates']
    ### put the actions into the hintbox here !!!!!!!!!!!!!!!!!!!!!
def insertChildActions(canvasDlg, catmenu, categoriesPopup, itab):
    ####
    try:
        #subfile = os.path.abspath(tfile[:tfile.rindex('\\')+1]+itab+'Subtree.txt')
        #print _('checking file ')+subfile+_(' for more tabs')
        #f = open(subfile, 'r')
        if itab.hasChildNodes(): subTabs = itab.childNodes
        else: return
        
        for child in subTabs:
            if child.nodeName == 'group': # we found another group
                childTab = catmenu.addMenu(unicode(child.getAttribute('name')))
                categoriesPopup.catActions.append(childTab)
                insertChildActions(canvasDlg, childTab, categoriesPopup, child)
                insertWidgets(canvasDlg, childTab, categoriesPopup, unicode(child.getAttribute('name')))
                
    except: #subtabs don't exist
        redRLog.log(redRLog.REDRCORE, redRLog.ERROR, redRLog.formatException())
        return
def insertWidgets(canvasDlg, catmenu, categoriesPopup, catName):
    #print 'Widget Registry is \n\n' + unicode(widgetRegistry) + '\n\n'
    widgets = None
    #print unicode(canvasDlg.widgetRegistry['templates'])
    try:
        for wName in redRObjects.widgetRegistry()['widgets'].keys(): ## move across all of the widgets in the widgetRegistry.  This is different from the templates that are tagged as templates
            widgetInfo = redRObjects.widgetRegistry()['widgets'][wName]
            try:
                if unicode(catName) in widgetInfo.tags: # add the widget, wtags is the list of tags in the widget, catName is the name of the category that we are adding
                    icon = QIcon(widgetInfo.icon)
                    act = catmenu.addAction(icon, widgetInfo.name)
                    
                    act.widgetInfo = widgetInfo
                    act.category = catmenu
                    if not widgetInfo.name in categoriesPopup.widgetActionNameList:
                        categoriesPopup.allActions.append(act)
                        categoriesPopup.widgetActionNameList.append(widgetInfo.name)
            except Exception as inst: 
                redRLog.log(redRLog.REDRCORE, redRLog.ERROR,redRLog.formatException())
                pass
    except Exception as inst:
        redRLog.log(redRLog.REDRCORE, redRLog.ERROR, 'Exception in Tabs with widgetRegistry %s' % inst)
class SearchBox(redRlineEditHint):
    def __init__(self, widget, label=_('Search'),orientation='horizontal', items = [], toolTip = None,  width = -1, callback = None, **args):
        redRlineEditHint.__init__(self, widget = widget, label = label,displayLabel=False,
        orientation = orientation, items = items, toolTip = toolTip, width = width, callback = callback, **args)
        self.searchBox = redRSearchDialog()
        QObject.connect(self, SIGNAL('returnPressed()'), self.searchDialog)
            
    def eventFilter(self, object, ev):
        try: # a wrapper that prevents problems for the listbox debigging should remove this
            if object != self.listWidget and object != self:
                return 0
            if ev.type() == QEvent.MouseButtonPress:
                self.listWidget.hide()
                return 1
                    
            consumed = 0
            if ev.type() == QEvent.KeyPress:
                consumed = 1
                if ev.key() in [Qt.Key_Enter, Qt.Key_Return]:
                    #print _('Return pressed')
                    self.doneCompletion()
                elif ev.key() == Qt.Key_Escape:
                    self.listWidget.hide()
                    #self.setFocus()
                elif ev.key() in [Qt.Key_Up, Qt.Key_Down, Qt.Key_Home, Qt.Key_End, Qt.Key_PageUp, Qt.Key_PageDown]:
                    
                    self.listWidget.setFocus()
                    self.listWidget.event(ev)
                else:
                    #self.setFocus()
                    self.event(ev)
            return consumed
        except: 
            redRLog.log(redRLog.REDRCORE, redRLog.ERROR, redRLog.formatException())
            return 0
        
    def searchDialog(self):
        if unicode(self.text()) in self.itemsAsStrings:
            return
            
        else:
            itemText = unicode(self.text())
            #print _('Searching ')+itemText+' on Red-R.org'
            self.searchBox.show()
            url = 'http://www.red-r.org/?s='+itemText
            self.searchBox.updateUrl(url)