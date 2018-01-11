# Author: Gregor Leban (gregor.leban@fri.uni-lj.si) modified by Kyle R Covington
#

import os, sys, re, glob, stat, redRLog

#from orngSignalManager import OutputSignal, InputSignal
from PyQt4.QtCore import *
from PyQt4.QtGui import *
# print 'Importing orngRegistry.py'
import redRPackageManager
import signals
import xml.dom.minidom
# redRDir = os.path.split(os.path.split(os.path.abspath(__file__))[0])[0]
# if not redRDir in sys.path:
    # sys.path.append(redRDir)

import redREnviron
import redRi18n
# def _(a):
    # return a
_ = redRi18n.Coreget_()
class WidgetDescription:
    def __init__(self, **attrs):
        self.__dict__.update(attrs)
class TemplateDescription:
    def __init__(self, **attrs):
        self.__dict__.update(attrs)
        
class WidgetCategory(dict):
    def __init__(self, directory, widgets):
        self.update(widgets)
        self.directory = directory

AllPackages = {}
def readCategories():
    # print '##########################in readCategories'
    redRLog.log(redRLog.REDRCORE, redRLog.INFO, _('Loading repository of packages.'))
    global widgetsWithError 
    widgetDirName = os.path.realpath(redREnviron.directoryNames["libraryDir"])
    canvasSettingsDir = os.path.realpath(redREnviron.directoryNames["canvasSettingsDir"])
    cacheFilename = os.path.join(canvasSettingsDir, "cachedWidgetDescriptions.pickle")

    try:
        import cPickle
        cats = cPickle.load(file(cacheFilename, "rb"))
        cachedWidgetDescriptions = dict([(w.fullName, w) for cat in cats.values() for w in cat.values()])
    except:
        redRLog.log(redRLog.REDRCORE, redRLog.ERROR, redRLog.formatException())
        cachedWidgetDescriptions = {} 

    directories = []
    for dirName in os.listdir(widgetDirName):
        directory = os.path.join(widgetDirName, dirName)
        if os.path.isdir(directory):
            directories.append((dirName, directory, ""))

    categories = {'widgets':[], 'templates':[], 'tags': None}     
    allWidgets = []
    theTags = xml.dom.minidom.parseString('<tree></tree>')
    for dirName, directory, plugin in directories:
        if not os.path.isfile(os.path.join(directory,'package.xml')): continue
        f = open(os.path.join(directory,'package.xml'), 'r')
        mainTabs = xml.dom.minidom.parse(f)
        f.close()
        package = redRPackageManager.packageManager.parsePackageXML(mainTabs)
        # we read in all the widgets in dirName, directory in the directories
        widgets = readWidgets(os.path.join(directory), package, cachedWidgetDescriptions)  ## calls an internal function
        AllPackages[package['Name']] = package
        if mainTabs.getElementsByTagName('menuTags'):
            newTags = mainTabs.getElementsByTagName('menuTags')[0].childNodes
            for tag in newTags:
                if tag.nodeName == 'group': 
                    addTagsSystemTag(theTags.childNodes[0],tag)

        #print '#########widgets',widgets
        allWidgets += widgets
    categories['tags'] = theTags
    # print theTags
    if allWidgets: ## collect all of the widgets and set them in the catepories
        categories['widgets'] = WidgetCategory(plugin and directory or "", allWidgets)

    allTemplates = []
    for dirName, directory, plugin in directories:
        templates = readTemplates(os.path.join(directory,'templates')) # a function to read in the templates that are in the directories
        allTemplates += templates
        #print templates
        
    allTemplates += readTemplates(redREnviron.directoryNames['templatesDir'])
    categories['templates'] = allTemplates
    cPickle.dump(categories, file(cacheFilename, "wb"))
    if splashWindow:
        splashWindow.hide()
    
    redRLog.log(redRLog.REDRCORE, redRLog.INFO, _('Finished loading repository of packages.'))
    return categories ## return the widgets and the templates

hasErrors = False
splashWindow = None
widgetsWithError = []

def addTagsSystemTag(tags,newTag):
                
    name = unicode(newTag.getAttribute('name'))
    # move through the group tags in tags, if you find the grouname of tag 
    #then you don't need to add it, rather just add the child tags to that tag.
    #tags = theTags.childNodes[0]
    #print tags.childNodes, _('Child Nodes')
    for t in tags.childNodes:
        if t.nodeName == 'group':
            #print t
            if unicode(t.getAttribute('name')) == name: ## found the right tag
                #print _('Found the name')
                #print t.childNodes
                for tt in newTag.childNodes:
                    if tt.nodeName == 'group':
                        addTagsSystemTag(t, tt) # add the child tags
            
                return
                
    ## if we made it this far we didn't find the right tag so we need to add all of the tag xml to the tags xml
    #print '|#|Name not found, appending to group.  This is normal, dont be worried.'
    tags.appendChild(newTag)
    #theTags.childNodes[0] = tags    
def getXMLText(nodelist):
    rc = ''
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc = rc + node.data
            
    rc = unicode(rc).strip()
    return rc

def readWidgets(directory, package, cachedWidgetDescriptions):
    import sys, imp
    global hasErrors, splashWindow, widgetsWithError
    import compileall
    compileall.compile_dir(directory,quiet=True) # compile the directory for later importing.
    #print '################readWidgets', directory, package
    widgets = []
    for filename in glob.iglob(os.path.join(directory,'widgets', "*.py")):
        if os.path.isdir(filename) or os.path.islink(filename):
            continue
        
        datetime = unicode(os.stat(filename)[stat.ST_MTIME])
        cachedDescription = cachedWidgetDescriptions.get(filename, None)
        if cachedDescription and cachedDescription.time == datetime and hasattr(cachedDescription, "inputClasses"):
            widgets.append((cachedDescription.name, cachedDescription))
            continue
        
        dirname, fname = os.path.split(filename)
        widgetName = os.path.splitext(fname)[0]
        widgetID = unicode(package['Name']+'_'+os.path.split(filename)[1].split('.')[0])
        
        widgetMetaData = {}
        metaFile = os.path.join(directory,'meta','widgets',widgetName+'.xml')
        if not os.path.exists(metaFile):
            redRLog.log(redRLog.REDRCORE, redRLog.ERROR, _('<b>Meta file for %s does not exist.</b>') % (filename))
            continue
        try:
            widgetMetaXML = xml.dom.minidom.parse(metaFile)
        except Exception as inst:
            redRLog.log(redRLog.REDRCORE, redRLog.ERROR, redRLog.formatException()) 
            redRLog.log(redRLog.REDRCORE, redRLog.ERROR, _('<b>Error loading meta data for %s; %s</b>') % (metaFile, unicode(inst)))
            continue
        widgetMetaData['name'] = getXMLText(widgetMetaXML.getElementsByTagName('name')[0].childNodes)
        widgetMetaData['icon'] = getXMLText(widgetMetaXML.getElementsByTagName('icon')[0].childNodes)
        widgetMetaData['description'] = getXMLText(widgetMetaXML.getElementsByTagName('summary')[0].childNodes)
        widgetMetaData['details'] = getXMLText(widgetMetaXML.getElementsByTagName('details')[0].childNodes)
        
        widgetMetaData['tags'] = []
        for tag in widgetMetaXML.getElementsByTagName('tags')[0].childNodes:
            if getXMLText(tag.childNodes) != '':
                widgetMetaData['tags'].append(getXMLText(tag.childNodes))

        widgetMetaData['inputs'] = []
        if len(widgetMetaXML.getElementsByTagName('input')):
            for input in widgetMetaXML.getElementsByTagName('input'):
                widgetMetaData['inputs'].append((
                getXMLText(input.getElementsByTagName('signalClass')[0].childNodes),
                getXMLText(input.getElementsByTagName('description')[0].childNodes)))
        
        widgetMetaData['outputs'] = []
        if len(widgetMetaXML.getElementsByTagName('output')):
            for outputs in widgetMetaXML.getElementsByTagName('output'):
                widgetMetaData['outputs'].append(
                (getXMLText(outputs.getElementsByTagName('signalClass')[0].childNodes),
                getXMLText(outputs.getElementsByTagName('description')[0].childNodes)))
        
        # print widgetMetaData

        if not splashWindow:
            logo = QPixmap(os.path.join(redREnviron.directoryNames["canvasDir"], "icons", "splash.png"))
            splashWindow = QSplashScreen(logo, Qt.WindowStaysOnTopHint)
            splashWindow.setMask(logo.mask())
            splashWindow.show()
            
        splashWindow.showMessage("Registering widget %s" % widgetMetaData['name'], Qt.AlignHCenter + Qt.AlignBottom)
        qApp.processEvents()
        
        # We import modules using imp.load_source to avoid storing them in sys.modules,
        # but we need to append the path to sys.path in case the module would want to load
        # something
        dirnameInPath = dirname in sys.path
        if not dirnameInPath:
            sys.path.append(dirname)
        # print widgetName, 'redREnviron' in sys.modules.keys()
        try:
            wmod = imp.load_source(package['Name'] + '_' + widgetName, filename)
        except Exception, msg:
            redRLog.log(redRLog.REDRCORE, redRLog.ERROR, _('Exception occurred in <b>%s: %s<b>') % (filename, msg))
            redRLog.log(redRLog.REDRCORE, redRLog.DEBUG, redRLog.formatException())
            continue
        
        # __import__('libraries.' + package['Name'] + '.widgets.' + widgetName)
        #wmod.__dict__['widgetFilename'] = filename
        # if not dirnameInPath and dirname in sys.path: # I have no idea, why we need this, but it seems to disappear sometimes?!
            # sys.path.remove(dirname)
        
        widgetInfo = WidgetDescription(
                     name = widgetMetaData['name'],
                     packageName = package['Name'],
                     package = package,
                     time = datetime,
                     fileName = package['Name'] + '_' + widgetName,
                     widgetName = widgetName,
                     fullName = filename
                     )
        #redRLog.log(redRLog.REDRCORE, redRLog.DEBUG, 'logging widget info %s' % widgetInfo.name)
        for k,v in widgetMetaData.items():
            setattr(widgetInfo,k,v)
     
        widgetInfo.tooltipText = "<b>%s</b><br />%s" % (widgetInfo.name, widgetInfo.description)

        if len(widgetInfo.inputs):
            widgetInfo.tooltipText +='<hr><b>Inputs</b><dl>'
            for x in widgetInfo.inputs:
                widgetInfo.tooltipText +='<dt>%s</dt><dd>%s</dd>' % x
            widgetInfo.tooltipText +='</dl>'
        else:
            widgetInfo.tooltipText +='<hr><b>Inputs</b><dl>'
            widgetInfo.tooltipText +='<dt>None</dt><dd></dd>' 
            widgetInfo.tooltipText +='</dl>'

        if len(widgetInfo.outputs):
            widgetInfo.tooltipText +='<hr><b>Outputs</b><dl>'
            for x in widgetInfo.outputs:
                widgetInfo.tooltipText +='<dt>%s</dt><dd>%s</dd>' % x
            widgetInfo.tooltipText +='</dl>'
        else:
            widgetInfo.tooltipText +='<hr><b>Inputs</b><dl>'
            widgetInfo.tooltipText +='<dt>None</dt><dd></dd>' 
            widgetInfo.tooltipText +='</dl>'

            
        widgetInfo.icon = os.path.join(redREnviron.directoryNames['libraryDir'], widgetInfo.packageName,'icons', widgetInfo.icon)
        if not os.path.isfile(widgetInfo.icon):
            if os.path.isfile(os.path.join(redREnviron.directoryNames['libraryDir'], widgetInfo.packageName,'icons', 'Default.png')): 
                widgetInfo.icon = os.path.join(redREnviron.directoryNames['libraryDir'], widgetInfo.packageName,'icons', 'Default.png')
            else:
                widgetInfo.icon = os.path.join(redREnviron.directoryNames['libraryDir'],'base', 'icons', 'Unknown.png')
            
        widgets.append((widgetID, widgetInfo))
        
    return widgets

def readTemplates(directory):
    import sys, imp
    global hasErrors, splashWindow, widgetsWithError
    
    # print '################readWidgets', directory, package
    templates = []
    for filename in glob.iglob(os.path.join(directory, "*.rrts")):
        if os.path.isdir(filename) or os.path.islink(filename):
            continue  # protects from a direcoty that has .rrs in it I guess

        dirname, fname = os.path.split(filename)
        # dirname, package = os.path.split(dirname)
        templateName = fname
        #widgetName = package + '_' + widget
        try:
            if not splashWindow:
                import redREnviron
                logo = QPixmap(os.path.join(redREnviron.directoryNames["canvasDir"], "icons", "splash.png"))
                splashWindow = QSplashScreen(logo, Qt.WindowStaysOnTopHint)
                splashWindow.setMask(logo.mask())
                splashWindow.show()
                
            splashWindow.showMessage("Registering template %s" % templateName, Qt.AlignHCenter + Qt.AlignBottom)
            qApp.processEvents()
            templateInfo = TemplateDescription(name = templateName, file = filename) 
            templates.append(templateInfo)
        except Exception, msg:
            redRLog.log(redRLog.REDRCORE, redRLog.ERROR,redRLog.formatException())
        
    return templates
def loadPackage(package):
    # print package
    downloadList = {}
    downloadList[package['Name']] = {'Version':unicode(package['Version']['Number']), 'installed':False}
    deps = redRPackageManager.packageManager.getDependencies(downloadList)
    downloadList.update(deps)
    # print downloadList
    # for name,version in downloadList.items():
        # if package =='base': continue
        # if not hasattr(redRGUI,name):
            # redRGUI.registerQTWidgets(name)
        # if not hasattr(signals,name):
            # signals.registerRedRSignals(name)
    
    
    
    
### we really need to change this...
re_inputs = re.compile(r'[ \t]+self.inputs\s*=\s*(?P<signals>\[[^]]*\])', re.DOTALL)
re_outputs = re.compile(r'[ \t]+self.outputs\s*=\s*(?P<signals>\[[^]]*\])', re.DOTALL)


re_tuple = re.compile(r"\(([^)]+)\)")

def getSignalList(regex, data):
    inmo = regex.search(data)
    if inmo:
        return unicode([tuple([y[0] in "'\"" and y[1:-1] or unicode(y) for y in (x.strip() for x in ttext.group(1).split(","))])
               for ttext in re_tuple.finditer(inmo.group("signals"))])
    else:
        return "[]"
