## <redRObjects Module.  This module (not a class) will contain and provide access to widget icons, lines, widget instances, and other redRObjects.  Accessor functions are provided to retrieve these objects, create new objects, and distroy objects.>
    # Copyright (C) 2010 Kyle R Covington

    # This program is free software: you can redistribute it and/or modify
    # it under the terms of the GNU General Public License as published by
    # the Free Software Foundation, either version 3 of the License, or
    # (at your option) any later version.

    # This program is distributed in the hope that it will be useful,
    # but WITHOUT ANY WARRANTY; without even the implied warranty of
    # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    # GNU General Public License for more details.

    # You should have received a copy of the GNU General Public License
    # along with this program.  If not, see <http://www.gnu.org/licenses/>.

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import orngCanvasItems, redREnviron, orngView, time, orngRegistry, redRLog
import redRi18n
# def _(a):
    # return a
_ = redRi18n.Coreget_()
defaultTabName = _('General')
_widgetRegistry = {}
_lines = {}
_widgetIcons = {defaultTabName:[]}
_widgetInstances = {}
_canvasTabs = {}
_canvasView = {}
_canvasScene = {}
_activeTab = ''
schemaDoc = None
canvasDlg = None
def setSchemaDoc(doc):
    global schemaDoc
    schemaDoc = doc
def setCanvasDlg(dlg):
    global canvasDlg
    canvasDlg = dlg
def readCategories():
    global _widgetRegistry
    _widgetRegistry = orngRegistry.readCategories()

def widgetRegistry():
    global _widgetRegistry
    if _widgetRegistry == {} or len(_widgetRegistry.keys()) == 0:
        readCategories()
    return _widgetRegistry
    
##############################
######      Tabs        ######
##############################
def tabNames():
    return _canvasView.keys()

def makeTabView(tabname, parent):
    global _activeTab
    w = QWidget()
    w.setLayout(QVBoxLayout())
    _canvasScene[tabname] = QGraphicsScene()
    _canvasView[tabname] = orngView.SchemaView(parent, tabname, _canvasScene[tabname], w)
    w.layout().addWidget(_canvasView[tabname])
    _activeTab = tabname
    _widgetIcons[tabname] = []
    return w
    
# def removeTabView(tabname, parent):
    
def activeTab():
    global _activeTab
    global _canvasView
    return _canvasView[_activeTab]

def scenes():
    global _canvasScene
    return [s for k, s in _canvasScene.items()]
def views():
    global _canvasView
    return _canvasView.values()
def activeCanvas():
    global _canvasScene
    global _activeTab
    return _canvasScene[_activeTab]
def activeTabName():
    global _activeTab
    return _activeTab
    
def makeSchemaTab(tabname):
    if tabname in _canvasTabs.keys():
        return activeTab(tabname)
        
    _canvasTabs[tabname] = QWidget()
    _canvasTabs[tabname].setLayout(QVBoxLayout())
    _tabsWidget.addTab(_canvasTabs[tabname], tabname)
    #_canvas[tabname] = QGraphicsScene()
    _canvasView[tabname] = orngView.SchemaView(self, _canvas[tabname], _canvasTabs[tabname])
    _canvasTabs[tabname].layout().addWidget(self.canvasView[tabname])
    _widgetIcons[tabName] = []
    setActiveTab(tabname)
def setActiveTab(tabname):
    global _activeTab
    _activeTab = tabname
def removeSchemaTab(tabname):
    if tabname == defaultTabName: return ## can't remove the general tab
    global _canvasView
    #global _canvas
    #global _canvasTabs
    global _canvasScene
    del _canvasView[tabname]
    del _canvasScene[tabname]
    del _widgetIcons[tabname]
    #del _canvas[tabname]
    #del _canvasTabs[tabname]
    
    
###############################
#######     icons       #######
###############################
def getIconsByTab(tabs = None):  # returns a dict of lists of icons for a specified tab, if no tab specified then all incons on all tabs are returned.
    global _widgetIcons
    global _canvasScene
    if tabs == None:
        tabs = _canvasScene.keys()
    if type(tabs) != list:
        tabs = [tabs]
    #print tabs, _('Tabs')
    tabIconsList = {}
    for t in tabs:
        tabIconsList[t] = _widgetIcons[t]
    return tabIconsList

def getWidgetByInstance(instance):
    global _widgetIcons
    for t in _widgetIcons.values():
        for widget in t:
            if widget.instance() == instance:
                return widget
    else:
        
        raise Exception(_('Widget %s not found in %s') % (instance, _widgetIcons))
    
def newIcon(canvas, tab, info, pic, dlg, instanceID, tabName):
    if getWidgetByIDActiveTabOnly(instanceID):
        return getWidgetByIDActiveTabOnly(instanceID)
    newwidget = orngCanvasItems.CanvasWidget(canvas, tab, info, pic, dlg, instanceID = instanceID, tabName = tabName)
    
    _widgetIcons[tabName].append(newwidget) # put a new widget into the stack with a timestamp.
    return newwidget
    
def getIconIDByIcon(icon):
    for k, i in _widgetIcons.items():
        if i == icon:
            return k
    return None

def getIconByIconID(id):
    return _widgetIcons[id]
    
def getIconByIconCaption(caption):
    icons = []
    for t in _widgetIcons.values():
        for i in t:
            if i.caption == caption:
                icons.append(i)
    return icons
    
def getIconByIconInstanceRef(instance):
    icons = []
    for t in _widgetIcons.values():
        for i in t:
            if i.instanceID == instance.widgetID:
                icons.append(i)
    return icons
    
def getIconByIconInstanceID(id):
    icons = []
    for t in _widgetIcons.values():
        for i in t:
            if i.instanceID == id:
                icons.append(i)
    return icons
def instanceOnTab(inst, tabName):
    global _widgetIcons
    for t in _widgetIcons.values():
        for i in t:
            if i.instance() == inst and i.tab == tabName:
                return True
    return False
def getWidgetByIDActiveTabOnly(widgetID):
    for t in _widgetIcons.values():
        #print widget.instanceID
        for widget in t:
            if (widget.instanceID == widgetID) and (widget.tab == activeTabName()):
                return widget
    return None
    
def removeWidgetIcon(icon):
    global _widgetIcons
    for t in _widgetIcons.values():
        redRLog.log(redRLog.REDRCORE, redRLog.DEBUG, _('widget icon values %s') % str(t))
        while icon in t:
            redRLog.log(redRLog.REDRCORE, redRLog.DEBUG, _('removing widget icon instance %s') % icon)
            t.remove(icon)
###########################
######  instances       ###
###########################

def showAllWidgets(): # move to redRObjects
        for k, i in _widgetInstances.items():
            i.show()
def closeAllWidgets():
    for k, i in _widgetInstances.items():
        i.close()
        
def addInstance(sm, info, settings, insig, outsig, id = None):
    global _widgetInstances
    global _widgetIcons
    global _widgetInfo
    redRLog.log(redRLog.REDRCORE, redRLog.DEBUG, _('adding instance number %s name %s') % (id, info.name))
    m = __import__(info.fileName)
    instance = m.__dict__[info.widgetName].__new__(m.__dict__[info.widgetName],
    _owInfo = redREnviron.settings["owInfo"],
    _owWarning = redREnviron.settings["owWarning"],
    _owError = redREnviron.settings["owError"],
    _owShowStatus = redREnviron.settings["owShow"],
    _packageName = info.packageName)
    instance.__dict__['_widgetInfo'] = info
    
    if info.name == 'Dummy': 
        instance.__init__(signalManager = sm,
        forceInSignals = insig, forceOutSignals = outsig)
    else: instance.__init__(signalManager = sm)
    
    instance.loadGlobalSettings()
    if settings:
        try:
            instance.setSettings(settings)
            # if '_customSettings' in settings.keys():
                # instance.loadCustomSettings(settings['_customSettings'])
            # else:
            instance.loadCustomSettings(settings)
        except Exception as inst:
            # print '##########################\n'*5 
            redRLog.log(redRLog.REDRCORE, redRLog.ERROR, _('redRObjects addInstance; error in setting settings or custom settings. <b>%s<b>') % inst)
            redRLog.log(redRLog.REDRCORE, redRLog.DEBUG,redRLog.formatException())
            

    instance.setProgressBarHandler(activeTab().progressBarHandler)   # set progress bar event handler
    instance.setProcessingHandler(activeTab().processingHandler)
    #instance.setWidgetStateHandler(self.updateWidgetState)
    #instance.setEventHandler(self.canvasDlg.output.widgetEvents)
    instance.setWidgetWindowIcon(info.icon)
    #instance.canvasWidget = self
    instance.widgetInfo = info
    if id != None:
        redRLog.log(redRLog.REDRCORE, redRLog.DEBUG, _('setting custom widget ID %s, We must be loading') % id)
        instance.widgetID = id
        instance.variable_suffix = '_' + instance.widgetID
        instance.resetRvariableNames()
    else:
        id = instance.widgetID
    redRLog.log(redRLog.REDRCORE, redRLog.DEBUG, _('instance ID is %s') % instance.widgetID)
    if id in _widgetInstances.keys():
        redRLog.log(redRLog.REDRCORE, redRLog.DEBUG, _('id was found in the keys, placing as new ID'))
        ## this is interesting since we aren't supposed to have this, just in case, we throw a warning
        redRLog.log(redRLog.REDRCORE, redRLog.WARNING, _('Warning: widget id already in the keys, setting new widget instance'))
        id = unicode(time.time())
        instance.widgetID = id
        instance.variable_suffix = '_' + instance.widgetID
        instance.resetRvariableNames()
    if not instance:
        raise Exception(_('Error in loading widget %s') % id)
    _widgetInstances[id] = instance
    
    return id
def getWidgetInstanceByID(id):
    global _widgetInstances
    #redRLog.log(redRLog.REDRCORE, redRLog.DEBUG, 'Loading widget %s keys are %s' % (id, _widgetInstances.keys()))
    try:
        return _widgetInstances[id]
    except Exception as inst:
        redRLog.log(redRLog.REDRCORE, redRLog.ERROR, _('Error in locating widget %s, available widget ID\'s are %s, %s') % (id, _widgetInstances.keys(), unicode(inst)))
def getWidgetInstanceByTempID(id):
    global _widgetInstances
    for w in _widgetInstances.values():
        if w.tempID == id:
            return w
def instances(wantType = 'list'):
    global _widgetInstances
    if wantType == 'list':## return all of the instances in a list
        redRLog.log(redRLog.REDRCORE, redRLog.DEBUG, _('Widget instances are %s') % unicode(_widgetInstances.values()))
        return _widgetInstances.values()
    else:
        return _widgetInstances
def removeWidgetInstanceByID(id):
    try:
        widget = getWidgetInstanceByID(id)
        removeWidgetInstance(widget)
        del _widgetInstances[id]
    except: 
        redRLog.log(redRLog.REDRCORE, redRLog.DEBUG, 'Failed to remove the widget instance %s' % id)
        
    # finally:
        # try:
            # del _widgetInstances[id]
        # except: pass
def removeWidgetInstance(widget):
    redRLog.log(redRLog.REDRCORE, redRLog.DEBUG, _('Removing widget instance %s') % widget)
    widget.onDeleteWidget()
    import sip
    sip.delete(widget)
###########################
######  lines           ###
###########################

def getLinesByTab(tabs = None):
    global _lines
    global _canvasScene
    if tabs == None:
        tabs = _canvasScene.keys()
    if type(tabs) != list:
        tabs = [tabs]
    tabLinesList = {}
    for t in tabs:
        lineList = []
        for k, li in _lines.items():
            if li.tab == t:
                lineList.append(li)
        tabLinesList[t] = lineList
    return tabLinesList

def getLinesByInstanceIDs(outInstance, inInstance):
    __lineList = []
    tempLines = []
    for k, l in _lines.items():
        __lineList.append((l, l.outWidget, l.inWidget))
    for ll in __lineList:
        if (ll[1].instanceID == outInstance) and (ll[2].instanceID == inInstance):
            tempLines.append(ll[0])
    return tempLines
    
def getLine(outIcon, inIcon):  ## lines are defined by an in icon and an out icon.  there should only be one valid combination in the world.
    __lineList = []
    for k, l in _lines.items():
        __lineList.append((l, l.outWidget, l.inWidget))
    for ll in __lineList:
        if (ll[1] == outIcon) and (ll[2] == inIcon):
            return ll[0]
    return None
def addCanvasLine(outWidget, inWidget, enabled = -1):
    global schemaDoc
    #redRLog.log(redRLog.REDRCORE, redRLog.INFO, _('Adding canvas line'))
    line = orngCanvasItems.CanvasLine(schemaDoc.signalManager, schemaDoc.canvasDlg, schemaDoc.activeTab(), outWidget, inWidget, schemaDoc.activeCanvas(), activeTabName())
    _lines[unicode(time.time())] = line
    if enabled:
        line.setEnabled(1)
    else:
        line.setEnabled(0)
    line.show()
    outWidget.addOutLine(line)
    outWidget.updateTooltip()
    inWidget.addInLine(line)
    inWidget.updateTooltip()
    return line
def addLine(outWidgetInstance, inWidgetInstance, enabled = 1):
        global schemaDoc
        # redRLog.log(redRLog.REDRCORE, redRLog.INFO, 'Adding line outWidget %s, inWidget %s' % (
        # outWidgetInstance.caption, inWidgetInstance.caption))
        ## given an out and in instance connect a line to all of the icons with those instances.
        tabIconStructure = getIconsByTab()
        ot = activeTabName()
        owi = outWidgetInstance
        iwi = inWidgetInstance
        for tname, icons in tabIconStructure.items():
            schemaDoc.setTabActive(tname)
            o = None
            i = None
            
            for ic in icons:
                if ic.instance() == iwi:
                    i = ic
                    redRLog.log(redRLog.REDRCORE, redRLog.DEBUG, _('found in widget %s') % ic)
                if ic.instance() == owi:
                    o = ic
                    redRLog.log(redRLog.REDRCORE, redRLog.DEBUG, _('found out widget %s') % ic)
            if i!= None and o != None:  # this means that there are the widget icons in question in the canvas so we should add a line between them.
                line = getLine(o, i)
                redRLog.log(redRLog.REDRCORE, redRLog.DEBUG, _('the matching line is %s') % line)
                if not line:
                    line = addCanvasLine(o, i, enabled = enabled)
                    line.refreshToolTip()
            
        schemaDoc.setTabActive(ot)
        updateLines()
        return 1
def removeLine(outWidgetInstance, inWidgetInstance, outSignalName, inSignalName):
        redRLog.log(redRLog.REDRCORE, redRLog.DEBUG, _('Removing Line'))
        tabIconStructure = getIconsByTab()
        owi = outWidgetInstance
        iwi = inWidgetInstance
        for tname, icons in tabIconStructure.items():
            
            o = None
            i = None
            for ic in icons:
                if ic.instance() == iwi:
                    i = ic
                if ic.instance() == owi:
                    o = ic
                    
            if i!= None and o != None:  # this means that there are the widget icons in question in the canvas so we should add a line between them.
                line = getLine(o, i)
                if line:
                    removeLineInstance(line)
            
            
def removeLineInstance(line):
    obsoleteSignals = line.outWidget.instance().outputs.getSignalLinks(line.inWidget.instance())
    redRLog.log(redRLog.REDRCORE, redRLog.DEBUG, _('Removing obsolete signals %s') % obsoleteSignals)
    redRLog.log(redRLog.REDRCORE, redRLog.DEBUG, 'removing the following signals %s' % obsoleteSignals)
    for (s, id) in obsoleteSignals:
        signal = line.inWidget.instance().inputs.getSignal(id)
        line.outWidget.instance().outputs.removeSignal(signal, s)
    for k, l in _lines.items():
        if l == line:
            del _lines[k]   
    line.inWidget.removeLine(line)
    line.outWidget.removeLine(line)
    line.inWidget.updateTooltip()
    line.outWidget.updateTooltip()
    line.remove()
def lines():
    return _lines
def updateLines():
    global _lines
    for l in _lines.values():
        l.updateStatus()
def getLinesByWidgetInstanceID(outID, inID):  # must return a list of lines that match the outID and inID.
    global _lines
    tempLines = []
    for k, l in _lines.items():
        if l.outWidget.instanceID == outID and l.inWidget.instanceID == inID:
            tempLines.append(l)
    return tempLines