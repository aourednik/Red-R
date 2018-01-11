"""
<name>R Variable Selection</name>
<tags>R</tags>
<icon>rexecutor.png</icon>
"""
from OWRpy import * 
import redRGUI 
import libraries.base.signalClasses.REnvironment as renv
import libraries.base.signalClasses.RVariable as rvar
import libraries.base.signalClasses.RVector as rvec
import libraries.base.signalClasses.RList as rlist
import libraries.base.signalClasses.RMatrix as rmat
import libraries.base.signalClasses.RDataFrame as rdf
import libraries.base.signalClasses.RArbitraryList as ral

from libraries.base.qtWidgets.button import button
from libraries.base.qtWidgets.checkBox import checkBox
from libraries.base.qtWidgets.listBox import listBox
from libraries.base.qtWidgets.widgetBox import widgetBox
unicode(self.function.getChecked())+
class RVarSeparator(OWRpy): 
    globalSettingsList = ['commitButton']
    def __init__(self, parent=None, signalManager=None):
        OWRpy.__init__(self)
       
        self.inputs.addInput('id0', _('R Environment'), renv.REnvironment, self.process)

        self.outputs.addOutput('id0', _('R Session'), renv.REnvironment)
        self.outputs.addOutput('id1', _('Non-Standard R Variable'), rvar.RVariable)
        self.outputs.addOutput('id2', _('R Data Frame (Data Table)'), rdf.RDataFrame)
        self.outputs.addOutput('id3', _('R List'), rlist.RList)
        self.outputs.addOutput('id4', _('R Vector'), rvec.RVector)
        self.outputs.addOutput('ral', _('R Arbitrary List'), ral.RArbitraryList)

       
        # self.help.setHtml('The R Variable Separator is used to separate variables from a loaded R session.  Connecting the R Loader widget to this widget will display a list of available variables in the local environment to which the session was loaded.  Clicking on an element in the list will send that element on to downstream widgets.  One should take note of the class of the element that is sent as this will specify the output connection of the data.  More infromation is available on the <a href="http://www.red-r.org/?cat=10">RedR website</a>.')

        self.controlArea.setMinimumWidth(300)
        self.varBox = listBox(self.controlArea, label = _('Variables'), callback = self.select)
        
        box = widgetBox(self.controlArea, orientation='horizontal') 
        #self.filecombo.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum)
        self.controlArea.layout().setAlignment(box,Qt.AlignRight)
        
        self.commitButton = redRCommitButton(box,label=_('Commit'),callback=self.commit,
        processOnInput=True,processOnChange=True)

    def process(self, data):
        if not data: return
        self.envName = data.getData()

        dataList = self.R('local(ls(), '+self.envName+')', wantType = 'list')
        
        if not dataList:
            self.status.setText(_('No data in the R session'))
            return 
        
        self.varBox.update(dataList)
        if self.commitButton.processOnInput():
            self.commit()
           
        
    def select(self):
        if self.commitButton.processOnChange():
            self.commit()
            
    def commit(self):
        #must declare explilcitly as a string or an error will occur.  We remove NA's just in case they are in the data
        self.sendThis = unicode('local('+self.varBox.selectedItems()[0].text()+', '+self.envName+')') 
        
        #put logic for finding the type of variable that the object is and sending it from that channel of the output
        
        dataClass = self.R('class('+self.sendThis+')')
            
        if type(dataClass) is str:
            if dataClass in ['numeric', 'character', 'real', 'complex', 'factor']: # we have a numeric vector as the object
                newData = rvec.RVector(data = self.sendThis)
                self.rSend('id4', newData)
                self.status.setText(_('Data sent through the R Vector channel'))
            elif dataClass == 'character': #we have a character vector as the object
                newData = rvec.RVector(data = self.sendThis)
                self.rSend('id4', newData)
                self.status.setText(_('Data sent through the R Vector channel'))
            elif dataClass == 'data.frame': # the object is a data.frame
                newData = rdf.RDataFrame(data = self.sendThis)
                self.rSend('id2', newData)
                self.status.setText(_('Data sent through the R Data Frame channel'))
            elif dataClass == 'matrix': # the object is a matrix
                
                newData = rmat.RMatrix(data = self.sendThis)
                
                self.rSend('id2', newData)
                self.status.setText(_('Data sent through the R Data Frame channel'))
            elif dataClass == 'list': # the object is a list
                for i in range(self.R('length('+self.sendThis+')')):
                    if self.R('class(%s[[%s]])' % (self.sendThis, i), silent = True) not in ['numeric', 'character', 'real', 'complex', 'factor']:
                        newData = ral.RArbitraryList(data = self.sendThis)
                        self.status.setText(_('Data sent through the R Arbitrary List channel'))
                        self.rSend('ral', newData)
                        return
                newData = rlist.RList(data = self.sendThis)
                self.rSend('id3', newData)
                self.status.setText(_('Data sent through the R List channel'))
            else:    # the data is of a non-normal type send anyway as generic  
                newData = rvar.RVariable(data = self.sendThis)
                self.rSend('id1', newData)
                self.status.setText(_('Data sent through the R Object channel'))
        else:
            newData = rvar.RVariable(data = self.sendThis)
            self.rSend('id1', newData)
            self.status.setText(_('Data sent through the R Object channel'))
