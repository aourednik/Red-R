def parseFile(f, skipList = None):
    newF = []
    if skipList == None:
        skipList = []
    l = f.readline()
    while l:
        matches = re.findall(r"'[A-Za-z0-9\ \(\)\[\]\!\?\.\-\_]*'", l)
        matches += re.findall(r'"[A-Za-z0-9\ \(\)\[\]\!\?\.\-\_]*"', l)
        if len(matches) == 0:
            newF.append(l)
        else:
            print 'the line is :: %s' % l
            for m in matches:
                if m in skipList: continue
                print 'type 1 to change %s to _(%s), type 2 to never see this again, or 3 to edit the entire line.' % (m, m)
                myReturn = raw_input('')
                if myReturn == str(1):
                    l = l.replace(m, '_(%s)' % m)
                elif myReturn == str(2):
                    skipList.append(m)
                elif myReturn == str(3):
                    newLine = raw_input('')
                    newF.append(newLine)
            newF.append(l)
        l = f.readline()
    return newF
a = os.listdir('C:/Python26/Lib/site-packages/RedRWorkingTrunk/libraries/base/widgets')
skipList = []
for i in a:
    if os.path.isdir(os.path.join('C:/Python26/Lib/site-packages/RedRWorkingTrunk/libraries/base/widgets', i)): continue
    if not os.path.isfile(os.path.join('C:/Python26/Lib/site-packages/RedRWorkingTrunk/libraries/base/widgets', i)): continue
    elif i[0] == 'l': continue
    elif 'l'+i in a: continue
    elif '.pyc' in i: continue
    else:
        with open(os.path.join('C:/Python26/Lib/site-packages/RedRWorkingTrunk/libraries/base/widgets', i), 'r') as f:
            n = parseFile(f, skipList)
            f.close()
            g = open(os.path.join('C:/Python26/Lib/site-packages/RedRWorkingTrunk/libraries/base/widgets', 'l'+i), 'w')
            g.write(''.join(n))
            g.close()