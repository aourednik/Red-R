"""
<name>Notes</name>
<tags>R</tags>
<icon>notes.png</icon>
"""

from OWRpy import *


class notes(OWRpy):
    
    def __init__(self, parent=None, signalManager=None):

        OWRpy.__init__(self)
        self.controlArea.layout().addWidget(self.notesBox)