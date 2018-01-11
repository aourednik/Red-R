################################################################
## Red-R is a visual programming interface for R designed to bring 
## the power of the R statistical environment to a broader audience.
## Copyright (C) 2010  name of Red-R Development
## 
## This program is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License
## as published by the Free Software Foundation; either version 2
## of the License, or (at your option) any later version.
## 
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
## 
## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
################################################################

# R Signal Thread
## Controls the execution of R funcitons into the underlying R session

import sys, os, redREnviron, numpy
os.environ['R_HOME'] = os.path.join(redREnviron.directoryNames['RDir'])
    
import rpy3.robjects as rpy
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import redrrpy._conversion as co
import redRLog

# import redRi18n
def _(a):
    return a
# _ = redRi18n.Coreget_()
mutex = QMutex()
def assign(name, object):
    try:
        rpy.r.assign(name, object)
        redRLog.log(redRLog.R, redRLog.DEBUG, _('Assigned object to %s') % name)
        return True
    except:
        redRLog.log(redRLog.REDRCORE, redRLog.ERROR, redRLog.formatException())
        return False
def Rcommand(query, silent = False, wantType = 'convert', listOfLists = False):
    
    unlocked = mutex.tryLock()
    if not unlocked:
        mb = QMessageBox(_("R Session Locked"), _("The R Session is currently locked, please wait for the prior execution to finish."), QMessageBox.Information, 
        QMessageBox.Ok | QMessageBox.Default,
        QMessageBox.NoButton, 
        QMessageBox.NoButton, 
        qApp.canvasDlg)
        mb.exec_()
        return
        
    
    output = None
    if not silent:
        redRLog.log(redRLog.R, redRLog.DEBUG, redRLog.getSafeString(query))
    #####################Forked verions of R##############################
    # try:
        # output = qApp.R.R(query)            
    # except Exception as inst:
        # print inst
        # x, y = inst
        # print showException
        #self.status.setText('Error occured!!')
        # mutex.unlock()
        # raise qApp.rpy.RPyRException(unicode(y))
        
        # return None # now processes can catch potential errors
    #####################Forked verions of R##############################
    try:
        
        output = rpy.r(unicode(query).encode('Latin-1'))
    except Exception as inst:
        redRLog.log(redRLog.R, redRLog.CRITICAL, _("Error occured in the R session.\nThe orriginal query was %s.\nThe error is %s.") % (query, inst))
        mutex.unlock()
        raise RuntimeError(unicode(inst) + '  Orriginal Query was:  ' + unicode(query))
        return None # now processes can catch potential errors
    if wantType == 'NoConversion': 
        mutex.unlock()
        return output
    # elif wantType == 'list':
        # co.setWantType(1)
    # elif wantType == 'dict':
        # co.setWantType(2)
    # print output.getrclass()
    
    output = convertToPy(output)
    # print 'converted', type(output)
    if wantType == None:
        mutex.unlock()
        raise Exception(_('WantType not specified'))
    
    if type(output) == list and len(output) == 1 and wantType != 'list':
        output = output[0]
    
    elif wantType == 'list':
        if type(output) is list:
            pass
        elif type(output) in [str, int, float, bool]:
            output =  [output]
        elif type(output) is dict:
            newOutput = []
            for name in output.keys():
                nl = output[name]
                newOutput.append(nl)
            output = newOutput
        elif type(output) is numpy.ndarray:
            output = output.tolist()
        else:
            print _('Warning, conversion was not of a known type;'), unicode(type(output))
    elif wantType == 'listOfLists':
        # print _('Converting to list of lists')
        
        if type(output) in [str, int, float, bool]:
            output =  [[output]]
        elif type(output) in [dict]:
            newOutput = []
            for name in output.keys():
                nl = output[name]
                if type(nl) not in [list]:
                    nl = [nl]
                newOutput.append(nl)                
            output = newOutput
        elif type(output) in [list, numpy.ndarray]:
            if len(output) == 0:
                output = [output]
            elif type(output[0]) not in [list]:
                output = [output]
        else:
            print _('Warning, conversion was not of a known type;'), str(type(output))
                
    mutex.unlock()
    return output
	
def convertToPy(inobject):
    #print _('in convertToPy'), inobject.getrclass()        
    try:
        if inobject.getrclass()[0] not in ['data.frame', 'matrix', 'list', 'array', 'numeric', 'vector', 'complex', 'boolean', 'bool', 'factor', 'logical', 'character', 'integer']:
            return inobject
        return co.convert(inobject)
    except Exception as e:
        redRLog.log(redRLog.REDRCORE, redRLog.ERROR, unicode(e))
        return None
def getInstalledLibraries():
    if sys.platform=="win32":
        libPath = os.path.join(redREnviron.directoryNames['RDir'],'library').replace('\\','/')
        return Rcommand('as.vector(installed.packages(lib.loc="' + libPath + '")[,1])', wantType = 'list')
    else:
        Rcommand('.libPaths(new = "'+personalLibDir+'")')
        return Rcommand('as.vector(installed.packages()[,1])', wantType = 'list')
loadedLibraries = []
def setLibPaths(libLoc):
    Rcommand('.libPaths(\''+unicode(libLoc)+'\')', wantType = 'NoConversion') ## sets the libPaths argument for the directory tree that will be searched for loading and installing librarys
    
if sys.platform=="win32":
    libPath = os.path.join(os.environ['R_HOME'], 'library').replace('\\','/')
else:
    libPath = personalLibDir
setLibPaths(libPath)
def require_librarys(librarys, repository = 'http://cran.r-project.org'):
        
        # if sys.platform=="win32":
            # libPath = '\"'+os.path.join(redREnviron.directoryNames['RDir'],'library').replace('\\','/')+'\"'
        # else:
            # libPath = '\"'+personalLibDir+'\"'
        #Rcommand('Sys.chmod('+libPath+', mode = "7777")') ## set the file permissions
        loadedOK = True
        # print 'libPath', libPath
        installedRPackages = getInstalledLibraries()
        
        Rcommand('local({r <- getOption("repos"); r["CRAN"] <- "' + repository + '"; options(repos=r)})')
        if type(librarys) == str: # convert to list if it isn't already
            librarys = [librarys]
        # print _('librarys'), librarys
        # print _('installedRPackages'), installedRPackages
        
        for library in librarys:
            if library in loadedLibraries: 
                redRLog.log(redRLog.R, redRLog.DEBUG, _('Library already loaded'))
                continue
            # print _('in loop'), library, library in installedRPackages
            # print installedRPackages
            if installedRPackages and library and (library in installedRPackages):
                redRLog.log(redRLog.R, redRLog.DEBUG, 'Loading library %s.' % library)
                Rcommand('require(' + library + ')') #, lib.loc=' + libPath + ')')
                
                loadedLibraries.append(library)
            elif library:
                if redREnviron.checkInternetConnection():
                    mb = QMessageBox(_("Download R Library"), _("You are missing some key files for this widget.\n\n%s\n\nWould you like to download it?") % unicode(library), QMessageBox.Information, QMessageBox.Ok | QMessageBox.Default, QMessageBox.Cancel | QMessageBox.Escape, QMessageBox.NoButton,qApp.canvasDlg)
                    if mb.exec_() == QMessageBox.Ok:
                        try:
                            redRLog.log(redRLog.R, redRLog.INFO, _('Installing library %s.') % library)
                            Rcommand('setRepositories(ind=1:7)', wantType = 'NoConversion')
                            Rcommand('install.packages("' + library + '")', wantType = 'NoConversion')#, lib=' + libPath + ')')
                            loadedOK = Rcommand('require(' + library + ')', wantType = 'NoConversion')# lib.loc=' + libPath + ')')
                            installedRPackages = getInstalledLibraries() ## remake the installedRPackages list
                            
                        except:
                            redRLog.log(redRLog.REDRCORE, redRLog.ERROR, redRLog.formatException())
                            redRLog.log(redRLog.R, redRLog.CRITICAL, _('Library load failed'))
                            loadedOK = False
                    else:
                        loadedOK = False
                else:
                    loadedOK = False
                if loadedOK:
                    loadedLibraries.append(library)
                        
        return loadedOK
