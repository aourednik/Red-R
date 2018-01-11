## ConSig Widget.  Purpose is to calculate the consig score from a list of genes.





"""
<name>ConSig</name>
<author>Kyle R Covington kyle@red-r.org</author>
<description>Generates a set of ConSig Scores from a given gene list.  Will also accept a connection to a list of reference genes and a set of disriptors of genes.  The requirement of the discriptor is that it contain a set of concepts and geneID's that match the geneID's that are in the reference list.  Other data from the concepts map is appended to the end of the final table of scores.</description>
<RFunctions>graphics:hist</RFunctions>
<tags>Data Manipulation</tags>
<icon></icon>
"""
from OWRpy import * 
import OWGUI, os
from libraries.base.signalClasses.RVariable import RVariable as redRRVariable
from libraries.base.signalClasses.RList import RList as redRRList
from libraries.base.signalClasses.RArbitraryList import RArbitraryList as redRArbitrary
from libraries.base.signalClasses.RDataFrame import RDataFrame as redRDataFrame
from libraries.base.qtWidgets.comboBox import comboBox
from libraries.base.qtWidgets.lineEdit import lineEdit
from libraries.base.qtWidgets.groupBox import groupBox
from libraries.base.qtWidgets.splitter import splitter as redRSplitter
from libraries.base.qtWidgets.tabWidget import tabWidget as redRTabWidget
from libraries.base.qtWidgets.widgetLabel import widgetLabel as redRWidgetLabel
from libraries.base.qtWidgets.commitButton import commitButton as redRCommitButton
from libraries.base.qtWidgets.button import button
class ConSig(OWRpy): 
    
    def __init__(self, parent=None, signalManager=None):
        OWRpy.__init__(self)
        self.setRvariableNames(['genesScores', 'conceptScores'])
        self.concepts = ''          ## the concepts, optional will replace the reading of the file
        self.geneIDs = ''           ## the geneIDs to be found in the concepts
        self.reference = ''         ## the set of reference genes, 
        self.packageDir = ''        ## the packageDir where all of the concept files are stored if not otherwise available.
        self.map = None
        self.go = None
        
        self.inputs.addInput('geneIDs', 'Gene ID List', redRDataFrame, self.processGeneIDs)
        self.inputs.addInput('consigData', 'Concepts Data [optional]', redRDataFrame, self.processConcepts)
        self.inputs.addInput('referenceList', 'Gene Reference List [optional]', redRRList, self.processReference)
        
        self.outputs.addOutput('scores', 'ConSig Concept Scores', redRDataFrame)
        self.outputs.addOutput('genescores', 'ConSig Gene Scores', redRDataFrame)
        
        myTabWidget = redRTabWidget(self.controlArea)
        geneIDArea = myTabWidget.createTabPage('Gene ID\'s')
        conceptsArea = myTabWidget.createTabPage('Concepts')
        fileSetupArea = myTabWidget.createTabPage('File Setup')
        
        ## file selection for consig files
        self.dirLabel = redRWidgetLabel(fileSetupArea, 'No Directory Currently Selected')
        button(fileSetupArea, label = 'Change File Directory', callback = self.changeFileDir)
        
        ## concepts area
        button(conceptsArea, label = 'Parse Concepts', callback = self.parseConcepts)
        
        ## 
        self.genes_geneIDCol = comboBox(geneIDArea, label = 'Gene ID Column')
        self.genes_scoreCol = comboBox(geneIDArea, label = 'Gene Scores (Weights)')
        
        redRCommitButton(self.controlArea, label = 'Commit', callback = self.commit)
    def changeFileDir(self):
        fn = QFileDialog.getExistingDirectory(self, "Choose Directory")
        if fn.isEmpty(): return
        fn = unicode(fn)
        self.packageDir = fn
        self.dirLabel.setText('Current Directory is %s' % fn)
        
    def processConcepts(self, data):
        if data:
            self.concepts = data.getData()
        else:
            self.concepts = ''
            
    def processGeneIDs(self, data):
        if data:
            self.geneIDs = data.getData()
            self.genes_geneIDCol.update(self.R('names('+self.geneIDs+')'))
            
            self.genes_scoreCol.update(['None'] + self.R('names('+self.geneIDs+')'))
        else:
            self.geneIDs = ''
    def processReference(self, data):
        if data:
            self.reference = data.getData()
        else:
            self.reference = ''
    def parseConcepts(self):
        if self.concepts == '':
            if self.packageDir == '': return
            else:
                self.map, self.go = self.mapTerm(os.path.join(self.packageDir, "concepts2gene_v100108_delparent.txt"))
        else:
            if self.conceptColumn.currentText() == self.geneIDColumn.currentText(): return 
            self.map, self.go = self.mapTermFromDict(self.R(self.concepts, wantType = 'dict'))

    def commit(self):
        if self.geneIDs == '': return
        if not self.map: return
        if not self.go: return
        print 'Making genes'
        genes = self.makeGenesFromDict(self.R(self.geneIDs, wantType = 'dict'), unicode(self.genes_geneIDCol.currentText()), unicode(self.genes_scoreCol.currentText()))
        conceptScore = self.calcConcepts(self.map, genes)  ## make the concept scores
        weight, weightDel = self.weightConcepts(conceptScore)
        
        if self.reference != '':
            geneScore = self.scoreGenes(self.R(self.reference, wantType = 'dict')[unicode(self.referenceColumn.currentText())], genes, weight, weightDel, self.go)
        else:
            geneScore = self.scoreGenes(self.R(self.geneIDs, wantType = 'dict')[unicode(self.genes_geneIDCol.currentText())], genes, weight, weightDel, self.go)
        print geneScore
        ## now we have a concept score and a gene score so the only thing to do is to ouptut those to a data frame.
        g = geneScore.keys()
        s = [unicode(a) for a in geneScore.values()]
        c = conceptScore.keys()
        t = [unicode(a[0]) for a in conceptScore.values()]
        n = [unicode(a[1]) for a in conceptScore.values()]
        self.R(self.Rvariables['genesScores']+'<-data.frame(GeneNames = c("'+'","'.join(g)+'"), Score = c('+','.join(s)+'))', wantType = 'NoConversion')
        self.R(self.Rvariables['conceptScores']+'<-data.frame(ConceptNames = c("'+'","'.join(c)+'"), Enrichment = c('+','.join(t)+'), Total = c('+','.join(n)+'))', wantType = 'NoConversion')
        newDataGenes = redRDataFrame(data = self.Rvariables['genesScores'])
        newDataConcepts = redRDataFrame(data = self.Rvariables['conceptScores'])
        self.rSend('scores', newDataConcepts)
        self.rSend('genescores', newDataGenes)
    def mapTerm(self, file):
        f = open(file, 'r')
        map = {}
        go = {}
        for l in f:
            line = l.strip('\n').split('\t')
            if line[0] not in map.keys():
                map[line[0]] = {}
            map[line[0]][line[1]] = 1
            if line[1] not in go.keys():
                go[line[1]] = {}
            go[line[1]][line[0]] = 1
        f.close()
        return (map, go)
    def mapTermFromDict(self, d):
        map = {}
        go = {}
        for i in range(len(d[unicode(self.conceptColumn.currentText())])):
            if d[unicode(self.conceptColumn.currentText())][i] not in map.keys():
                map[d[unicode(self.conceptColumn.currentText())][i]] = []
            map[d[unicode(self.conceptColumn.currentText())][i]].append(d[unicode(self.geneIDColumn.currentText())][i])
            if d[unicode(self.geneIDColumn.currentText())][i] not in go.keys():
                go[d[unicode(self.geneIDColumn.currentText())][i]] = []
            go[d[unicode(self.geneIDColumn.currentText())][i]].append(d[unicode(self.conceptColumn.currentText())][i])
        return (map, go)
    def makeGenesFromDict(self, d, geneID, scoreID = None):
        if scoreID == 'None': scoreID = None
        genes = []
        print type(d)
        if type(d) != dict:
            print d
        for i in range(len(d[geneID])):
            g = []
            g.append(unicode(d[geneID][i]))
            if scoreID:
                g.append(d[scoreID][i])
            genes.append(g)
        print genes
        return genes 
    def calcConcepts(self, map, genes, verbose = False):
        conceptScore = {}
        print genes
        for concept in map.keys():
            t = 0.0
            n = 0
            print map[concept]
            for geneid in map[concept]:
                for g in genes:
                    if geneid == g[0]:
                        print 'Got One'
                        if len(g) > 1:
                            t += float(g[1])  ## we incorporate the weight
                        else:
                            t += 1
                n += 1 
            conceptScore[concept] = [t, n]
        return conceptScore
        
    def weightConcepts(self, conceptScore):
        import math
        weight = {}
        weightdel = {}
        for c in conceptScore.keys():
            try:
                t = conceptScore[c][0]
                n = conceptScore[c][1]
                weight[c] = math.copysign(math.log(1+abs(t)/(n*0.5))/math.log(10), float(t))
                weightdel[c] = math.copysign(math.log(1+(abs(t)-1)/float(n)*0.5)/math.log(10), float(t))
            except Exception as inst:
                print 'Exception occured', line, unicode(inst)
        return (weight, weightdel)
        
    def scoreGenes(self, allGenes, genes, weight, weightdel, go):
        score = {}
        print allGenes, 'All Genes'
        print go.keys()
        for g in allGenes:
            print g
            g = unicode(g)
            if g not in go.keys(): 
                print 'gene %s not in keys' % g
                continue
            sum = 0
            n = 0
            if g in genes:
                for g1 in go[g]:
                    if g1 in weightdel.keys():
                        sum += weightdel[g1]
                    n += 1 
            else:
                for g1 in go[g]:
                    if g1 in weight.keys():
                        sum += weight[g1]
                    n += 1 
            score[g] = float(sum)/(float(n)/float(2))
        return score
    # def test(self):
        # t = self.R(self.geneIDs, wantType = 'Convert')
        # print type(t)
        # t2 = self.R(self.geneIDs)
        # print type(t2)