# modifications by Kyle R Covington and Anup Parikh#
# OWWidget.py
# Orange Widget
# A General Orange Widget, from which all the Orange Widgets are derived
#

# import redRGUI 
from libraries.base.qtWidgets.textEdit import textEdit as redRtextEdit
from libraries.base.qtWidgets.button import button as redRbutton
from libraries.base.qtWidgets.groupBox import groupBox as redRgroupBox
from libraries.base.qtWidgets.widgetLabel import widgetLabel as redRwidgetLabel
from libraries.base.qtWidgets.widgetBox import widgetBox as redRwidgetBox
from libraries.base.qtWidgets.statusLabel import statusLabel as redRStatusLabel
from PyQt4 import QtWebKit
import urllib, os, redREnviron
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import redRStyle
from datetime import date
import redRi18n
# def _(a):
    # return a
_ = redRi18n.Coreget_()
class redRWidgetGUI(QMainWindow):
    def __new__(cls, *arg, **args):
        self = QMainWindow.__new__(cls)
        
        #print "arg", arg
        #print "args: ", args
        self.currentContexts = {}   # the "currentContexts" MUST be the first thing assigned to a widget
        self._useContexts = 1       # do you want to use contexts
        self._owInfo = 1            # currently disabled !!!
        self._owWarning = 1         # do we want to see warnings
        self._owError = 1           # do we want to see errors
        self._owShowStatus = 0      # do we want to see warnings and errors in status bar area of the widget
        self._guiElements = []      # used for automatic widget debugging

        
        for key in args:
            if key in ["_owInfo", "_owWarning", "_owError", "_owShowStatus", "_useContexts", "_packageName"]:
                self.__dict__[key] = args[key]        # we cannot use __dict__.update(args) since we can have many other

        return self

    def __init__(self, parent=None, signalManager=None, title=_("Generic Red-R Widget"), 
    savePosition=True, wantGUIDialog = 0, resizingEnabled=1, **args):
        """
        Initialization
        Parameters:
            title - The title of the\ widget, including a "&" (for shortcut in about box)
            wantGraph - displays a save graph button or not
        """

        # if resizingEnabled: 
        QMainWindow.__init__(self, parent, Qt.Window)
        # else:               
        #QMainWindow.__init__(self, parent, Qt.Dialog | Qt.MSWindowsFixedSizeDialogHint)# | Qt.WindowMinimizeButtonHint)

        # directories are better defined this way, otherwise .ini files get written in many places
        #self.__dict__.update(redREnviron.directoryNames)

        # self.setCaption(title.replace("&","")) # used for widget caption

        self.captionTitle = self._widgetInfo.widgetName
        self.progressBarHandler = None  # handler for progress bar events
        self.processingHandler = None   # handler for processing events


        self.widgetStateHandler = None
        self.widgetState = {"Info":{}, "Warning":{}, "Error":{}}

        self.windowState = {}
        self.savePosition = True
        self.hasBeenShown = False
        self.hasAdvancedOptions = wantGUIDialog
        self.setLayout(QVBoxLayout())
        self.layout().setMargin(2)
        self.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum)
        topWidgetPart = redRwidgetBox(self, orientation="vertical", margin=0)
        topWidgetPart.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum)
        self.setCentralWidget(topWidgetPart)
        self.controlArea = redRwidgetBox(topWidgetPart, orientation="vertical", margin=4)
        self.controlArea.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.controlArea.setMinimumWidth(300)
        # topWidgetPart.layout().setAlignment(self.controlArea,Qt.AlignTop | Qt.AlignLeft)

        bottomArea = redRwidgetBox(topWidgetPart, orientation="horizontal", margin=4)
        self.bottomAreaLeft = redRwidgetBox(bottomArea, orientation = 'horizontal')
        self.bottomAreaCenter = redRwidgetBox(bottomArea, sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed),
        orientation = 'horizontal')
        self.bottomAreaRight = redRwidgetBox(bottomArea, orientation = 'horizontal')
        #start widget GUI
        
        
        ### status bar ###
        self.statusBar = QStatusBar()
        self.statusBar.setLayout(QHBoxLayout())
        self.statusBar.setSizeGripEnabled(False)
        
        self.setStatusBar(self.statusBar)
        
        self.RIndicator = redRwidgetLabel(self.statusBar)
        self.statusBar.addWidget(self.RIndicator)
        self.setRIndicator(False)
        
        
        
        self.status = redRStatusLabel(self.statusBar, '')
        self.status.setStatus(0)
        self.status.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.statusBar.addPermanentWidget(self.status,4)
        #self.statusBar.setStyleSheet("QStatusBar { border-top: 2px solid gray; } ")
        # self.statusBar.setStyleSheet("QLabel { border-top: 2px solid red; } ")

        ################
        # Notes Dock ###
        ################
        minWidth = 200
        self.notesDock=QDockWidget(_('Notes'))
        self.notesDock.setObjectName('widgetNotes')
        
        QObject.connect(self.notesDock,SIGNAL('topLevelChanged(bool)'),self.updateDock)
        
        self.notesDock.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)
        self.notesDock.setMinimumWidth(minWidth)
        self.notesDock.setAllowedAreas(Qt.RightDockWidgetArea | Qt.TopDockWidgetArea | Qt.BottomDockWidgetArea)
        self.addDockWidget(Qt.RightDockWidgetArea,self.notesDock)

        self.notesBox = redRwidgetBox(None,orientation=QVBoxLayout())
        self.notesDock.setWidget(self.notesBox)
        
        self.notesBox.setMinimumWidth(minWidth)
        self.notesBox.setMinimumHeight(50)
        self.notesBox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        redRwidgetLabel(self.notesBox, label="Notes:", icon=redRStyle.notesIcon)

        self.notes = redRtextEdit(self.notesBox, label = _('Notes'), displayLabel=False)
        self.notes.setMinimumWidth(minWidth)
        self.notes.setMinimumHeight(50)
        self.notes.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        
        
        ################
        # R output ###
        ################
        self.RoutputDock=QDockWidget(_('R Output'))
        self.RoutputDock.setObjectName('RoutputDock')
        
        QObject.connect(self.RoutputDock,SIGNAL('topLevelChanged(bool)'),self.updateDock)
        
        self.RoutputDock.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)
        self.RoutputDock.setMinimumWidth(minWidth)
        self.RoutputDock.setAllowedAreas(Qt.RightDockWidgetArea | Qt.TopDockWidgetArea | Qt.BottomDockWidgetArea)
        
        self.addDockWidget(Qt.RightDockWidgetArea,self.RoutputDock)

        self.ROutputBox = redRwidgetBox(None,orientation=QVBoxLayout())
        self.RoutputDock.setWidget(self.ROutputBox)

        self.ROutputBox.setMinimumHeight(50)
        redRwidgetLabel(self.ROutputBox, label=_("R code executed in this widget:"),
        icon=redRStyle.RIcon)

        self.ROutput = redRtextEdit(self.ROutputBox, label = _('R Output'),displayLabel=False)
        self.ROutput.setMinimumWidth(minWidth)
        self.ROutput.setMinimumHeight(50)
        self.ROutput.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        redRbutton(self.ROutputBox, label = _('Run Selected Code'), callback = self._runSelectedRCode, toolTip = _('You may select any code to execute in the R session.  This will override anything that other widgets have done to this point and will be overriden when this widget executes again.  Use this with great caution.'))
        
        ### help ####
        self.helpFile = None
        
        if hasattr(self,'_widgetInfo'):
            (file,ext) = os.path.basename(self._widgetInfo.fullName).split('.')
            path = os.path.join(redREnviron.directoryNames['libraryDir'],
            self._widgetInfo.package['Name'],'help',file+'.html')
            if os.path.exists(path):
                self.helpFile = path
        if not self.helpFile:
            self.helpFile = 'http://www.red-r.org/documentation'

                
        
        
        ################
        # Status Bar ###
        ################
        
        self.windowState['documentationState'] = {'notesBox':True,'ROutputBox':False}

        docBox = redRwidgetBox(self.controlArea,orientation='horizontal',spacing=4)
        
        self.showNotesButton = redRbutton(docBox, '',toggleButton=True, 
        icon=os.path.join(redREnviron.directoryNames['picsDir'], 'Notes-icon.png'),
        toolTip=_('Notes'),
        callback = self.updateDocumentationDock)
        self.showROutputButton = redRbutton(docBox, '',toggleButton=True, 
        icon=os.path.join(redREnviron.directoryNames['picsDir'], 'R_icon.png'),
        toolTip=_('R Code'),
        callback = self.updateDocumentationDock)
        
        self.printButton = redRbutton(docBox, "",
        icon=os.path.join(redREnviron.directoryNames['picsDir'], 'printer_icon.png'),
        toolTip=_('Print'),
        callback = self.createReport)

        self.showHelpButton = redRbutton(docBox, '',
        icon=os.path.join(redREnviron.directoryNames['picsDir'], 'help_icon.png'),
        toolTip=_('Help'),
        callback = self.showHelp)

        self.includeInReport = redRbutton(docBox, '', 
        icon=os.path.join(redREnviron.directoryNames['picsDir'], 'report_icon.png'),
        toolTip=_('Include In Report'), toggleButton = True)
        self.includeInReport.setChecked(True)
        
        ###############################################
        self.statusBar.addPermanentWidget(docBox)
        # self.statusBar.addPermanentWidget(self.showNotesButton)
        # self.statusBar.addPermanentWidget(self.showROutputButton)
        # self.statusBar.addPermanentWidget(self.showHelpButton)        
        # self.statusBar.addPermanentWidget(self.printButton)
        # self.statusBar.addPermanentWidget(self.includeInReport)
        
        
        self.GUIDialogDialog = None
        self.windowState['leftDockState'] = False
        if self.hasAdvancedOptions:
            self.leftDock=QDockWidget(_('Advanced Options'))
            self.leftDock.setObjectName('leftDock')
            self.connect(self.leftDock,SIGNAL('topLevelChanged(bool)'),self.updateDock)
            self.leftDock.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)
            self.leftDock.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
            self.addDockWidget(Qt.LeftDockWidgetArea,self.leftDock)
            self.GUIDialog = redRwidgetBox(self.leftDock,orientation='vertical')
            self.GUIDialog.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
            self.leftDock.setWidget(self.GUIDialog)
            self.leftDockButton = redRbutton(self.bottomAreaLeft, _('Advanced Options'),toggleButton=True, callback = self.showLeftDock)
            self.statusBar.insertPermanentWidget(2,self.leftDockButton)
            self.windowState['leftDockState'] = True
  
        # print '|#| end init of redRWidgetGUI %s' % unicode(self.windowState)
        
    # uncomment this when you need to see which events occured
    """
    def event(self, e):
        #eventDict = dict([(0, 'None'), (1, 'Timer'), (2, 'MouseButtonPress'), (3, 'MouseButtonRelease'), (4, 'MouseButtonDblClick'), (5, 'MouseMove'), (6, 'KeyPress'), (7, 'KeyRelease'), (8, 'FocusIn'), (9, 'FocusOut'), (10, 'Enter'), (11, 'Leave'), (12, 'Paint'), (13, 'Move'), (14, 'Resize'), (15, 'Create'), (16, 'Destroy'), (17, 'Show'), (18, 'Hide'), (19, 'Close'), (20, 'Quit'), (21, 'Reparent'), (22, 'ShowMinimized'), (23, 'ShowNormal'), (24, 'WindowActivate'), (25, 'WindowDeactivate'), (26, 'ShowToParent'), (27, 'HideToParent'), (28, 'ShowMaximized'), (30, 'Accel'), (31, 'Wheel'), (32, 'AccelAvailable'), (33, 'CaptionChange'), (34, 'IconChange'), (35, 'ParentFontChange'), (36, 'ApplicationFontChange'), (37, 'ParentPaletteChange'), (38, 'ApplicationPaletteChange'), (40, 'Clipboard'), (42, 'Speech'), (50, 'SockAct'), (51, 'AccelOverride'), (60, 'DragEnter'), (61, 'DragMove'), (62, 'DragLeave'), (63, 'Drop'), (64, 'DragResponse'), (70, 'ChildInserted'), (71, 'ChildRemoved'), (72, 'LayoutHint'), (73, 'ShowWindowRequest'), (80, 'ActivateControl'), (81, 'DeactivateControl'), (1000, 'User')])
        eventDict = dict([(0, "None"), (130, "AccessibilityDescription"), (119, "AccessibilityHelp"), (86, "AccessibilityPrepare"), (114, "ActionAdded"), (113, "ActionChanged"), (115, "ActionRemoved"), (99, "ActivationChange"), (121, "ApplicationActivated"), (122, "ApplicationDeactivated"), (36, "ApplicationFontChange"), (37, "ApplicationLayoutDirectionChange"), (38, "ApplicationPaletteChange"), (35, "ApplicationWindowIconChange"), (68, "ChildAdded"), (69, "ChildPolished"), (71, "ChildRemoved"), (40, "Clipboard"), (19, "Close"), (82, "ContextMenu"), (52, "DeferredDelete"), (60, "DragEnter"), (62, "DragLeave"), (61, "DragMove"), (63, "Drop"), (98, "EnabledChange"), (10, "Enter"), (150, "EnterEditFocus"), (124, "EnterWhatsThisMode"), (116, "FileOpen"), (8, "FocusIn"), (9, "FocusOut"), (97, "FontChange"), (159, "GraphicsSceneContextMenu"), (164, "GraphicsSceneDragEnter"), (166, "GraphicsSceneDragLeave"), (165, "GraphicsSceneDragMove"), (167, "GraphicsSceneDrop"), (163, "GraphicsSceneHelp"), (160, "GraphicsSceneHoverEnter"), (162, "GraphicsSceneHoverLeave"), (161, "GraphicsSceneHoverMove"), (158, "GraphicsSceneMouseDoubleClick"), (155, "GraphicsSceneMouseMove"), (156, "GraphicsSceneMousePress"), (157, "GraphicsSceneMouseRelease"), (168, "GraphicsSceneWheel"), (18, "Hide"), (27, "HideToParent"), (127, "HoverEnter"), (128, "HoverLeave"), (129, "HoverMove"), (96, "IconDrag"), (101, "IconTextChange"), (83, "InputMethod"), (6, "KeyPress"), (7, "KeyRelease"), (89, "LanguageChange"), (90, "LayoutDirectionChange"), (76, "LayoutRequest"), (11, "Leave"), (151, "LeaveEditFocus"), (125, "LeaveWhatsThisMode"), (88, "LocaleChange"), (153, "MenubarUpdated"), (43, "MetaCall"), (102, "ModifiedChange"), (4, "MouseButtonDblClick"), (2, "MouseButtonPress"), (3, "MouseButtonRelease"), (5, "MouseMove"), (109, "MouseTrackingChange"), (13, "Move"), (12, "Paint"), (39, "PaletteChange"), (131, "ParentAboutToChange"), (21, "ParentChange"), (75, "Polish"), (74, "PolishRequest"), (123, "QueryWhatsThis"), (14, "Resize"), (117, "Shortcut"), (51, "ShortcutOverride"), (17, "Show"), (26, "ShowToParent"), (50, "SockAct"), (112, "StatusTip"), (100, "StyleChange"), (87, "TabletMove"), (92, "TabletPress"), (93, "TabletRelease"), (171, "TabletEnterProximity"), (172, "TabletLeaveProximity"), (1, "Timer"), (120, "ToolBarChange"), (110, "ToolTip"), (78, "UpdateLater"), (77, "UpdateRequest"), (111, "WhatsThis"), (118, "WhatsThisClicked"), (31, "Wheel"), (132, "WinEventAct"), (24, "WindowActivate"), (103, "WindowBlocked"), (25, "WindowDeactivate"), (34, "WindowIconChange"), (105, "WindowStateChange"), (33, "WindowTitleChange"), (104, "WindowUnblocked"), (126, "ZOrderChange"), (169, "KeyboardLayoutChange"), (170, "DynamicPropertyChange")])
        if eventDict.has_key(e.type()):
            print unicode(self.windowTitle()), eventDict[e.type()]
        return QMainWindow.event(self, e)
    """
    def _runSelectedRCode(self):
        code = unicode(self.ROutput.textCursor().selectedText())
        self.R(code, wantType = 'NoConversion')
    def setRIndicator(self,isActive):
        
        if isActive:
            self.RIndicator.setPixmap(QPixmap(os.path.join(redREnviron.directoryNames['canvasIconsDir'],'redLight.png')))
            self.RIndicator.setToolTip(_('R is currently running. Please wait...'))
        else:
            self.RIndicator.setPixmap(QPixmap(os.path.join(redREnviron.directoryNames['canvasIconsDir'],'greenLight.png')))
            self.RIndicator.setToolTip(_('R is idle.'))
        qApp.processEvents()
        # self.RStateIdle = QIcon(os.path.join(redREnviron.directoryNames['canvasIconsDir'],'Green_Light.gif'))
        # self.RStateRunning = QIcon(os.path.join(redREnviron.directoryNames['canvasIconsDir'],'Red_Light.gif'))

    def showHelp(self):
        if self.helpFile:
            import webbrowser
            webbrowser.open_new_tab(self.helpFile)

        
    def createReport(self, printer = None):
        
        
        qApp.canvasDlg.reports.createReportsMenu(
        [canvasWidget(caption=self._widgetInfo.widgetName, instance=self)],schemaImage=False)
        
        
    

    def updateDock(self,ev):
        #print self.windowTitle()
        if self.notesDock.isFloating():
            self.notesDock.setWindowTitle(self.windowTitle() + _(' Notes'))
        else:
            self.notesDock.setWindowTitle(_('Notes'))
            
        if self.RoutputDock.isFloating():
            self.RoutputDock.setWindowTitle(self.windowTitle() + _(' R Output'))
        else:
            self.RoutputDock.setWindowTitle(_('R Output'))
            
        if hasattr(self, "leftDock"): 
            if self.leftDock.isFloating():
                self.leftDock.setWindowTitle(self.windowTitle() + _(' Advanced Options'))
            else:
                self.leftDock.setWindowTitle(_('Advanced Options'))

    
    def showLeftDock(self):
        #print _('in updatedock left'), self.leftDockButton.isChecked()
        
        if self.leftDockButton.isChecked():
            self.leftDock.show()
            self.windowState['leftDockState'] = True
        else:
            self.leftDock.hide()
            self.windowState['leftDockState'] = False
            
    def updateDocumentationDock(self):
        #print _('in updatedock right')
        if 'documentationState' not in self.windowState.keys():
            self.windowState['documentationState'] = {}
        
        
        if self.showNotesButton.isChecked():
            self.notesDock.show()
            self.windowState['documentationState']['notesBox'] = True
        else:
            self.notesDock.hide()
            self.windowState['documentationState']['notesBox'] = False

        if self.showROutputButton.isChecked():
            self.RoutputDock.show()
            self.windowState['documentationState']['ROutputBox'] = True
        else:
            self.RoutputDock.hide()
            self.windowState['documentationState']['ROutputBox'] = False
        
        # if True in self.windowState['documentationState'].values():
            # self.rightDock.show()
        # else:
            # self.rightDock.hide()
        

    def saveWidgetWindowState(self):
        self.windowState["geometry"] = self.saveGeometry()
        self.windowState["state"] = self.saveState()
        self.windowState['pos'] = self.pos()
        self.windowState['size'] = self.size()
        
    def closeEvent(self, event):
        #print _('in owrpy closeEvent')
        if self.notesDock.isFloating():
            self.notesDock.hide()
        if self.RoutputDock.isFloating():
            self.RoutputDock.hide()
            
        if hasattr(self, "leftDock") and self.leftDock.isFloating():
            self.leftDock.hide()
        
        for i in self.findChildren(QDialog):
            i.setHidden(True)
        
        if self.hasBeenShown and not self.isHidden():
            self.saveWidgetWindowState()
        self.saveGlobalSettings()
        self.customCloseEvent()

        
    def customCloseEvent(self):
        pass

    # when widget is resized, save new width and height into widgetWidth and widgetHeight. some widgets can put this two
    # variables into settings and last widget shape is restored after restart
    def resizeEvent(self, ev):
        QMainWindow.resizeEvent(self, ev)
        self.saveWidgetWindowState()
        # print ev

    # when widget is moved, save new x and y position into widgetXPosition and widgetYPosition. some widgets can put this two
    # variables into settings and last widget position is restored after restart
    def moveEvent(self, ev):
        QMainWindow.moveEvent(self, ev)
        # print ev.type()
        self.saveWidgetWindowState()



    # override the default show function.
    # after show() we must call processEvents because show puts some LayoutRequests in queue
    # and we must process them immediately otherwise the width(), height(), ... of elements in the widget will be wrong
    def show(self):
        
        # print _('owbasewidget show')
        #print '|#| in onShow'
        # print self.windowState
        self.hasBeenShown = True
        if 'state' in self.windowState.keys():
            self.restoreState(self.windowState['state'])
        if 'geometry' in self.windowState.keys():
            self.restoreGeometry(self.windowState['geometry'])
       
        if 'size' in self.windowState.keys():
            self.resize(self.windowState['size'])
        if 'pos' in self.windowState.keys():
            self.move(self.windowState['pos'])

        
        if self.hasAdvancedOptions and ('leftDockState' in self.windowState):
            try:
                self.leftDockButton.setChecked(self.windowState['leftDockState'])
                self.showLeftDock()
            except:
                redRLog.log(redRLog.REDRCORE, redRLog.ERROR, redRLog.formatException())
                self.hasAdvancedOptions = False
        
        if 'documentationState' in self.windowState.keys():
            self.showNotesButton.setChecked(self.windowState['documentationState']['notesBox'])
            self.showROutputButton.setChecked(self.windowState['documentationState']['ROutputBox'])
        self.updateDocumentationDock()
        
        self.hide()
        QMainWindow.show(self)
        qApp.processEvents()


    def setWidgetWindowIcon(self, iconName):
        #print '|#| setWidgetIcon redRWidgetGUI'
        icon = QIcon(iconName)
        self.setWindowIcon(icon)
        


    # def setCaption(self, caption):
        # if self.parent != None and isinstance(self.parent, QTabWidget):
            # self.parent.setTabText(self.parent.indexOf(self), caption)
        # else:
        # self.captionTitle = caption     # we have to save caption title in case progressbar will change it
        # self.setWindowTitle(caption)

    def setWidgetStateHandler(self, handler):
        self.widgetStateHandler = handler

    def setInformation(self, id = 0, text = None):
        self.setState("Info", id, text)
        #self.setState("Warning", id, text)

    def setWarning(self, id = 0, text = ""):
        self.setState("Warning", id, text)
        #self.setState("Info", id, text)        # if we want warning just set information

    def setError(self, id = 0, text = ""):
        self.setState("Error", id, text)
    
    def removeInformation(self,id=None):
        if id == None:
            #print '|#| remove information'
            self.setState("Info", self.widgetState['Info'].keys())
        else:
            self.setState("Info", id)
    
    def removeWarning(self,id=None):
        if id == None:
            self.setState("Warning", self.widgetState['Warning'].keys())
        else:
            self.setState("Warning", id)
            
    def removeError(self,id=None):
        if id == None:
            self.setState("Error", self.widgetState['Error'].keys())
        else:
            self.setState("Error", id)
            
    def setState(self, stateType, id, text =None):
        changed = 0
        if type(id) == list:
            for val in id:
                if self.widgetState[stateType].has_key(val):
                    self.widgetState[stateType].pop(val)
                    #print '|#| pop %s' % unicode(val)
                    changed = 1
        else:
            #if type(id) == str:
                #text = id; id = 0       # if we call information(), warning(), or error() function with only one parameter - a string - then set id = 0
            if not text:
                if self.widgetState[stateType].has_key(id):
                    self.widgetState[stateType].pop(id)
                    changed = 1
            else:
                self.widgetState[stateType][id] = text
                changed = 1

        if changed:
            if self.widgetStateHandler:
                self.widgetStateHandler()
            # elif text: # and stateType != "Info":
                # self.printEvent(stateType + " - " + text)
            #qApp.processEvents()
        return changed

    def openWidgetHelp(self):

        try:
            import webbrowser
            url = 'http://www.red-r.org/help.php?widget=' + os.path.basename(self._widgetInfo.fullName)
            webbrowser.open(url, 0, 1)
            return
        except:
            redRLog.log(redRLog.REDRCORE, redRLog.ERROR, redRLog.formatException())
            pass

        # try:
            # import webbrowser
            # webbrowser.open("http://www.ailab.si/orange/doc/widgets/catalog/%s/%s.htm" % (self._category, self.__class__.__name__[2:]))
            # return
        # except:
            # pass
    
    def keyPressEvent(self, e):
        if e.key() in (Qt.Key_Help, Qt.Key_F1):
            self.openWidgetHelp()
#            e.ignore()
        else:
            QMainWindow.keyPressEvent(self, e)

    def focusInEvent(self, *ev):
        #print "focus in"
        #if qApp.canvasDlg.settings["synchronizeHelp"]:  on ubuntu: pops up help window on first widget focus for every widget   
        #    qApp.canvasDlg.helpWindow.showHelpFor(self, True)
        QMainWindow.focusInEvent(self, *ev)
        
    # ############################################
    # PROGRESS BAR FUNCTIONS
    def progressBarInit(self):
        self.progressBarValue = 0
        # self.startTime = time.time()
        # self.setWindowTitle(self.captionTitle + " (0% complete)")
        if self.progressBarHandler:
            self.progressBarHandler(self, 0)

    def progressBarSet(self, value):
        self.progressBarValue = value
        if self.progressBarHandler: self.progressBarHandler(self, value)
        qApp.processEvents()

    def progressBarAdvance(self, value):
        self.progressBarSet(self.progressBarValue+value)

    def progressBarFinished(self):
        # self.setWindowTitle(self.captionTitle)
        if self.progressBarHandler: self.progressBarHandler(self, 101)

    # handler must be a function, that receives 2 arguments. First is the widget instance, the second is the value between -1 and 101
    def setProgressBarHandler(self, handler):
        self.progressBarHandler = handler

    def setProcessingHandler(self, handler):
        self.processingHandler = handler
        


class canvasWidget:
    def __init__(self, **attrs):
        self.__dict__.update(attrs)


# if __name__ == "__main__":
    # a = QApplication(sys.argv)
    # ow = OWWidget()
    # ow.show()
    # a.exec_()
    # ow.saveGlobalSettings()
