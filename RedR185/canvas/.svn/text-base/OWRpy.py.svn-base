#
# An Orange-Rpy class
# 
# Should include all the functionally need to connect Orange to R 
#

from redRWidgetGUI import *
from widgetSignals import *
from widgetSession import *
from PyQt4.QtGui import *
import RSession, redREnviron, os, redRReports,redRLog
#import rpy
from libraries.base.qtWidgets.graphicsView import graphicsView as redRgraphicsView
from libraries.base.qtWidgets.widgetBox import widgetBox as redRwidgetBox
from libraries.base.qtWidgets.button import button as redRButton
from libraries.base.qtWidgets.spinBox import spinBox as redRSpinBox
from libraries.base.qtWidgets.lineEdit import lineEdit as redRLineEdit
from libraries.base.qtWidgets.textEdit import textEdit as redRTextEdit
from libraries.base.qtWidgets.separator import separator as redRSeparator
from libraries.base.qtWidgets.filterTable import filterTable as redRFilterTable
from libraries.base.qtWidgets.radioButtons import radioButtons as redRRadioButtons
from libraries.base.qtWidgets.listBox import listBox as redRListBox
from libraries.base.qtWidgets.widgetBox import widgetBox as redRWidgetBox
from libraries.base.qtWidgets.checkBox import checkBox as redRCheckBox
from libraries.base.qtWidgets.commitButton import commitButton as redRCommitButton
from libraries.base.qtWidgets.comboBox import comboBox as redRComboBox
from libraries.base.qtWidgets.groupBox import groupBox as redRGroupBox
from libraries.base.qtWidgets.splitter import splitter as redRSplitter
from libraries.base.qtWidgets.statusLabel import statusLabel as redRStatusLabel

import redRi18n
# def _(a):
    # return a
_ = redRi18n.Coreget_()
class OWRpy(widgetSignals,redRWidgetGUI,widgetSession):   
    uniqueWidgetNumber = 0
    globalRHistory = []
    def __init__(self,wantGUIDialog = 0):
        
        widgetSignals.__init__(self, None, None)
        self.dontSaveList = self.__dict__.keys()
        #print self.dontSaveList

        redRWidgetGUI.__init__(self, parent=None, signalManager=None, title=None, wantGUIDialog=wantGUIDialog)
        self.dontSaveList = self.__dict__.keys()
        for x in ['status','notes','ROutput','widgetState']: self.dontSaveList.remove(x)
        
        widgetSession.__init__(self,self.dontSaveList)
        
        self.saveSettingsList = []  # a list of lists or strings that we will save.
        OWRpy.uniqueWidgetNumber += 1
        ctime = unicode(time.time())
        self.sessionID = 0  # a unique ID for the session.  This is not saved or reset when the widget is loaded.  Rather this added when the widget is loaded.  This allows for multiple widgets to use the same 
        self.widgetID = unicode(OWRpy.uniqueWidgetNumber) + '_' + ctime
        self.variable_suffix = '_' + self.widgetID
        self.Rvariables = {}
        self.RvariablesNames = []
        self.setRvariableNames(['title'])
        self.requiredRLibraries = []
        self.device = {}
        self.packagesLoaded = 0
        self.widgetRHistory = []
        self.reportOrder = None
        self.tempID = None
        

    def log(level,comment):
        redRLog.log(redRLog.REDRWIDGET,level,comment,widget=self.widgetID)
        
    def resetRvariableNames(self, id = None):
        if id:
            self.widgetID = id
            self.variable_suffix = '_' + self.widgetID
        for x in self.RvariablesNames:
            self.Rvariables[x] = x + self.variable_suffix
    def setRvariableNames(self,names):
        
        #names.append('loadSavedSession')
        for x in names:
            self.Rvariables[x] = x + self.variable_suffix
            self.RvariablesNames.append(x)
            
    def makeCM(self, Variable):
        self.R(Variable+'<-list()', wantType = 'NoConversion')
    def addToCM(self, colname = 'tmepColname', CM = None, values = None):
        if CM == None: return
        if values == None: return
        if type(values) == type([]):
            values = 'c('+','.join(values)+')'
        self.R(CM+'$'+colname+self.variable_suffix+'<-'+values, wantType = 'NoConversion') # commit to R

    def R(self, query, callType = 'getRData', processingNotice=False, silent = False, showException=True, wantType = 'convert', listOfLists = True):
        
        self.setRIndicator(True)
        #try:
        if processingNotice:
            self.status.setStatus(4)
            
        qApp.setOverrideCursor(Qt.WaitCursor)
        try:
            commandOutput = RSession.Rcommand(query = query, silent = silent, wantType = wantType, listOfLists = listOfLists)
        except RuntimeError as inst:
            #print _('asdfasdfasdf'), inst
            redRLog.log(redRLog.REDRCORE, redRLog.ERROR, redRLog.formatException())
            qApp.restoreOverrideCursor()
            self.setRIndicator(False)
            if showException:
                QMessageBox.information(self, _('Red-R Canvas'),_('R Error: ')+ unicode(inst),  
                QMessageBox.Ok + QMessageBox.Default)
            
            raise RuntimeError(unicode(inst))
            return None # now processes can catch potential errors
        
        #except: 
        #    print _('R exception occurred')
        self.processing = False
        if processingNotice:
            self.status.setStatus(5)
            

            #self.progressBarFinished()
        if not silent:
            OWRpy.globalRHistory.append(query)
            self.widgetRHistory.append(query)
            
            self.ROutput.setCursorToEnd()
            self.ROutput.append('> '+ query) #Keep track automatically of what R functions were performed.
    
        qApp.restoreOverrideCursor()
        self.setRIndicator(False)
        return commandOutput
   
    def assignR(self, name, object):
        assignOK = RSession.assign(name, object)
        if not assignOK:
            QMessageBox.information(self, _('Red-R Canvas'),_('Object was not assigned correctly in R, please tell package manager.'),  
            QMessageBox.Ok + QMessageBox.Default)
            raise Exception, _('Object was not assigned correctly in R, please tell package manager.')
        else:
            histquery = _('Assign ')+unicode(name)+_(' to ')+unicode(object)
            OWRpy.globalRHistory.append(histquery)
            self.widgetRHistory.append(histquery)

            self.ROutput.setCursorToEnd()
            self.ROutput.append('> '+ histquery)

    def savePDF(self, query, dwidth= 7, dheight = 7, file = None):
        #print unicode(redREnviron.settings)
        if file == None and ('HomeFolder' not in redREnviron.settings.keys()):
            file = QFileDialog.getSaveFileName(self, "Save File", os.path.abspath(redREnviron.settings['saveSchemaDir']), "PDF (*.PDF)")
        elif file == None: 
            file = QFileDialog.getSaveFileName(self, "Save File", os.path.abspath(redREnviron.settings['HomeFolder']), "PDF (*.PDF)")
        if file.isEmpty(): return
        file = unicode(file)

        if file: redREnviron.settings['HomeFolder'] = os.path.split(file)[0]
        self.R('pdf(file = "'+file+'", width = '+unicode(dwidth)+', height = '+unicode(dheight)+')')
        self.R(query, 'setRData')
        self.R('dev.off()')
        self.status.setText('File saved as \"'+file+'\"')
        self.notes.setCursorToEnd()
        self.notes.insertHtml('<br> Image saved to: '+unicode(file)+'<br>')
    
    def Rplot(self, command, dwidth=6, dheight=6, devNumber = 0, imageType = 'svg'):
        ## reformat the query for plotting, separate the function from the parameters.
        function = command[:command.find('(')]
        query = command[command.find('(')+1:command.rfind(')')]
        if unicode(devNumber) in self.device:
            self.device[unicode(devNumber)].plot(query = query, function = function, dwidth = dwidth, dheight = dheight)
        else:
            if 'plottingArea' not in dir(self):
                self.plottingArea = redRwidgetBox(self.controlArea, orientation = 'horizontal')
            self.device[unicode(devNumber)] = redRgraphicsView(self.plottingArea, name = self.captionTitle)
            self.device[unicode(devNumber)].plot(query = query, function = function, dwidth = dwidth, dheight = dheight)
            
        return
        
    def getReportText2(self, fileDir):
        ## move through all of the qtWidgets in self and show their report outputs, should be implimented by each widget.
        children = self.controlArea.children()
        #print children
        import re
        text = ''
        for i in children:
            try:
                #print i.__class__.__name__
                if isinstance(i, QBoxLayout):
                    c = i.children()
                    for c1 in c:
                        text += c1.getReportText(fileDir)
                elif re.search('PyQt4|OWGUIEx|OWToolbars',unicode(type(i))) or i.__class__.__name__ in redRGUI.qtWidgets:
                    ## we can try to get the settings of this.
                    text += i.getReportText(fileDir)
                    #print i.__class__.__name__
            except Exception as inst:
                redRLog.log(redRLog.REDRCORE, redRLog.ERROR, inst)
                continue
        return text
    def getReportText3(self, fileDir):
        ## move through all of the qtWidgets in self and show their report outputs, 
        ## should be implimented by each widget.
        from redRGUI import qtWidgetBox
        children = self.controlArea.children() + self.bottomAreaRight.children() + self.bottomAreaCenter.children() + self.bottomAreaLeft.children()
        # print 'OWRpy= ',children
        #import re
        reportData = {}
        for i in children:
            if isinstance(i, qtWidgetBox):
                d = i.getReportText(fileDir)
                if type(d) is dict:
                    reportData.update(d)
                # dd = []
                # if type(d) is list:
                    # for x in d:
                        # x['includeInReports'] = i.includeInReports
                        # dd.append(x)
                    # reportData = reportData + dd
                # elif d:
                    # d['includeInReports'] = i.includeInReports
                    # reportData.append(d)
        
        return reportData

        # arrayOfArray = []
        # for d in reportData:
            # if type(d) is dict:
                # arrayOfArray.append([d['label'], d['text']])
            # elif type(d) is list:
                # for x in d:
                    # arrayOfArray.append([x['label'], x['text']])
                    
        # import pprint
        # pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(arrayOfArray)
        # text = redRReports.createTable(arrayOfArray,columnNames = [_('Parameter'),_('Value')],
        # tableName=_('Parameters'))
        # return text        

    def require_librarys(self, librarys, repository = None):
        qApp.setOverrideCursor(Qt.WaitCursor)
        if not repository and 'CRANrepos' in redREnviron.settings.keys():
            repository = redREnviron.settings['CRANrepos']
        
        #print _('Loading required librarys')
        success = RSession.require_librarys(librarys = librarys, repository = repository)
        self.requiredRLibraries.extend(librarys)
        qApp.restoreOverrideCursor()
        return success
    def onDeleteWidget(self):
        #print '|#| onDeleteWidget OWRpy'

        for k in self.Rvariables:
            #print self.Rvariables[k]
            self.R('if(exists("' + self.Rvariables[k] + '")) { rm(' + self.Rvariables[k] + ') }', wantType = 'NoConversion')
        # send none through the signals
        self.outputs.propogateNone(ask = False)
        self.outputs.clearAll()
        self.customWidgetDelete()
        # if self.outputs:
            # for output in self.outputs:
                # self.callSignalDelete(output[0])

    def customWidgetDelete(self):
        pass #holder function for other widgets

    def reloadWidget(self):
        pass
    def sendRefresh(self):
        self.signalManager.refresh()
            
    def refresh(self):
        pass # function that listens for a refresh signal.  This function should be overloaded in widgets that need to listen.


###########################################
