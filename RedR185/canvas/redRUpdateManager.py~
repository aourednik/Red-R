from libraries.base.qtWidgets.dialog import dialog as redRdialog
from libraries.base.qtWidgets.treeWidgetItem import treeWidgetItem as redRtreeWidgetItem
from libraries.base.qtWidgets.button import button as redRbutton
from libraries.base.qtWidgets.textEdit import textEdit as redRtextEdit
from libraries.base.qtWidgets.tabWidget import tabWidget as redRtabWidget
from libraries.base.qtWidgets.treeWidget import treeWidget as redRtreeWidget
from libraries.base.qtWidgets.widgetBox import widgetBox as redRwidgetBox
from libraries.base.qtWidgets.webViewBox import webViewBox as redRwebViewBox

## package manager class redRPackageManager.  Contains a dlg for the package manager which reads xml from the red-r.org website and compares it with a local package system on the computer

import os, sys, redREnviron, urllib2, zipfile, traceback
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtNetwork import *
import xml.dom.minidom
import redRGUI, re , redRLog
import xml.etree.ElementTree as etree
from datetime import date
import win32api, win32process
from win32com.shell import shell, shellcon
import redRi18n
# def _(a):
    # return a
_ = redRi18n.Coreget_()
class updateManager():
    def __init__(self,schema):
        self.schema = schema
        #self.urlOpener = urllib2.FancyURLopener()
        self.version = redREnviron.version['REDRVERSION']
        self.repository = 'http://www.red-r.org/redr_updates/Red-R-' + self.version
            
        
    def checkForUpdate(self):
        print 'checkForUpdate'
        file = os.path.join(redREnviron.directoryNames['canvasSettingsDir'],'red-RUpdates.xml')
        f = urllib2.urlopen(self.repository +'/currentVersion.xml')
        output = open(file,'wb')
        output.write(f.read())
        output.close()
        
        #self.downloadFile(self.repository +'/currentVersion.xml', file)
        
        self.availableUpdate = self.parseUpdatesXML(file)
        if (self.availableUpdate['redRVerion'] == self.version 
        and self.availableUpdate['SVNVersion'] > redREnviron.version['SVNVERSION']):
            return True
        else: return False
    
    def showUpdateDialog(self,auto=False):
        if not redREnviron.checkInternetConnection():
            if not auto:
              self.createDialog(_('No Internet Connection'),False)
            return

        today = date.today()
        if redREnviron.settings['checkedForUpdates'] != 0:
            diff =  today - redREnviron.settings['checkedForUpdates']
            if int(diff.days) < 2 and auto:
                return
                
        redREnviron.settings['checkedForUpdates'] = today
        redREnviron.saveSettings()
        avaliable = self.checkForUpdate()
        if avaliable:
            html = _("<h2>Red-R %s</h2><h4>Revision:%s; Date: %s</h4><br>%s") % (
            self.availableUpdate['redRVerion'],self.availableUpdate['SVNVersion'],
            self.availableUpdate['date'],self.availableUpdate['changeLog']) 
            self.createDialog(html,True)
        elif not avaliable and not auto:
            self.createDialog(_('You have the most current version of Red-R %s.') % self.version,False)

    def parseUpdatesXML(self,fileName):
        f = open(fileName, 'r')
        updatesXML = xml.dom.minidom.parse(f)
        f.close()
        # updatesXML = xml.dom.minidom.parseString(xml)
        update = {}
        update['redRVerion'] = self.getXMLText(updatesXML.getElementsByTagName('redRVerion')[0].childNodes)
        update['SVNVersion'] = self.getXMLText(updatesXML.getElementsByTagName('SVNVersion')[0].childNodes)
        update['date'] = self.getXMLText(updatesXML.getElementsByTagName('date')[0].childNodes)
        update['changeLog'] = self.getXMLText(updatesXML.getElementsByTagName('changeLog')[0].childNodes)
        update['compiledFileName'] = self.getXMLText(updatesXML.getElementsByTagName('compiledFileName')[0].childNodes)
        update['developerFileName'] = self.getXMLText(updatesXML.getElementsByTagName('developerFileName')[0].childNodes)
        return update

    def getXMLText(self, nodelist):
        rc = ''
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                rc = rc + node.data
                
        rc = str(rc).strip()
        return rc

    def createDialog(self,html,avaliable):
        UpdatePopup = redRdialog(self.schema, title = _('Update Manager'))
        
        changeLogBox = redRwebViewBox(UpdatePopup,label=_('Update'),displayLabel=False)
        changeLogBox.setMinimumWidth(350)
        changeLogBox.setMinimumHeight(350)
        changeLogBox.setHtml(html)
        
        buttonArea2 = redRwidgetBox(UpdatePopup,orientation = 'horizontal', 
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed),alignment=Qt.AlignRight)
        if avaliable:
            redRbutton(buttonArea2, label = _('Close Red-R and Update'), callback = UpdatePopup.accept)
        redRbutton(buttonArea2, label = _('Cancel'), callback = UpdatePopup.reject)
        if UpdatePopup.exec_() == QDialog.Accepted:
            self.downloadUpdate(update)
        
    def showNoUpdates(self):
        UpdatePopup = redRdialog(self.schema, title = _('Update Manager'))
        UpdatePopup.setMinimumWidth(350)
        UpdatePopup.setMinimumHeight(350)
        changeLogBox = redRwebViewBox(UpdatePopup)
        changeLogBox.setHtml(_('You have the most current version of Red-R %s.') % self.version)
        
        buttonArea2 = redRwidgetBox(UpdatePopup,orientation = 'horizontal', 
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed),alignment=Qt.AlignRight)
        
        redRbutton(buttonArea2, label = _('Done'), callback = UpdatePopup.reject)
        UpdatePopup.exec_()    
    def showNoInternet(self):
        UpdatePopup = redRdialog(self.schema, title = _('Update Manager'))
        UpdatePopup.setMinimumWidth(350)
        UpdatePopup.setMinimumHeight(350)
        changeLogBox = redRwebViewBox(UpdatePopup)
        changeLogBox.setHtml(_('No Internet Connection.'))
        
        buttonArea2 = redRwidgetBox(UpdatePopup,orientation = 'horizontal', 
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed),alignment=Qt.AlignRight)
        
        redRbutton(buttonArea2, label = _('Done'), callback = UpdatePopup.reject)
        UpdatePopup.exec_()
    def showUpdateAvaliable(self,update):
        UpdatePopup = redRdialog(self.schema, title = _('Update Manager'))
        
        changeLogBox = redRwebViewBox(UpdatePopup)
        changeLogBox.setMinimumWidth(350)
        changeLogBox.setMinimumHeight(350)
        html = _("<h2>Red-R %s</h2><h4>Revision:%s; Date: %s</h4>") % (
        update['redRVerion'],update['SVNVersion'],update['date']) 

        changeLogBox.setHtml(html +'<br>' +update['changeLog'])
        
        buttonArea2 = redRwidgetBox(UpdatePopup,orientation = 'horizontal', 
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed),alignment=Qt.AlignRight)
        
        redRbutton(buttonArea2, label = 'Close Red-R and Update', callback = UpdatePopup.accept)
        redRbutton(buttonArea2, label = _('Cancel'), callback = UpdatePopup.reject)
        if UpdatePopup.exec_() == QDialog.Accepted:
            self.downloadUpdate(update)
        
    def downloadUpdate(self,update):
        if redREnviron.version['TYPE'] =='compiled':
            url = update['compiledFileName']
            file = os.path.join(redREnviron.directoryNames['downloadsDir'],
            os.path.basename(update['compiledFileName']))
        else:
            url = update['developerFileName']
            file = os.path.join(redREnviron.directoryNames['downloadsDir'],
            os.path.basename(update['developerFileName']))
        
        # self.execUpdate(file)
        # return
        print url, file
        self.progressBar = QProgressDialog(self.schema)
        self.progressBar.setCancelButtonText(QString())
        self.progressBar.setWindowTitle('Downloading...')
        self.progressBar.setLabelText('Downloading...')
        self.progressBar.setMaximum(100)
        i = 0
        self.progressBar.setValue(i)
        self.progressBar.show()
        self.manager = QNetworkAccessManager(self.schema)
        reply = self.manager.get(QNetworkRequest(QUrl(url)))
        
        self.manager.connect(reply,SIGNAL("downloadProgress(qint64,qint64)"), self.updateProgress)
        
        self.manager.connect(self.manager,SIGNAL("finished(QNetworkReply*)"),
        lambda reply: self.replyFinished(reply, file,self.closeAndUpdate))
        # self.downloadFile(url,file,finishedFun=self.closeAndUpdate, progressFun=self.updateProgress)
    
    def updateProgress(self, read,total):
        self.progressBar.setValue(round((float(read) / float(total))*100))
        qApp.processEvents()
       
    def execUpdate(self,file):
        installDir = os.path.split(os.path.abspath(redREnviron.directoryNames['redRDir']))[0]
        # print installDir
        cmd = "%s /D=%s" % (file,installDir)
        try:
            shell.ShellExecuteEx(shellcon.SEE_MASK_NOCLOSEPROCESS,0,'open',file,"/D=%s" % installDir,
            redREnviron.directoryNames['downloadsDir'],0)
            # win32process.CreateProcess('Red-R update',cmd,'','','','','','','')
        except:
            
            redRLog.log(redRLog.REDRCORE, redRLog.ERROR,redRLog.formatException())
            mb = QMessageBox(_("Error"), _("There was an Error in updating Red-R."), 
                QMessageBox.Information, QMessageBox.Ok | QMessageBox.Default, 
                QMessageBox.NoButton, QMessageBox.NoButton, self.schema)
            mb.exec_()
            return
        # print _('asdfasdfa')
        
    def closeAndUpdate(self,file):
        qApp.canvasDlg.closeEvent(QCloseEvent(),postCloseFun=lambda:self.execUpdate(file))
        
    # def downloadFile(self,url,file,finishedFun=None, progressFun=None):    
        # self.manager = QNetworkAccessManager(self.schema)
        # reply = self.manager.get(QNetworkRequest(QUrl(url)))
        
        # if progressFun:
            # self.manager.connect(reply,SIGNAL("downloadProgress(qint64,qint64)"), progressFun)
        
        # self.manager.connect(self.manager,SIGNAL("finished(QNetworkReply*)"),
        # lambda reply: self.replyFinished(reply, file,finishedFun))
    def replyFinished(self, reply,file,finishedFun):
        self.reply = reply
        output = open(file,'wb')
        alltext = self.reply.readAll()
        output.write(alltext)
        output.close()
        if finishedFun:
            finishedFun(file)


