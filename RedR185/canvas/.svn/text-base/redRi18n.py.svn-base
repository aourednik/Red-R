## redRi18n (internationalization)  a module to control the internationalization of Red-R, ideally this should use the _() syntax that is common to the internationalization community.

## Copywrite 2011 Kyle R Covington

import redREnviron, gettext, os

core_ = None
def superfallback(a):
    return a

def Coreget_(domain = 'messages', locale = os.path.join(redREnviron.directoryNames['redRDir'], 'languages'), languages = [redREnviron.settings['language']], fallback = False):
    global core_
    if core_ != None:
        return core_
    else:
        try:
            t = gettext.translation(domain, locale, languages = ['latin'], fallback = fallback)
            core_ = t.gettext
            return core_  # returns the function
        except Exception as inst:
            print 'Exception occured in setting the get_ function, %s' % unicode(inst)
            return superfallback
        
def get_(domain = 'messages', package = 'base', languages = redREnviron.settings['language'], fallback = False):
    try:
        t = gettext.translation(domain, locale  = os.path.join(redREnviron.directoryNames['libraryDir'], package, 'languages'), languages = redREnviron.settings['language'], fallback = fallback)
        return t.gettext  # returns the function
    except Exception as inst:
        print 'Exception occured in setting the get_ function, %s' % unicode(inst)
        return superfallback