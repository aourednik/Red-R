"""
<name>Widget Maker</name>
<tags>R</tags>
"""

from OWRpy import *
import redRGUI
import libraries.base.signalClasses as signals
from libraries.base.qtWidgets import tabWidget, lineEdit, widgetLabel, widgetBox, button, checkBox, comboBox
import redRi18n
_ = redRi18n.get_(package = 'base')
class widgetMaker(OWRpy):
    def __init__(self, parent=None, signalManager=None):
        settingsList = ['output_txt', 'parameters']
        OWRpy.__init__(self)
        
        self.functionParams = ''
        self.widgetInputsName = []
        self.widgetInputsClass = []
        self.widgetInputsFunction = []
        self.numberInputs = 0
        self.numberOutputs = 0
        
        self.fieldList = {}
        self.functionInputs = {}
        self.processOnConnect = 1

        # GUI
        # several tabs with different parameters such as loading in a function, setting parameters, setting inputs and outputs
        tabs = tabWidget.tabWidget(self.controlArea)
        functionTab = tabs.createTabPage(_("Function Info"))
        codeTab = tabs.createTabPage(_("Code"))
        box = widgetBox.widgetBox(functionTab, "")
        box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.infoa = widgetLabel.widgetLabel(box, '')
        self.packageName = lineEdit.lineEdit(box, label = _('Package:'), orientation = 1)
        button.button(box, 'Load Package', callback = self.loadRPackage)
        self.functionName = lineEdit.lineEdit(box, label = _('Function Name:'), orientation = 1)
        button.button(box, 'Parse Function', callback = self.parseFunction)
        self.argsLineEdit = lineEdit.lineEdit(box, label = _('GUI Args'))
        self.connect(self.argsLineEdit, SIGNAL('textChanged(QString)'), self.setArgsLineEdit)
        box = widgetBox.widgetBox(functionTab)
        box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.inputArea = QTableWidget()
        box.layout().addWidget(self.inputArea)
        self.inputArea.setColumnCount(7)
        box = widgetBox.widgetBox(functionTab, orientation = 'horizontal')
        #self.inputArea.hide()
        self.connect(self.inputArea, SIGNAL("itemClicked(QTableWidgetItem*)"), self.inputcellClicked)
        
        self.functionAllowOutput = checkBox.checkBox(box, label = _('Allow Output'), displayLable = False, buttons = [_('Allow Output')])
        self.captureROutput = checkBox.checkBox(box, buttons = [_('Show Output')])
        
        
        #self.inputsCombobox = redRGUI.comboBox(box, label = 'Input Class:', items = self.getRvarClass_classes())
        self.outputsCombobox = comboBox.comboBox(box, label = _('Output Class:'), items = self.getRvarClass_classes())
        button.button(box, label = _('Accept Inputs'), callback = self.acceptInputs)
        button.button(box, _('Generate Code'), callback = self.generateCode)
        button.button(box, _('Launch Widget'), callback = self.launch)
        
        self.codeArea = QTextEdit()
        codeTab.layout().addWidget(self.codeArea)
        
    def getRvarClass_classes(self):
        # dirs = dir(signals)
        # redRClasses = []
        # for thisItem in dirs:
            # attribute = getattr(signals, thisItem)
            # try:
                # if issubclass(attribute, signals.RVariable):
                    # redRClasses.append(thisItem)
            # except: pass
        return dir(signals)
    def setArgsLineEdit(self, string):
        myargs = unicode(self.argsLineEdit.text()).split(' ')
        for thisArg in myargs:
            if thisArg not in self.args.keys():
                self.args[thisArg] = ''
                
        self.updateInputs()
    def launch(self):
        import redREnviron, orngRegistry, os
        widgetDirName = redREnviron.directoryNames["widgetDir"]
        #print 'dir:' + widgetDirName
        path = os.path.join(widgetDirName, "blank", "widgets", "RedR" + unicode(self.functionName.text()).replace('.', '_') + ".py")
        #print 'path:' + path
        if not os.path.exists(os.path.split(path)[0]):
            os.makedirs(os.path.split(path)[0])
        file = open(os.path.abspath(path), "wt")
        tmpCode = unicode(self.codeArea.toPlainText())
        tmpCode = tmpCode.replace('<pre>', '')
        tmpCode = tmpCode.replace('</pre>', '')
        tmpCode = tmpCode.replace('&lt;', '<')
        tmpCode = tmpCode.replace('&gt;', '>')
        file.write(tmpCode)
        file.close()
        
        #reload all the widgets including those in the prototype dir we just created 
        #orngCanvas.OrangeCanvasDlg.reloadWidgets()
        
        #orngRegistry.readCategories()
        qApp.canvasDlg.reloadWidgets()  # yay!!! it works
        
    def loadRPackage(self):
        
        if not self.require_librarys([unicode(self.packageName.text())]):
            self.status.setText(_('R Libraries Not Loaded.'))
        
    def parseFunction(self):
        self.args = {}
        try:
            self.R('help('+unicode(self.functionName.text())+')', wantType = 'NoConversion') # show the help for the user to see the args.
            holder = self.R('capture.output(args('+unicode(self.functionName.text())+'))')
            s = ''
            functionParams = s.join(holder)
            print unicode(self.functionName.text())
            self.infoa.setText(_("Function called successfully."))
            print 'function called successfully'
            print unicode(self.functionParams)
        except:
            self.infoa.setText(_("Error with calling function."))
            return
            
        start = functionParams.find('(')+1 #where the args start 
        end = functionParams.rfind(')') # where the args end.
        tmp = functionParams[start:end]
        
        tmp = tmp.replace(' ','') #remove the spaces
        tmp = tmp.replace("','", '##')
        tmp = tmp.replace('","', '##')
        tmp = tmp.split(',')
        for el in tmp:
            tmp2 = el.split('=')
            tmp2[0] = tmp2[0].replace('.', '_')
            if tmp2[0] != '___': # don't pay attention to optional params
                if len(tmp2) > 1:
                    
                    self.args[tmp2[0]] = tmp2[1]
                else:
                    self.args[tmp2[0]] = ''
            
        for arg in self.args.keys():
            if self.args[arg][0:2] == 'c(':
                self.args[arg] = self.args[arg].replace("'", '')
                self.args[arg] = self.args[arg].replace('"', '')
                start = self.args[arg].find('(')+1
                end = self.args[arg].rfind(')')
                self.args[arg] = self.args[arg][start:end] #strip out the brackets
                self.args[arg] = self.args[arg].replace('##', ",")
                self.args[arg] = self.args[arg].split(',')
        
        self.argsLineEdit.setText(' '.join(self.args.keys()))
        self.updateInputs()
        
    def updateInputs(self):
        self.inputArea.clear()
        self.inputArea.setRowCount(int(len(unicode(self.argsLineEdit.text()).split(' '))))

        self.inputArea.show()
        self.inputArea.setHorizontalHeaderLabels([_('Name'), _('Input Type'), _('Required'), _('Signal Class'), _('Input class'), _('Default'), _('Options')])
        n=0
        for arg in unicode(self.argsLineEdit.text()).split(' '):
            arg = arg.replace('.', '_') # python uses points for class refference
            itemname = QTableWidgetItem(unicode(arg))
            #itemClass = QTableWidgetItem
            self.inputArea.setItem(n,0,itemname)
            cw = QComboBox()
            cw.addItems([_('Widget Input'), _('Connection Input')])
            self.inputArea.setCellWidget(n,1,cw)
            re = QComboBox()
            re.addItems([_('Optional'), _('Required')])
            self.inputArea.setCellWidget(n,2,re)
            ic = QComboBox()
            ic.addItems(self.getRvarClass_classes())
            self.inputArea.setCellWidget(n,3,ic)
            ipt = QComboBox()
            ipt.addItems([_('lineEdit'), _('radioButtons'), _('comboBox'), _('checkBox')])
            self.inputArea.setCellWidget(n, 4, ipt)
            dt = QLineEdit()
            dt.setText(unicode(self.args[arg]))
            self.inputArea.setCellWidget(n, 5, dt)
            opt = QLineEdit()
            self.inputArea.setCellWidget(n, 6, opt)
            
            n += 1
        
    def acceptInputs(self): #accept the criteria in the input Area
        for i in xrange(self.inputArea.rowCount()):
            #print 'i:'+unicode(i)
            combo = self.inputArea.cellWidget(i, 1)
            #print combo
            if combo.currentText() == _('Widget Input'):
                recombo = self.inputArea.cellWidget(i, 2)
                #print unicode(self.inputArea.item(i ,0).text())
                dt = self.inputArea.cellWidget(i, 5)
                self.fieldList[unicode(self.inputArea.item(i, 0).text())] = {'default':unicode(dt.text()), 'required':recombo.currentText(), 'opt':unicode(self.inputArea.cellWidget(i, 6).text()), 'ipt':unicode(self.inputArea.cellWidget(i, 4).currentText())}
                
            else:
                ic = self.inputArea.cellWidget(i, 3)
                self.functionInputs[unicode(self.inputArea.item(i,0).text())] = unicode(ic.currentText())
            
    def inputcellClicked(self, item):
        self.inputArea.editItem(item)
    
    def generateCode(self):
        self.acceptInputs()
        self.makeHeader()
        self.makeInitHeader()
        self.makeGUI()
        self.makeProcessSignals()
        self.makeCommitFunction()
        #self.makeRsendFunction()
        
        self.combineCode()
        
    def makeHeader(self):
        self.headerCode = '"""\n'
        self.headerCode += '&lt;name&gt;'+self.functionName.text()+'&lt;/name&gt;\n'
        self.headerCode += '&lt;author&gt;Generated using Widget Maker written by Kyle R. Covington&lt;/author&gt;\n'
        self.headerCode += '&lt;description&gt;&lt;/description&gt;\n'
        self.headerCode += '&lt;RFunctions&gt;'+self.packageName.text()+':'+self.functionName.text()+'&lt;/RFunctions&gt;\n'
        self.headerCode += '&lt;tags&gt;Prototypes&lt;/tags&gt;\n'
        self.headerCode += '&lt;icon&gt;&lt;/icon&gt;\n'
        self.headerCode += '"""\n'
        self.headerCode += 'from OWRpy import * \n'
        for i in ['lineEdit', 'radioButtons', 'comboBox', 'checkBox', 'textEdit']:
            self.headerCode += 'from libraries.base.qtWidgets.%s import %s as redR%s \n' % (i,i,i)
        self.headerCode += 'import libraries.base.signalClasses as signals\n\n'
        
    def makeInitHeader(self):
        self.initCode = ''
        self.initCode += 'class RedR'+self.functionName.text().replace('.', '_')+'(OWRpy): \n'
        self.initCode += '\tsettingsList = []\n'
        self.initCode += '\tdef __init__(self, parent=None, signalManager=None):\n'

        self.initCode += '\t\tOWRpy.__init__(self)\n'
        if (_('Allow Output') in self.functionAllowOutput.getChecked()) or (_('Show Output') in self.captureROutput.getChecked()):
            self.initCode += '\t\tself.setRvariableNames(["'+self.functionName.text()+'"])\n'
            self.initCode += '\t\tself.data = {}\n'
        if unicode(self.packageName.text()) != '':
            self.initCode += '\t\tif not self.require_librarys(["'+unicode(self.packageName.text())+'"]):\n'
            self.initCode += '\t\t\tself.status.setText(_(\'R Libraries Not Loaded.\'))\n'
        if len(self.functionInputs.keys()) > 0:
            for inputName in self.functionInputs.keys():
                self.initCode += "\t\tself.RFunctionParam_"+inputName+" = ''\n"
            #self.initCode += '\t\tself.inputs = ['
            for element in self.functionInputs.keys():
                self.initCode += '\t\tself.inputs.addInput("'+element+'", _("'+element+'"), signals.'+self.functionInputs[element]+'.'+self.functionInputs[element]+', self.process'+element+')\n'
        if 'Allow Output' in self.functionAllowOutput.getChecked():
            self.initCode += '\t\tself.outputs.addOutput("'+self.functionName.text()+' Output",_("'+self.functionName.text()+' Output"), signals.'+unicode(self.outputsCombobox.currentText())+'.'+unicode(self.outputsCombobox.currentText())+')\n'
        self.initCode += '\t\t\n'
        
    def makeGUI(self):
        self.guiCode = ''
        
        for element in self.fieldList.keys():
            if element == '___':
                continue
            else:
                self.guiCode += '\t\tself.RFunctionParam'+element+'_'+unicode(self.fieldList[element]['ipt'])+' = redR'+unicode(self.fieldList[element]['ipt'])+'(self.controlArea, label = "'+element+':"'
                ## ipt types ['lineEdit', 'radioBox', 'comboBox', 'checkBox']
                
                if self.fieldList[element]['ipt'] == 'lineEdit':
                    self.guiCode += ', text = \''+self.fieldList[element]['default']+'\')\n'
                elif self.fieldList[element]['ipt'] == 'radioButtons':
                    
                    self.guiCode += ', buttons = ["'+'","'.join([a.strip() for a in self.fieldList[element]['default'].split(',')])+'"], setChecked = "'+self.fieldList[element]['opt'].strip()+'")\n'
                elif self.fieldList[element]['ipt'] == 'comboBox':
                    self.guiCode += ', items = ["'+'","'.join([a.strip() for a in self.fieldList[element]['default'].split(',')])+'"])\n'
                elif self.fieldList[element]['ipt'] == 'checkBox':
                    self.guiCode += ')\n'
                
        self.guiCode += '\t\tredRCommitButton(self.bottomAreaRight, "Commit", callback = self.commitFunction)\n'
        if _('Show Output') in self.captureROutput.getChecked():
            self.guiCode += '\t\tself.RoutputWindow = redRtextEdit(self.controlArea, label = _("R Output Window"))\n'
            #self.guiCode += '\t\tself.controlArea.layout().addWidget(self.RoutputWindow)\n'

    def makeProcessSignals(self):
        self.processSignals = ''
        for inputName in self.functionInputs.keys():
            self.processSignals += '\tdef process'+inputName+'(self, data):\n'
            
            self.processSignals += '\t\tif data:\n'
            self.processSignals += '\t\t\tself.RFunctionParam_'+inputName+'=data.getData()\n'
            self.processSignals += '\t\t\t#self.data = data\n'
            if self.processOnConnect:
                self.processSignals += '\t\t\tself.commitFunction()\n'
            self.processSignals += '\t\telse:\n'
            self.processSignals += '\t\t\tself.RFunctionParam_'+inputName+'=\'\'\n'
                
    def makeCommitFunction(self):
        self.commitFunction = ''
        self.commitFunction += '\tdef commitFunction(self):\n'
        for inputName in self.functionInputs.keys():
            self.commitFunction += "\t\tif unicode(self.RFunctionParam_"+inputName+") == '': return\n"
        for element in self.fieldList.keys():
            if self.fieldList[element]['required'] == 'Required' and self.fieldList[element]['ipt'] == 'lineEdit':
                self.commitFunction += "\t\tif unicode(self.RFunctionParam"+ element +"_lineEdit.text()) == '': return\n"
        self.commitFunction += "\t\tinjection = []\n"
        for element in self.fieldList.keys():
            relement = element.replace('_', '.')
            if self.fieldList[element]['ipt'] == 'lineEdit':
                self.commitFunction += "\t\tif unicode(self.RFunctionParam"+ element +"_lineEdit.text()) != '':\n"
                self.commitFunction += "\t\t\tstring = '"+relement+"='+unicode(self.RFunctionParam"+ element +"_lineEdit.text())+''\n"
                self.commitFunction += "\t\t\tinjection.append(string)\n"
            elif self.fieldList[element]['ipt'] == 'comboBox':
                self.commitFunction += "\t\tstring = ',"+relement+"='+unicode(self.RFunctionParam"+element+"_comboBox.currentText())+''\n"
                self.commitFunction += "\t\tinjection.append(string)\n"
            else:
                self.commitFunction += "\t\t## make commit function for self.RFunctionParam"+element+"_"+self.fieldList[element]['ipt']+"\n\n"
                
        self.commitFunction += "\t\tinj = ''.join(injection)\n"
        self.commitFunction += "\t\tself.R("
        if ('Allow Output' in self.functionAllowOutput.getChecked()) or ('Show Output' in self.captureROutput.getChecked()):
            self.commitFunction += "self.Rvariables['"+self.functionName.text()+"']+'&lt;-"+self.functionName.text()+"("
        else:
            self.commitFunction += "'"+self.functionName.text()+"("
        for element in self.functionInputs.keys():
            if element != '___':
                relement = element.replace('_', '.')
                self.commitFunction += relement+"='+unicode(self.RFunctionParam_"+element+")+',"
        #self.commitFunction = self.commitFunction[:-2] #remove the last element
        # for element in self.fieldList.keys():
            # if element == '...':
                # pass
            # else:
                # self.commitFunction += element+"='+unicode(self.RFunctionParam_"+element+")+',"
        # self.commitFunction = self.commitFunction[:-1]
        self.commitFunction += "'+inj+'"
        self.commitFunction += ")')\n"
        if 'Show Output' in self.captureROutput.getChecked():
            self.commitFunction += "\t\tself.R(\'txt<-capture.output(\'+self.Rvariables[\'"+self.functionName.text()+"\']+\')\')\n"
            self.commitFunction += "\t\tself.RoutputWindow.clear()\n"
            self.commitFunction += "\t\ttmp = self.R('paste(txt, collapse =\x22\x5cn\x22)')\n"
            self.commitFunction += "\t\tself.RoutputWindow.insertHtml('&lt;br&gt;&lt;pre&gt;'+tmp+'&lt;/pre&gt;')\n"
            
                    # pasted = self.rsession('paste(txt, collapse = " \n")')
        # self.thistext.insertPlainText('>>>'+self.command+'##Done')
        # self.thistext.insertHtml('<br><pre>'+pasted+'<\pre><br>')
        
        
        if 'Allow Output' in self.functionAllowOutput.getChecked():
            self.commitFunction += '\t\tnewData = signals.'+unicode(self.outputsCombobox.currentText())+'.'+unicode(self.outputsCombobox.currentText())+'(data = self.Rvariables["'+self.functionName.text()+'"]) # moment of variable creation, no preexisting data set.  To pass forward the data that was received in the input uncomment the next line.\n'
            self.commitFunction += '\t\t#newData.copyAllOptinoalData(self.data)  ## note, if you plan to uncomment this please uncomment the call to set self.data in the process statemtn of the data whose attributes you plan to send forward.\n'
            self.commitFunction += '\t\tself.rSend("'+self.functionName.text()+' Output", newData)\n'

    def combineCode(self):
        self.completeCode = '<pre>'
        self.completeCode += self.headerCode+self.initCode+self.guiCode+self.processSignals+self.commitFunction
        self.completeCode += '</pre>'
        self.codeArea.setHtml(self.completeCode)