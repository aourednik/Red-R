# Major modifications Anup Parikh
# OWWidget.py
# Orange Widget
# A General Orange Widget, from which all the Orange Widgets are derived
#
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import signals
from string import *
from orngSignalManager import *
import signals
from redRSignalManager import *
import orngDoc, redRLog, redRObjects, redRi18n

# def _(a):
    # return a
_ = redRi18n.Coreget_()
class widgetSignals():
    def __init__(self, parent = None, signalManager = None):
        # do we want to save widget position and restore it on next load
        

        # number of control signals, that are currently being processed
        # needed by signalWrapper to know when everything was sent
        # self.parent = parent
        self.needProcessing = 0     # used by signalManager
        if not signalManager: self.signalManager = globalSignalManager        # use the global instance of signalManager  - not advised
        else:                 self.signalManager = signalManager              # use given instance of signal manager

        self.working = 0     #used to monitor when the widget is working.  Other widgets can check this to supress functions or to check on up/down stream widgets.
        self.linksOutWidgets = {}
        self.inputs = InputHandler(self)     # signalName:(dataType, handler, onlySingleConnection)
        self.outputs = OutputHandler(self)    # signalName: dataType
        self.wrappers =[]    # stored wrappers for widget events
        self.linksIn = {}      # signalName : (dirty, widgetFrom, handler, signalData)
        self.linksOut = {}       # signalName: (signalData, id)
        self.connections = {}   # dictionary where keys are (control, signal) and values are wrapper instances. Used in connect/disconnect
        # self.controlledAttributes = ControlledAttributesDict(self)
        self.closing = False # is the widget closing, if so don't process any signals
        self.loadSavedSession = False # is the widget closing, if so don't process any signals
        # self.sentItems = []
        self.eventHandler = None


    def send(self, signalName, value):
        ## make sure that the name is actually in the outputs, if not throw an error.
        if not self.outputs.hasOutputName(signalName):
            redRLog.log(redRLog.REDRCORE, redRLog.ERROR, _("Warning! Signal '%s' is not a valid signal name for the '%s' widget. Please fix the signal name.") % (signalName, self.captionTitle))
            raise Exception(_('Signal name mismatch'))
        self.outputs.setOutputData(signalName, value)
        self.outputs.processData(signalName)
        ## clear the warnings, info, and errors
        self.removeError()
        self.removeInformation()
        self.removeWarning()
        self.refreshToolTips()
        self.ROutput.setCursorToEnd()
        self.ROutput.append(_('\n##Data sent through the %s channel\n') % unicode(self.outputs.outputNames()[signalName])) #Keep track automatically of what R functions were performed.
        
        redRObjects.updateLines()
    def refreshToolTips(self):
        lines = redRObjects.lines()
        for l in lines.values():

            if l.outWidget.instance() == self:
                l.refreshToolTip()
    def callSignalDelete(self, name):
        if self.linksOut.has_key(name):
        
            for id in self.linksOut[name]:
                try:
                    self.linksOut[name][id].deleteSignal()
                except Exception as inst:
                    redRLog.log(redRLog.REDRCORE, redRLog.ERROR, redRLog.formatException())
        
    def rSend(self, name, variable, updateSignalProcessingManager = 1):
        #print 'send from:', self.windowTitle(),  '; signal:', name, '; data:', variable
        try:
            self.callSignalDelete(name)
            self.send(name, variable)
            self.removeInformation(id = 'attention')
            self.removeError()
            #self.sentItems.append((name, variable))
            self.status.setStatus(2)
        except:
            self.setError(id = 'sendError', text = _('Failed to send data'))
            redRLog.log(redRLog.REDRCORE,redRLog.CRITICAL,redRLog.formatException())
            self.status.setStatus(3)
        
        self.R('gc()', wantType = 'NoConversion')
        redRLog.log(redRLog.REDRWIDGET,redRLog.INFO,_('Data sent from slot %s') % name)

    # does widget have a signal with name in inputs
    def hasInputName(self, name):
        for input in self.inputs:
            if name == input[0]: return 1
        return 0

    # does widget have a signal with name in outputs
    def hasOutputName(self, name):
        for output in self.outputs:
            if name == output[0]: return 1
        return 0

    def getInputType(self, signalName):
        for input in self.inputs:
            if input[0] == signalName: return input[1]
        return None

    def getOutputType(self, signalName):
        for output in self.outputs:
            if output[0] == signalName: return output[1]
        return None
    """
    # ########################################################################
    def connect(self, control, signal, method):
        wrapper = SignalWrapper(self, method)
        self.connections[(control, signal)] = wrapper   # save for possible disconnect
        self.wrappers.append(wrapper)
        QMainWindow.connect(control, signal, wrapper)
        #QWidget.connect(control, signal, method)        # ordinary connection useful for dialogs and windows that don't send signals to other widgets


    def disconnect(self, control, signal, method=None):
        wrapper = self.connections[(control, signal)]
        QMainWindow.disconnect(control, signal, wrapper)
    """
    """
    def getConnectionMethod(self, control, signal):
        if (control, signal) in self.connections:
            wrapper = self.connections[(control, signal)]
            return wrapper.method
        else:
            return None


    def signalIsOnlySingleConnection(self, signalName):
        for i in self.inputs:
            input = InputSignal(*i)
            if input.name == signalName: return input.single
    
    def addOutputConnection(self, widgetTo, signalName):
        existing = []
        if self.linksOutWidgets.has_key(signalName):
            existing = self.linksOutWidgets[signalName]
            existing.append(widgetTo)
        else:
            self.linksOutWidgets[signalName] = [widgetTo]
    def addInputConnection(self, widgetFrom, signalName):
        for i in range(len(self.inputs)):
            if self.inputs[i][0] == signalName:
                handler = self.inputs[i][2]
                break

        existing = []
        if self.linksIn.has_key(signalName):
            existing = self.linksIn[signalName]
            for (dirty, widget, handler, data) in existing:
                if widget == widgetFrom: return             # no need to add new tuple, since one from the same widget already exists
        self.linksIn[signalName] = existing + [(0, widgetFrom, handler, [])]    # (dirty, handler, signalData)
        #if not self.linksIn.has_key(signalName): self.linksIn[signalName] = [(0, widgetFrom, handler, [])]    # (dirty, handler, signalData)

    
    def removeOutputConnection(self, widgetTo, signalName):
        if self.linksOutWidgets.has_key(signalName):
            links = self.linksOutWidgets[signalName]
            links.remove(widgetTo)
            self.linksOutWidgets[signalName] = links
            
        
    def removeInputConnection(self, widgetFrom, signalName):
        if self.linksIn.has_key(signalName):
            links = self.linksIn[signalName]
            for i in range(len(self.linksIn[signalName])):
                if widgetFrom == self.linksIn[signalName][i][1]:
                    self.linksIn[signalName].remove(self.linksIn[signalName][i])
                    if self.linksIn[signalName] == []:  # if key is empty, delete key value
                        del self.linksIn[signalName]
        self.processSignals()

    # return widget, that is already connected to this singlelink signal. If this widget exists, the connection will be deleted (since this is only single connection link)
    def removeExistingSingleLink(self, signal):
        #print unicode(self.inputs)
        #print unicode(self.outputs)
        for i in self.inputs:
            #print unicode(*i) + _(' input owbasewidget')
            input = InputSignal(*i)
            if input.name == signal and not input.single: return None

        for signalName in self.linksIn.keys():
            if signalName == signal:
                widget = self.linksIn[signalName][0][1]
                del self.linksIn[signalName]
                return widget

        return None

    """
    def handleNewSignals(self):
        # this is called after all new signals have been handled
        # implement this in your widget if you want to process something only after you received multiple signals
        pass

    # signal manager calls this function when all input signals have updated the data
    def setLoadingSavedSession(self,state):
        #print _('setting setloadingSavedSession'), state
        self.loadSavedSession = state

    def processSignals(self, convert = False): ## not called inside of this class 
        #print '|#| processSignals %s' % unicode(self.windowTitle())
        if self.closing == True:
            return
        
        #print '|#| loadSavedSessionState %s' % unicode(self.loadSavedSession)
        if self.loadSavedSession:
            self.needProcessing = 0
            return
        
        
        self.signalManager.setNeedAttention(self)  # don't know what this does exactly
        
        if self.processingHandler: self.processingHandler(self, 1)    # focus on active widget
        newSignal = 0        # did we get any new signals
        self.working = 1
        # we define only a way to handle signals that have defined a handler function
        for signal in self.inputs:        # we go from the first to the last defined input
            key = signal[0]
            if self.linksIn.has_key(key):
                for i in range(len(self.linksIn[key])):
                    (dirty, widgetFrom, handler, signalData) = self.linksIn[key][i]
                    #print dirty,widgetFrom,handler, signalData
                    # print 'data being passed: ' + unicode(signalData)
                     
                    if not (handler and dirty): continue
                    # print _('do the work')
                    newSignal = 1
                    qApp.setOverrideCursor(Qt.WaitCursor)
                    try:
                        for (oldValue, id, nameFrom) in signalData:
                            if oldValue == None:
                                value = oldValue
                            else: # the value had better be one of our signals or a child of one
                                if not isinstance(oldValue, signals.BaseRedRVariable):  ## if not a BaseRedRVariable except
                                    raise Exception, 'Signal not a child of a Red-R signal'
                                
                                if signal[1] != 'All':
                                    #print '|#| CONVERSION of %s to ' % oldValue.__class__, signal[1]
                                    if isinstance(oldValue, signal[1]):
                                        value = oldValue.convertToClass(signal[1])
                                    else:
                                        #try:
                                        value = signal[1](data = '', checkVal = False) ## make a dummy signal to handle the conversion
                                        value = value.convertFromClass(oldValue)
                                        # except:
                                            # raise Exception, _('No conversion function')
                                else:
                                    value = oldValue ## send self with no conversion
                            if self.signalIsOnlySingleConnection(key):
                                #print "ProcessSignals: Calling %s with %s" % (handler, value)
                                handler(value)
                                
                            else:
                                #print "ProcessSignals: Calling %s with %s (ID is %s)" % (handler, value, widgetFrom.widgetID)
                                handler(value, widgetFrom.widgetID)
                            
                    except:
                        thistype, val, traceback = sys.exc_info()
                        #print _('Some exception occured')
                        sys.excepthook(thistype, val, traceback)  # we pretend that we handled the exception, so that we don't crash other widgets
                    qApp.restoreOverrideCursor()

                    self.linksIn[key][i] = (0, widgetFrom, handler, []) # clear the dirty flag

        if newSignal == 1:
            self.handleNewSignals()

        if self.processingHandler:
            self.processingHandler(self, 0)    # remove focus from this widget
            
        self.working = 0
        self.needProcessing = 0

    # set new data from widget widgetFrom for a signal with name signalName
    def updateNewSignalData(self, widgetFrom, signalName, value, id, signalNameFrom):
        #print _('updating new signal data')
        if not self.linksIn.has_key(signalName): return
        for i in range(len(self.linksIn[signalName])):
            (dirty, widget, handler, signalData) = self.linksIn[signalName][i]
            if widget == widgetFrom:
                if self.linksIn[signalName][i][3] == []:
                    self.linksIn[signalName][i] = (1, widget, handler, [(value, id, signalNameFrom)])
                else:
                    found = 0
                    for j in range(len(self.linksIn[signalName][i][3])):
                        (val, ID, nameFrom) = self.linksIn[signalName][i][3][j]
                        if ID == id and nameFrom == signalNameFrom:
                            self.linksIn[signalName][i][3][j] = (value, id, signalNameFrom)
                            found = 1
                    if not found:
                        self.linksIn[signalName][i] = (1, widget, handler, self.linksIn[signalName][i][3] + [(value, id, signalNameFrom)])
        self.needProcessing = 1
        

    def setEventHandler(self, handler):
        self.eventHandler = handler



    # if we are in debug mode print the event into the file
    def printEvent(self, text, eventVerbosity = 1):
        self.signalManager.addEvent(self.captionTitle + ": " + text, eventVerbosity = eventVerbosity)
        if self.eventHandler:
            self.eventHandler(self.captionTitle + ": " + text, eventVerbosity)



