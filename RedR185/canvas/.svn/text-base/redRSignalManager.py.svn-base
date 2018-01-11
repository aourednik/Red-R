from PyQt4.QtCore import *
from PyQt4.QtGui import *
import orngDoc, redRObjects, redRLog
import redRi18n
# def _(a):
    # return a
_ = redRi18n.Coreget_()
class OutputHandler:
    def __init__(self, parent):                         ## set up the outputHandler, this will take care of sending signals to 
        self.outputSignals = {}
        self.connections = {}
        self.parent = parent # the parent that owns the OutputHandler
    def getAllOutputs(self):
        return self.outputSignals
    def addOutput(self, id, name, signalClass):
        self.outputSignals[id] = {'name':name, 'signalClass':signalClass, 'connections':{}, 'value':None, 'parent':self.parent, 'sid':id}   # set up an 'empty' signal
    def clearAll(self):
        for id, outputSignal in self.outputSignals.items():
            val = outputSignal['value']
            if val == None: continue
            val.deleteSignal() # calls the distructor function for the signal
        self.outputSignals = {}
        self.connections = {}
    def connectSignal(self, signal, id, enabled = 1, process = True):
        try:
            redRLog.log(redRLog.REDRCORE, redRLog.DEBUG, _('Trying to connect signal and process.'))
            if id not in self.outputSignals.keys():
                redRLog.log(redRLog.REDRCORE, redRLog.WARNING, _('Signal Manager connectSignal: id not in output keys'))
                return False
            if not signal or signal == None:
                redRLog.log(redRLog.REDRCORE, redRLog.WARNING, _('Signal Manager connectSignal: no signal or signal is None'))
                return False
            self.outputSignals[id]['connections'][signal['id']] = {'signal':signal, 'enabled':enabled}
            # now send data through
            signal['parent'].inputs.addLink(signal['sid'], self.getSignal(id))
            redRObjects.addLine(self.parent, signal['parent'])
            if process:
                #print _('processing signal')
                self._processSingle(self.outputSignals[id], self.outputSignals[id]['connections'][signal['id']])
            return True
        except Exception as inst:
            redRLog.log(redRLog.REDRCORE, redRLog.ERROR, redRLog.formatException())
            redRLog.log(redRLog.REDRCORE, redRLog.ERROR, _('redRSignalManager connectSignal: error in connecting signal %s') % unicode(inst))
            return False
        redRLog.logConnection(self.parent.widgetInfo.fileName, signal['parent'].widgetInfo.fileName)
        redRObjects.updateLines()
    def outputIDs(self):
        return self.outputSignals.keys()
    def outputNames(self):
        out = {}
        for key, value in self.outputSignals.items():
            out[key] = value['name']
        return out
    def outputValues(self):
        out = {}
        for key, value in self.outputSignals.items():
            out[key] = value['value']
        return out
    def removeSignal(self, signal, id):
        redRLog.log(redRLog.REDRCORE, redRLog.DEBUG, _('Removing signal %s, %s') % (signal, id))
        ## send None through the signal to the handler before we disconnect it.
        if signal['id'] in self.outputSignals[id]['connections'].keys():                                 # check if the signal is there to begin with otherwise we don't do anything
            try:
                if self.outputSignals[id]['connections'][signal['id']]['signal']['multiple']:
                    self.outputSignals[id]['connections'][signal['id']]['signal']['handler'](
                        #self.outputSignals[signalName]['value'],
                        None,
                        self.parent.widgetID
                        )
                else:
                    self.outputSignals[id]['connections'][signal['id']]['signal']['handler'](
                        #self.outputSignals[signalName]['value']
                        None
                        )
            except:
                redRLog.log(redRLog.REDRCORE, redRLog.ERROR, redRLog.formatException())
                pass
            finally:
                ## remove the signal from the outputSignals
                del self.outputSignals[id]['connections'][signal['id']]
                signal['parent'].inputs.removeLink(signal['sid'], self.getSignal(id))
                # res = QMessageBox.question(None, _('Signal Propogation'), 'A signal is being removed, do you want to send No data through all downstream widgets?\nThis will remove any analysis done in downstream widgets.', QMessageBox.Yes | QMessageBox.No)
                # if res != QMessageBox.Yes: 
                    # print _('Deletion rejected')
                    # return
                #print _('propogating None in widgets')
                try:
                    signal['parent'].outputs.propogateNone()
                except:
                    redRLog.log(redRLog.REDRCORE, redRLog.ERROR, redRLog.formatException())
                    pass
    def setOutputData(self, signalName, value):
        self.outputSignals[signalName]['value'] = value
        
    def signalLinkExists(self, widget):
        ## move across the signals and determine if there is a link to the specified widget
        for id in self.outputSignals.keys():
            for con in self.outputSignals[id]['connections'].keys():
                if self.outputSignals[id]['connections'][con]['signal']['parent'] == widget:
                    return True
                    
        return False
        
    def getLinkPairs(self, widget):
        pairs = []
        for id in self.outputSignals.keys():
            for con in self.outputSignals[id]['connections'].keys():
                if self.outputSignals[id]['connections'][con]['signal']['parent'] == widget:
                    pairs.append((id, self.outputSignals[id]['connections'][con]['signal']['sid']))
        return pairs
    def getSignalLinks(self, widget):
        ## move across the signals and determine if there is a link to the specified widget
        links = []
        for id in self.outputSignals.keys():
            for con in self.outputSignals[id]['connections'].keys():
                if self.outputSignals[id]['connections'][con]['signal']['parent'] == widget:
                    links.append((id, self.outputSignals[id]['connections'][con]['signal']['sid']))
                    
        return links
    def getAllSignalLinksSignals(self):
        links = []
        for id in self.outputSignals.keys():
            for con in self.outputSignals[id]['connections'].keys():
                links.append(self.outputSignals[id]['connections'][con])
                    
        return links
    def getWidgetConnections(self, widget):
        links = []
        for id in self.outputSignals.keys():
            for con in self.outputSignals[id]['connections'].keys():
                if self.outputSignals[id]['connections'][con]['signal']['parent'] == widget:
                    links.append(self.outputSignals[id]['connections'][con])
                    
        return links
    def getSignal(self, id):
        if id in self.outputSignals.keys():
            return self.outputSignals[id]
        else:
            return None
    def setSignalEnabled(self, inWidget, enabled):
        for (name, value) in self.outputSignals.items():
            for (conName, conValue) in value['connections'].items():
                if inWidget == conValue['signal']['parent']:
                    conValue['enabled'] = enabled
    def isSignalEnabled(self, inWidget):
        for (name, value) in self.outputSignals.items():
            for (conName, conValue) in value['connections'].items():
                if inWidget == conValue['signal']['parent'] and conValue['enabled']:
                    return True
        return False
    def _processSingle(self, signal, connection):
        try:
            #print signal
            if not connection['enabled']: return 0
            handler = connection['signal']['handler']
            multiple = connection['signal']['multiple']
            #print '\n\n\n', connection['signal']['signalClass'], '\n\n\n'
            #print '\n\n\n', 'Signal Value is\n', signal['value'], '\n\n\n'
            if signal['value'] == None: # if there is no data then it doesn't matter what the signal class is, becase none will be sent anyway
                self._handleSignal(signal['value'], handler, multiple, connection['signal']['parent']) 
                self._handleNone(connection['signal']['parent'], connection['signal']['sid'], True)
                self._handleDirty(connection['signal']['parent'], connection['signal']['sid'], False)  ## undo the dirty signal
            elif signal['signalClass'] == 'All' or 'All' in connection['signal']['signalClass']:
                #print '\n\n\nprocessing signal %s using handler: %s with multiple: %s\n\n\n\n' % (signal['value'], handler, multiple)
                self._handleSignal(signal['value'], handler, multiple, connection['signal']['parent']) 
                self._handleDirty(connection['signal']['parent'], connection['signal']['sid'], False)  ## undo the dirty signal
                self._handleNone(connection['signal']['parent'], connection['signal']['sid'], False)   ## indicate that the signal doesn't have a None
            elif signal['signalClass'] in connection['signal']['signalClass']:
                self._handleSignal(signal['value'], handler, multiple, connection['signal']['parent'])
                self._handleDirty(connection['signal']['parent'], connection['signal']['sid'], False)  ## undo the dirty signal
                self._handleNone(connection['signal']['parent'], connection['signal']['sid'], False)   ## indicate that the signal doesn't have a None
            else:
                sentSignal = False
                for sig in connection['signal']['signalClass']:
                    try:
                        if sig in signal['signalClass'].convertToList:
                            newVal = signal['value'].convertToClass(sig)
                            self._handleSignal(newVal, handler, multiple, connection['signal']['parent'])
                            self._handleDirty(connection['signal']['parent'], connection['signal']['sid'], False)  ## undo the dirty signal
                            self._handleNone(connection['signal']['parent'], connection['signal']['sid'], False)   ## indicate that the signal doesn't have a None
                            connection['signal']['value'] = newVal
                            sentSignal = True
                            break
                        elif signal['signalClass'] in sig.convertFromList:
                            tempSignal = sig(data = '', checkVal = False)                       ## make a temp holder to handle the processing.
                            newVal = tempSignal.convertFromClass(signal['value'])
                            self._handleSignal(newVal, handler, multiple, connection['signal']['parent'])
                            self._handleDirty(connection['signal']['parent'], connection['signal']['sid'], False)  ## undo the dirty signal
                            self._handleNone(connection['signal']['parent'], connection['signal']['sid'], False)   ## indicate that the signal doesn't have a None
                            connection['signal']['value'] = newVal
                            sentSignal = True
                            break
                    except:
                        redRLog.log(redRLog.REDRCORE, redRLog.ERROR,redRLog.formatException())
                if sentSignal == False:
                    ## we made it this far and the signal is still not sent.  The user must have allowed this to get this far so we send the signal anyway.
                    self._handleSignal(signal['value'], handler, multiple, connection['signal']['parent'])
                    self._handleDirty(connection['signal']['parent'], connection['signal']['sid'], False)  ## undo the dirty signal
                    self._handleNone(connection['signal']['parent'], connection['signal']['sid'], False)   ## indicate that the signal doesn't have a None
        except:
            redRLog.log(redRLog.REDRCORE, redRLog.ERROR,redRLog.formatException())
            
    def processData(self, id):
        # collect the signal ID
        signal = self.getSignal(id)
        
        # collect the connections
        connections = signal['connections']
        
        ## mark signals as dirty, this should happen before processing any data
        for cKey in connections.keys():
            self._markDirty(connections[cKey])
        ## update the canvas to indicate that the signal is not dirty any more
        
        ## handle conversions and send data.
        for cKey in connections.keys():
            self._processSingle(signal, connections[cKey])
    def markAllDirty(self):
        return
        ## step one, get all of the connections
        cons = self.getAllSignalLinksSignals() ## gets all of the signals attached to any output signal
        for c in cons:
            self._markDirty(c)
    def _markDirty(self, connection):
        return
        #print 'Connection\n',connection, '\n\n'
        
        parent = connection['signal']['parent']
        id = connection['signal']['sid']
        #self._handleDirty(parent, id, dirty = True)
    def _handleDirty(self, parentWidget, id, dirty):
        return
    def _handleNone(self, parentWidget, id, none):
        parentWidget.inputs.markNone(id, none)
        links = self.getWidgetConnections(parentWidget)
        lines = redRObjects.getLinesByInstanceIDs(self.parent.widgetID, parentWidget.widgetID)
        for line in lines:
            #print _('The line is '), line, _('the signal is '), none
            for l in links:
                if parentWidget.inputs.getSignal(l['signal']['sid'])['none']:
                    line.setNoData(True)
                    redRObjects.activeCanvas().update()
                    return
                else:
                    line.setNoData(False)
                    redRObjects.activeCanvas().update()
    def _handleSignal(self, value, handler, multiple, parentWidget):
        try:
            if multiple:
                handler(value, self.parent.widgetID)
            else:   
                handler(value)
            parentWidget.status.setText(_('New Data Received'))
            parentWidget.removeWarning(id = 'signalHandlerWarning')
        except:
            
            error = _("Error occured in processing signal in this widget.\nPlease check the widgets.\n")
            parentWidget.setWarning(id = 'signalHandlerWarning', text = unicode(error))
            #print error
            redRLog.log(redRLog.REDRCORE, redRLog.ERROR,redRLog.formatException())
            parentWidget.status.setText(_('Error in processing signal'))
            
    def hasOutputName(self, name):
        return name in self.outputSignals.keys()
    def getSignalByName(self, name):
        for signal in self.outputSignals.keys():
            fullSignal = self.outputSignals[signal]
            if fullSignal['name'] == name:
                return signal
            
    ########  Loading and Saving ##############
    
    def returnOutputs(self):
        ## move through the outputs and return a list of outputs and connections.  these connections should be reconnected on reloading of the widget, ideally we will only put atomics into this outputHandler
        data = {}
        for (key, value) in self.outputSignals.items():
            
            data[key] = {'name':value['name'], 'signalClass':unicode(value['signalClass']), 'connections':{}}
            if value['value']:
                data[key]['value'] = value['value'].saveSettings()
            else:
                data[key]['value'] = None
            for (vKey, vValue) in value['connections'].items():
                data[key]['connections'][vKey] = {'id':vValue['signal']['sid'], 'parentID':vValue['signal']['parent'].widgetID, 'enabled':vValue['enabled']} ## now we know the widgetId and the signalID (sid) used for connecting widgets in the future.
                
            
        return data
    def setOutputs(self, data, tmp = False):
        for (key, value) in data.items():
            if key not in self.outputSignals.keys():
                #print _('Signal does not exist')
                continue
            ## find the signal from the widget and connect it
            for (vKey, vValue) in value['connections'].items():
                ### find the widget
                if not tmp:
                    widget = redRObjects.getWidgetInstanceByID(vValue['parentID'])
                elif tmp:
                    widget = redRObjects.getWidgetInstanceByTempID(vValue['parentID'])
                redRLog.log(redRLog.REDRCORE, redRLog.DEBUG, 'Widget is %s' % widget)
                if not widget:
                    redRLog.log(redRLog.REDRCORE, redRLog.DEBUG, 'Failed to find widget %s' % vValue['parentID'])
                    return
                inputSignal = widget.inputs.getSignal(vValue['id'])
                self.connectSignal(inputSignal, key, vValue['enabled'], process = False)  # connect the signal but don't send data through it.
                if tmp:
                    self.propogateNone(ask = False)
    def linkingWidgets(self):
        widgets = []
        for (i, s) in self.outputSignals.items():
            for (id, ls) in s['connections'].items():
                if ls['signal']['parent'] not in widgets:
                    widgets.append(ls['signal']['parent'])
        return widgets
    def propogateNone(self, ask = True):    
        ## send None through all of my output channels
        redRLog.log(redRLog.REDRCORE, redRLog.DEBUG, _('Propagating None through signal'))
        for id in self.outputIDs():
            #print 'None sent in widget %s through id %s' % (self.parent.widgetID, id)
            self.parent.send(id, None)
        
        ## identify all of the downstream widgets and send none through them, then propogateNone in their inputs
        
        dWidgets = self.linkingWidgets()
        #print dWidgets
        ## send None through all of the channels
        for w in dWidgets:
            w.outputs.propogateNone(ask = False)
    def propogateDirty(self):
        ## tell all connected widgets to set their signals to be dirty
        dWidgets = self.linkingWidgets()
        for w in dWidgets:
            w.propogateDirty()
            
    
class InputHandler:
    def __init__(self, parent):
        self.inputs = {}
        self.links = {}
        self.parent = parent # the parent widget that owns the InputHandler
    def getAllInputs(self):
        return self.inputs
    def addInput(self, id, name, signalClass, handler, multiple = False):
        if type(signalClass) not in [list]:
            signalClass = [signalClass]
        self.inputs[id] = {
            'value': None,                                      ## should only be set by an outputHandler 
            'name':name,
            'signalClass':signalClass,
            'handler':handler,
            'multiple':multiple,
            'sid':id, 
            'id':unicode(id)+'_'+self.parent.widgetID, 
            'parent':self.parent,
            'dirty':False,
            'none': False}
    def markDirty(self, id, dirty = True): # mark an input as dirty
        self.inputs[id]['dirty'] = dirty
        if dirty:
            self.propogateDirty() ## if an in signal is dirty then the out signals should also be dirty.
    def markNone(self, id, none = True):
        self.inputs[id]['none'] = none  ## if a signal has none then it needs to be set to show red.
    def dirty(self):                        # check if inputs are dirty
        for k, i in self.inputs.items():
            if i['dirty']: return True
        return False
    def clean(self):                        # check if inputs are clean (opposite of dirty)
        return not self.dirty()
    def propogateDirty(self):
        self.parent.outputs.markAllDirty()
    def signalIDs(self):
        return self.inputs.keys()

    def getSignal(self, id):
        if id in self.inputs.keys():
            return self.inputs[id]
        else:
            return None
    def matchConnections(self, outputHandler):
        ## determine if there are any valid matches between the signal handlers
        for outputKey in outputHandler.outputSignals.keys():
            for inputKey in self.inputs.keys():
                OSignalClass = outputHandler.outputSignals[outputKey]['signalClass']
                for ISignalClass in self.inputs[inputKey]['signalClass']:
                    if OSignalClass == 'All' or ISignalClass == 'All':
                        return True
                    elif OSignalClass == ISignalClass:
                        return True
                    elif 'convertToList' in dir(OSignalClass) and ISignalClass in OSignalClass.convertToList:
                        return True
                    elif 'convertFromList' in dir(ISignalClass) and OSignalClass in ISignalClass.convertFromList:
                        return True
                    # else:
                        # print OSignalClass
                        # print ISignalClass
                        
                        # print unicode(OSignalClass.convertToList)
                        # print unicode(ISignalClass.convertFromList)
        return False
        
    def getPossibleConnections(self, outputHandler):
        ## determine if there are any valid matches between the signal handlers
        connections = []
        for outputKey in outputHandler.outputSignals.keys():
            for inputKey in self.inputs.keys():
                OSignalClass = outputHandler.outputSignals[outputKey]['signalClass']
                for ISignalClass in self.inputs[inputKey]['signalClass']:
                    if OSignalClass == 'All' or ISignalClass == 'All':
                        connections.append((outputKey, inputKey))
                        break
                    elif OSignalClass == ISignalClass:
                        connections.append((outputKey, inputKey))
                        break
                    elif 'convertToList' in dir(OSignalClass) and ISignalClass in OSignalClass.convertToList:
                        connections.append((outputKey, inputKey))
                        break
                    elif 'convertFromList' in dir(ISignalClass) and OSignalClass in ISignalClass.convertFromList:
                        connections.append((outputKey, inputKey))
                        break
        return connections
    def doesSignalMatch(self, id, signalClass):
        if signalClass == 'All': return True
        elif 'All' in self.getSignal(id)['signalClass']: return True
        elif signalClass in self.getSignal(id)['signalClass']: return True
        for s in self.getSignal(id)['signalClass']:
            if s in signalClass.convertToList:
                return True
            else:
                if signalClass in s.convertFromList:
                    return True
                    
        return False
    def addLink(self, sid, signal):
        if sid not in self.links.keys():
            self.links[sid] = []
        if self.getSignal(sid)['multiple']:
            self.links[sid].append(signal)
        else:
            for link in self.links[sid]:
                link['parent'].removeSignal(self.getSignal(sid), link['sid'])
            self.links[sid].append(signal)
    def removeLink(self, sid, signal):
        if sid not in self.links.keys(): return
        self.links[sid].remove(signal)
        
    
    def getLinks(self, sid):
        if sid not in self.links.keys():
            self.links[sid] = []
        return self.links[sid]
    ######### Loading and Saving ##############
    def returnInputs(self):
        return None  ## no real reason to return any of this becasue the outputHandler does all the signal work
        