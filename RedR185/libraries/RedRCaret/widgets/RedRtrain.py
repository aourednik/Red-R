"""
<name>train</name>
<author>Generated using Widget Maker written by Kyle R. Covington</author>
<description></description>
<RFunctions>caret:train</RFunctions>
<tags>Prototypes</tags>
<icon></icon>
"""
from OWRpy import * 
from libraries.base.qtWidgets.lineEdit import lineEdit as redRlineEdit 
from libraries.base.qtWidgets.radioButtons import radioButtons as redRradioButtons 
from libraries.base.qtWidgets.comboBox import comboBox as redRcomboBox 
from libraries.base.qtWidgets.checkBox import checkBox as redRcheckBox 
from libraries.base.qtWidgets.textEdit import textEdit as redRtextEdit 
from libraries.base.qtWidgets.RFormulaEntry import RFormulaEntry as redRRFormulaEntry
import libraries.base.signalClasses as signals

class RedRtrain(OWRpy): 
    settingsList = []
    def __init__(self, parent=None, signalManager=None):
        OWRpy.__init__(self)
        self.require_librarys(["caret"])
        self.setRvariableNames(["train", 'tempData'])
        self.data = {}
        self.RFunctionParam_data = ''
        self.inputs.addInput("data", "data", [signals.RArbitraryList.RArbitraryList, signals.RDataFrame.RDataFrame], self.processdata)
        self.outputs.addOutput("train Output","train Output", signals.RModelFit.RModelFit)
        
        self.trainingData = redRcomboBox(self.controlArea, label = 'Training Data:')
        self.RFunctionParamcustomArgs_lineEdit = redRlineEdit(self.controlArea, label = "customArgs:", text = '')
        #self.RFunctionParamtrControl_lineEdit = redRlineEdit(self.controlArea, label = "trControl:", text = '')
        self.RFunctionParammethod_comboBox = redRcomboBox(self.controlArea, label = "Method:", items = ["ada", "bagEarth", "bagFDA", "blackboost", "cforest", "ctree", "ctree2", "earth", "enet", "fda", "gamboost", "gaussprPoly", "gaussprRadial", "gaussprLinear", "gbm", "glm", "glmboost", "glmnet", "gpls", "J48", "JRip", "knn", "lars", "lasso", "lda", "Linda", "lm", "lmStepAIC", "LMT", "logitBoost", "lssvmPoly", "lssvmRadial", "lvq", "M5Rules", "mda", "multinom", "nb", "nnet", "nodeHarvest", "OneR", "pam", "pcaNNet", "pcr", "pda", "pda2", "penalized", "pls", "ppr", "qda", "QdaCov", "rda", "rf", "rlm", "rpart", "rvmLinear", "rvmPoly", "rvmRadial", "sda", "sddaLDA", "sddaQDA", "slda", "smda","sparseLDA", "spls", "stepLDA", "stepQDA", "superpc", "svmPoly", "svmRadial", "svmLinear", "treebag","vbmpRadial"])
        #self.formula = redRRFormulaEntry(self.controlArea)
        self.resultVariable = redRcomboBox(self.controlArea, label = 'Class Data:')
        self.RFunctionParamform_lineEdit = redRlineEdit(self.controlArea, label = "form:", text = '')
        self.RoutputWindow = redRtextEdit(self.controlArea, label = "R Output Window")
        redRCommitButton(self.bottomAreaRight, "Commit", callback = self.commitFunction)
    def processdata(self, data):
        
        if data:
            if self.R('class('+data.getData()+')') == 'data.frame':
                self.R(self.Rvariables['tempData']+'<-list(TrainingData = '+data.getData()+')', wantType = 'NoConversion')
                self.RFunctionParam_data = self.Rvariables['tempData']
            else:
                self.RFunctionParam_data=data.getData()
            #self.data = data
            self.trainingData.update(self.R('names('+self.RFunctionParam_data+')'))
            #self.formula.update(self.R('names('+self.RFunctionParam_data+'[[1]])'))
            self.resultVariable.update(self.R('names('+self.RFunctionParam_data+'[[1]])'))
            #self.commitFunction()
        else:
            self.RFunctionParam_data=''
    def commitFunction(self):
        if unicode(self.RFunctionParam_data) == '': return
        injection = []
        if unicode(self.RFunctionParamcustomArgs_lineEdit.text()) != '':
            string =','+unicode(self.RFunctionParamcustomArgs_lineEdit.text())
            injection.append(string)
        #if unicode(self.RFunctionParamtrControl_lineEdit.text()) != '':
        string = ',trControl= trainControl(verbose = FALSE, returnResamp = "all")'#+unicode(self.RFunctionParamtrControl_lineEdit.text())+''
        injection.append(string)
        
        # formula = self.formula.Formula()
        # if formula[0] != '':
            # string = ',form='+formula[0]+' ~ '  ##unicode(self.RFunctionParamform_lineEdit.text())+''
            # if formula[1] != '':
                # string += formula[1]
            # else:
                # string += '.'
            # injection.append(string)
        string = ',method=\"'+unicode(self.RFunctionParammethod_comboBox.currentText())+'\"'
        injection.append(string)
        inj = ''.join(injection)
        self.R(self.Rvariables['train']+'<-train(x='+unicode(self.RFunctionParam_data)+'[[\''+unicode(self.trainingData.currentText())+'\']][,!names('+unicode(self.RFunctionParam_data)+'[[\''+unicode(self.trainingData.currentText())+'\']]) %in% c(\''+unicode(self.resultVariable.currentText())+'\')], y = '+unicode(self.RFunctionParam_data)+'[[\''+unicode(self.trainingData.currentText())+'\']][,c(\''+unicode(self.resultVariable.currentText())+'\')]'+inj+')')
        newData = signals.RModelFit.RModelFit(data = self.Rvariables["train"]) # moment of variable creation, no preexisting data set.  To pass forward the data that was received in the input uncomment the next line.
        #newData.copyAllOptinoalData(self.data)  ## note, if you plan to uncomment this please uncomment the call to set self.data in the process statemtn of the data whose attributes you plan to send forward.
        self.rSend("train Output", newData)
        self.R('txt<-capture.output('+self.Rvariables['train']+')', wantType = 'NoConversion')
        self.RoutputWindow.clear()
        tmp = self.R('paste(txt, collapse ="\n")')
        self.RoutputWindow.insertPlainText(tmp)