from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import string
import time as ti
from datetime import tzinfo, timedelta, datetime, time
import traceback
import os.path, os
import redREnviron, redRLog, SQLiteSession
from libraries.base.qtWidgets.button import button as redRbutton
from libraries.base.qtWidgets.checkBox import checkBox as redRcheckBox
from libraries.base.qtWidgets.widgetBox import widgetBox as redRwidgetBox
from libraries.base.qtWidgets.dialog import dialog as redRdialog
from libraries.base.qtWidgets.widgetLabel import widgetLabel as redRwidgetLabel
from libraries.base.qtWidgets.comboBox import comboBox as redRComboBox
from libraries.base.qtWidgets.radioButtons import radioButtons as redRradiobuttons
from libraries.base.qtWidgets.tabWidget import tabWidget as redRTabWidget
from libraries.base.qtWidgets.textEdit import textEdit as redRTextEdit
from libraries.base.qtWidgets.lineEdit import lineEdit as redRLineEdit

import redRi18n
# def _(a):
    # return a
_ = redRi18n.Coreget_()

class OutputWindow(QDialog):
    def __init__(self, canvasDlg, *args):
        QDialog.__init__(self, None, Qt.Window)
        self.setLayout(QVBoxLayout())
        
        self.textOutput = QTextEdit(self)
        self.textOutput.setReadOnly(1)
        self.textOutput.zoomIn(1)
        self.allOutput = ''
        self.layout().addWidget(self.textOutput)

        self.unfinishedText = ""
        
        w = h = 500
        if redREnviron.settings.has_key("outputWindowPos"):
            desktop = qApp.desktop()
            deskH = desktop.screenGeometry(desktop.primaryScreen()).height()
            deskW = desktop.screenGeometry(desktop.primaryScreen()).width()
            w, h, x, y = redREnviron.settings["outputWindowPos"]
            if x >= 0 and y >= 0 and deskH >= y+h and deskW >= x+w: 
                self.move(QPoint(x, y))
            else: 
                w = h = 500
        self.resize(w, h)
        self.lastTime = ti.time()
        self.hide()

    def outputManager(self, table, level, comment,html):
        if level >= redRLog.CRITICAL and redREnviron.settings["focusOnCatchException"] and hasattr(qApp,'canvasDlg'):
            self.showExceptionTab()
        cursor = QTextCursor(self.textOutput.textCursor())                
        cursor.movePosition(QTextCursor.End, QTextCursor.MoveAnchor)      
        self.textOutput.setTextCursor(cursor)                             
        if html:
            self.textOutput.insertHtml(comment)                                          
        else:
            self.textOutput.insertPlainText(comment)                              
            
        cursor.movePosition(QTextCursor.End, QTextCursor.MoveAnchor)      
    

    def showExceptionTab(self):
        self.hide()
        self.show()
        # self.tw.setCurrentIndex(1)
    def showEvent(self, ce):
        ce.accept()
        QDialog.showEvent(self, ce)
        settings = redREnviron.settings
        if settings.has_key("outputWindowPos"):
            w, h, x, y = settings["outputWindowPos"]
            self.move(QPoint(x, y))
            self.resize(w, h)
        
    def hideEvent(self, ce):
        redREnviron.settings["outputWindowPos"] = (self.width(), self.height(), self.pos().x(), self.pos().y())
        ce.accept()
        QDialog.hideEvent(self, ce)
                
    def closeEvent(self,ce):
        redREnviron.settings["outputWindowPos"] = (self.width(), self.height(), self.pos().x(), self.pos().y())
        # if getattr(self.canvasDlg, "canvasIsClosing", 0):
            # self.catchException(0)
            # self.catchOutput(0)
            # ce.accept()
        QDialog.closeEvent(self, ce)
        # else:
            # self.hide()

    def clear(self):
        self.textOutput.clear()

    # print text produced by warning and error widget calls
    def widgetEvents(self, text, eventVerbosity = 1):
        if redREnviron.settings["outputVerbosity"] >= eventVerbosity:
            if text != None:
                self.write(unicode(text))
            self.setStatusBarEvent(QString(text))

    # simple printing of text called by print calls
    def safe_unicode(self,obj):
        try:
            return unicode(obj)
        except UnicodeEncodeError:
            # obj is unicode
            return unicode(obj).encode('unicode_escape')

    def getSafeString(self, s):
        return unicode(s).replace("<", "&lt;").replace(">", "&gt;")

    def uploadYes(self):
        self.msg.done(1)

    def uploadNo(self):
        self.msg.done(0)
    def rememberResponse(self):
        if _('Remember my Response') in self.remember.getChecked():
            self.checked = True
            redREnviron.settings['askToUploadError'] = 0

        else:
            self.checked = False
        
    def uploadException(self,err):
        try:
            import httplib,urllib
            import sys,pickle,os, re
            #print redREnviron.settings['askToUploadError'], 'askToUploadError'
            #print redREnviron.settings['uploadError'], 'uploadError'
            if not redREnviron.settings['askToUploadError']:
                res = redREnviron.settings['uploadError']
            else:
                self.msg = redRdialog(parent=self,title='Red-R Error')
                
                error = redRwidgetBox(self.msg,orientation='vertical')
                redRwidgetLabel(error, label='Do you wish to report the Error Log?')
                buttons = redRwidgetBox(error,orientation='horizontal')

                redRbutton(buttons, label = _('Yes'), callback = self.uploadYes)
                redRbutton(buttons, label = _('No'), callback = self.uploadNo)
                self.checked = False
                self.remember = redRcheckBox(error,buttons=[_('Remember my Response')],callback=self.rememberResponse)
                res = self.msg.exec_()
                redREnviron.settings['uploadError'] = res
            #print res
            if res == 1:
                #print 'in res'
                err['version'] = redREnviron.version['SVNVERSION']
                err['type'] = redREnviron.version['TYPE']
                err['redRversion'] = redREnviron.version['REDRVERSION']
                #print err['traceback']
                
                
                ##err['output'] = self.allOutput
                if os.name == 'nt':
                    err['os'] = 'Windows'
                # else:
                    # err['os'] = 'Not Specified'
                if redREnviron.settings['canContact']:
                    err['email'] = redREnviron.settings['email']
                # else:
                    # err['email'] = 'None; no contact'
                #err['id'] = redREnviron.settings['id']
                #print err, 'Error'
                params = urllib.urlencode(err)
                headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
                conn = httplib.HTTPConnection("localhost",80)
                conn.request("POST", "/errorReport.php", params,headers)
                
            else:
                return
        except: 
            redRLog.log(redRLog.REDRCORE, redRLog.ERROR, redRLog.formatException())
            pass
    
    """
    def exceptionHandler(self, type, value, tracebackInfo):
        print 'Exception Occured, please see the output for more details.\n'
        if redREnviron.settings["focusOnCatchException"]:
            self.canvasDlg.menuItemShowOutputWindow()

        text = self.formatException(type,value,tracebackInfo)
        
        
        t = datetime.today().isoformat(' ')
        toUpload = {}
        #toUpload['time'] = t
        toUpload['errorType'] = self.getSafeString(type.__name__)
        toUpload['traceback'] = text
        #toUpload['file'] = os.path.split(traceback.extract_tb(tracebackInfo, 10)[0][0])[1]
        
        if redREnviron.settings["printExceptionInStatusBar"]:
            self.setStatusBarEvent("Unhandled exception of type %s occured at %s. See output window for details." % ( unicode(type) , t))

        
        cursor = QTextCursor(self.exceptionText.textCursor())                # clear the current text selection so that
        cursor.movePosition(QTextCursor.End, QTextCursor.MoveAnchor)      # the text will be appended to the end of the
        self.exceptionText.setTextCursor(cursor)                             # existing text
        self.exceptionText.insertHtml(text)                                  # then append the text
        cursor = QTextCursor(self.exceptionText.textCursor())                # clear the current text selection so that
        cursor.movePosition(QTextCursor.End, QTextCursor.MoveAnchor)      # the text will be appended to the end of the
        self.exceptionText.setTextCursor(cursor)
        
        if redREnviron.settings["writeLogFile"]:
            self.logFile.write(unicode(text) + "<br>\n")
        
        self.uploadException(toUpload)
"""
        
