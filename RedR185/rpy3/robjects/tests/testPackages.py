import unittest
import rpy2.robjects as robjects
import rpy2.robjects.packages as packages
rinterface = robjects.rinterface

class PackagesTestCase(unittest.TestCase):

    def testNew(self):
        env = robjects.Environment()
        env['a'] = robjects.StrVector('abcd')
        env['b'] = robjects.IntVector((1,2,3))
        env['c'] = robjects.r(''' function(x) x^2''')
        pck = robjects.packages.Package(env, "dummy_package")
        self.assertTrue(isinstance(pck.a, robjects.Vector))
        self.assertTrue(isinstance(pck.b, robjects.Vector))
        self.assertTrue(isinstance(pck.c, robjects.Function))


    def testNewWithDot(self):
        env = robjects.Environment()
        env['a.a'] = robjects.StrVector('abcd')
        env['b'] = robjects.IntVector((1,2,3))
        env['c'] = robjects.r(''' function(x) x^2''')
        pck = robjects.packages.Package(env, "dummy_package")
        self.assertTrue(isinstance(pck.a_a, robjects.Vector))
        self.assertTrue(isinstance(pck.b, robjects.Vector))
        self.assertTrue(isinstance(pck.c, robjects.Function))

    def testNewWithDotConflict(self):
        env = robjects.Environment()
        env['a.a'] = robjects.StrVector('abcd')
        env['a_a'] = robjects.IntVector((1,2,3))
        env['c'] = robjects.r(''' function(x) x^2''')
        self.assertRaises(packages.LibraryError,
                          robjects.packages.Package,
                          env, "dummy_package")


    def testNewWithDotConflict(self):
        env = robjects.Environment()
        env['__dict__'] = robjects.StrVector('abcd')
        env['a_a'] = robjects.IntVector((1,2,3))
        env['c'] = robjects.r(''' function(x) x^2''')
        self.assertRaises(packages.LibraryError,
                          robjects.packages.Package,
                          env, "dummy_package")


class ImportrTestCase(unittest.TestCase):
    def testImportStats(self):
        stats = robjects.packages.importr('stats')
        self.assertTrue(isinstance(stats, robjects.packages.Package))

class WherefromTestCase(unittest.TestCase):
    def testWherefrom(self):
        stats = robjects.packages.importr('stats')
        rnorm_pack = robjects.packages.wherefrom('rnorm')
        self.assertEquals('package:stats',
                          rnorm_pack.do_slot('name')[0])
        
def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(PackagesTestCase)
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(ImportrTestCase))
    return suite

if __name__ == '__main__':
     unittest.main()
