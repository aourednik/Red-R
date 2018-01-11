# Author: Gregor Leban (gregor.leban@fri.uni-lj.si) modified by Kyle R Covington and Anup Parikh
# Description:
#    document class - main operations (save, load, ...)
#
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys, os, os.path, traceback, redRLog
from xml.dom.minidom import Document, parse
import xml.dom.minidom
import orngView, orngCanvasItems
from orngDlgs import *
import RSession, globalData, redRPackageManager, redRStyle, redRHistory, redREnviron
import redRi18n
from orngSignalManager import SignalManager, SignalDialog
import cPickle, math, zipfile, urllib, sip, redRObjects, redRSaveLoad
from libraries.base.qtWidgets.textEdit import textEdit as redRTextEdit
from libraries.base.qtWidgets.splitter import splitter as redRSplitter
from libraries.base.qtWidgets.button import button as redRbutton
#import pprint, 
# pp = pprint.PrettyPrinter(indent=4)

# def _(a):
    # return a
_ = redRi18n.get_('messages', os.path.join(redREnviron.directoryNames['redRDir'], 'languages'), languages = ['French'])
class SchemaDoc(QWidget):
    def __init__(self, canvasDlg, *args):
        QWidget.__init__(self, *args)
        global _
        _ = redRi18n.get_('messages', os.path.join(redREnviron.directoryNames['redRDir'], 'languages'), languages = ['French'])
        self.canvasDlg = canvasDlg
        self.ctrlPressed = 0
        self.version = 'trunk'                  # should be changed before making the installer or when moving to a new branch.
        #self.lines = []                         # list of orngCanvasItems.CanvasLine items
        #self.widgets = []                       # list of orngCanvasItems.CanvasWidget items
        self.signalManager = SignalManager()    # signal manager to correctly process signals

        self.sessionID = 0
        self.schemaPath = redREnviron.settings["saveSchemaDir"]
        self.schemaName = ""
        
        self.loadedSettingsDict = {}
        self.setLayout(QHBoxLayout())
        # self.splitter = redRSplitter(self)
        # left = self.splitter.widgetArea()
        self.tabsWidget = QTabWidget()
        self.tabsWidget.setDocumentMode(True)
        self.tabsWidget.setTabsClosable(True)
        self.tabsWidget.setMovable(True)
        self.tabsWidget.tabBar().setShape(QTabBar.RoundedNorth)
        addTabButton = redRbutton(None,label='',
        icon=os.path.join(redREnviron.directoryNames['canvasIconsDir'],'plus.png'),
        callback=self.newTab)
        self.tabsWidget.setCornerWidget(addTabButton.controlArea)
        QObject.connect(self.tabsWidget, SIGNAL('currentChanged(int)'), self.resetActiveTab)
        QObject.connect(self.tabsWidget, SIGNAL('tabCloseRequested(int)'), self.removeTab)
        self.layout().addWidget(self.tabsWidget)
        #self.canvas = QGraphicsScene(0,0,2000,2000)
        
        
        self.widgetPopupMenu = CanvasPopup(self)
        
        
        self.instances = {}
        self.makeSchemaTab(_('General'))
        
        self.layout().setMargin(0)
        self.RVariableRemoveSupress = 0
        self.urlOpener = urllib.FancyURLopener()
        # log.setOutputManager(self)
        # self.printOutput = canvasDlg.printOutput
        redRObjects.setSchemaDoc(self)
        redRSaveLoad.setSchemaDoc(self)

    def resetActiveTab(self, int):
        self.setActiveTab(unicode(self.tabsWidget.tabText(int)))
    def setActiveTab(self, tabname):
        redRObjects.setActiveTab(tabname)
    def widgets(self):
        wlist = []
        rolist = redRObjects.getIconsByTab()
        for k, l in rolist.items():
            wlist += l
        return wlist
    def lines(self):
        llist = []
        rolist = redRObjects.getLinesByTab()
        for k, l in rolist.items():
            llist += l
        return llist
    def widgetIcons(self, tab):  # moving to redrObjects / moved
        return redRObjects.getIconsByTab(tab)
    def widgetLines(self, tab): # moving to redrObjects / moved
        return redRObjects.getLinesByTab(tab)
    def activeTab(self): # part of the view
        return redRObjects.activeTab()
    def activeTabName(self):    # part of the view
        return unicode(self.tabsWidget.tabText(self.tabsWidget.currentIndex()))
    def activeCanvas(self):     # part of the view
        return redRObjects.activeCanvas() # self.canvas[unicode(self.tabsWidget.tabText(self.tabsWidget.currentIndex()))]
    def setTabActive(self, name):   # part of the view
        for i in range(self.tabsWidget.count()):
            if unicode(self.tabsWidget.tabText(i)) == name:
                self.tabsWidget.setCurrentIndex(i)
                break
        
    def makeSchemaTab(self, tabname):   # part of the view
        redRLog.log(redRLog.REDRCORE, redRLog.INFO, _('Make a new tab called %s.') % tabname)
        if tabname in redRObjects.tabNames():
            self.setTabActive(tabname)
            return
        redRObjects.setActiveTab(tabname)
        self.tabsWidget.addTab(redRObjects.makeTabView(tabname, self), tabname)
    def removeTab(self,index):
        mb = QMessageBox(_("Remove Tab"), _("Are you sure that you want to remove the tab?\n\nAny widgets that have not been cloned will be lost."), 
        QMessageBox.Information, QMessageBox.Ok | QMessageBox.Default, 
        QMessageBox.No | QMessageBox.Escape, QMessageBox.NoButton,self)
        
        if mb.exec_() == QMessageBox.Ok:
            self.removeSchemaTab(unicode(self.tabsWidget.tabText(index)))
       
    def removeCurrentTab(self):
    
        mb = QMessageBox(_("Remove Current Tab"), _("Are you sure that you want to remove the current tab?\n\nAny widgets that have not been cloned will be lost."), 
            QMessageBox.Information, QMessageBox.Ok | QMessageBox.Default, 
            QMessageBox.No | QMessageBox.Escape, QMessageBox.NoButton,self)
        
        if mb.exec_() == QMessageBox.Ok:
            self.removeSchemaTab(redRObjects.activeTabName())
    
    def removeSchemaTab(self, tabname):
        # set the tab in question to the active tab, this will set the current tab index so we can remove easily.
        self.setTabActive(tabname)
        
        ## first we need to clear all of the widgets from the tab
        
        while len(redRObjects.getIconsByTab(tabname)[tabname]) != 0:  # I know that these while loops may not be so efficient, but if we don't do this then reference counts get really messed up!!!
            self.removeWidget(redRObjects.getIconsByTab(tabname)[tabname][0])

        ## next find the index
        i = self.tabsWidget.currentIndex()
        ## remove the widget
        if tabname != _('General'):  ## General tab is a special case, this will always be present.
            self.tabsWidget.removeTab(i)
            ## remove the references to the tab in the redRObjects
            redRObjects.removeSchemaTab(tabname)
    def selectAllWidgets(self):
        self.activeTab().selectAllWidgets()
    # add line connecting widgets outWidget and inWidget
    # if necessary ask which signals to connect
    def addLine(self, outWidget, inWidget, enabled = True, process = True, ghost = False):  # adds the signal link between the data and instantiates the line on the canvas.  move to the signal manager or the view?
        
        if outWidget == inWidget: 
            raise Exception, _('Same Widget')
        
        # check if line already exists
        line = self.getLine(outWidget, inWidget)
        if line:
            self.resetActiveSignals(outWidget, inWidget, None, enabled)
            return line
        canConnect = inWidget.instance().inputs.matchConnections(outWidget.instance().outputs)
        
        if not canConnect:
            mb = QMessageBox(_("Failed to Connect"), _("Connection Not Possible\n\nWould you like to search for templates\nwith these widgets?"), 
                QMessageBox.Information, QMessageBox.Ok | QMessageBox.Default, 
                QMessageBox.No | QMessageBox.Escape, QMessageBox.NoButton)
            if mb.exec_() == QMessageBox.Ok:
                ## go to the website and see if there are templates with the widgets in question
                import webbrowser
                url = 'http://www.red-r.org/?s='+outWidget.widgetInfo.name+'+'+inWidget.widgetInfo.name
                
                webbrowser.open(url)
                
            mb = QMessageBox(_("Failed to Connect"), _("Not valid connection.\nWould you like to force this connection anyway?\n\nTHIS MIGHT CAUSE ERRORS AND EVEN CRASH RED-R!!!"), 
                QMessageBox.Information, QMessageBox.Ok | QMessageBox.Default, 
                QMessageBox.No | QMessageBox.Escape, QMessageBox.NoButton)
            if mb.exec_() == QMessageBox.No:
                return None

        if process != False:
            dialog = SignalDialog(self.canvasDlg, None)
            dialog.setOutInWidgets(outWidget, inWidget)

            # if there are multiple choices, how to connect this two widget, then show the dialog
        
            possibleConnections = inWidget.instance().inputs.getPossibleConnections(outWidget.instance().outputs)  #  .getConnections(outWidget, inWidget)
            if len(possibleConnections) > 1 or len(possibleConnections) == 0:
                #print possibleConnections
                #dialog.addLink(possibleConnections[0][0], possibleConnections[0][1])  # add a link between the best signals.
                if dialog.exec_() == QDialog.Rejected:
                    return None
                possibleConnections = dialog.getLinks()
            

            #self.signalManager.setFreeze(1)
            redRLog.log(redRLog.REDRCORE, redRLog.INFO, _('Possible Connections are %s') % str(possibleConnections))
            for (outName, inName) in possibleConnections:
                
                self.addLink(outWidget, inWidget, outName, inName, enabled, process = process)

        #self.signalManager.setFreeze(0, outWidget.instance)

        # if signals were set correctly create the line, update widget tooltips and show the line
        line = self.getLine(outWidget, inWidget)
        if line:
            outWidget.updateTooltip()
            inWidget.updateTooltip()
        redRHistory.addConnectionHistory(outWidget,inWidget)
        redRLog.log(redRLog.REDRCORE, redRLog.INFO, _('Add connection between %s and %s.') % (outWidget.caption, inWidget.caption))
        return line


    # reset signals of an already created line
    def resetActiveSignals(self, outWidget, inWidget, newSignals = None, enabled = 1):
        #print "<extra>orngDoc.py - resetActiveSignals() - ", outWidget, inWidget, newSignals
        signals = []
        for line in self.lines():
            if line.outWidget == outWidget and line.inWidget == inWidget:
                signals = line.getSignals()

        if newSignals == None:
            dialog = SignalDialog(self.canvasDlg, None)
            dialog.setOutInWidgets(outWidget, inWidget)
            for (outName, inName) in signals:
                #print "<extra>orngDoc.py - SignalDialog.addLink() - adding signal to dialog: ", outName, inName
                dialog.addLink(outName, inName)

            # if there are multiple choices, how to connect this two widget, then show the dialog
            if dialog.exec_() == QDialog.Rejected:
                return

            newSignals = dialog.getLinks()

        for (outName, inName) in signals:
            if (outName, inName) not in newSignals:
                self.removeLink(outWidget, inWidget, outName, inName)
                signals.remove((outName, inName))

        #self.signalManager.setFreeze(1)
        for (outName, inName) in newSignals:
            if (outName, inName) not in signals:
                self.addLink(outWidget, inWidget, outName, inName, enabled)
        #self.signalManager.setFreeze(0, outWidget.instance)

        outWidget.updateTooltip()
        inWidget.updateTooltip()


    # add one link (signal) from outWidget to inWidget. if line doesn't exist yet, we create it
    def addLink(self, outWidget, inWidget, outSignalName, inSignalName, enabled = 1, fireSignal = 1, process = True, loading = False):
        ## addLink should move through all of the icons on all canvases and check if there are icons which are clones of the outWidget and inWidget
        ## after this lines should be created between those widgets and the lines should be set to enabled and data.
        
        if inWidget.instance().inputs.getSignal(inSignalName):
            if not inWidget.instance().inputs.getSignal(inSignalName)['multiple']:
                ## check existing link to the input signal
                
                existing = inWidget.instance().inputs.getLinks(inSignalName)
                for l in existing:
                    l['parent'].outputs.removeSignal(inWidget.instance().inputs.getSignal(inSignalName), l['sid'])
                    redRObjects.removeLine(l['parent'], inWidget.instance(), l['sid'], inSignalName)
        
        
        redRObjects.addLine(outWidget.instance(), inWidget.instance(), enabled = enabled)
        
        
        ok = outWidget.instance().outputs.connectSignal(inWidget.instance().inputs.getSignal(inSignalName), outSignalName, process = process)#    self.signalManager.addLink(outWidget, inWidget, outSignalName, inSignalName, enabled)
        if not ok and not loading:
            #remove the lines
            redRObjects.removeLine(outWidget.instance(), inWidget.instance(), outSignalName, inSignalName)
            ## we should change this to a dialog so that the user can connect the signals manually if need be.
            QMessageBox.information( self, "Red-R Canvas", "Unable to add link. Something is really wrong; try restarting Red-R Canvas.", QMessageBox.Ok + QMessageBox.Default )
            

            return 0
        elif not ok:
            return 0
        else:
            return 1
    def addLink175(self, outWidget, inWidget, outSignalName, inSignalName, enabled = 1, fireSignal = 1, process = False, loading = False):
        ## compatibility layer for older schemas on changing signal classes.  this is actually a good way to allow for full compatibility between versions.

        ## this is where we have a diversion from the normal loading.  obviously if we made it to here there aren't the signal names in the in or out widgets that match.
        ##      we will open a dialog and show the names of the signals and ask the user to connect them
        dialog = SignalDialog(self.canvasDlg, None)
        from libraries.base.qtWidgets.widgetLabel import widgetLabel
        widgetLabel(dialog, 'Please connect the signals that best match these: %s to %s' % (outSignalName, inSignalName)) 
        dialog.setOutInWidgets(outWidget, inWidget)

        # if there are multiple choices, how to connect this two widget, then show the dialog
    
        possibleConnections = inWidget.instance().inputs.getPossibleConnections(outWidget.instance().outputs)  #  .getConnections(outWidget, inWidget)
        if len(possibleConnections) > 1:
            #print possibleConnections
            #dialog.addLink(possibleConnections[0][0], possibleConnections[0][1])  # add a link between the best signals.
            if dialog.exec_() == QDialog.Rejected:
                return None
            possibleConnections = dialog.getLinks()
        

        #self.signalManager.setFreeze(1)
        for (outName, inName) in possibleConnections:
            
            self.addLink(outWidget, inWidget, outName, inName, enabled, process = False)  # under no circumstance will we process an old signal again.
        
    ### moved to redRObjects
    # remove only one signal from connected two widgets. If no signals are left, delete the line
    def removeLink(self, outWidget, inWidget, outSignalName, inSignalName):
        outWidget.outputs.removeSignal(inWidgetInstance.inputs.getSignal(inSignalName), outSignalName)
    
        if not outWidget.outputs.signalLinkExists(inWidgetInstance): ## move through all of the icons and remove all lines connecting, only do this if there is no more signal.
            return redRObjects.removeLine(outWidget, inWidget, outSignalName, inSignalName)
    
    def newTab(self): # part of the view
        td = NewTabDialog(self.canvasDlg)
        if td.exec_() != QDialog.Rejected:
            if unicode(td.tabName.text()) == "": return
            self.makeSchemaTab(unicode(td.tabName.text()))
            self.setTabActive(unicode(td.tabName.text()))
    def cloneToTab(self):   # part of the view
        redRSaveLoad.collectIcons()
        if len(redRSaveLoad._tempWidgets) == 0: 
            redRLog.log(redRLog.REDRCORE, redRLog.DEBUG, _('No tempWidgets to clone!!!'))
            return
        tempWidgets = redRSaveLoad._tempWidgets
        td = CloneTabDialog(self.canvasDlg)
        if td.exec_() == QDialog.Rejected: return ## nothing interesting to do
        try:
            tabName = unicode(td.tabList.selectedItems()[0].text())
        except: return 
        #if tabName == unicode(self.tabsWidget.tabText(self.tabsWidget.currentIndex())): return # can't allow two of the same widget on a tab.
        for w in tempWidgets:
            redRLog.log(redRLog.REDRCORE, redRLog.INFO, _('Create a clone widget %s in tab %s.') % ( w.caption + _(' (Clone)'), tabName))
            self.cloneWidget(w, viewID = tabName, x = w.x(), y = w.y(), caption = w.caption)
        self.setTabActive(tabName) ## set the new tab as active so the user knows something happened.
    def cloneWidget(self, widget, viewID = None, x= -1, y=-1, caption = "", widgetSettings = None, saveTempDoc = True):
        ## we want to clone the widget.  This involves moving to the correct view and placing the icon on the canvas but setting the instance to be the same as the widget instance on the other widget.
        self.setTabActive(viewID)
        if redRObjects.instanceOnTab(widget.instance(), viewID): return 1      ## the widget must already be on the tab so we can't add it again.
        qApp.setOverrideCursor(Qt.WaitCursor)
        try:
            newwidget = redRObjects.newIcon(self.activeCanvas(), self.activeTab(), widget.widgetInfo, redRStyle.defaultWidgetIcon, self.canvasDlg, instanceID = widget.instance().widgetID, tabName = self.activeTabName()) ## set the new orngCanvasItems.CanvasWidget, this item contains the instance!!!
        except:
            type, val, traceback = sys.exc_info()
            redRLog.log(redRLog.REDRCORE, redRLog.ERROR, unicode(traceback))
            sys.excepthook(type, val, traceback)  # we pretend that we handled the exception, so that it doesn't crash canvas
            qApp.restoreOverrideCursor()
            return None

        self.resolveCollisions(newwidget, x, y)

        if caption == "":
            caption = widget.caption + _(' (Clone)')
        newwidget.updateText(caption)
        self.activeCanvas().update()

        ### add lines to widgets on the current active tab if there is a link from the widget in question to one of the other widgets on the canvas.
        #print _('Adding lines')
        tabWidgets = redRObjects.getIconsByTab(self.activeTabName())[self.activeTabName()]
        tabWidgetInstances = [i.instance() for i in tabWidgets]
        lines = redRObjects.lines()
        
        for l in lines.values(): # move across all of the lines, l is each line
            if (l.outWidget.instance() == newwidget.instance() or l.inWidget.instance() == newwidget.instance()) and (l.outWidget.instance() in tabWidgetInstances) and (l.inWidget.instance() in tabWidgetInstances): ## this line contains widgets that are on the active canvas and involves the newwidget.  If this line doesn't exist on this tab then we need to make it.
                line = None
                if l.outWidget.instance() == newwidget.instance():
                    if redRObjects.getLine(newwidget, l.inWidget) != None:  # the line already exists
                        continue  
                    else:
                        for w in tabWidgets:
                            if w.instance() == l.inWidget.instance():
                                ow = w
                                break
                        line = redRObjects.addCanvasLine(newwidget, w, self)
                elif l.inWidget.instance() == newwidget.instance():
                    if redRObjects.getLine(l.outWidget, newwidget) != None: continue # the line already exists
                    else:
                        for w in tabWidgets:
                            if w.instance() == l.outWidget.instance():
                                iw = w
                                break
                        line = redRObjects.addCanvasLine(w, newwidget, self)
                if line:
                    line.setNoData(l.noData)
                        
        
        qApp.restoreOverrideCursor()
        return newwidget
 
    #def addWidgetInstance(self, name, inputs = None, outputs = None, widgetID = None):
    def addWidgetIcon(self, widgetInfo, instanceID):
        ## handle the caption here so we don't run into conflicts in the future
        caption = widgetInfo.name
        if self.getWidgetByCaption(caption):
            i = 2
            while self.getWidgetByCaption(caption + " (" + unicode(i) + ")"): i+=1
            caption = caption + " (" + unicode(i) + ")"
            
        newwidget = redRObjects.newIcon(self.activeCanvas(), self.activeTab(), widgetInfo, redRStyle.defaultWidgetIcon, self.canvasDlg, instanceID =  instanceID, tabName = self.activeTabName())## set the new orngCanvasItems.CanvasWidget
        newwidget.caption = caption
        newwidget.updateText(caption)
        ##self.widgets.append(newwidget)
        return newwidget
    def addWidget(self, widgetInfo, x= -1, y=-1, caption = "", widgetSettings = None, saveTempDoc = True, forceInSignals = None, forceOutSignals = None, id = None):
        qApp.setOverrideCursor(Qt.WaitCursor)
        try:
            instanceID = self.addInstance(self.signalManager, widgetInfo, widgetSettings, forceInSignals, forceOutSignals, id = id)
            newwidget = self.addWidgetIcon(widgetInfo, instanceID)
            #if widgetInfo.name == 'dummy' and (forceInSignals or forceOutSignals):
            redRLog.log(redRLog.REDRCORE, redRLog.INFO, _('Create new widget named %s.') % newwidget.caption)
        except:
            type, val, traceback = sys.exc_info()
            redRLog.log(redRLog.REDRCORE, redRLog.ERROR, unicode(traceback))
            sys.excepthook(type, val, traceback)  # we pretend that we handled the exception, so that it doesn't crash canvas
            qApp.restoreOverrideCursor()
            return None

        self.resolveCollisions(newwidget, x, y)
            
        newwidget.instance().setWindowTitle(newwidget.caption)
        
        self.activeCanvas().update()

        # show the widget and activate the settings
        try:
            self.signalManager.addWidget(newwidget.instance())
            newwidget.show()
            newwidget.updateTooltip()
            newwidget.setProcessing(1)
            # if redREnviron.settings["saveWidgetsPosition"]:
                # newwidget.instance().restoreWidgetPosition()
            newwidget.setProcessing(0)
        except:
            type, val, traceback = sys.exc_info()
            sys.excepthook(type, val, traceback)  # we pretend that we handled the exception, so that it doesn't crash canvas

            
        ## try to set up the ghost widgets
        qApp.restoreOverrideCursor()
        return newwidget.instanceID
    def addInstance(self, signalManager, widgetInfo, widgetSettings = None, forceInSignals = None, forceOutSignals = None, id = None):
        return redRObjects.addInstance(signalManager, widgetInfo, settings = widgetSettings, insig = forceInSignals, outsig = forceOutSignals, id = id)
        
    def returnInstance(self, id):
        return redRObjects.getWidgetInstanceByID(id)
    def resolveCollisions(self, newwidget, x, y):
        if x==-1 or y==-1:
            if self.activeTab().getSelectedWidgets():
                x = self.activeTab().getSelectedWidgets()[-1].x() + 110
                y = self.activeTab().getSelectedWidgets()[-1].y()
            elif self.widgets() != []:
                x = self.widgets()[-1].x() + 110  # change to selected widget 
                y = self.widgets()[-1].y()
            else:
                x = 30
                y = 50
        newwidget.setCoords(x, y)
        # move the widget to a valid position if necessary
        invalidPosition = (self.activeTab().findItemTypeCount(self.activeCanvas().collidingItems(newwidget), orngCanvasItems.CanvasWidget) > 0)
        if invalidPosition:
            for r in range(20, 200, 20):
                for fi in [90, -90, 180, 0, 45, -45, 135, -135]:
                    xOff = r * math.cos(math.radians(fi))
                    yOff = r * math.sin(math.radians(fi))
                    rect = QRectF(x+xOff, y+yOff, 48, 48)
                    invalidPosition = self.activeTab().findItemTypeCount(self.activeCanvas().items(rect), orngCanvasItems.CanvasWidget) > 0
                    if not invalidPosition:
                        newwidget.setCoords(x+xOff, y+yOff)
                        break
                if not invalidPosition:
                    break
    
    def instanceStillWithIcon(self, instanceID):
        for widget in self.widgets():
            
            if widget.instanceID == instanceID:
                return True
        return False
    # remove widget
    def removeWidget(self, widget, saveTempDoc = True):
        if not widget:
            redRLog.log(redRLog.REDRCORE, redRLog.DEBUG, _('Bad widget supplied %s') % widget)
            return
        instanceID = widget.instanceID
        #widget.closing = close
        try:
            while widget.inLines != []: redRObjects.removeLineInstance(widget.inLines[0])
            while widget.outLines != []:  redRObjects.removeLineInstance(widget.outLines[0])
        except Exception as inst:
            redRLog.log(redRLog.REDRCORE, redRLog.DEBUG, _('Error in removing lines %s') % str(inst))
        #self.signalManager.removeWidget(widget.instance()) # sending occurs before this point
        try:
            redRLog.log(redRLog.REDRCORE, redRLog.DEBUG, _('trying to remove widget icon %s') % widget)
            widget.remove() ## here we need to check if others have the widget instance.
            redRObjects.removeWidgetIcon(widget)
        except Exception as inst:
            redRLog.log(redRLog.REDRCORE, redRLog.DEBUG, _('Error in removing widget icon %s') %widget)
        if not self.instanceStillWithIcon(instanceID):
            redRLog.log(10, 9, 3, _('Removing Widget'))
            redRObjects.removeWidgetInstanceByID(instanceID)
    def clear(self):
        self.canvasDlg.setCaption()
        for t in redRObjects.tabNames():
            #if t == _('General'): continue
            self.removeSchemaTab(t)
        RSession.Rcommand('rm(list = ls())')
        #self.activeCanvas().update()
        scenes = redRObjects.scenes()
        for s in scenes:
            s.update()
        self.schemaName = ""
        #self.saveTempDoc()
        

    def enableAllLines(self):
        for k, line in redRObjects.lines().items():
            self.signalManager.setLinkEnabled(line.outWidget.instance, line.inWidget.instance, 1)
            line.setEnabled(1)
            #line.repaintLine(self.canvasView)
        self.activeCanvas().update()

    def disableAllLines(self):
        for k, line in redRObjects.lines().items():
            self.signalManager.setLinkEnabled(line.outWidget.instance, line.inWidget.instance, 0)
            line.setEnabled(0)
            #line.repaintLine(self.canvasView)
        self.activeCanvas().update()

    # return a new widget instance of a widget with filename "widgetName"
    def addWidgetByFileName(self, widgetFileName, x, y, caption = '', widgetSettings=None, saveTempDoc = True, forceInSignals = None, forceOutSignals = None, id = None):
        try:
            if widgetFileName == 'base_dummy': print _('Loading dummy step 1a')
            widget = redRObjects.widgetRegistry()['widgets'][widgetFileName]
            return self.addWidget(widget, x, y, caption, widgetSettings, saveTempDoc, forceInSignals, forceOutSignals, id = id)
        except Exception as inst:
            redRLog.log(redRLog.REDRCORE, redRLog.ERROR, _('Loading exception occured for widget ')+widgetFileName+' '+unicode(inst))
            
            return None
    # addWidgetIconByFileName(name, x = xPos, y = yPos + addY, caption = caption, instance = instance) 
    def addWidgetIconByFileName(self, name, x= -1, y=-1, caption = "", instance = None):
        
        widget = redRObjects.widgetRegistry()['widgets'][name]
        newwidget = self.addWidgetIcon(widget, instance)
        self.resolveCollisions(newwidget, x, y)
        if caption != "": 
            newwidget.updateText(caption)
    def addWidgetInstanceByFileName(self, name, settings = None, inputs = None, outputs = None, id = None):
        #try:
            #if widgetFileName == 'base_dummy': print _('Loading dummy step 1a')
        widget = redRObjects.widgetRegistry()['widgets'][name]
        return self.addInstance(self.signalManager, widget, settings, inputs, outputs, id = id)
        # except Exception as inst:
            # redRLog.log(redRLog.REDRCORE, redRLog.ERROR,  _('Loading exception occured for widget ')+name+' '+unicode(inst))
            
            # return None
    # return the widget icon that has caption "widgetName"
    def getWidgetByCaption(self, widgetName):
        return redRObjects.getIconByIconCaption(widgetName)
    def getWidgetByInstance(self, instance):
        return redRObjects.getIconByIconInstanceRef(instance)
    def getWidgetByID(self, widgetID):
        return redRObjects.getIconByIconInstanceID(widgetID)
    def getWidgetByIDActiveTabOnly(self, widgetID):
        return redRObjects.getWidgetByIDActiveTabOnly(widgetID)
    def getWidgetCaption(self, widgetInstance):
        widget = redRObjects.getIconByIconInstanceRef(widgetInstance)
        if widget == None:
            redRLog.log(redRLog.REDRCORE, redRLog.ERROR, _("Error. Attempted to Access Invalid widget instance : "), widgetInstance)
            return ""
        return widget.caption

    # get line from outWidget to inWidget
    def getLine(self, outWidget, inWidget):
        return redRObjects.getLine(outWidget, inWidget)
    # find canvasItems from widget ID
    def findWidgetFromID(self, widgetID):
        return redRObjects.getIconByIconInstanceID()

    # find orngCanvasItems.CanvasWidget from widget instance
    def findWidgetFromInstance(self, widgetInstance):
        return redRObjects.getIconByIconInstanceRef(widgetInstance)
    def handleDirty(self, ow, iw, dirty):
        line = self.getLine(ow, iw)
        if not line or line == None:
            
            return
        line.dirty = dirty
        
        self.canvas.update()
    def handleNone(self, ow, iw, none):
        line = self.getLine(ow, iw)
        if line:
            line.noData = none
            line.refreshToolTip()
            redRLog.log(redRLog.REDRCORE, redRLog.INFO, _('Setting line %s noData slot to %s') % (line, noData))
            
        self.canvas.update()
    # ###########################################
    # SAVING, LOADING, ....
    # ###########################################
    def minimumY(self):
        return redRSaveLoad.minimumY()


    def saveDocumentAs(self):
        return redRSaveLoad.saveDocumentAs()
        

        
    def checkID(self, widgetID):
        for widget in self.widgets():
            if widget.instance().widgetID == widgetID:
                return False
        else:
            return True
        
    def checkWidgetDuplication(self, widgets):
        for widget in widgets.getElementsByTagName("widget"):
            widgetIDisNew = self.checkID(widget.getAttribute('widgetID'))
            if widgetIDisNew == False:
                qApp.restoreOverrideCursor()
                QMessageBox.critical(self, _('Red-R Canvas'), 
                _('Widget ID is a duplicate, I can\'t load this!!!'),  QMessageBox.Ok)
                return False
        return True

    
    def dumpWidgetVariables(self):
        for widget in self.widgets():
            self.canvasDlg.output.write("<hr><b>%s</b><br>" % (widget.caption))
            v = vars(widget.instance).keys()
            v.sort()
            for val in v:
                self.canvasDlg.output.write("%s = %s" % (val, getattr(widget.instance, val)))
            
    def keyReleaseEvent(self, e):
        self.ctrlPressed = int(e.modifiers()) & Qt.ControlModifier != 0
        e.ignore()
    
    def keyPressEvent(self, e):
        self.ctrlPressed = int(e.modifiers()) & Qt.ControlModifier != 0
        if e.key() > 127:
            #e.ignore()
            QWidget.keyPressEvent(self, e)
            return

        # the list could include (e.ShiftButton, "Shift") if the shift key didn't have the special meaning
        pressed = "-".join(filter(None, [int(e.modifiers()) & x and y for x, y in [(Qt.ControlModifier, "Ctrl"), (Qt.AltModifier, "Alt")]]) + [chr(e.key())])
        widgetToAdd = self.canvasDlg.toolbarFunctions.widgetShortcuts.get(pressed)
        if widgetToAdd:
            self.addWidget(widgetToAdd)
            if e.modifiers() & Qt.ShiftModifier and len(self.widgets()) > 1:
                self.addLine(self.widgets()[-2], self.widgets()[-1])
        else:
            #e.ignore()
            QWidget.keyPressEvent(self, e)
            
    

class CloneTabDialog(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        global _
        _ = redRi18n.get_('messages', os.path.join(redREnviron.directoryNames['redRDir'], 'languages'), languages = ['French'])
        self.setWindowTitle(_('New Tab'))
        
        self.setLayout(QVBoxLayout())
        layout = self.layout()
        mainWidgetBox = QWidget(self)
        mainWidgetBox.setLayout(QVBoxLayout())
        layout.addWidget(mainWidgetBox)
        
        mainWidgetBox.layout().addWidget(QLabel(_('Select the Destination for the Clone.'), mainWidgetBox))
        
        
        topWidgetBox = QWidget(mainWidgetBox)
        topWidgetBox.setLayout(QHBoxLayout())
        mainWidgetBox.layout().addWidget(topWidgetBox)
        
        self.tabList = QListWidget(topWidgetBox)
        self.tabList.addItems(redRObjects.tabNames())
        topWidgetBox.layout().addWidget(self.tabList)
        
        buttonWidgetBox = QWidget(mainWidgetBox)
        buttonWidgetBox.setLayout(QHBoxLayout())
        mainWidgetBox.layout().addWidget(buttonWidgetBox)
        
        acceptButton = QPushButton(_('Accept'), buttonWidgetBox)
        cancelButton = QPushButton(_('Cancel'), buttonWidgetBox)
        buttonWidgetBox.layout().addWidget(acceptButton)
        buttonWidgetBox.layout().addWidget(cancelButton)
        QObject.connect(acceptButton, SIGNAL("clicked()"), self.accept)
        QObject.connect(cancelButton, SIGNAL("clicked()"), self.reject)
class NewTabDialog(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        global _
        _ = redRi18n.get_('messages', os.path.join(redREnviron.directoryNames['redRDir'], 'languages'), languages = ['French'])
        self.setWindowTitle(_('New Tab'))
        
        self.setLayout(QVBoxLayout())
        layout = self.layout()
        mainWidgetBox = QWidget(self)
        mainWidgetBox.setLayout(QVBoxLayout())
        layout.addWidget(mainWidgetBox)
        
        mainWidgetBox.layout().addWidget(QLabel(_('New Tab Name'), mainWidgetBox))
        
        
        topWidgetBox = QWidget(mainWidgetBox)
        topWidgetBox.setLayout(QHBoxLayout())
        mainWidgetBox.layout().addWidget(topWidgetBox)
        
        self.tabName = QLineEdit(topWidgetBox)
        topWidgetBox.layout().addWidget(self.tabName)
        
        buttonWidgetBox = QWidget(mainWidgetBox)
        buttonWidgetBox.setLayout(QHBoxLayout())
        mainWidgetBox.layout().addWidget(buttonWidgetBox)
        
        acceptButton = QPushButton(_('Accept'), buttonWidgetBox)
        cancelButton = QPushButton(_('Cancel'), buttonWidgetBox)
        buttonWidgetBox.layout().addWidget(acceptButton)
        buttonWidgetBox.layout().addWidget(cancelButton)
        QObject.connect(acceptButton, SIGNAL("clicked()"), self.accept)
        QObject.connect(cancelButton, SIGNAL("clicked()"), self.reject)
class TemplateDialog(QDialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        global _
        _ = redRi18n.get_('messages', os.path.join(redREnviron.directoryNames['redRDir'], 'languages'), languages = ['French'])
        self.setWindowTitle(_('Save as template'))
        
        self.setLayout(QVBoxLayout())
        layout = self.layout()
        
        mainWidgetBox = QWidget(self)
        mainWidgetBox.setLayout(QVBoxLayout())
        layout.addWidget(mainWidgetBox)
        
        mainWidgetBox.layout().addWidget(QLabel(_('Set tags as comma ( , ) delimited list'), mainWidgetBox))
        
        
        topWidgetBox = QWidget(mainWidgetBox)
        topWidgetBox.setLayout(QHBoxLayout())
        mainWidgetBox.layout().addWidget(topWidgetBox)
        
        topWidgetBox.layout().addWidget(QLabel(_('Tags:'), topWidgetBox))
        self.tagsList = QLineEdit(topWidgetBox)
        topWidgetBox.layout().addWidget(self.tagsList)
        
        bottomWidgetBox = QWidget(mainWidgetBox)
        bottomWidgetBox.setLayout(QVBoxLayout())
        mainWidgetBox.layout().addWidget(bottomWidgetBox)
        
        bottomWidgetBox.layout().addWidget(QLabel(_('Description:'), bottomWidgetBox))
        self.descriptionEdit = QTextEdit(bottomWidgetBox)
        bottomWidgetBox.layout().addWidget(self.descriptionEdit)
        
        buttonWidgetBox = QWidget(mainWidgetBox)
        buttonWidgetBox.setLayout(QHBoxLayout())
        mainWidgetBox.layout().addWidget(buttonWidgetBox)
        
        acceptButton = QPushButton(_('Accept'), buttonWidgetBox)
        cancelButton = QPushButton(_('Cancel'), buttonWidgetBox)
        buttonWidgetBox.layout().addWidget(acceptButton)
        buttonWidgetBox.layout().addWidget(cancelButton)
        QObject.connect(acceptButton, SIGNAL("clicked()"), self.accept)
        QObject.connect(cancelButton, SIGNAL("clicked()"), self.reject)
        
from libraries.base.qtWidgets.lineEditHint import lineEditHint as redRlineEditHint
     
class SearchBox(redRlineEditHint):
    def __init__(self, widget, label=_('Search'),orientation='horizontal', items = [], toolTip = None,  width = -1, callback = None, **args):
        redRlineEditHint.__init__(self, widget = widget, label = label,displayLabel=True,
        orientation = orientation, items = items, toolTip = toolTip, width = width, callback = callback, **args)
        global _
        _ = redRi18n.get_('messages', os.path.join(redREnviron.directoryNames['redRDir'], 'languages'), languages = ['French'])
            
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
        except: return 0
class CanvasWidgetAction(QWidgetAction):
    def __init__(self, parent, actions):
        QWidgetAction.__init__(self, parent)
        global _
        _ = redRi18n.get_('messages', os.path.join(redREnviron.directoryNames['redRDir'], 'languages'), languages = ['French'])
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
    def __init__(self, parent):
        QMenu.__init__(self, parent)
        global _
        _ = redRi18n.get_('messages', os.path.join(redREnviron.directoryNames['redRDir'], 'languages'), languages = ['French'])
        self.allActions = []
        self.templateActions = []
        self.widgetActionNameList = []
        self.catActions = []
        self.quickActions = []
        self.candidates = []
        cats = redRObjects.widgetRegistry()
        self.suggestDict = {} #dict([(widget.name, widget) for widget in reduce(lambda x,y: x+y, [cat.values() for cat in cats.values()])]) ## gives an error in linux
        self.suggestItems = [QListWidgetItem(QIcon(widget.info), widget.name) for widget in self.suggestDict.values()]
        self.categoriesYOffset = 0
        self.setStyleSheet(""" QMenu { background-color: #fffff0; selection-background-color: blue; } QMenu::item:disabled { color: #dddddd } QMenu::separator {height: 1px; background: #dddddd; margin-left: 3px; margin-right: 4px;}""")   
        self.constructCategoriesPopup()
        
    def showEvent(self, ev):
        QMenu.showEvent(self, ev)
#        if self.actions() != []:
#            self.actions()[0].defaultWidget().setFocus()
        if self.actions() != []:
            self.actions()[0].defaultWidget().setFocus()
        
    def constructCategoriesPopup(self):
        mainTabs = redRObjects.widgetRegistry()['tags']
        treeXML = mainTabs.childNodes[0]
        #print treeXML.childNodes
        
        for itab in treeXML.childNodes:
            if itab.nodeName == 'group': #picked a group element
                catmenu = self.addMenu(unicode(itab.getAttribute('name')))
                self.catActions.append(catmenu) # put the catmenu in the categoriespopup
                self.insertChildActions(catmenu, self, itab)
                self.insertWidgets(catmenu, self, unicode(itab.getAttribute('name'))) 
        # print redREnviron.settings["WidgetTabs"]
        try:
            for category, show in redREnviron.settings["WidgetTabs"]:
                if not show or not redRObjects.widgetRegistry().has_key(category):
                    continue
                catmenu = self.addMenu(category)
                self.catActions.append(catmenu)
                #print self.canvas.widgetRegistry[category]
                for widgetInfo in sorted(redRObjects.widgetRegistry()[category].values(), key=lambda x:x.priority):
                    icon = QIcon(widgetInfo.icon)
                    act = catmenu.addAction(icon, widgetInfo.name)
                    
                    act.widgetInfo = widgetInfo
                    act.category = catmenu
                    #self.allActions.append(act)
        except Exception as inst:
            redRLog.log(redRLog.REDRCORE, redRLog.ERROR,redRLog.formatException())
        
        ### Add the templates to the popup, these should be actions with a function that puts a templates icon and loads the template
        for template in redRObjects.widgetRegistry()['templates']:
            try:
                icon = QIcon(os.path.join(redREnviron.directoryNames['picsDir'], 'Default.png'))
                act = catmenu.addAction(icon, template.name)
                act.templateInfo = template
                self.templateActions.append(act)
            except Exception as inst:
                redRLog.log(redRLog.REDRCORE, redRLog.ERROR,redRLog.formatException())
        #self.allActions += widgetRegistry['templates']
        ### put the actions into the hintbox here !!!!!!!!!!!!!!!!!!!!!
    def insertChildActions(self,catmenu, categoriesPopup, itab):
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
                    self.catActions.append(childTab)
                    self.insertChildActions(childTab, self, child)
                    self.insertWidgets(childTab, self, unicode(child.getAttribute('name')))
                    
        except: #subtabs don't exist
            return
    def insertWidgets(self,catmenu, categoriesPopup, catName):
        #print 'Widget Registry is \n\n' + unicode(widgetRegistry) + '\n\n'
        widgets = None
        #print unicode(self.canvas.widgetRegistry['templates'])
        try:
            for wName in redRObjects.widgetRegistry()['widgets'].keys(): ## move across all of the widgets in the widgetRegistry.  This is different from the templates that are tagged as templates
                widgetInfo = redRObjects.widgetRegistry()['widgets'][wName]
                try:
                    if unicode(catName) in widgetInfo.tags: # add the widget, wtags is the list of tags in the widget, catName is the name of the category that we are adding
                        icon = QIcon(widgetInfo.icon)
                        act = catmenu.addAction(icon, widgetInfo.name)
                        
                        act.widgetInfo = widgetInfo
                        act.category = catmenu
                        if not widgetInfo.name in self.widgetActionNameList:
                            self.allActions.append(act)
                            self.widgetActionNameList.append(widgetInfo.name)
                except Exception as inst: 
                    redRLog.log(redRLog.REDRCORE, redRLog.ERROR,redRLog.formatException())
                    pass
        except Exception as inst:
            redRLog.log(redRLog.REDRCORE, redRLog.ERROR, _('Exception in Tabs with widgetRegistry %s') % inst)
        
    
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
            


        

        
        
        
        