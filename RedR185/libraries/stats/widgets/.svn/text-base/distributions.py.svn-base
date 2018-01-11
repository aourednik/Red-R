"""
<name>Generate Distributions</name>
<author>Anup Parikh anup@red-r.org</author>
<RFunctions>stats:rnorm, stats:rbeta, stats:rbinom, stats:rcauchy, stats:rchisq</RFunctions>
<tags>Stats</tags>
<icon>rexecutor.png</icon>
"""

#OWRpy is the parent of all widgets. 
#Contains all the functionality for connecting the widget to the underlying R session.
from OWRpy import *
import os.path, redREnviron
# signalClasses classes contain the data that is passed between widgets. 
# In this case we are using the RDataFrame and RMatrix signals
from libraries.base.signalClasses.RVector import RVector as redRRVector
from libraries.base.signalClasses.RList import RList as redRRList



# redRGUI contains all the QT gui elements. 
# These elements all have special functions for saving and loading state. 
from libraries.base.qtWidgets.button import button
from libraries.base.qtWidgets.checkBox import checkBox
from libraries.base.qtWidgets.radioButtons import radioButtons
from libraries.base.qtWidgets.comboBox import comboBox as redRcomboBox
from libraries.base.qtWidgets.widgetBox import widgetBox
from libraries.base.qtWidgets.lineEdit import lineEdit as redRlineEdit
from libraries.base.qtWidgets.groupBox import groupBox
from libraries.base.qtWidgets.spinBox import spinBox as RedRSpinBox

# our first widget. Must be a child of OWRpy class
# The wiget class name must be the same as the file name
class distributions(OWRpy):
    
    # Python init statement is the class constructor 
    # Here you put all the code that will run as soon as the widget is put on the canvas
    def __init__(self, parent=None, signalManager=None):
        #Here we init the parent class of our widget OWRpy.
        OWRpy.__init__(self)
        
        #create a R variable cor in the R session.
        #the output variable will not conflict with some other widgets variables
        self.setRvariableNames(["distri"])

        # Define the outputs of this widget
        self.outputs.addOutput('id0', 'Results', redRRVector)

        
        #START THE GUI LAYOUT
        area = widgetBox(self.controlArea,orientation='horizontal')       
        options = widgetBox(area,orientation='vertical')
        area.layout().setAlignment(options,Qt.AlignTop)
        self.count = RedRSpinBox(options, label='# Observations to Generate', min = 0,max=60000000, value = 10)
        
        self.methodButtons = redRcomboBox(options,  label = "Distributions", 
        items = [("rnorm", "Normal"),
        ('rbeta','Beta'),
        ('rbinom','Binomial'),
        ('rcauchy','Cauchy'),
        ('rchisq','Chi Square'),
        ('rexp','Exponential'),
        ('rf','F'),
        ('rgamma','Gamma') ],
        editable=True, callback = self.onDistChange)
        
        textBoxWidth = 70
        self.distOptions = widgetBox(options)
        self.normalDist = groupBox(self.distOptions,label='Normal Distribution')
        self.normMean = redRlineEdit(self.normalDist, label='Mean',id='mean', text='0', width=textBoxWidth)
        self.normSD = redRlineEdit(self.normalDist, label='Standard Deviations',id='sd', text='1',width=textBoxWidth)
        
        self.betaDist = groupBox(self.distOptions,label='Beta Distribution')
        self.betaShape1 = redRlineEdit(self.betaDist, label='Shape 1', id='shape1', width=textBoxWidth,text='1')
        self.betaShape2 = redRlineEdit(self.betaDist, label='Shape 2', id='shape2', width=textBoxWidth,text='1')
        self.betaNCP = redRlineEdit(self.betaDist, label='Non-centrality', id='ncp', width=textBoxWidth,text='0')
        self.betaDist.hide()

        
        self.binomDist = groupBox(self.distOptions,label='Binomial Distribution')
        self.binomSize = redRlineEdit(self.binomDist, label='Size', id='size', width=textBoxWidth,text='1')
        self.binomProb = redRlineEdit(self.binomDist, label='Probability', id='prob', width=textBoxWidth,text='.5')
        self.binomDist.hide()
        
        
        self.cauchyDist = groupBox(self.distOptions,label='Cauchy Distribution')
        self.cauchyLocation = redRlineEdit(self.cauchyDist, label='Location', id='location', width=textBoxWidth,text='0')
        self.cauchyScale = redRlineEdit(self.cauchyDist, label='Scale', id='scale', width=textBoxWidth,text='1')
        self.cauchyDist.hide()
        
        self.gammaDist = groupBox(self.distOptions,label='Gamma Distribution')
        self.gammaShape = redRlineEdit(self.gammaDist, label='Shape', id='location', width=textBoxWidth,text='1')
        self.gammaRate = redRlineEdit(self.gammaDist, label='Rate', id='scale', width=textBoxWidth,text='1')
        self.gammaScale = redRlineEdit(self.gammaDist, label='Scale', id='scale', width=textBoxWidth,text='.5')
        self.gammaDist.hide()
        
        self.chiDist = groupBox(self.distOptions,label='Chi Square Distribution')
        self.chiDF = redRlineEdit(self.chiDist, label='Degrees of Freedom', id='df', width=textBoxWidth,text='1')
        self.chiNCP = redRlineEdit(self.chiDist, label='Non-centrality', id='ncp', width=textBoxWidth,text='0')
        self.chiDist.hide()
        
        self.fDist = groupBox(self.distOptions,label='F Distribution')
        self.fDF1 = redRlineEdit(self.fDist, label='Degrees of Freedom 1', id='df1', width=textBoxWidth,text='1')
        self.fDF2 = redRlineEdit(self.fDist, label='Degrees of Freedom 2', id='df2', width=textBoxWidth,text='1')
        self.fNCP = redRlineEdit(self.fDist, label='Non-centrality', id='ncp', width=textBoxWidth,text='0')
        self.fDist.hide()
        
        self.expDist = groupBox(self.distOptions,label='Exponential Distribution')
        self.expRate = redRlineEdit(self.expDist, label='Rate ', id='rate', width=textBoxWidth,text='1')
        self.expDist.hide()
        
        commit = redRCommitButton(options, "Commit", toolTip='Calculate values', callback = self.commitFunction)
        options.layout().setAlignment(commit, Qt.AlignRight)
        
    # Based on the user selections some parameters is not valid. This is all documented in the R help for cor/var/cov
    # Here we are instructing the GUI to disable those parameters that are invalid. 
    def onDistChange(self):
        for i in self.distOptions.findChildren(groupBox):
            i.setHidden(True)
        # print self.distOptions.findChild(self.methodButtons.currentId(),widgetBox)
        # self.distOptions.findChild(widgetBox,self.methodButtons.currentId()).show()
        
        if self.methodButtons.currentId() == 'rnorm':
            self.normalDist.show()
        elif self.methodButtons.currentId() == 'rbeta':
            self.betaDist.show()
        elif self.methodButtons.currentId() == 'rbinom':
            self.binomDist.show()
        elif self.methodButtons.currentId() == 'rcauchy':
            self.cauchyDist.show()
        elif self.methodButtons.currentId() == 'rchisq':
            self.chiDist.show()
        elif self.methodButtons.currentId() == 'rexp':
            self.expDist.show()
        elif self.methodButtons.currentId() == 'rf':
            self.fDist.show()
        elif self.methodButtons.currentId() == 'rgamma':
            self.gammaDist.show()
                
    # this function actually does the work in R 
    # its call by clicking the Commit button
    # or when data is received, if the checkbox is checked.
    def collectParameters(self):
        self.injection = []
        dist = unicode(self.methodButtons.currentId())
        if dist =='rnorm':
            self.injection.append('%s=%s' % (self.normMean.widgetId(), self.normMean.text()))
            self.injection.append('%s=%s' % (self.normSD.widgetId(), self.normSD.text()))
        elif dist =='rbeta':
            self.injection.append('%s=%s' % (self.betaShape1.widgetId(), self.betaShape1.text()))
            self.injection.append('%s=%s' % (self.betaShape2.widgetId(), self.betaShape2.text()))
            self.injection.append('%s=%s' % (self.betaNCP.widgetId(), self.betaNCP.text()))
        elif dist == 'rbinom':
            self.injection.append('%s=%s' % (self.binomSize.widgetId(), self.binomSize.text()))
            self.injection.append('%s=%s' % (self.binomProb.widgetId(), self.binomProb.text()))
        elif dist == 'rcauchy':
            self.injection.append('%s=%s' % (self.cauchyLocation.widgetId(), self.cauchyLocation.text()))
            self.injection.append('%s=%s' % (self.cauchyScale.widgetId(), self.cauchyScale.text()))
        elif dist == 'rchisq':
            self.injection.append('%s=%s' % (self.chiDF.widgetId(), self.chiDF.text()))
            self.injection.append('%s=%s' % (self.chiNCP.widgetId(), self.chiNCP.text()))
        elif dist == 'rexp':
            self.injection.append('%s=%s' % (self.expRate.widgetId(), self.expRate.text()))
        elif dist == 'rf':
            self.injection.append('%s=%s' % (self.fDF1.widgetId(), self.fDF1.text()))
            self.injection.append('%s=%s' % (self.fDF2.widgetId(), self.fDF2.text()))
            self.injection.append('%s=%s' % (self.fNCP.widgetId(), self.fNCP.text()))
        elif dist == 'rgamma':
            self.injection.append('%s=%s' % (self.gammaRate.widgetId(), self.gammaRate.text()))
            self.injection.append('%s=%s' % (self.gammaScale.widgetId(), self.gammaScale.text()))
            self.injection.append('%s=%s' % (self.gammaShape.widgetId(), self.gammaShape.text()))
        
        return self.injection
        
    def commitFunction(self):        
        # START COLLECTION THE R PARAMETERS THAT WILL CREATE THE R CODE TO EXECUTE
        dist = unicode(self.methodButtons.currentId())
        self.injection = self.collectParameters()
        

        # combine all the parameters in the a string    
        inj = ','.join(self.injection)
        
        # make the R call. The results will be saved in the 'cor' variable we declared earlier
        self.R('%s <- %s(%s,%s)' % (self.Rvariables['distri'], dist, self.count.value(),inj), wantType = 'NoConversion')
        
        # create a new signal of type RMatrix and load the results 
        newData = redRRVector(data = '%s' % self.Rvariables["distri"]) 
        # send the signal forward
        self.rSend("id0", newData)
  
    
    def getReportText(self, fileDir):
        text = 'Generate data from a given distribution.\n\n'
        text += '**Parameters:**\n\n'
        text += 'Distribution:  '+unicode(self.methodButtons.currentText())+'\n\n'
        text += 'Number of observations generated:  '+unicode(self.count.value())+'\n\n'
        text += 'Distribution parameters:\n\n'
        
        self.injection = self.collectParameters()
        for x in self.injection:
            text += '\t%s\n\n' % x
            
        return text

