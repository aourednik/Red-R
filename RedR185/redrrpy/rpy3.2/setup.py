## setup file for the conversion module Kyle R. Covington Copywrite 2010

from distutils.core import setup, Extension
import os
RHOME = '/usr/lib/R'  # this must be changed if the location of the R installation is different from the default or if the user wishes to use versions of R other than 2.9.2
include_dirs = [ os.path.join(RHOME.strip(), 'include'), os.path.join(RHOME.strip(), 'bin'),
		os.path.join(RHOME.strip(), 'bin'), os.path.join(RHOME.strip(), 'lib'),
                '~/R-2.12.1/src/include',         
                         
                         'src' ]
libraries= ['R']
r_libs = [ # Different verisons of R put .so/.dll in different places
              os.path.join(RHOME, 'bin'),  # R 2.0.0+
              os.path.join(RHOME, 'lib'),  # Pre 2.0.0
             ]
library_dirs = r_libs
        
        
module1 = Extension('_conversion',
                    sources = ['src/conversion.c']
                    ,
                    include_dirs=include_dirs,
                    libraries=libraries,
                    library_dirs=library_dirs)
setup (name = 'Conversion',
       version = '1.0',
       description = 'This module provides the conversion function to convert rpy2 objects to standard python types.',
       ext_modules = [module1])