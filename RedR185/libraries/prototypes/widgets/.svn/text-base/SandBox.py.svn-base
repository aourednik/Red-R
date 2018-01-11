"""
<name>SandBox</name>
<description></description>
<tags>Prototypes</tags>
<priority>9010</priority>
"""

from OWRpy import *
import OWGUI,glob,imp, time
import redRGUI
import signals



class SandBox(OWRpy):
    def __init__(self, parent=None, signalManager=None):
        OWRpy.__init__(self)
        self.lineEditText = ''
        
        ### GUI ###
        self.textEdit = redRTextEdit(self.controlArea, label = 'output')
        redRCommitButton(self.controlArea, label = 'Commit', callback = self.runBench)
        self.R('a <- list(b = c(1,2,3), d = c(6,7,8))', wantType = 'NoConversion')
        
    def runBench(self):
        for i in range(20):
            t1 = time.time()
            self.R('rnorm(100000)', wantType = 'list')
            t2 = time.time()
            self.textEdit.insertPlainText(unicode(t2-t1) + '\n')
        
        