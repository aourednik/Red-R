## <redRSaveLoad Module.  This module (not a class) will contain and provide functions for loading and saving of objects.  The module will make great use of the redRObjects module to access and instantiate objects.>
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
import os, sys, redRObjects, cPickle, redREnviron, redRLog, globalData, RSession, redRPackageManager
import redRi18n
# def _(a):
    # return a
_ = redRi18n.Coreget_()
import cPickle, math, zipfile, urllib, sip
from xml.dom.minidom import Document, parse
from orngSignalManager import SignalManager
schemaPath = redREnviron.settings["saveSchemaDir"]
_schemaName = ""
canvasDlg = None
schemaDoc = None
signalManager = SignalManager()
_tempWidgets = []
notesTextWidget = None
sessionID = 1
def setNotesWidget(widget):
    global notesTextWidget
    notesTextWidget = widget
def setSchemaDoc(doc):
    global schemaDoc
    schemaDoc = doc
def setCanvasDlg(dlg):
    global canvasDlg
    canvasDlg = dlg
def minimumY():
    y = 0
    for w in redRObjects.getIconsByTab(redRObjects.activeTabName())[redRObjects.activeTabName()]:
        if w.y() > y:
            y = w.y()
    if y != 0:
        y += 30
    return y
    
## ideas behind saveing.  we should think about the possibility that there will be a template in the saving process.

### we should save all of the R session in the event of saving the main file
### we need to save instances, icons, and connections.  As the instances are the core they will be saved first as all other objects must reffer to them, then we will instantiate the connections between the widgets, finally the tabs and icons will be instantiated because they do not require anything but references to the instances and their connection handlers.

### saveing the instances is fairly strait forward as is reloading them except that the signals must be started after all of the instances are loaded...  Thus there should be a special function for this.  Additionally, in the event of a template we can't only rely on the instance ID because this might be duplicated if a template is loaded multiple times.  To handle this templates will use a template crutch to map template id's to widget id's during loading.  For example, load instances and map old instnce ID's to new instance id's using the templateCrutchDict.  On loading of the signals and the icons we use the templateCrutchDict we connect signals using that instead of the orriginal ID's.


    
    
def saveIcon(widgetIconsXML, wi, doc):
    #redRLog.log(redRLog.REDRCORE, redRLog.INFO, 'orngDoc makeTemplate; saving widget %s' % wi)
    witemp = doc.createElement('widgetIcon')
    witemp.setAttribute('name', unicode(wi.getWidgetInfo().fileName))             # save icon name
    witemp.setAttribute('instance', unicode(wi.instance().widgetID))        # save instance ID
    witemp.setAttribute("xPos", unicode(int(wi.x())) )      # save the xPos
    witemp.setAttribute("yPos", unicode(int(wi.y())) )      # same the yPos
    witemp.setAttribute("caption", wi.caption)          # save the caption
    widgetIconsXML.appendChild(witemp)

def saveInstances(instances, widgets, doc, progressBar):
    settingsDict = {}
    requireRedRLibraries = {}
    progress = 0
    if type(instances) == dict:
        instances = instances.values()
    for widget in instances:
        temp = doc.createElement("widget")
        
        temp.setAttribute("widgetName", widget.widgetInfo.fileName)
        temp.setAttribute("packageName", widget.widgetInfo.package['Name'])
        temp.setAttribute("packageVersion", widget.widgetInfo.package['Version']['Number'])
        temp.setAttribute("widgetFileName", os.path.basename(widget.widgetInfo.fullName))
        temp.setAttribute('widgetID', widget.widgetID)
        temp.setAttribute('captionTitle', unicode(widget.windowTitle()))
        print _('save in orngDoc ') + unicode(widget.captionTitle)
        progress += 1
        progressBar.setValue(progress)
        
        s = widget.getSettings()
        i = widget.getInputs()
        o = widget.getOutputs()
        c = widget.outputs.returnOutputs()
        
        settingsDict[widget.widgetID] = {}
        settingsDict[widget.widgetID]['settings'] = cPickle.dumps(s,2)
        settingsDict[widget.widgetID]['inputs'] = cPickle.dumps(i,2)
        settingsDict[widget.widgetID]['outputs'] = cPickle.dumps(o,2)
        settingsDict[widget.widgetID]['connections'] = cPickle.dumps(c, 2)
        
        if widget.widgetInfo.package['Name'] != 'base' and widget.widgetInfo.package['Name'] not in requireRedRLibraries.keys():
            requireRedRLibraries[widget.widgetInfo.package['Name']] = widget.widgetInfo.package
    
        widgets.appendChild(temp)
    return (widgets, settingsDict, requireRedRLibraries)
    
def makeTemplate(filename = None, copy = False):
    ## this is different from saving.  We want to make a special file that only has the selected widgets, their connections, and settings.  No R data or tabs are saved.
    if copy and len(_tempWidgets) == 0: return 
    elif len(_tempWidgets) == 0:
        mb = QMessageBox(_("Save Template"), _("No widgets are selected.\nTemplates require widgets to be selected before saving as template."), 
            QMessageBox.Information, QMessageBox.Ok | QMessageBox.Default, 
            QMessageBox.No | QMessageBox.Escape, QMessageBox.NoButton)
        
        mb.exec_()
        return
    if not copy:
        if not filename:
            redRLog.log(redRLog.REDRCORE, redRLog.ERROR, _('orngDoc in makeTemplate; no filename specified, this is highly irregular!! Exiting from template save.'))
            return
        tempDialog = TemplateDialog()
        if tempDialog.exec_() == QDialog.Rejected:
            return
    else:
        filename = redREnviron.directoryNames['tempDir']+'/copy.rrts'
    progressBar = startProgressBar(
    _('Saving ')+unicode(os.path.basename(filename)),
    _('Saving ')+unicode(os.path.basename(filename)),
    len(redRObjects.instances(wantType = 'list'))+len(redRObjects.lines().values())+3)
    progress = 0
    # create xml document
    (doc, schema, header, widgets, lines, settings, required, tabs, saveTagsList, saveDescription) = makeXMLDoc()
    requiredRLibraries = {}
    
    # save the widgets
    tempWidgets = {}
    if copy:
        for w in _tempWidgets:
            tempWidgets[w.instanceID] = w.instance()
    else:
        for w in redRObjects.activeTab().getSelectedWidgets():
            tempWidgets[w.instanceID] = w.instance()
    (widgets, settingsDict, requireRedRLibraries) = saveInstances(tempWidgets, widgets, doc, progressBar)
    # save the icons and the lines
    sw = redRObjects.activeTab().getSelectedWidgets()
    #redRLog.log(redRLog.REDRCORE, redRLog.ERROR, 'orngDoc makeTemplate; selected widgets: %s' % sw)
    temp = doc.createElement('tab')
    temp.setAttribute('name', 'template')
    
    ## set all of the widget icons on the tab
    widgetIcons = doc.createElement('widgetIcons')
    for wi in sw:
        saveIcon(widgetIcons, wi, doc)
        
    # tabLines = doc.createElement('tabLines')
    # for line in redRObjects.getLinesByTab()[redRObjects.activeTabName()]:
        # redRLog.log(redRLog.REDRCORE, redRLog.INFO, 'orngDoc makeTemplate; checking line %s, inWidget %s, outWidget %s' % (line, line.inWidget, line.outWidget))
        # if (line.inWidget not in sw) or (line.outWidget not in sw): 
            # continue
        # saveLine(tabLines, line)
        
    temp.appendChild(widgetIcons)       ## append the widgetIcons XML to the global XML
    #temp.appendChild(tabLines)          ## append the tabLines XML to the global XML
    tabs.appendChild(temp)

    
    ## save the global settings ##
    settingsDict['_globalData'] = cPickle.dumps(globalData.globalData,2)
    settingsDict['_requiredPackages'] =  cPickle.dumps({'R': requiredRLibraries.keys(),'RedR': requireRedRLibraries},2)
    #print requireRedRLibraries
    file = open(os.path.join(redREnviron.directoryNames['tempDir'], 'settings.pickle'), "wt")
    file.write(unicode(settingsDict))
    file.close()
    
    if not copy:
        taglist = unicode(tempDialog.tagsList.text())
        tempDescription = unicode(tempDialog.descriptionEdit.toPlainText())
        saveTagsList.setAttribute("tagsList", taglist)
        saveDescription.setAttribute("tempDescription", tempDescription)
        
    xmlText = doc.toprettyxml()
    progress += 1
    progressBar.setValue(progress)
    
    
    tempschema = os.path.join(redREnviron.directoryNames['tempDir'], "tempSchema.tmp")
    file = open(tempschema, "wt")
    file.write(xmlText)
    file.close()
    zout = zipfile.ZipFile(filename, "w")
    zout.write(tempschema,"tempSchema.tmp")
    zout.write(os.path.join(redREnviron.directoryNames['tempDir'], 'settings.pickle'),'settings.pickle')
    zout.close()
    doc.unlink()
    if copy:
        loadTemplate(filename)
        
    
    progress += 1
    progressBar.setValue(progress)
    progressBar.close()
    #redRLog.log(redRLog.REDRCORE, redRLog.ERROR, _('Template saved successfully'))
    return True
def collectIcons():
    global _tempWidgets
    redRLog.log(redRLog.REDRCORE, redRLog.DEBUG, _('Collecting Icons'))
    _tempWidgets = redRObjects.activeTab().getSelectedWidgets()
    redRLog.log(redRLog.REDRCORE, redRLog.DEBUG, _('Selected widgets are %s') % _tempWidgets)
def copy():
    ## copy the selected files and reload them as templates in the schema
    collectIcons()
    redRLog.log(redRLog.REDRCORE, redRLog.DEBUG, _('Making a copy with widgets %s') % _tempWidgets)
    makeTemplate(copy=True)
def savePipeline():
    #redRLog.log(redRLog.REDRCORE, redRLog.ERROR, _('Saving Pipeline'))
    name = QFileDialog.getSaveFileName(None, _("Save Template"), redREnviron.directoryNames['templatesDir'], "Red-R Widget Template (*.rrts)")
    if not name or name == None: return False
    name = unicode(name)
    if unicode(name) == '': return False
    if os.path.splitext(unicode(name))[0] == '': return False
    if os.path.splitext(unicode(name))[1].lower() != ".rrpipe": name = name + '.rrpipe'
    return save(filename = name, template = False, copy = False, pipe = True)
def saveDocument():
    #redRLog.log(redRLog.REDRCORE, redRLog.ERROR, _('Saving Document'))
    #return
    if _schemaName == "":
        return saveDocumentAs()
    else:
        return save(None,False)
def save(filename = None, template = False, copy = False, pipe = False):
    global _schemaName
    global schemaPath
    global notesTextWidget
    #redRLog.log(redRLog.REDRCORE, redRLog.ERROR, '%s' % filename)
    if filename == None and not copy:
        filename = os.path.join(schemaPath, _schemaName)
    elif copy:
        filename = os.path.join(redREnviron.directoryNames['tempDir'], 'copy.rrts')
    #redRLog.log(redRLog.REDRCORE, redRLog.ERROR, 'Saveing file as name %s' % filename)
    progressBar = startProgressBar(
    _('Saving ')+unicode(os.path.basename(filename)),
    _('Saving ')+unicode(os.path.basename(filename)),
    len(redRObjects.instances())+len(redRObjects.lines())+3)
    progress = 0

    # create xml document
    (doc, schema, header, widgets, lines, settings, required, tabs, saveTagsList, saveDescription) = makeXMLDoc()
    requiredRLibraries = {}
    
    
    #save widgets
    tempWidgets = redRObjects.instances(wantType = 'dict') ## all of the widget instances, these are not the widget icons
    (widgets, settingsDict, requireRedRLibraries) = saveInstances(tempWidgets, widgets, doc, progressBar)
    
    
    # save tabs and the icons and the channels
    if not copy or template:
        #tabs.setAttribute('tabNames', unicode(self.canvasTabs.keys()))
        for t in redRObjects.tabNames():
            temp = doc.createElement('tab')
            temp.setAttribute('name', t)
            ## set all of the widget icons on the tab
            widgetIcons = doc.createElement('widgetIcons')
            for wi in redRObjects.getIconsByTab(t)[t]:  ## extract only the list for this tab thus the [t] syntax
                saveIcon(widgetIcons, wi, doc)
            # tabLines = doc.createElement('tabLines')
            # for line in self.widgetLines(t)[t]:
                # saveLine(tabLines, line)
                
            temp.appendChild(widgetIcons)       ## append the widgetIcons XML to the global XML
            #temp.appendChild(tabLines)          ## append the tabLines XML to the global XML
            tabs.appendChild(temp)
    
    
    ## save the global settings ##
    if notesTextWidget:
        globalData.setGlobalData('Notes', 'globalNotes', unicode(notesTextWidget.toHtml()))
    
    settingsDict['_globalData'] = cPickle.dumps(globalData.globalData,2)
    settingsDict['_requiredPackages'] =  cPickle.dumps({'R': requiredRLibraries.keys(),'RedR': requireRedRLibraries},2)
    
    #print requireRedRLibraries
    file = open(os.path.join(redREnviron.directoryNames['tempDir'], 'settings.pickle'), "wt")
    file.write(unicode(settingsDict))
    file.close()
    if template:
        taglist = unicode(tempDialog.tagsList.text())
        tempDescription = unicode(tempDialog.descriptionEdit.toPlainText())
        saveTagsList.setAttribute("tagsList", taglist)
        saveDescription.setAttribute("tempDescription", tempDescription)
        
    xmlText = doc.toprettyxml()
    progress += 1
    progressBar.setValue(progress)

    if not template and not copy and not pipe:
        tempschema = os.path.join(redREnviron.directoryNames['tempDir'], "tempSchema.tmp")
        tempR = os.path.join(redREnviron.directoryNames['tempDir'], "tmp.RData").replace('\\','/')
        file = open(tempschema, "wt")
        file.write(xmlText)
        file.close()
        doc.unlink()
        
        progressBar.setLabelText('Saving Data...')
        progress += 1
        progressBar.setValue(progress)

        RSession.Rcommand('save.image("' + tempR + '")')  # save the R data
        
        createZipFile(filename,[],[redREnviron.directoryNames['tempDir']])# collect the files that are in the tempDir and save them into the zip file.
    elif template:
        tempschema = os.path.join(redREnviron.directoryNames['tempDir'], "tempSchema.tmp")
        file = open(tempschema, "wt")
        file.write(xmlText)
        file.close()
        zout = zipfile.ZipFile(filename, "w")
        zout.write(tempschema,"tempSchema.tmp")
        zout.write(os.path.join(redREnviron.directoryNames['tempDir'], 'settings.pickle'),'settings.pickle')
        zout.close()
        doc.unlink()
    elif copy:
        tempschema = os.path.join(redREnviron.directoryNames['tempDir'], "tempSchema.tmp")
        file = open(tempschema, "wt")
        file.write(xmlText)
        file.close()
        zout = zipfile.ZipFile(filename, "w")
        zout.write(tempschema,"tempSchema.tmp")
        zout.write(os.path.join(redREnviron.directoryNames['tempDir'], 'settings.pickle'),'settings.pickle')
        zout.close()
        doc.unlink()
        loadTemplate(filename)
        
    
    
    progress += 1
    progressBar.setValue(progress)
    progressBar.close()
    if os.path.splitext(filename)[1].lower() == ".rrs":
        (schemaPath, schemaName) = os.path.split(filename)
        redREnviron.settings["saveSchemaDir"] = schemaPath
        canvasDlg.toolbarFunctions.addToRecentMenu(filename)
        canvasDlg.setCaption(schemaName)
    redRLog.log(redRLog.REDRCORE, redRLog.INFO, 'Document Saved Successfully to %s' % filename)
    return True
# load a scheme with name "filename"

####################
####   loading #####
####################
def loadRequiredPackages(required, loadingProgressBar):
    try:  # protect the required functions in a try statement, we want to load these things and they should be there but we can't force it to exist in older schemas, so this is in a try.
        required = cPickle.loads(required)
        if len(required) > 0:
            if 'CRANrepos' in redREnviron.settings.keys():
                repo = redREnviron.settings['CRANrepos']
            else:
                repo = None
            loadingProgressBar.setLabelText(_('Loading required R Packages. If not found they will be downloaded.\n This may take a while...'))
            RSession.require_librarys(required['R'], repository=repo)
        
        installedPackages = redRPackageManager.packageManager.getInstalledPackages()
        downloadList = {}
        print type(required['RedR'])
        #print required['RedR']
        
        for name,package in required['RedR'].items():
            #print package
            if not (package['Name'] in installedPackages.keys() 
            and package['Version']['Number'] == installedPackages[package['Name']]['Version']['Number']):
                downloadList[package['Name']] = {'Version':unicode(package['Version']['Number']), 'installed':False}

        if len(downloadList.keys()) > 0:
            pm = redRPackageManager.packageManagerDialog()
            pm.show()
            pm.askToInstall(downloadList, _('The following packages need to be installed before the session can be loaded.'))
    except Exception as inst: 
        redRLog.log(redRLog.REDRCORE, redRLog.ERROR, _('redRSaveLoad loadRequiredPackages; error loading package %s') % inst)  

def loadTemplate(filename, caption = None, freeze = 0):
    
    loadDocument(filename = filename, caption = caption, freeze = freeze)

def loadDocument(filename, caption = None, freeze = 0, importing = 0):
    global _schemaName
    global schemaPath
    global globalNotes
    redRLog.log(redRLog.REDRCORE, redRLog.INFO, _('Loading Document %s') % filename)
    import redREnviron
    if filename.split('.')[-1] in ['rrts']:
        tmp=True
        pipe = False
    elif filename.split('.')[-1] in ['rrs']:
        tmp=False
        pipe = False
    elif filename.split('.')[-1] in ['rrpipe']:         ## pipeline, no data but everything else there.
        pipe = True
        tmp = False
    else:
        QMessageBox.information(None, 'Red-R Error', 
        _('Cannot load file with extension %s') % unicode(filename.split('.')[-1]),  
        QMessageBox.Ok + QMessageBox.Default)
        return
    
    loadingProgressBar = startProgressBar(_('Loading %s') % unicode(os.path.basename(filename)),
    _('Loading %s') % unicode(filename), 2)
    
        
    # set cursor
    qApp.setOverrideCursor(Qt.WaitCursor)
    
    if os.path.splitext(filename)[1].lower() == ".rrs":
        schemaPath, _schemaName = os.path.split(filename)
        canvasDlg.setCaption(caption or _schemaName)
    if importing: # a normal load of the session
        _schemaName = ""

    loadingProgressBar.setLabelText(_('Loading Schema Data, please wait'))

    ### unzip the file ###
    
    zfile = zipfile.ZipFile( unicode(filename), "r" )
    for name in zfile.namelist():
        file(os.path.join(redREnviron.directoryNames['tempDir'],os.path.basename(name)), 'wb').write(zfile.read(name)) ## put the data into the tempdir for this session for each file that was in the temp dir for the last schema when saved.
    doc = parse(os.path.join(redREnviron.directoryNames['tempDir'],'tempSchema.tmp')) # load the doc data for the data in the temp dir.

    ## get info from the schema
    schema = doc.firstChild
    try:
        
        version = schema.getElementsByTagName("header")[0].getAttribute('version')
        if not version:
            redRLog.log(redRLog.REDRCORE, redRLog.WARNING, _('Version Tag Missing, using Red-R 1.80 loading specifications'))            ## we should move everything to the earlier versions of orngDoc for loading.
            loadDocument180(filename, caption = None, freeze = 0, importing = 0)
            loadingProgressBar.hide()
            loadingProgressBar.close()
            return
        else:
            print _('The version is:%s') % version
    except Exception as inst:
        redRLog.log(redRLog.REDRCORE, redRLog.ERROR, redRLog.formatException())
        redRLog.log(redRLog.REDRCORE, redRLog.WARNING, _('Error in loading the schema %s, reverting to load with 1.80 settings') % inst)
        loadDocument180(filename, caption = None, freeze = 0, importing = 0)
        loadingProgressBar.hide()
        loadingProgressBar.close()
        return
    widgets = schema.getElementsByTagName("widgets")[0]
    tabs = schema.getElementsByTagName("tabs")[0]
    #settings = schema.getElementsByTagName("settings")
    f = open(os.path.join(redREnviron.directoryNames['tempDir'],'settings.pickle'))
    settingsDict = eval(unicode(f.read()))
    f.close()
    
    ## load the required packages
    loadRequiredPackages(settingsDict['_requiredPackages'], loadingProgressBar = loadingProgressBar)
    
    ## make sure that there are no duplicate widgets.
    if not tmp and not pipe:
        ## need to load the r session before we can load the widgets because the signals will beed to check the classes on init.
        if not checkWidgetDuplication(widgets = widgets):
            QMessageBox.information(canvasDlg, _('Schema Loading Failed'), _('Duplicated widgets were detected between this schema and the active one.  Loading is not possible.'),  QMessageBox.Ok + QMessageBox.Default)
    
            return
        RSession.Rcommand('load("' + os.path.join(redREnviron.directoryNames['tempDir'], "tmp.RData").replace('\\','/') +'")')
    
    loadingProgressBar.setLabelText(_('Loading Widgets'))
    loadingProgressBar.setMaximum(len(widgets.getElementsByTagName("widget"))+1)
    loadingProgressBar.setValue(0)
    if not tmp:
        globalData.globalData = cPickle.loads(settingsDict['_globalData'])
        if notesTextWidget and ('none' in globalData.globalData.keys()) and ('globalNotes' in globalData.globalData['none'].keys()):
            notesTextWidget.setHtml(globalData.globalData['none']['globalNotes']['data'])
        (loadedOkW, tempFailureTextW) = loadWidgets(widgets = widgets, loadingProgressBar = loadingProgressBar, loadedSettingsDict = settingsDict, tmp = tmp)
    
    ## LOAD tabs
    #####  move through all of the tabs and load them.
    (loadedOkT, tempFailureTextT) = loadTabs(tabs = tabs, loadingProgressBar = loadingProgressBar, tmp = tmp, loadedSettingsDict = settingsDict)
    if not tmp:
        redRLog.log(10, 9,3,_('Setting Signals'))
        for widget in redRObjects.instances():
            redRLog.log(10, 9, 9, _('Setting Signals for %s') % widget)
            try:
                if widget.widgetID not in settingsDict.keys(): continue
                widget.outputs.setOutputs(cPickle.loads(settingsDict[widget.widgetID]['connections']), tmp)
            except Exception as inst:
                redRLog.log(redRLog.REDRCORE, redRLog.ERROR, redRLog.formatException())
                redRLog.log(1, 9, 1, _('Error setting signals %s, Settings are %s') % (inst, settingsDict[widget.widgetID].keys()))
    else:
        for widget in redRObjects.instances():
            if widget.tempID and widget.tempID in settingsDict.keys():
                widget.outputs.setOutputs(cPickle.loads(settingsDict[widget.tempID]['connections']), tmp)
    if pipe:        ## send none through all of the data.
        for w in redRObjects.instances():
            w.outputs.propogateNone(ask = False)
    for widget in redRObjects.instances():
        widget.tempID = None  ## we set the temp ID to none so that there won't be a conflict with other temp loading.
        
    ## some saved sessions may have widget instances that are available but that do not match to icons.  This shouldn't happen normally but if it does then we have instances that can persist without us knowing about it.  We clear those here.
    for i in redRObjects.instances():
        try:
            redRObjects.getWidgetByInstance(i)
        except:
            redRLog.log(redRLog.REDRCORE, redRLog.ERROR, redRLog.formatException())
            try:
                redRObjects.removeWidgetInstance(i)
            except: 
                redRLog.log(redRLog.REDRCORE, redRLog.ERROR, redRLog.formatException())
                pass
    qApp.restoreOverrideCursor() 
    qApp.restoreOverrideCursor()
    qApp.restoreOverrideCursor()
    loadingProgressBar.hide()
    loadingProgressBar.close()
    redRObjects.updateLines()
def loadDocument180(filename, caption = None, freeze = 0, importing = 0):
    global sessionID
    import redREnviron
    if filename.split('.')[-1] in ['rrts']:
        tmp=True
    elif filename.split('.')[-1] in ['rrs']:
        tmp=False
    else:
        QMessageBox.information(self, _('Red-R Error'), 
        _('Cannot load file with extension %s') % unicode(filename.split('.')[-1]),  
        QMessageBox.Ok + QMessageBox.Default)
        return
    
    loadingProgressBar = startProgressBar(_('Loading %s') % unicode(os.path.basename(filename)),
    _('Loading ')+unicode(filename), 2)
    
    ## What is the purpose of this???
    if not os.path.exists(filename):
        if os.path.splitext(filename)[1].lower() != ".tmp":
            QMessageBox.critical(self, _('Red-R Canvas'), 
            _('Unable to locate file "%s"') % filename,  QMessageBox.Ok)
        return
        loadingProgressBar.hide()
        loadingProgressBar.close()
    ###
        
    # set cursor
    qApp.setOverrideCursor(Qt.WaitCursor)
    
    if os.path.splitext(filename)[1].lower() == ".rrs":
        schemaPath, _schemaName = os.path.split(filename)
        canvasDlg.setCaption(caption or _schemaName)
    if importing: # a normal load of the session
        _schemaName = ""

    loadingProgressBar.setLabelText(_('Loading Schema Data, please wait'))

    ### unzip the file ###
    
    zfile = zipfile.ZipFile( unicode(filename), "r" )
    for name in zfile.namelist():
        file(os.path.join(redREnviron.directoryNames['tempDir'],os.path.basename(name)), 'wb').write(zfile.read(name)) ## put the data into the tempdir for this session for each file that was in the temp dir for the last schema when saved.
    doc = parse(os.path.join(redREnviron.directoryNames['tempDir'],'tempSchema.tmp')) # load the doc data for the data in the temp dir.

    ## get info from the schema
    schema = doc.firstChild
    widgets = schema.getElementsByTagName("widgets")[0]
    lines = schema.getElementsByTagName('channels')[0]
    f = open(os.path.join(redREnviron.directoryNames['tempDir'],'settings.pickle'))
    settingsDict = eval(unicode(f.read()))
    f.close()
    
    #settingsDict = eval(unicode(settings[0].getAttribute("settingsDictionary")))
    loadedSettingsDict = settingsDict
    
    loadRequiredPackages(settingsDict['_requiredPackages'], loadingProgressBar = loadingProgressBar)
    
    ## make sure that there are no duplicate widgets.
    if not tmp:
        ## need to load the r session before we can load the widgets because the signals will beed to check the classes on init.
        if not checkWidgetDuplication(widgets = widgets):
            QMessageBox.information(self, _('Schema Loading Failed'), _('Duplicated widgets were detected between this schema and the active one.  Loading is not possible.'),  QMessageBox.Ok + QMessageBox.Default)
    
            return
        RSession.Rcommand('load("' + os.path.join(redREnviron.directoryNames['tempDir'], "tmp.RData").replace('\\','/') +'")')
    
    loadingProgressBar.setLabelText(_('Loading Widgets'))
    loadingProgressBar.setMaximum(len(widgets.getElementsByTagName("widget"))+1)
    loadingProgressBar.setValue(0)
    globalData.globalData = cPickle.loads(loadedSettingsDict['_globalData'])
    (loadedOkW, tempFailureTextW) = loadWidgets180(widgets = widgets, loadingProgressBar = loadingProgressBar, loadedSettingsDict = loadedSettingsDict, tmp = tmp)
    
    lineList = lines.getElementsByTagName("channel")
    loadingProgressBar.setLabelText(_('Loading Lines'))
    (loadedOkL, tempFailureTextL) = loadLines(lineList, loadingProgressBar = loadingProgressBar, 
    freeze = freeze, tmp = tmp)

    #for widget in redRObjects.instances(): widget.updateTooltip()
    #activeCanvas().update()
    #saveTempDoc()
    
    if not loadedOkW and loadedOkL:
        failureText = tempFailureTextW + tempFailureTextL
        QMessageBox.information(canvasDlg, _('Schema Loading Failed'), _('The following errors occured while loading the schema: <br><br>') + failureText,  QMessageBox.Ok + QMessageBox.Default)
    
    for widget in redRObjects.instances():
        widget.setLoadingSavedSession(False)
    qApp.restoreOverrideCursor() 
    qApp.restoreOverrideCursor()
    qApp.restoreOverrideCursor()
    loadingProgressBar.hide()
    loadingProgressBar.close()
    if tmp:
        sessionID += 1
    

def loadTabs(tabs, loadingProgressBar, tmp, loadedSettingsDict = None):
    # load the tabs
    
    loadedOK = True
    for t in tabs.getElementsByTagName('tab'):
        if not tmp:
            redRLog.log(redRLog.REDRCORE, redRLog.DEBUG, 'Loading tab %s' % t)
            schemaDoc.makeSchemaTab(t.getAttribute('name'))
            schemaDoc.setTabActive(t.getAttribute('name'))
        addY = minimumY()
        for witemp in t.getElementsByTagName('widgetIcons')[0].getElementsByTagName('widgetIcon'):
            name = witemp.getAttribute('name')             # save icon name
            instance = witemp.getAttribute('instance')        # save instance ID
            
            xPos = int(witemp.getAttribute("xPos"))      # save the xPos
            yPos = int(witemp.getAttribute("yPos"))      # same the yPos
            if not tmp:
                try:
                    caption = witemp.getAttribute("caption")          # save the caption
                    redRLog.log(1, 5, 3, _('loading widgeticon %(NAME)s, %(INSTANCE)s, %(CAPTION)s') % {'NAME':name, 'INSTANCE':instance, 'CAPTION':caption})
                    schemaDoc.addWidgetIconByFileName(name, x = xPos, y = yPos + addY, caption = caption, instance = instance) ##  add the widget icon 
                except Exception as inst:
                    redRLog.log(1, 9, 1, _('Loading exception occured for %s, %s') % (name, inst))
            else:
                #print 'loadedSettingsDict %s' % loadedSettingsDict.keys()
                caption = ""
                settings = cPickle.loads(loadedSettingsDict[instance]['settings'])
            
                import time
                loadingInstanceID = unicode(time.time())
                newwidget = schemaDoc.addWidgetByFileName(name, x = xPos, y = yPos + addY, widgetSettings = settings, id = loadingInstanceID)
                nw = redRObjects.getWidgetInstanceByID(newwidget)
                ## if tmp we need to set the tempID
                nw.tempID = instance
                nw.widgetID = loadingInstanceID
                nw.variable_suffix = '_' + loadingInstanceID
                nw.resetRvariableNames()
                ## send None through all of the widget ouptuts if this is a template
                nw.outputs.propogateNone()
        
    return (True, '')

def loadWidgets(widgets, loadingProgressBar, loadedSettingsDict, tmp):
        
    lpb = 0
    loadedOk = 1
    failureText = ''
    for widget in widgets.getElementsByTagName("widget"):
        try:
            name = widget.getAttribute("widgetName")
            #print name
            widgetID = widget.getAttribute('widgetID')
            caption = widget.getAttribute('captionTitle')
            #print widgetID
            settings = cPickle.loads(loadedSettingsDict[widgetID]['settings'])
            inputs = cPickle.loads(loadedSettingsDict[widgetID]['inputs'])
            outputs = cPickle.loads(loadedSettingsDict[widgetID]['outputs'])
            #print _('adding instance'), widgetID, inputs, outputs
            newwidget = addWidgetInstanceByFileName(name, settings, inputs, outputs, id = widgetID)
            if newwidget and tmp:
                import time
                nw = redRObjects.getWidgetInstanceByID(newwidget)
                ## if tmp we need to set the tempID
                nw.tempID = widgetID
                nw.widgetID = unicode(time.time())
                nw.variable_suffix = '_' + widgetID
                nw.resetRvariableNames()
                ## send None through all of the widget ouptuts if this is a template
                nw.outputs.propogateNone()
            nw = redRObjects.getWidgetInstanceByID(newwidget)
            nw.setWindowTitle(caption)
            #print _('Settings'), settings
            lpb += 1
            loadingProgressBar.setValue(lpb)
        except Exception as inst:
            redRLog.log(redRLog.REDRCORE, redRLog.ERROR, redRLog.formatException())
            redRLog.log(redRLog.REDRCORE, redRLog.ERROR, unicode(inst))
    ## now the widgets are loaded so we can move on to setting the connections
    
    return (loadedOk, failureText)
def loadLines(lineList, loadingProgressBar, freeze, tmp):
    global sessionID
    failureText = ""
    loadedOk = 1
    for line in lineList:
        ## collect the indicies of the widgets to connect.
        inIndex = line.getAttribute("inWidgetIndex")
        outIndex = line.getAttribute("outWidgetIndex")
        print inIndex, outIndex
        
        if inIndex == None or outIndex == None or str(inIndex) == '' or str(outIndex) == '': # drive down the except path
            print inIndex, outIndex 
            
            raise Exception
        if freeze: enabled = 0
        else:      enabled = line.getAttribute("enabled")
        #print str(line.getAttribute('signals'))
        ## collect the signals to be connected between these widgets.
        signals = eval(str(line.getAttribute("signals")))
        #print '((((((((((((((((\n\nSignals\n\n', signals, '\n\n'
        if tmp: ## index up the index to match sessionID
            inIndex += '_'+str(sessionID)
            outIndex += '_'+str(sessionID)
            print inIndex, outIndex, _('Settings template ID to these values')
        inWidget = redRObjects.getWidgetInstanceByID(inIndex)
        outWidget = redRObjects.getWidgetInstanceByID(outIndex)
        
        #print inWidget, outWidget, '#########$$$$$#########$$$$$$#######'
        if inWidget == None or outWidget == None:
            print 'Expected ID\'s', inIndex, outIndex

            failureText += _("<nobr>Failed to create a signal line between widgets <b>%s</b> and <b>%s</b></nobr><br>") % (outIndex, inIndex)
            loadedOk = 0
            continue
            
        ## add a link for each of the signals.
        for (outName, inName) in signals:
            ## try to add using the new settings
            sig = inWidget.inputs.getSignal(inName)
            outWidget.outputs.connectSignal(sig, outName, enabled, False)
            #if not schemaDoc.addLink(outWidget, inWidget, outName, inName, enabled, loading = True, process = False): ## connect the signal but don't process.
                ## try to add using the old settings
            #    schemaDoc.addLink175(outWidget, inWidget, outName, inName, enabled)
        #print '######## enabled ########\n\n', enabled, '\n\n'
        #self.addLine(outWidget, inWidget, enabled, process = False)
        #self.signalManager.setFreeze(0)
        qApp.processEvents()
        
    return (loadedOk, failureText)
def addWidgetInstanceByFileName(name, settings = None, inputs = None, outputs = None, id = None):
    widget = redRObjects.widgetRegistry()['widgets'][name]
    return redRObjects.addInstance(signalManager, widget, settings, inputs, outputs, id)
    
        
def loadWidgets180(widgets, loadingProgressBar, loadedSettingsDict, tmp):
    lpb = 0
    loadedOk = 1
    failureText = ''
    addY = minimumY()
    for widget in widgets.getElementsByTagName("widget"):
        try:
            name = widget.getAttribute("widgetName")

            widgetID = widget.getAttribute('widgetID')
            settings = cPickle.loads(loadedSettingsDict[widgetID]['settings'])
            inputs = cPickle.loads(loadedSettingsDict[widgetID]['inputs'])
            outputs = cPickle.loads(loadedSettingsDict[widgetID]['outputs'])
            xPos = int(widget.getAttribute('xPos'))
            yPos = int(widget.getAttribute('yPos'))
            caption = unicode(widget.getAttribute('caption'))
            ## for backward compatibility we need to make both the widgets and the instances.
            #addWidgetInstanceByFileName(name, settings, inputs, outputs)
            widgetInfo =  redRObjects.widgetRegistry()['widgets'][name]
            if tmp:
                widgetID += '_'+str(sessionID)
            schemaDoc.addWidget(widgetInfo, x= xPos, y= yPos, caption = caption, widgetSettings = settings, forceInSignals = inputs, forceOutSignals = outputs, id = widgetID)
            #print _('Settings'), settings
            lpb += 1
            loadingProgressBar.setValue(lpb)
        except Exception as inst:
            redRLog.log(redRLog.REDRCORE, redRLog.ERROR, redRLog.formatException())
            print unicode(inst), _('Widget load failure 180')
    return (loadedOk, failureText)
def getXMLText(nodelist):
    rc = ''
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc = rc + node.data
    return rc
#####################
### zip files ###
#####################
def addFolderToZip(myZipFile,folder):
    import glob
    folder = folder.encode('ascii') #convert path to ascii for ZipFile Method
    for file in glob.glob(folder+"/*"):
            if os.path.isfile(file):
                
                myZipFile.write(file, os.path.basename(file), zipfile.ZIP_DEFLATED)
            elif os.path.isdir(file):
                addFolderToZip(myZipFile,file)

def createZipFile(zipFilename,files,folders):
    
    myZipFile = zipfile.ZipFile(zipFilename, "w" ) # Open the zip file for writing 
    
    for file in files:
        file = file.encode('ascii') #convert path to ascii for ZipFile Method
        if os.path.isfile(file):
            (filepath, filename) = os.path.split(file)
            myZipFile.write( file, filename, zipfile.ZIP_DEFLATED )

    for folder in  folders:   
        addFolderToZip(myZipFile,folder)  
    myZipFile.close()
    return (1,zipFilename)
    
def toZip(file, filename):
    zip_file = zipfile.ZipFile(filename, 'w')
    if os.path.isfile(file):
        zip_file.write(file)
    else:
        addFolderToZip(zip_file, file)
    zip_file.close()
    
def saveDocumentAs():
    global _schemaName
    global schemaPath
    name = QFileDialog.getSaveFileName(None, _("Save File"), os.path.join(schemaPath, _schemaName), "Red-R Widget Schema (*.rrs)")
    if not name or name == None: return False
    name = unicode(name)
    if unicode(name) == '': return False
    if os.path.splitext(unicode(name))[0] == "": return False
    if os.path.splitext(unicode(name))[1].lower() != ".rrs": name = name + ".rrs"
    #redRLog.log(redRLog.REDRCORE, redRLog.ERROR, 'saveDocument: name is %s' % name)
    schemaPath, _schemaName = os.path.split(name)
    return save(name,template=False)
def checkWidgetDuplication(widgets):
    for widget in widgets.getElementsByTagName("widget"):
        #widgetIDisNew = self.checkID(widget.getAttribute('widgetID'))
        if widget.getAttribute('widgetID') in redRObjects.instances(wantType = 'dict').keys():
            qApp.restoreOverrideCursor()
            QMessageBox.critical(canvasDlg, _('Red-R Canvas'), 
            _('Widget ID is a duplicate, I can\'t load this!!!'),  QMessageBox.Ok)
            return False
    return True
def saveTemplate():
    name = QFileDialog.getSaveFileName(None, _("Save Template"), redREnviron.directoryNames['templatesDir'], "Red-R Widget Template (*.rrts)")
    if not name or name == None: return False
    name = unicode(name)
    if unicode(name) == '': return False
    if os.path.splitext(unicode(name))[0] == '': return False
    if os.path.splitext(unicode(name))[1].lower() != ".rrts": name = name + '.rrts'
    return makeTemplate(unicode(name),copy=False)

def makeXMLDoc():
    doc = Document() ## generates the main document type.
    schema = doc.createElement("schema")
    header = doc.createElement('header')
    # make the header
    header.setAttribute('version', redREnviron.version['REDRVERSION'])
    widgets = doc.createElement("widgets")  # holds the widget instances
    lines = doc.createElement("channels")  # holds the lines
    settings = doc.createElement("settings")  
    required = doc.createElement("required")  # holds the required elements
    tabs = doc.createElement("tabs") # the tab names are saved here.
    saveTagsList = doc.createElement("TagsList")
    saveDescription = doc.createElement("saveDescription")
    doc.appendChild(schema)
    schema.appendChild(widgets)
    #schema.appendChild(lines)
    schema.appendChild(settings)
    schema.appendChild(required)
    schema.appendChild(saveTagsList)
    schema.appendChild(saveDescription)
    schema.appendChild(tabs)
    schema.appendChild(header)
    return (doc, schema, header, widgets, lines, settings, required, tabs, saveTagsList, saveDescription)
def startProgressBar(title,text,max):
    progressBar = QProgressDialog()
    progressBar.setCancelButtonText(QString())
    progressBar.setWindowTitle(title)
    progressBar.setLabelText(text)
    progressBar.setMaximum(max)
    progressBar.setValue(0)
    progressBar.show()
    return progressBar

    
class TemplateDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        
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