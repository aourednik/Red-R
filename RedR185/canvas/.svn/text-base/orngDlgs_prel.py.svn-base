# Author: Gregor Leban (gregor.leban@fri.uni-lj.si) modified by Kyle R Covington
# Description:
#    signal dialog, canvas options dialog

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from orngCanvasItems import MyCanvasText
import OWGUI, sys, os 
import RSession
import redREnviron, re, redRStyle, redRObjects
import redRLog
from libraries.base.qtWidgets.button import button as redRbutton
from libraries.base.qtWidgets.webViewBox import webViewBox as redRwebViewBox
from libraries.base.qtWidgets.listBox import listBox as redRlistBox
from libraries.base.qtWidgets.widgetLabel import widgetLabel as redRwidgetLabel
from libraries.base.qtWidgets.spinBox import spinBox as redRSpinBox
from libraries.base.qtWidgets.checkBox import checkBox as redRCheckBox
from libraries.base.qtWidgets.comboBox import comboBox as comboBox
import redRi18n

class ColorIcon(QToolButton):
    def __init__(self, parent, color):
        QToolButton.__init__(self, parent)
        self.color = color
        self.setMaximumSize(20,20)
        self.connect(self, SIGNAL("clicked()"), self.showColorDialog)
        self.updateColor()

    def updateColor(self):
        pixmap = QPixmap(16,16)
        painter = QPainter()
        painter.begin(pixmap)
        painter.setPen(QPen(self.color))
        painter.setBrush(QBrush(self.color))
        painter.drawRect(0, 0, 16, 16);
        painter.end()
        self.setIcon(QIcon(pixmap))
        self.setIconSize(QSize(16,16))


    def drawButtonLabel(self, painter):
        painter.setBrush(QBrush(self.color))
        painter.setPen(QPen(self.color))
        painter.drawRect(3, 3, self.width()-6, self.height()-6)

    def showColorDialog(self):
        color = QColorDialog.getColor(self.color, self)
        if color.isValid():
            self.color = color
            self.updateColor()
            self.repaint()

# canvas dialog
class CanvasOptionsDlg(QDialog):
    def __init__(self, canvasDlg, *args):
        apply(QDialog.__init__,(self,) + args)
        self._ = redRi18n.get_('messages', os.path.join(redREnviron.directoryNames['redRDir'], 'languages'), languages = ['French'])
        self.canvasDlg = canvasDlg
        self.settings = dict(redREnviron.settings)        # create a copy of the settings dict. in case we accept the dialog, we update the redREnviron.settings with this dict
        if sys.platform == "darwin":
            self.setWindowTitle(self._("Preferences"))
        else:
            self.setWindowTitle(self._("Canvas Options"))
        self.topLayout = QVBoxLayout(self)
        self.topLayout.setSpacing(0)
        self.resize(350,300)
        self.toAdd = []
        self.toRemove = []

        self.tabs = QTabWidget(self)
        GeneralTab = OWGUI.widgetBox(self.tabs, margin = 4)
        GeneralTab.layout().setAlignment(Qt.AlignTop)
        # lookandFeel = OWGUI.widgetBox(self.tabs, margin = 4)
        # lookandFeel.layout().setAlignment(Qt.AlignTop)
        ExceptionsTab = OWGUI.widgetBox(self.tabs, margin = 4)
        ExceptionsTab.layout().setAlignment(Qt.AlignTop)
        RSettings = OWGUI.widgetBox(self.tabs, margin = 4)
        RSettings.layout().setAlignment(Qt.AlignTop)
        
        self.tabs.addTab(GeneralTab, "General")
        # self.tabs.addTab(lookandFeel, "Look and Feel")
        self.tabs.addTab(ExceptionsTab, "Exceptions & Logging")
        self.tabs.addTab(RSettings, 'R Settings')
        QObject.connect(self.tabs, SIGNAL('currentChanged(int)'), self.onTabChange)
        #GeneralTab.layout().addStretch(1)
        
        # #################################################################
        # GENERAL TAB
        generalBox = OWGUI.widgetBox(GeneralTab, 'General Options')
        
        self.emailEdit = OWGUI.lineEdit(generalBox, self.settings, "email", "Email Address:", orientation = 'horizontal')
        
        # self.helpModeSelection = OWGUI.checkBox(generalBox,self.settings,'helpMode',
        # 'Show help icons')

        
        self.dontAskBeforeCloseCB= OWGUI.checkBox(generalBox, self.settings, "dontAskBeforeClose", 
        "Don't ask to save schema before closing", debuggingEnabled = 0)
        
        
        # #################################################################
        # LOOK AND FEEL TAB
        
        # validator = QIntValidator(self)
        # validator.setRange(0,10000)
        lookFeelBox = OWGUI.widgetBox(GeneralTab, "Look and Feel Options")

        self.snapToGridCB = OWGUI.checkBox(lookFeelBox, self.settings, "snapToGrid", 
        "Snap widgets to grid", debuggingEnabled = 0)
        self.showSignalNamesCB = OWGUI.checkBox(lookFeelBox, self.settings, "showSignalNames", 
        "Show signal names between widgets", debuggingEnabled = 0)
        self.saveWidgetsPositionCB = OWGUI.checkBox(lookFeelBox, self.settings, "saveWidgetsPosition", 
        "Save size and position of widgets", debuggingEnabled = 0)
        
        items = ["%d x %d" % (v,v) for v in redRStyle.iconSizeList]
        # val = min(len(items)-1, self.settings['schemeIconSize'])
        self.schemeIconSizeCombo = OWGUI.comboBoxWithCaption(lookFeelBox, self.settings, 'schemeIconSize', 
        "Scheme icon size:", items = items, tooltip = "Set the size of the widget icons on the scheme", 
        debuggingEnabled = 0)

        # redREnviron.settings["toolbarIconSize"] = min(len(items)-1, redREnviron.settings["toolbarIconSize"])
        
        self.toolbarIconSizeCombo = OWGUI.comboBoxWithCaption(lookFeelBox, self.settings, "toolbarIconSize", 
        "Widget Tree Icon size:", items = items, 
        tooltip = "Set the size of the widget icons in the toolbar, tool box, and tree view area", 
        debuggingEnabled = 0)

        # hbox1 = OWGUI.widgetBox(GeneralTab, orientation = "horizontal")
        
        # canvasDlgSettings = OWGUI.widgetBox(hbox1, "Canvas Dialog Settings")
        # schemeSettings = OWGUI.widgetBox(hbox1, "Scheme Settings") 
         
        # self.widthSlider = OWGUI.qwtHSlider(canvasDlgSettings, self.settings, "canvasWidth", 
        # minValue = 300, maxValue = 1200, label = "Canvas width:  ", step = 50, precision = " %.0f px", debuggingEnabled = 0)
        
        # self.heightSlider = OWGUI.qwtHSlider(canvasDlgSettings, self.settings, "canvasHeight", 
        # minValue = 300, maxValue = 1200, label = "Canvas height:  ", step = 50, precision = " %.0f px", debuggingEnabled = 0)
        
        # OWGUI.separator(canvasDlgSettings)
        

        OWGUI.comboBox(lookFeelBox, self.settings, "style", label = "Window style:", orientation = "horizontal", 
        items = redRStyle.QtStyles, sendSelectedValue = 1, debuggingEnabled = 0)
        OWGUI.checkBox(lookFeelBox, self.settings, "useDefaultPalette", "Use style's standard palette", debuggingEnabled = 0)
        
        self.language = comboBox(lookFeelBox, label = 'Language', items = [u'English', u'Fran\u00E7aise', u'Deutsch'])
        # selectedWidgetBox = OWGUI.widgetBox(schemeSettings, orientation = "horizontal")
        # self.selectedWidgetIcon = ColorIcon(selectedWidgetBox, redRStyle.widgetSelectedColor)
        # selectedWidgetBox.layout().addWidget(self.selectedWidgetIcon)
        # selectedWidgetLabel = OWGUI.widgetLabel(selectedWidgetBox, " Selected widget")

        # activeWidgetBox = OWGUI.widgetBox(schemeSettings, orientation = "horizontal")
        # self.activeWidgetIcon = ColorIcon(activeWidgetBox, redRStyle.widgetActiveColor)
        # activeWidgetBox.layout().addWidget(self.activeWidgetIcon)
        # selectedWidgetLabel = OWGUI.widgetLabel(activeWidgetBox, " Active widget")

        # activeLineBox = OWGUI.widgetBox(schemeSettings, orientation = "horizontal")
        # self.activeLineIcon = ColorIcon(activeLineBox, redRStyle.lineColor)
        # activeLineBox.layout().addWidget(self.activeLineIcon)
        # selectedWidgetLabel = OWGUI.widgetLabel(activeLineBox, " Active Lines")

        # inactiveLineBox = OWGUI.widgetBox(schemeSettings, orientation = "horizontal")
        # self.inactiveLineIcon = ColorIcon(inactiveLineBox, redRStyle.lineColor)
        # inactiveLineBox.layout().addWidget(self.inactiveLineIcon)
        # selectedWidgetLabel = OWGUI.widgetLabel(inactiveLineBox, " Inactive Lines")
        
        

        # #################################################################
        # EXCEPTION TAB
        
        debug = OWGUI.widgetBox(ExceptionsTab, "Debug")
        # self.setDebugModeCheckBox = OWGUI.checkBox(debug, self.settings, "debugMode", "Set to debug mode") # sets the debug mode of the canvas.
        
        
        self.verbosityCombo = OWGUI.comboBox(debug, self.settings, "outputVerbosity", label = "Set level of widget output: ", 
        orientation='horizontal', items=redRLog.logLevelsName)
        self.displayTraceback = OWGUI.checkBox(debug, self.settings, "displayTraceback", 'Display Traceback')
        
        # self.exceptionLevel = redRSpinBox(debug, label = 'Exception Print Level:', toolTip = 'Select the level of exception that will be printed to the Red-R general output', min = 0, max = 9, value = redREnviron.settings['exceptionLevel'])
        # self.otherLevel = redRSpinBox(debug, label = 'General Print Level:', toolTip = 'Select the level of general logging that will be output to the general output', min = 0, max = 9, value = redREnviron.settings['minSeverity'])
        
        exceptions = OWGUI.widgetBox(ExceptionsTab, "Exceptions")
        #self.catchExceptionCB = QCheckBox('Catch exceptions', exceptions)
        self.focusOnCatchExceptionCB = OWGUI.checkBox(exceptions, self.settings, "focusOnCatchException", 'Show output window on exception')
        # self.printExceptionInStatusBarCB = OWGUI.checkBox(exceptions, self.settings, "printExceptionInStatusBar", 'Print last exception in status bar')
        self.printExceptionInStatusBarCB = OWGUI.checkBox(exceptions, self.settings, "uploadError", 'Submit Error Report')
        self.printExceptionInStatusBarCB = OWGUI.checkBox(exceptions, self.settings, "askToUploadError", 'Always ask before submitting error report')

        output = OWGUI.widgetBox(ExceptionsTab, "Log File")
        #self.catchOutputCB = QCheckBox('Catch system output', output)
        self.writeLogFileCB  = OWGUI.checkBox(output, self.settings, "writeLogFile", 
        "Save content of the Output window to a log file")
        hbox = OWGUI.widgetBox(output, orientation = "horizontal")
        
        self.logFile = OWGUI.lineEdit(hbox, self.settings, "logFile", "Log File:", orientation = 'horizontal')
        self.okButton = OWGUI.button(hbox, self, "Browse", callback = self.browseLogFile)
        self.showOutputLog = redRbutton(output, label = 'Show Log File', callback = self.showLogFile)
        self.numberOfDays = redRSpinBox(output, label = 'Keep File for X days:', min = -1, value = self.settings['keepForXDays'], callback = self.numberOfDaysChanged)
        
        # self.focusOnCatchOutputCB = OWGUI.checkBox(output, self.settings, "focusOnCatchOutput", 'Focus output window on system output')
        # self.printOutputInStatusBarCB = OWGUI.checkBox(output, self.settings, "printOutputInStatusBar", 'Print last system output in status bar')

        ExceptionsTab.layout().addStretch(1)

        #####################################
        # R Settings Tab
        self.rlibrariesBox = OWGUI.widgetBox(RSettings, 'R Libraries')
        self.libInfo = redRwidgetLabel(self.rlibrariesBox, label='Repository URL: '+ self.settings['CRANrepos'])
        
        
        ################################ Global buttons  ######################
        # OK, Cancel buttons
        hbox = OWGUI.widgetBox(self, orientation = "horizontal", sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed))
        hbox.layout().addStretch(1)
        self.okButton = OWGUI.button(hbox, self, "OK", callback = self.accept)
        self.cancelButton = OWGUI.button(hbox, self, "Cancel", callback = self.reject)
        #self.connect(self.tabOrderList, SIGNAL("currentRowChanged(int)"), self.enableDisableButtons)

        self.topLayout.addWidget(self.tabs)
        self.topLayout.addWidget(hbox)
    def numberOfDaysChanged(self):
        redRLog.log(redRLog.DEBUG, redRLog.ERROR, 'changing day value to %s' % int(self.numberOfDays.value()))
        self.settings['keepForXDays'] = int(self.numberOfDays.value())
    def showLogFile(self):
        ## open a browser to show the log file.
        import webbrowser
        webbrowser.open(unicode(self.logFile.text()))
    def browseLogFile(self):
        fn = QFileDialog.getSaveFileName(self, "Save Log File", redREnviron.settings['logFile'],
        "Text file (*.html);; All Files (*.*)")
        #print unicode(fn)
        if fn.isEmpty(): return
        self.logFile.setText(fn)
        
        
    def onTabChange(self,index):
        # print 'onTabChange',index
        # get a data frame (dict) of r libraries
        if self.tabs.tabText(index) != 'R Settings':
            return
        try:
            if not self.libListBox: return
        except:
            self.libs = RSession.Rcommand('getCRANmirrors()')
            # place a listBox in the widget and fill it with a list of mirrors
            
            self.libListBox = redRlistBox(self.rlibrariesBox, label = 'Mirrors', 
            items = self.libs['Name'], callback = self.setMirror)
        
    def setMirror(self):
        # print 'setMirror'
        item = self.libListBox.currentRow()
        self.settings['CRANrepos'] = unicode(self.libs['URL'][item])
        RSession.Rcommand('local({r <- getOption("repos"); r["CRAN"] <- "' + unicode(self.libs['URL'][item]) + '"; options(repos=r)})')
        #print self.settings['CRANrepos']
        self.libInfo.setText('Repository URL changed to: '+unicode(self.libs['URL'][item]))
    def accept(self):
        # self.settings["widgetSelectedColor"] = self.selectedWidgetIcon.color.getRgb()
        # self.settings["widgetActiveColor"]   = self.activeWidgetIcon.color.getRgb()
        # self.settings["lineColor"]           = self.activeLineIcon.color.getRgb()
        
        # self.settings["exceptionLevel"] = int(self.exceptionLevel.value())
        # self.settings["minSeverity"] = int(self.otherLevel.value())
        
        # self.settings['helpMode'] = (str(self.helpModeSelection.getChecked()) in 'Show Help Icons')
        self.settings['keepForXDays'] = int(self.numberOfDays.value())
        self.settings['language'] = unicode(self.language.currentText())
        redREnviron.settings.update(self.settings)
        redREnviron.saveSettings()
        import redRLog
        redRLog.moveLogFile(redREnviron.settings['logFile'])
        # redRStyle.widgetSelectedColor = self.settings["widgetSelectedColor"]
        # redRStyle.widgetActiveColor   = self.settings["widgetActiveColor"]  
        # redRStyle.lineColor           = self.settings["lineColor"]          
        
        # update settings in widgets in current documents
        for widget in self.canvasDlg.schema.widgets():
            widget.instance()._owInfo      = redREnviron.settings["owInfo"]
            widget.instance()._owWarning   = redREnviron.settings["owWarning"]
            widget.instance()._owError     = redREnviron.settings["owError"]
            widget.instance()._owShowStatus= redREnviron.settings["owShow"]
            # widget.instance.updateStatusBarState()
            widget.resetWidgetSize()
            widget.updateWidgetState()
          
        # update tooltips for lines in all documents
        for line in self.canvasDlg.schema.lines():
            line.showSignalNames = redREnviron.settings["showSignalNames"]
            line.updateTooltip()

        redRObjects.activeTab().repaint()
        
        QDialog.accept(self)
        
        

    # move selected widget category up
    def moveUp(self):
        for i in range(1, self.tabOrderList.count()):
            if self.tabOrderList.item(i).isSelected():
                item = self.tabOrderList.takeItem(i)
                for j in range(self.tabOrderList.count()): self.tabOrderList.item(j).setSelected(0)
                self.tabOrderList.insertItem(i-1, item)
                item.setSelected(1)

    # move selected widget category down
    def moveDown(self):
        for i in range(self.tabOrderList.count()-2,-1,-1):
            if self.tabOrderList.item(i).isSelected():
                item = self.tabOrderList.takeItem(i)
                for j in range(self.tabOrderList.count()): self.tabOrderList.item(j).setSelected(0)
                self.tabOrderList.insertItem(i+1, item)
                item.setSelected(1)

    def enableDisableButtons(self, itemIndex):
        self.upButton.setEnabled(itemIndex > 0)
        self.downButton.setEnabled(itemIndex < self.tabOrderList.count()-1)
        catName = unicode(self.tabOrderList.currentItem().text())
        if not self.canvasDlg.widgetRegistry.has_key(catName): return
        self.removeButton.setEnabled(os.path.normpath(redREnviron.directoryNames['widgetDir']) not in os.path.normpath(self.canvasDlg.widgetRegistry[catName].directory))
        #self.removeButton.setEnabled(1)

    def addCategory(self):
        dir = unicode(QFileDialog.getExistingDirectory(self, "Select the folder that contains the add-on:"))
        if dir != "":
            if os.path.split(dir)[1] == "widgets":     # register a dir above the dir that contains the widget folder
                dir = os.path.split(dir)[0]
            if os.path.exists(os.path.join(dir, "widgets")):
                name = os.path.split(dir)[1]
                self.toAdd.append((name, dir))
                self.tabOrderList.addItem(name)
                self.tabOrderList.item(self.tabOrderList.count()-1).setCheckState(Qt.Checked)
            else:
                QMessageBox.information( None, "Information", 'The specified folder does not seem to contain an Orange add-on.', QMessageBox.Ok + QMessageBox.Default)
            
        
    def removeCategory(self):
        curCat = unicode(self.tabOrderList.item(self.tabOrderList.currentRow()).text())
        if QMessageBox.warning(self,'Orange Canvas', "Unregister widget category '%s' from Orange canvas?\nThis will not remove any files." % curCat, QMessageBox.Ok , QMessageBox.Cancel | QMessageBox.Default | QMessageBox.Escape) == QMessageBox.Ok:
            self.toRemove.append((curCat, self.canvasDlg.widgetRegistry[curCat].directory))
            item = self.tabOrderList.takeItem(self.tabOrderList.row(self.tabOrderList.currentItem()))
            #if item: item.setHidden(1)


class KeyEdit(QLineEdit):
    def __init__(self, parent, key, invdict, widget, invInvDict):
        QLineEdit.__init__(self, parent)
        self.setText(key)
        #self.setReadOnly(True)
        self.invdict = invdict
        self.widget = widget
        self.invInvDict = invInvDict

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Delete or e.key() == Qt.Key_Backspace:
            pressed = "<none>"
            self.setText(pressed)
            prevkey = self.invdict.get(self.widget)
            if prevkey:
                del self.invdict[self.widget]
                del self.invInvDict[prevkey]
            return

        if e.key() not in range(32, 128): # + range(Qt.Key_F1, Qt.Key_F35+1): -- this wouldn't work, see the line below, and also writing to file etc.
            e.ignore()
            return

        pressed = "-".join(filter(None, [e.modifiers() & x and y for x, y in [(Qt.ControlModifier, "Ctrl"), (Qt.AltModifier, "Alt")]]) + [chr(e.key())])

        assigned = self.invInvDict.get(pressed, None)
        if assigned and assigned != self and QMessageBox.question(self, "Confirmation", "'%(pressed)s' is already assigned to '%(assigned)s'. Override?" % {"pressed": pressed, "assigned": assigned.widget.name}, QMessageBox.Yes | QMessageBox.Default, QMessageBox.No | QMessageBox.Escape) == QMessageBox.No:
            return
        
        if assigned:
            assigned.setText("<none>")
            del self.invdict[assigned.widget]
        self.setText(pressed)
        self.invdict[self.widget] = pressed
        self.invInvDict[pressed] = self
        

# widget shortcuts dialog
class WidgetShortcutDlg(QDialog):
    def __init__(self, canvasDlg, *args):
        apply(QDialog.__init__,(self,) + args)
        self.canvasDlg = canvasDlg
        self.setWindowTitle("Widget Shortcuts")
        self.setLayout(QVBoxLayout())
        self.layout().setSpacing(10)
        self.resize(700,500)

        self.invDict = dict([(y, x) for x, y in canvasDlg.widgetShortcuts.items()])
        invInvDict = {}

        self.tabs = QTabWidget(self)
        
        extraTabs = [(name, 1) for name in canvasDlg.widgetRegistry.keys() if name not in [tab for (tab, s) in redREnviron.settings["WidgetTabs"]]]
        for tabName, show in redREnviron.settings["WidgetTabs"] + extraTabs:
            if not canvasDlg.widgetRegistry.has_key(tabName):
                continue
            scrollArea = QScrollArea()
            self.tabs.addTab(scrollArea, tabName)
            #scrollArea.setWidgetResizable(1)       # you have to use this or set size to wtab manually - otherwise nothing gets shown

            wtab = QWidget(self.tabs)
            scrollArea.setWidget(wtab)

            widgets = [(int(widgetInfo.priority), name, widgetInfo) for (name, widgetInfo) in canvasDlg.widgetRegistry[tabName].items()]
            widgets.sort()
            rows = (len(widgets)+2) / 3
            layout = QGridLayout(wtab)

            for i, (priority, name, widgetInfo) in enumerate(widgets):
                x = i / rows
                y = i % rows

                hlayout = QHBoxLayout()
                mainBox = QWidget(wtab)
                mainBox.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
                mainBox.setLayout(hlayout)
                layout.addWidget(mainBox, y, x, Qt.AlignTop | Qt.AlignLeft)
                label = QLabel(wtab)
                label.setPixmap(QIcon(widgetInfo.icon).pixmap(40))
                hlayout.addWidget(label)

                optionsw = QWidget(self)
                optionsw.setLayout(QVBoxLayout())
                hlayout.addWidget(optionsw)
                optionsw.layout().addStretch(1)

                OWGUI.widgetLabel(optionsw, name)
                key = self.invDict.get(widgetInfo, "<none>")
                le = KeyEdit(optionsw, key, self.invDict, widgetInfo, invInvDict)
                optionsw.layout().addWidget(le)
                invInvDict[key] = le
                le.setFixedWidth(60)

            wtab.resize(wtab.sizeHint())

        # OK, Cancel buttons
        hbox = OWGUI.widgetBox(self, orientation = "horizontal", sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed))
        hbox.layout().addStretch(1)
        self.okButton = OWGUI.button(hbox, self, "OK", callback = self.accept)
        self.cancelButton = OWGUI.button(hbox, self, "Cancel", callback = self.reject)
        self.okButton.setDefault(True)

        self.layout().addWidget(self.tabs)
        self.layout().addWidget(hbox)


class AboutDlg(QDialog):
    def __init__(self, *args):
        apply(QDialog.__init__,(self,) + args)
        self.topLayout = QVBoxLayout(self)
        self.setWindowFlags(Qt.Popup)
        
        logoImage = QPixmap(os.path.join(redREnviron.directoryNames["canvasDir"], "icons", "splash.png"))
        logo = redRwidgetLabel(self, "")
        logo.setPixmap(logoImage)
        info = redREnviron.version
        self.about = redRwebViewBox(self,label='About Info',displayLabel=False)
        self.about.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.about.setMinimumHeight(150)
        self.about.setHtml('<h2>' + info['NAME'] + " " + info['REDRVERSION'] + '</h2>' + 
        'Type: ' + info['TYPE'] + '; Revision: ' + info['SVNVERSION'] +
        '; Build Time: ' + info['DATE'] + '; Copy Number:' + unicode(redREnviron.settings['id']) + '' +
        '<h3>Red-R Core Development Team (<a href="http://www.red-r.org">Red-R.org</a>)</h3>')
        self.licenceButton = redRbutton(self, 'Licence', callback = self.showLicence)
        b = QDialogButtonBox(self)
        b.setCenterButtons(1)
        self.layout().addWidget(b)
        butt = b.addButton(QDialogButtonBox.Close)
        self.connect(butt, SIGNAL("clicked()"), self.accept)
    def showLicence(self):
        ## show the Red-R licence
        
        file = open(os.path.join(redREnviron.directoryNames['redRDir'], 'licence.txt'), 'r')
        text = file.read()
        file.close()
        
        self.about.setHtml('<pre>'+text+'</pre>')
        
if __name__=="__main__":
    import sys
    app = QApplication(sys.argv)
    dlg = AboutDlg(None)
    dlg.show()
    app.exec_()

