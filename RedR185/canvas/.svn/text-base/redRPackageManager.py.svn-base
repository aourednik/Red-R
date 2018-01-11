from libraries.base.qtWidgets.dialog import dialog as redRdialog
from libraries.base.qtWidgets.treeWidgetItem import treeWidgetItem as redRtreeWidgetItem
from libraries.base.qtWidgets.button import button as redRbutton
from libraries.base.qtWidgets.textEdit import textEdit as redRtextEdit
from libraries.base.qtWidgets.tabWidget import tabWidget as redRtabWidget
from libraries.base.qtWidgets.treeWidget import treeWidget as redRtreeWidget
from libraries.base.qtWidgets.widgetBox import widgetBox as redRwidgetBox
## package manager class redRPackageManager.  Contains a dlg for the package manager which reads xml from the red-r.org website and compares it with a local package system on the computer

import os, sys, redREnviron, urllib, zipfile, traceback, redRLog
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import xml.dom.minidom
import redRGUI, re 
import pprint
import xml.etree.ElementTree as etree
import redRi18n
# def _(a):
    # return a
_ = redRi18n.Coreget_()

## packageManager class handles package functions such as resolving rrp's resolving dependencies, appending packages to the package xml or any function that remotely has to do with handling packages
class packageManager:
    def __init__(self):
        self.urlOpener = urllib.FancyURLopener()
        self.repository = 'http://www.red-r.org/repository/Red-R-' + redREnviron.version['REDRVERSION'] 
        self.version = redREnviron.version['REDRVERSION']
        (self.updatePackages, self.localPackages, self.sitePackages) = self.getPackages()
        
    def resolveRDependencies(self, packageList):
        import RSession
        packageList = [x.strip() for x in packageList]
        RSession.require_librarys(packageList)

    def installRRP(self,packageName,filename):

        installDir = os.path.join(redREnviron.directoryNames['libraryDir'], packageName)
        #print _('installDir'), installDir
        import shutil
        import compileall
        shutil.rmtree(installDir, ignore_errors = True)  ## remove the old dir for copying
        
        os.mkdir(installDir) ## make the directory to store the zipfile into
        zfile = zipfile.ZipFile(filename, "r" )
        zfile.extractall(installDir)
        zfile.close()
        compileall.compile_dir(installDir) # compile the directory for later importing.
        ## now process the requires for R
        
        pack = self.readXML(os.path.join(installDir, 'package.xml'))
        if pack.getElementsByTagName('RLibraries'):
            Rpacks = self.getXMLText(pack.getElementsByTagName('RLibraries')[0].childNodes)
            self.resolveRDependencies(Rpacks.split(','))
            
        
    # read and parse the package xml file
    # return dict
    def getPackageInfo(self,filename):
        zfile = zipfile.ZipFile(filename, "r" )
        f = zfile.open('package.xml')
        xmlStr = f.read()
        f.close()
        packageXML = xml.dom.minidom.parseString(xmlStr)
        package = self.parsePackageXML(packageXML)
        return package
    # take a dict with package name as key and value a dict containing key 'installed' 
    # if value of 'installed' key is true do nothing and return else install 
    def downloadPackages(self,packages,window=None):
        if not redREnviron.checkInternetConnection():
            return False
        if not window:
            window  = qApp.canvasDlg
        progressBar = QProgressDialog(window)
        progressBar.setCancelButtonText(QString())
        progressBar.setWindowTitle(_('Installing Packages'))
        progressBar.setLabelText(_('Installing Packages ...'))
        progressBar.setMaximum(len(packages.keys())+1)
        i = 0
        progressBar.setValue(i)
        progressBar.show()
        OK = True
        for package,status in packages.items():
            if status['installed']: continue
            if not package in self.sitePackages: continue
            i = i + 1
            progressBar.setValue(i)
            progressBar.setLabelText(_('Installing: %s') % package)
            try:
                packageName = unicode(package+'-'+self.sitePackages[package]['Version']['Number']+'.zip')
                url = unicode(self.repository+'/'+package+'/'+packageName)
                path = os.path.join(redREnviron.directoryNames['downloadsDir'], unicode(packageName))
                #print url
                self.urlOpener.retrieve(url, path)
                #print path
                self.installRRP(package,path)
                redRLog.log(redRLog.REDRCORE, redRLog.INFO, _('Installing package %(PACKAGENAME)s from URL %(URL)s into path %(PATH)s') % {'PACKAGENAME':packageName, 'URL':url, 'PATH':path})
            except:
                redRLog.log(redRLog.REDRCORE, redRLog.ERROR, redRLog.formatException())
                try:
                    packageName = unicode(package+'-'+self.sitePackages[package]['Version']['Number']+'.zip')
                    url = unicode(self.repository+'/'+package+'/'+packageName)
                    path = os.path.join(redREnviron.directoryNames['downloadsDir'], unicode(packageName))
                    #print url
                    self.urlOpener.retrieve(url, path)
                    #print path
                    self.installRRP(package,path)
                except:
                    redRLog.log(redRLog.REDRCORE, redRLog.ERROR,redRLog.formatException())
                    OK=False
        qApp.canvasDlg.reloadWidgets()
        progressBar.hide()
        return OK

    # take a dict with package name as key and value a dict containing key 'installed' 
    # return a a dict with the same structure including all the required packages
    def getDependencies(self,packages):
        # print 'in getDependencies', packages
        deps = {}
        for name, package in packages.items():
            if (name in self.sitePackages.keys() and len(self.sitePackages[name]['Dependencies'])):
                for dep in self.sitePackages[name]['Dependencies']:
                    if (dep in self.localPackages.keys()): 
                        installed=True
                    else:
                        installed=False
                    t = {}
                    t[dep] = {'Version':self.sitePackages[dep]['Version']['Number'], 'installed':installed}
                    deps.update(t)
                    deps.update(self.getDependencies(t))

        return deps
    
    # takes an xml node and returns the text 
    def getXMLText(self, nodelist):
        rc = ''
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                rc = rc + node.data
                
        rc = unicode(rc).strip()
        return rc
    # takes a xml file name and returns an xml object
    def readXML(self, fileName):
        f = open(fileName, 'r')
        #print fileName
        mainTabs = xml.dom.minidom.parse(f)
        f.close()
        return mainTabs

    # takes an xml object representing a red-r package and creates a structured dict
    # TO-DO: should perform error checking to make sure the xml file is valid
    def parsePackageXML(self,node):
        packageDict = {}
        packageDict['Name'] = self.getXMLText(node.getElementsByTagName('Name')[0].childNodes)
        packageDict['Author'] = self.getXMLText(node.getElementsByTagName('Author')[0].childNodes)
        packageDict['License'] = self.getXMLText(node.getElementsByTagName('License')[0].childNodes)
        
        deps = self.getXMLText(node.getElementsByTagName('Dependencies')[0].childNodes)
        if (deps.lower() == 'none' or deps.lower() == 'base' or deps.lower() == ''):
            packageDict['Dependencies'] = []
        else:
            packageDict['Dependencies'] = deps.split(',')
            
        packageDict['Summary'] = self.getXMLText(node.getElementsByTagName('Summary')[0].childNodes)
        packageDict['Description'] = self.getXMLText(node.getElementsByTagName('Description')[0].childNodes)

        version = node.getElementsByTagName('Version')[0]
        # print node, version
        packageDict['Version'] = {}
        packageDict['Version']['Number'] = self.getXMLText(version.getElementsByTagName('Number')[0].childNodes)
        packageDict['Version']['Stability'] = self.getXMLText(version.getElementsByTagName('Stability')[0].childNodes)
        packageDict['Version']['Date'] = self.getXMLText(version.getElementsByTagName('Date')[0].childNodes)

        return packageDict
     
    ## moves through the local package file and returns a dict of packages with version, stability, update date, etc
    def getInstalledPackages(self):
        packageDict = {}
        for package in os.listdir(redREnviron.directoryNames['libraryDir']): 
            if not (os.path.isdir(os.path.join(redREnviron.directoryNames['libraryDir'], package)) 
            and os.path.isfile(os.path.join(redREnviron.directoryNames['libraryDir'],package,'package.xml'))):
                continue
    
            packageXML = self.readXML(os.path.join(redREnviron.directoryNames['libraryDir'],package,'package.xml'))
            
            packageDict[package] = self.parsePackageXML(packageXML)
            
        
        # pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(packageDict)
        return packageDict
        
    # downloads the packages.xml file from repository
    # The file is stored in the canvasSettingsDir/red-RPackages.xml
    def updatePackagesFromRepository(self):
        #print '|#| updatePackagesFromRepository'
        redRLog.log(redRLog.REDRCORE, redRLog.INFO, _('Updating packages from repository'))
        url = self.repository + '/packages.xml'
        file = os.path.join(redREnviron.directoryNames['canvasSettingsDir'],'red-RPackages.xml')
        from datetime import date
        redREnviron.settings['red-RPackagesUpdated'] = today = date.today()
        #print url, file
        self.urlOpener.retrieve(url, file)
    
    # runs through all the installed packages and creates red-RPackages.xml file
    # The file is stored in the canvasSettingsDir until overwritten by updatePackagesFromRepository function
    def createAvailablePackagesXML(self):
        xml = '<packages>'
        for package in os.listdir(redREnviron.directoryNames['libraryDir']): 
            if (os.path.isdir(os.path.join(redREnviron.directoryNames['libraryDir'], package)) 
            and os.path.isfile(os.path.join(redREnviron.directoryNames['libraryDir'],package,'package.xml'))):
                f = open(os.path.join(redREnviron.directoryNames['libraryDir'],package,'package.xml'),'r')
                xml = xml + '\n' + f.read()
                f.close()
        
        f = open(os.path.join(redREnviron.directoryNames['canvasSettingsDir'],'red-RPackages.xml'),'w')
        f.write(xml + '\n</packages>')
        f.close()

    ## moves through the local package file and returns a dict of packages with version, stability, update date, etc
    def getAvailablePackages(self):
        file = os.path.join(redREnviron.directoryNames['canvasSettingsDir'],'red-RPackages.xml')
        if not os.path.isfile(file):
            self.createAvailablePackagesXML()
        packages = self.readXML(file)
        if packages == None: 
            self.createAvailablePackagesXML()
        
        packageDict = {}
        for package in packages.firstChild.childNodes:
            if package.nodeType !=package.ELEMENT_NODE:
                continue
            p = self.parsePackageXML(package)
            packageDict[p['Name']] =  p
        
        # pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(packageDict)        
        return packageDict
        
    ## returns a tuple of dicts (packages needed updates, installed packages, and packages available on the repository)
    def getPackages(self):
        self.localPackages = self.getInstalledPackages()
        self.sitePackages = self.getAvailablePackages()
        if self.sitePackages == None:
            return (None, self.localPackages, None)
        
        self.updatePackages = {}
        
        ## loop through the package names and see what should be upgraded.
        for name,localPackage in self.localPackages.items():
            # this package must not be on Red-R.org any more.
            if name not in self.sitePackages.keys():
                continue
            else:
                remotePackage = self.sitePackages[name]

            if localPackage['Version']['Number'] != remotePackage['Version']['Number']:
                self.updatePackages[name] = {}
                self.updatePackages[name]['new'] = remotePackage
                self.updatePackages[name]['current'] = localPackage

        # pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(self.updatePackages)        

        return (self.updatePackages, self.localPackages, self.sitePackages)
        
class packageManagerDialog(redRdialog):
    def __init__(self,widget):
        redRdialog.__init__(self,widget, title = _('Package Manager'))
        
        self.setMinimumWidth(650)
        self.packageManager = packageManager
        
        ## GUI ##
        #### set up a screen that will show a listbox of packages that are on the system that should be updated, 
        
        self.tabsArea = redRtabWidget(self)
        self.updatesTab = self.tabsArea.createTabPage(name = _('Updates'))
        self.installedTab = self.tabsArea.createTabPage(name = _('Installed Packages'))
        self.availableTab = self.tabsArea.createTabPage(name = _('Available Packages'))
        
        #### layout of the tabsArea
        self.treeViewUpdates = redRtreeWidget(self.updatesTab, label=_('Update List'), displayLabel=False, 
        callback = self.updateItemClicked)  ## holds the tree view of all of the packages that need updating
        self.treeViewUpdates.setHeaderLabels([_('Package'), _('Author'), _('Summary'), 
        _('Current Version'), _('Current Version Stability'), _('New Version'), _('New Version Stability')])

        #self.treeViewUpdates.setSelectionModel(QItemSelectModel.Rows)
        self.treeViewUpdates.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.infoViewUpdates = redRtextEdit(self.updatesTab, label=_('Update Info'), displayLabel=False)  ## holds the info for a package
        redRbutton(self.updatesTab, _('Install Updates'), callback = self.installUpdates)
        
        self.treeViewInstalled = redRtreeWidget(self.installedTab, label=_('Update List'), displayLabel=False, 
        callback = self.installItemClicked)
        self.treeViewInstalled.setHeaderLabels([_('Package'), _('Author'), _('Summary'), _('Version'), _('Stability')])

        #self.treeViewInstalled.setSelectionModel(QItemSelectModel.Rows)
        self.treeViewInstalled.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.infoViewInstalled = redRtextEdit(self.installedTab, label=_('Install Info'), displayLabel=False)
        redRbutton(self.installedTab, _('Remove Packages'), callback = self.uninstallPackages)
        
        self.treeViewAvailable = redRtreeWidget(self.availableTab, label=_('Update List'), displayLabel=False, 
        callback = self.availableItemClicked)
        self.treeViewAvailable.setHeaderLabels([_('Package'), _('Author'), _('Summary'), _('Version'), _('Stability')])

        #self.treeViewAvailable.setSelectionModel(QItemSelectModel.Rows)
        self.treeViewAvailable.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.infoViewAvailable = redRtextEdit(self.availableTab, label=_('Avaliable Info'), displayLabel=False)
        redRbutton(self.availableTab, _('Install Packages'), callback = self.installNewPackage)
        
        #### buttons and the like
        buttonArea2 = redRwidgetBox(self,orientation = 'horizontal')
        redRbutton(buttonArea2, label = _('Update from Repository'), callback = self.loadPackagesLists)
        redRwidgetBox(buttonArea2, sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed),
        orientation = 'horizontal')
        redRbutton(buttonArea2, label = _('Done'), callback = self.accept)
    def installItemClicked(self, item1, item2):
        if item1:
            self.infoViewInstalled.setHtml(self.localPackages[unicode(item1.text(0))]['Description'])
    def updateItemClicked(self, item1, item2):
        if item1:
            self.infoViewUpdates.setHtml(self.availablePackages[unicode(item1.text(0))]['Description'])
    def availableItemClicked(self, item1, item2):
        if item1:
            self.infoViewAvailable.setHtml(self.availablePackages[unicode(item1.text(0))]['Description'])
    #### get the pakcages that are on Red-R.org  we ask before we do this and record the xml so we only have to get it once.
    def loadPackagesLists(self,force=True):
        if force:
            self.packageManager.updatePackagesFromRepository()
            self.tabsArea.setCurrentIndex(2)

            ask=False
        elif self.packageManager.sitePackages == None or redREnviron.settings['red-RPackagesUpdated'] == 0:
            ask=True
        else:
            from datetime import date
            today = date.today()
            diff =  today - redREnviron.settings['red-RPackagesUpdated']
            if int(diff.days) > 10: ask=True
            else: ask=False
        
        if ask and redREnviron.checkInternetConnection():
                if self.isHidden:
                    parent = qApp.canvasDlg
                else:
                    parent = self
                mb = QMessageBox("Update Package Repository", "Update package repository for Red-R.org?", 
                QMessageBox.Information, QMessageBox.Ok | QMessageBox.Default, 
                QMessageBox.No | QMessageBox.Escape, QMessageBox.NoButton, parent)
                if mb.exec_() == QMessageBox.Ok:
                    self.packageManager.updatePackagesFromRepository()
                    self.tabsArea.setCurrentIndex(2)
            
        (self.updates, self.localPackages, self.availablePackages) = self.packageManager.getPackages()

        self.updatesTab.setEnabled(True)
        self.availableTab.setEnabled(True)
        self.setUpdates(self.updates)
        self.setPackageList(self.treeViewInstalled, self.localPackages)
        self.setPackageList(self.treeViewAvailable, self.availablePackages)
        
    def show(self):
        redRdialog.show(self)
        self.loadPackagesLists(force=False)
    def exec_(self):
        self.loadPackagesLists(force=False)
        redRdialog.exec_(self)
        
    def setUpdates(self, packages):
        self.treeViewUpdates.clear()
        if not packages:
            return 
        
        for name,package in packages.items(): ## move across the package names
            current = package['current']
            new = package['new']
            
            line = [name, current['Author'], current['Summary'], 
            current['Version']['Number'], current['Version']['Stability'],
            new['Version']['Number'], new['Version']['Stability']]

            newChild = redRtreeWidgetItem(self.treeViewUpdates, line)
            
                
    def setPackageList(self, view, packages):
        ## there is something in the dict and we need to populate the treeview
        view.clear()
        if not packages:
            return 
        for name,package in packages.items(): ## move across the package names
            line = [name, package['Author'], package['Summary'], 
            package['Version']['Number'], package['Version']['Stability']]
            newChild = redRtreeWidgetItem(view, line)
            
                    
    def installUpdates(self):
        ### move through the selected items in the updates page, get the RRP locations and install the rrp's for the packages.
        selectedItems = self.treeViewUpdates.selectedItems()
        if len(selectedItems) ==0: return
        ### make the download list
        downloadList = {}
        for item in selectedItems:  
            name = unicode(item.text(0))
            downloadList[name] = {'Version':unicode(item.text(5)), 'installed':False}
        # print downloadList
        self.askToInstall(downloadList,"Are you sure that you want to update these packages?")
                
    def uninstallPackages(self):
        ## collect the packages that are selected.  Make sure that base isn't in the uninstall list.  Ask the user if he is sure that the files should be uninstalled, uninstall the packages (remove the files).
        selectedItems = self.treeViewInstalled.selectedItems()
        if len(selectedItems) ==0: return

        uninstallList = []
        for item in selectedItems:
            name = unicode(item.text(0))
            if name == 'base':  ## special case of trying to delete base.
                QMessageBox.information(self, _("Deleting Base"), _("You are not allowed to delete base."), QMessageBox.Ok)
                continue
            uninstallList.append(name)
        if len(uninstallList) ==0: return
        
        mb = QMessageBox(_("Uninstall Packages"), _("Are you sure that you want to uninstall these packages?\n\n")+
        "\n".join(uninstallList), QMessageBox.Information, 
        QMessageBox.Ok | QMessageBox.Default, QMessageBox.Cancel | QMessageBox.Escape, QMessageBox.NoButton,self)
        
        if mb.exec_() != QMessageBox.Ok:
            return
            
        import shutil
        for name in uninstallList:
            shutil.rmtree(os.path.join(redREnviron.directoryNames['libraryDir'], name), True)
        
        qApp.canvasDlg.reloadWidgets()
        self.loadPackagesLists(force=False)
    
    # Lists all packages that will be downloaded and installed
    # asks for permission to perform the actions
    def askToInstall(self,packages,msg):
        deps = self.packageManager.getDependencies(packages)
        mainStr = []
        depStr = []
        for package,version in packages.items():
            if not version['installed']:
                mainStr.append(package + '-' + version['Version'])
            
        for package,version in deps.items():
            if not version['installed'] and package not in packages.keys():
                depStr.append(package + '-' + version['Version'])
            
        
        msg = msg + _("\nRepository: Red-R.org\nPackages:\n-- ") + "\n-- ".join(mainStr)
        if len(depStr) > 0:
            msg = msg + _("\n With dependencies:\n-- ") + "\n-- ".join(depStr)
            
        mb = QMessageBox(_("Install Packages"), msg, 
        QMessageBox.Information, QMessageBox.Ok | QMessageBox.Default, 
        QMessageBox.Cancel | QMessageBox.Escape, QMessageBox.NoButton,self)
        if mb.exec_() != QMessageBox.Ok:
            return

        ## resolve the packages
        packages.update(deps)
        #print packages
        results = self.packageManager.downloadPackages(packages,window=self)
        self.loadPackagesLists()
        self.tabsArea.setCurrentIndex(1)
    
    # takes user selected list of packages from the available packages menu and installed them and all the dependencies
    def installNewPackage(self):
        selectedItems = self.treeViewAvailable.selectedItems()
        if len(selectedItems) ==0: return
        downloadList = {}
        for item in selectedItems:  
            name = unicode(item.text(0))
            downloadList[name] = {'Version':unicode(item.text(3)), 'installed':False}

        self.askToInstall(downloadList,_("Are you sure that you want to install these packages?"))

    # install file form file. Takes package rrp location and parses the xml file to dependencies
    # installs the local rrp file as well as all the required dependencies if they exist in the repository
    def installPackageFromFile(self,filename):
        try:
            package = self.packageManager.getPackageInfo(filename)
            
            if package['Name'] in self.localPackages.keys() and self.localPackages[package['Name']]['Version']['Number'] == package['Version']['Number']: 
                mb = QMessageBox(_("Install Package"), 'Package "%s" is already installed. Do you want to remove the current version and continue installation?' % package['Name'], 
                QMessageBox.Information, QMessageBox.Ok | QMessageBox.Default, 
                QMessageBox.No | QMessageBox.Escape, QMessageBox.NoButton,self)
                if mb.exec_() != QMessageBox.Ok:
                    return

                
            downloadList = {}
            downloadList[package['Name']] = {'Version':unicode(package['Version']['Number']), 'installed':False}
            deps = self.packageManager.getDependencies(downloadList)
            #print deps
            notFound = []
            download = {}
            for name,version in deps.items():
                if name in self.availablePackages.keys() and version['Version'] == self.availablePackages[name]['Version']['Number']:
                    download[name] = version
                else:
                    notFound.append(name)
            if len(notFound) > 0:
                mb = QMessageBox.warning(self,_("Install Package"), 
                _('The following packages are required but not found in the Red-R.org repository. Installation will not proceed.\n\n--')+
                '\n--'.join(notFound),
                QMessageBox.Ok)
                return
            else:
                msg = _("Are you sure that you want to install this package and its dependencies?\nRepository: Red-R.org\nPackage:\n--") + package['Name']
                if len(download.keys()) > 0:
                    msg = msg + _("\n With dependencies:\n--") + "\n--".join(deps.keys())
                    
                mb = QMessageBox(_("Install Package"), msg, 
                QMessageBox.Information, QMessageBox.Ok | QMessageBox.Default, 
                QMessageBox.Cancel | QMessageBox.Escape, QMessageBox.NoButton,self)
                if mb.exec_() != QMessageBox.Ok:
                    return
            #print filename
            self.packageManager.installRRP(package['Name'], filename)
            if len(download.keys()) > 0:
                results = self.packageManager.downloadPackages(download,window=self)
            else: #need to do this to refresh the widget tree
                qApp.canvasDlg.reloadWidgets()
            self.loadPackagesLists()
            self.tabsArea.setCurrentIndex(1)
        except Exception as inst:
            mb = QMessageBox.warning(self,_("Install Package"), 
                _('The following error occurred during the installation of your package.\nPlease contact the package maintainer to report this error.\n\n')+unicode(inst),
                QMessageBox.Ok)
            raise Exception, unicode(inst)
            

packageManager = packageManager()
