"""
<name>R Executor</name>
<tags>Special, R</tags>
<icon>rexecutor.png</icon>
"""

from OWRpy import *
import redRGUI
from libraries.base.signalClasses.RVariable import RVariable as redRRVariable
from libraries.base.signalClasses.RDataFrame import RDataFrame as redRRDataFrame
from libraries.base.signalClasses.RMatrix import RMatrix as redRRMatrix
from libraries.base.signalClasses.RList import RList as redRRList
from libraries.base.signalClasses.RVector import RVector as redRRVector
from libraries.base.qtWidgets.button import button
from libraries.base.qtWidgets.textEdit import textEdit
from libraries.base.qtWidgets.groupBox import groupBox
from libraries.base.qtWidgets.widgetLabel import widgetLabel
from libraries.base.qtWidgets.lineEdit import lineEdit
from libraries.base.qtWidgets.listBox import listBox
from libraries.base.qtWidgets.widgetBox import widgetBox
import redRi18n
_ = redRi18n.get_(package = 'base')
class rExecutor(OWRpy):
    settingsList = ['command', 'sendthis', 'sendt']
    def __init__(self, parent=None, signalManager=None):
        #OWWidget.__init__(self, parent, signalManager, "Sample Data")
        OWRpy.__init__(self, wantGUIDialog = 1)
        
        self.command = ''
        self.sendthis = ''
        self.sendt = {}
        self.dfselected = None
        self.setRvariableNames(['rExecutor', 'rExecutor_cm'])
        
        
        self.inputs.addInput('id0', _('R.object'), redRRVariable, self.process)

        self.outputs.addOutput('id0', _('R Data Frame'), redRRDataFrame)
        self.outputs.addOutput('id1', _('R List'), redRRList)
        self.outputs.addOutput('id2', _('R Vector'), redRRVector)
        self.outputs.addOutput('id3', _('R.object'), 'All')
        self.outputs.addOutput('id4', _('R Matrix'), redRRMatrix)

        #self.breakme()
        
        #self.help.setHtml('The R Executor widget provides direct access to the R session that runs under RedR.  R Executor can recieve any output from an R compatible widget.  The recieved data can be shown using the Recieved button.  The R history can be shown by pressing the RHistory button and the complete parsing of any recieved data is shown in the Metadata section.  More infromation is available on the <a href="http://www.red-r.org/?cat=10">RedR website</a>.')
        
        #GUI
        
        #GUIDialog
        self.box = groupBox(self.GUIDialog, _("R Executor Advanced"))
        self.infob = widgetLabel(self.box, "")
        
        self.infoa = widgetLabel(self.box, "")
        # grid
        area = widgetBox(self.controlArea, orientation = 'horizontal')
        area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        leftArea = widgetBox(self.box)
        leftArea.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Expanding)
        rightArea = widgetBox(area)

        runbox = groupBox(rightArea, label = _("Command Edit:"), orientation='horizontal')
        runbox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        #self.command = lineEdit(runbox, "", orientation=QHBoxLayout(), callback = self.runR, width = -1)
        self.command = textEdit(runbox, label = _('Command Edit:'))
        #self.command.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        processbutton = button(runbox, label = _("&Run"), callback = self.runR, width=100)
        statusBox = groupBox(rightArea, label = _("Status"))
        self.sendStatus = widgetLabel(statusBox, _('Nothing Sent'))
        self.dataBox = groupBox(leftArea, label = _("Input Infromation"))
        self.mystatus = widgetLabel(self.dataBox, _("No Input"))
        
        # self.metadataBox = widgetBox(leftArea, _("Metadata"))
        # self.infoM = widgetLabel(self.metadataBox, _("No Meta Data"))
        # self.metadataLB = listBox(self.metadataBox, callback = self.insertMetaDataVar)
        varbutton = button(leftArea, _("Recieved"), callback = self.putrecieved, width = 150)
        history = button(leftArea, _("RHistory"), callback = self.putRHistory, width = 150)
        button(leftArea, _("Clear Output"), callback = self.clearOutput)
        
        self.lsList = listBox(self.box, label = _('Available R Items'), items = self.R('ls()', wantType = 'list'), callback = self.addlsList)
        button(self.box, 'Refresh List', callback = self.refreshLsList)

        self.thistext = textEdit(rightArea,label=_('Output'), displayLabel=False)

        sendbutton = button(runbox, label = _("&Send"), toolTip = _('Send the data in the command line into the Red-R schema.'), callback =self.sendThis, width=100)
    def addlsList(self):
        self.command.insertPlainText(unicode(self.lsList.selectedItems()[0].text()))
    def refreshLsList(self):
        self.lsList.update(self.R('ls()', wantType = 'list'))
    def clearOutput(self):
        self.thistext.clear()
    def putrecieved(self):
        self.command.insert(unicode(self.data))
    def sendThis(self):
        if unicode(self.command.textCursor().selectedText()) != '':
                text = unicode(self.command.textCursor().selectedText())
        else:
                self.sendStatus.setText(_('No object Selected'))
                return
        thisdataclass = self.R('class('+unicode(text)+')')
        thisdata = unicode(text)
        # use upclassing to convert to signals class
        if thisdataclass.__class__.__name__ == 'list': #this is a special R type so just send as generic     
            newData = redRRVariable(data = unicode(text))
            self.rSend("id3", newData)
        elif thisdataclass.__class__.__name__ == 'str':
            if thisdataclass in ['numeric', 'character', 'logical']: # we have a numeric vector as the object
                newData = redRRVector(data = unicode(text))
                self.rSend("id2", newData)
                self.sendStatus.setText(thisdata+_(' sent through the R Vector channel'))
            elif thisdataclass in ['data.frame']:
                newData = redRRDataFrame(data = unicode(text))
                self.rSend("id0", newData)
                self.sendStatus.setText(thisdata+_(' sent through the R Data Frame channel'))
            elif thisdataclass in ['matrix']:
                newData = redRRMatrix(data = unicode(text))
                self.rSend("id4", newData)
                self.sendStatus.setText(thisdata+_(' sent through the Matrix channel'))
            elif thisdataclass == 'list': # the object is a list
                for i in range(self.R('length('+text+')')):
                    if self.R('class(%s[[%s]])' % (text, i), silent = True) not in ['numeric', 'character', 'real', 'complex', 'factor']:
                        newData = ral.RArbitraryList(data = self.sendThis)
                        self.status.setText(_('Data sent through the R Arbitrary List channel'))
                        self.rSend('ral', newData)
                        return
                newData = redRRList(data = unicode(text))
                self.rSend("id1", newData)
                self.sendStatus.setText(thisdata+_(' sent through the R List channel'))
            else:    # the data is of a non-normal type send anyway as generic
                newData = redRRVariable(data = unicode(text))
                self.rSend("id3", newData)
                self.sendStatus.setText(thisdata+_(' sent through the R Object channel'))
        else:
            newData = redRRVariable(data = unicode(text))
            self.rSend("id3", newData)
            self.sendStatus.setText(thisdata+' sent through the R Object channel')
    def runR(self):
        #self.R('txt<-"R error occured" #Benign error in case a real error occurs')
        try:
            if unicode(self.command.textCursor().selectedText()) != '':
                text = unicode(self.command.textCursor().selectedText())
            else:
                text = unicode(self.command.toPlainText())
            output = self.R('capture.output(eval(parse(text = \"'+unicode(text).replace('\"', '\\\"')+'\")))', wantType = 'list')

            #pasted = self.R('paste(txt, collapse = " \n")')
            # if type(pasted) != type(''):
                # pasted = 'Error occured with evaluation, please chech output for error.'
            #self.thistext.insertPlainText('>>>'+unicode(text)+'##Done')
            self.thistext.insertPlainText('\n'+'\n'.join(output)+'\n')
            self.thistext.setAlignment(Qt.AlignBottom)
        except Exception as inst:
            self.thistext.insertPlainText(_('Error Occurred: %s') % inst)
    def putRHistory(self):
        self.thistext.clear()
        self.thistext.insertPlainText('\n'.join(OWRpy.globalRHistory))
    def process(self, data):
        for output in self.outputs.outputIDs():
            self.rSend(output, None, 0)
        self.data = ''
        if data:
            self.data = unicode(data.getData())
            self.olddata = data
            
            self.infob.setText(self.data)
            # logic to handle assignment of the data elements
            thisclass = self.R('class('+self.data+')')
            #are there multipe classes for this object?
            if thisclass.__class__.__name__ == 'str': #there is only one class for this object in R
                if thisclass == 'numeric': # we have a numeric vector as the object
                    self.isNumeric()
                elif thisclass == 'character': #we have a character vector as the object
                    self.isCharacter()
                elif thisclass == 'data.frame': # the object is a data.frame
                    self.isDataFrame()
                elif thisclass == 'matrix': # the object is a matrix
                    self.isMatrix()
                elif thisclass == 'list': # the object is a list
                    self.isList()
                else:
                    self.mystatus.setText(_("R object is of non-standard type."))
            if thisclass.__class__.__name__ == 'list': # we need to handle multible classes 
                for item in thisclass:
                    if item == 'numeric': # we have a numeric vector as the object
                        self.isNumeric()
                    elif item == 'character': #we have a character vector as the object
                        self.isCharacter()
                    elif item == 'data.frame': # the object is a data.frame
                        self.isDataFrame()
                    elif item == 'matrix': # the object is a matrix
                        self.isMatrix()
                    elif item == 'list': # the object is a list
                        self.isList()
                    else:
                        self.mystatus.setText(_("R object is of non-standard type."))
                    
        else: return
    
    def isNumeric(self):
        self.mystatus.setText(_("Numeric Vector Connected of length %s") % unicode(self.R('length('+self.data+')')))
    def isCharacter(self):
        self.mystatus.setText(_("Character Vector Connected of length %s") % unicode(self.R('length('+self.data+')')))
    def isDataFrame(self):
        self.mystatus.setText(_("Data Frame Connected with %s columns") % unicode(self.R('length('+self.data+')')))
        colnames = self.R('colnames('+self.data+')')
        if colnames != 'NULL' and self.dfselected == None:
            self.dfselected = listBox(self.dataBox, self)
            for e in colnames:
                self.dfselected.addItem(e)
        elif colnames != 'NULL' and self.dfselected != None:
            self.dfselected.clear()
            for e in colnames:
                self.dfselected.addItem(e)
    def isMatrix(self):
        self.mystatus.setText(_("Matrix connected with %s elements and %s columns") % (unicode(self.R('length('+self.data+')')), unicode(self.R('length('+self.data+'[1,])'))))
        colnames = self.R('colnames('+self.data+')')
        if colnames != 'NULL' and colnames != '' and colnames != 'None' and colnames != None:
            self.dfselected = listBox(self.dataBox, self)
            try:
                for e in colnames:
                    self.dfselected.addItem(e)
            except:
                print _('Error with colnames, may not exist.')
    def isList(self):
        self.mystatus.setText(_("List object connected with %s elements") % unicode(self.R('length('+self.data+')')))
    
        
        