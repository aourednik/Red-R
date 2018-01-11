import os, cPickle, numpy, pprint, re, sys, redRLog
import redREnviron
import signals
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import redRGUI 
import signals 
# from SQLiteSession import *
 

class widgetSession():
    def __init__(self,dontSaveList):
        #collect the sent items
        
        #dont save these variables
        self.requiredAtts = ['notes', 'ROutput']
        self.loaded = False
        self.dontSaveList = dontSaveList
        self.defaultGlobalSettingsList = ['windowState']
        self.dontSaveList.extend(self.defaultGlobalSettingsList)
        self.dontSaveList.extend(['outputs','inputs', 'dontSaveList','redRGUIObjects','defaultGlobalSettingsList','globalSettingsList', 'loaded'])
        # self.sqlite = SQLiteHandler()


    def getSettings(self):  # collects settings for the save function, these will be included in the output file.  Called in orngDoc during save.
        redRLog.log(redRLog.REDRCORE, redRLog.DEBUG, 'moving to save'+unicode(self.captionTitle))
        import re
        settings = {}
        if self.saveSettingsList:  ## if there is a saveSettingsList then we just append the required elements to it.
            allAtts = self.saveSettingsList + self.requiredAtts
        else:
            allAtts = self.__dict__
        self.progressBarInit()
        i = 0
        for att in allAtts:
            # print att
            try:
                if att in self.dontSaveList or re.search('^_', att):
                    continue
                i += 1
                self.progressBarAdvance(i)
                # print 'frist att: ' + att
                var = getattr(self, att)
                settings[att] = self.returnSettings(var)
            except:
                redRLog.log(redRLog.REDRCORE, redRLog.ERROR,redRLog.formatException())
        settings['_customSettings'] = self.saveCustomSettings()
        tempSentItems = self.processSentItems()
        settings['sentItems'] = {'sentItemsList':tempSentItems}
        
        # import pprint
        # pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(settings)
       
        
        
        #settingsID = self.sqlite.saveObject(settings)
        self.progressBarFinished()
        return settings
    def saveCustomSettings(self): # dummy function that should be overwritten in child classes if they want the function
        pass
        
    def getInputs(self):
        
        return self.inputs.returnInputs()
        
    def getOutputs(self):
        return self.outputs.returnOutputs()

    def isPickleable(self,d):  # check to see if the object can be included in the pickle file
        import re
        #if isinstance(d,QObject):
        # print unicode(type(d))
        if re.search('PyQt4|OWGUIEx|OWToolbars',unicode(type(d))) or d.__class__.__name__ in redRGUI.qtWidgets:
            #print 'QT object NOT Pickleable'
            return False
        elif type(d) in [list, dict, tuple]:
            #ok = True
            if type(d) in [list, tuple]:
                for i in d:
                    if self.isPickleable(i) == False:
                        #ok = False
                        return False
                return True
            elif type(d) in [dict]:
                for k in d.keys():
                    if self.isPickleable(d[k]) == False:
                        #ok = False
                        return False
                return True
        elif type(d) in [type(None), str,unicode, int, float, bool, numpy.float64]:  # list of allowed save types, may epand in the future considerably
            return True
        elif isinstance(d, signals.BaseRedRVariable):
            return True
        else: 
            
            redRLog.log(redRLog.REDRCORE, redRLog.DEBUG, 'Type ' + unicode(d) + ' is not supported at the moment..')  # notify the developer that the class that they are using is not saveable
            return False
        
            
    def returnSettings(self,var, checkIfPickleable=True): ## parses through objects returning if they can be saved or not and collecting their settings.
        settings = {}
        # from redRGUI import qtWidgetBox
        from redRGUI import widgetState
        # from redRGUI import widgetState
        from signals import BaseRedRVariable
        # print 'var class', var.__class__.__name__, isinstance(var, BaseRedRVariable), issubclass(var.__class__,BaseRedRVariable)
        if isinstance(var, widgetState):
            # print 'getting gui settings\n\n'
            # try:
            v = {}
            v = var.getSettings()
            if v == None:
                v = var.getDefaultState()
            else:
                v.update(var.getDefaultState())
            # except: 
                # v = var.getDefaultState()
                # redRLog.log(redRLog.REDRCORE, redRLog.ERROR, 'Could not save qtWidgets class ' + var.__class__.__name__ + '.')
                #errorMsg='Could not save qtWidgets class ' + var.__class__.__name__ + '.')

            settings['redRGUIObject'] = {}
            if v: settings['redRGUIObject'] = v
        #elif isinstance(var, signals.BaseRedRVariable):
        elif isinstance(var, BaseRedRVariable) or issubclass(var.__class__,BaseRedRVariable) :
            settings['signalsObject'] = var.saveSettings()
            #print '|#| Saving signalsObject '#, settings['signalsObject']
        elif not checkIfPickleable: 
            settings['pythonObject'] =  var
        elif self.isPickleable(var):
            settings['pythonObject'] =  var
        elif type(var) in [list]:
           settings['list'] = []
           for i in var:
               settings['list'].append(self.returnSettings(i))
        elif type(var) is dict:
           #print var
           settings['dict'] = {}
           for k,v in var.iteritems():
               settings['dict'][k] = self.returnSettings(v)
        else:
            #print '#####################\n\nNo settings saved for %s\n\n############' % var
            settings = None
        return settings
    def processSentItems(self):
        ## make a list of the signal keys and the values of all of the sent items, shouldn't be hard
        items = []
        for (key, item) in self.outputs.getAllOutputs().items():
            if item['value']:
                items.append((key, item['value'].saveSettings()))

        return items
        
        
    def setSettings(self,settings, globalSettings = False):
        redRLog.log(redRLog.REDRCORE, redRLog.DEBUG, 'Loading settings')
        #settings = self.sqlite.setObject(settingsID)
        # import pprint
        # pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(settings)
        for k,v in settings.iteritems():
            try:
                #redRLog.log(redRLog.REDRCORE, redRLog.ERROR, 'Loading %s' % k)
                if k in ['inputs', 'outputs']: continue
                if v == None:
                    continue
                elif 'pythonObject' in v.keys():
                    #print '|#| Setting pythonObject %s to %s' % (k,unicode(v['pythonObject']))
                    self.__setattr__(k, v['pythonObject'])
                elif 'signalsObject' in v.keys():
                    #print '|#| Setting signalsObject'
                    varClass = self.setSignalClass(v['signalsObject'])
                    self.__setattr__(k, varClass)
                elif 'sentItemsList' in v.keys():
                    #print '|#| settingItemsList'
                    # print v['sentItemsList']
                    #self.setSentItemsList(v['sentItemsList'])        
                    for (sentItemName, sentItemDict) in v['sentItemsList']:
                        #print '|#| setting sent items %s to %s' % (sentItemName, unicode(sentItemDict))
                        #for kk,vv in sentItemDict.items():
                        var = self.setSignalClass(sentItemDict)
                        ## add compatibility layer for the case that the sent item name is not longer in existance or has changed
                        if sentItemName in self.outputs.outputIDs():
                            self.send(sentItemName, var)
                        else:
                            signalItemNames = [name for (key, name) in self.outputs.outputNames().items()]
                            if sentItemName in signalItemNames:
                                signalID = self.outputs.getSignalByName(sentItemName)
                                self.send(signalID, var)
                            else:
                                #print 'Error in matching item name'
                                from libraries.base.qtWidgets.dialog import dialog
                                tempDialog = dialog(None)
                                from libraries.base.qtWidgets.widgetLabel import widgetLabel
                                from libraries.base.qtWidgets.listBox import listBox
                                from libraries.base.qtWidgets.button import button
                                widgetLabel(tempDialog, 'Error occured in matching the loaded signal (Name:%s, Value:%s) to the appropriate signal name.\nPlease select the signal that matches the desired output,\n or press cancel to abandon the signal.' % (sentItemName, unicode(var)))
                                
                                #print self.outputs.outputSignals
                                itemListBox = listBox(tempDialog, items = signalItemNames)
                                button(tempDialog, label = 'Done', callback = tempDialog.accept)
                                button(tempDialog, label = 'Cancel', callback = tempDialog.reject)
                                res = tempDialog.exec_()
                                if res != QDialog.rejected:
                                    signalName = unicode(itemListBox.selectedItems()[0].text())
                                    signalID = self.outputs.getSignalByName(signalName)
                                    self.send(signalID, var)
    #############################################
                elif not hasattr(self,k):
                    continue
                elif 'redRGUIObject' in v.keys():
                    #print getattr(self, k)
                    try:
                        getattr(self, k).loadSettings(v['redRGUIObject'])
                        getattr(self, k).setDefaultState(v['redRGUIObject'])
                    except Exception as inst:
                        #print 'Exception occured during loading of settings.  These settings may not be the same as when the widget was closed.'
                        redRLog.log(redRLog.REDRCORE, redRLog.ERROR,redRLog.formatException())
                elif 'dict' in v.keys():
                    var = getattr(self, k)
                    #print 'dict',len(var),len(v['dict'])
                    if len(var) != len(v['dict']): continue
                    self.recursiveSetSetting(var,v['dict'])
                elif 'list' in v.keys():
                    var = getattr(self, k)
                    # print 'list',len(var),len(v['list'])
                    if len(var) != len(v['list']): continue
                    self.recursiveSetSetting(var,v['list'])
            except:
                redRLog.log(redRLog.REDRCORE, redRLog.ERROR, 'Exception occured during loading. The Error will be ignored.')
                redRLog.log(redRLog.REDRCORE, redRLog.DEBUG, redRLog.formatException())
        
        
    def setSignalClass(self, d):
        #print '|##| setSentRvarClass' #% unicode(d)
        
        # print d
        # print 'setting ', className
        try: # try to reload the output class from the signals
            
            # try to get the class variabel (var) this will be done by accessing the class info of the class attribute of data
            import imp
            ## find the libraries directory
            fp, pathname, description = imp.find_module('libraries', [redREnviron.directoryNames['redRDir']])
            #print 'loading module'
            varc = imp.load_module('libraries', fp, pathname, description)
            #print varc
            for mod in d['class'].split('.')[1:]:
                #print varc
                varc = getattr(varc, mod)
            var = varc(data = d['data']) 
            var.loadSettings(d)
            
        except: # if it doesn't exist we need to set the class something so we look to the outputs. 
            ## kick over to compatibility layer to add the settings. for 175 attributes
            redRLog.log(redRLog.REDRCORE, redRLog.ERROR, redRLog.formatException())
            try:
                for (key, val) in d.items():
                    ## find the libraries directory
                    fp, pathname, description = imp.find_module('libraries', [redREnviron.directoryNames['redRDir']])
                    #print 'loading module'
                    varc = imp.load_module('libraries', fp, pathname, description)
                    #print varc
                    for mod in val['class'].split('.')[1:]:
                        #print varc
                        varc = getattr(varc, mod)
                    var = varc(data = val['data']) 
                    var.loadSettings(val)
                    if fp:
                        fp.close()
            except:
                #print 'something is really wrong we need to set some kind of data so let\'s set it to the signals.RVariable'
                redRLog.log(redRLog.REDRCORE, redRLog.ERROR,redRLog.formatException())
                
                try:
                    var = signals.BaseRedRVariable(data = d['data']['data'], checkVal = False)
                except: ## fatal exception, there is no data in the data slot (the signal must not have data) we can't do anything so we except...
                    redRLog.log(redRLog.REDRCORE, redRLog.ERROR,redRLog.formatException())
                    #print 'Fatal exception in loading.  Can\'t assign the signal value'
                    var = None
        finally:
            if fp:
                fp.close()
        return var
            
    def recursiveSetSetting(self,var,d):
        # print 'recursiveSetSetting'
        
        if type(var) in [list,tuple]:
            for k in xrange(len(d)):
                if type(d[k]) is dict and 'redRGUIObject' in d[k].keys():
                    var[k].loadSettings(d[k]['redRGUIObject'])
                    var[k].setDefaultState(d[k]['redRGUIObject'])
                else:
                    self.recursiveSetSetting(var[k],d[k])
        elif type(var) is dict:
            for k,v in d.iteritems():
                if type(v) is dict and 'redRGUIObject' in v.keys():
                    var[k].loadSettings(v['redRGUIObject'])
                    var[k].setDefaultState(v['redRGUIObject'])
                else:
                    self.recursiveSetSetting(var[k],d[k])
        
    def loadCustomSettings(self,settings=None):
        pass

#############widget specific settings#####################
        ##########set global settings#############
    def loadGlobalSettings(self):
        file = self.getGlobalSettingsFile()
        if not file: return 
        try:
            file = open(file, "r")
            settings = cPickle.load(file)
            self.setSettings(settings, globalSettings = True)
        except:
            redRLog.log(redRLog.REDRCORE, redRLog.ERROR, redRLog.formatException())
            pass
        
    
    def getGlobalSettingsFile(self):
        # print 'getSettingsFile in owbasewidget'
        file = os.path.join(redREnviron.directoryNames['widgetSettingsDir'], self._widgetInfo.fileName + ".ini")
        if os.path.exists(file): return file
        else: return False

    
    # save global settings
    def saveGlobalSettings(self):
        #print '|#| owrpy global save settings'
        settings = {}
        
        if hasattr(self, "globalSettingsList"):
            self.globalSettingsList.extend(self.defaultGlobalSettingsList)
        else:
            self.globalSettingsList =  self.defaultGlobalSettingsList
        print self.globalSettingsList
        for name in self.globalSettingsList:
            #try:
            settings[name] = self.returnSettings(getattr(self,name),checkIfPickleable=False)
            #except:
            #   print "Attribute %s not found in %s widget. Remove it from the settings list." % (name, self._widgetInfo.widgetName)
        #print '%s' % unicode(settings)
        if settings:
            #settingsID = self.sqlite.saveObject(settings)
            file = self.getGlobalSettingsFile()
            file = open(file, "w")
            cPickle.dump(settings, file)
        
        #print '|#| owrpy global save settings done'

