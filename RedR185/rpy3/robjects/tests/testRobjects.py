import unittest
import rpy2.robjects as robjects
rinterface = robjects.rinterface
import array

class RInstanceTestCase(unittest.TestCase):


    def tearDow(self):
        robjects.r._dotter = False


    def testGetItem(self):
        letters_R = robjects.r["letters"]
        self.assertTrue(isinstance(letters_R, robjects.Vector))
        letters = (('a', 0), ('b', 1), ('c', 2), ('x', 23), ('y', 24), ('z', 25))
        for l, i in letters:
            self.assertTrue(letters_R[i] == l)
        
        as_list_R = robjects.r["as.list"]
        seq_R = robjects.r["seq"]
        
        mySeq = seq_R(0, 10)
        
        myList = as_list_R(mySeq)
        
        for i, li in enumerate(myList):
            self.assertEquals(i, myList[i][0])

    def testEval(self):
        # vector long enough to span across more than one line
        x = robjects.baseenv['seq'](1, 50, 2)
        res = robjects.r('sum(%s)' %x.r_repr())
        self.assertEquals(625, res[0])
        
class MappingTestCase(unittest.TestCase):

    def testMapperR2Python_string(self):
        sexp = rinterface.globalenv.get("letters")
        ob = robjects.default_ri2py(sexp)
        self.assertTrue(isinstance(ob, 
                                   robjects.Vector))

    def testMapperR2Python_boolean(self):
        sexp = rinterface.globalenv.get("T")
        ob = robjects.default_ri2py(sexp)
        self.assertTrue(isinstance(ob, 
                                   robjects.Vector))

    def testMapperR2Python_function(self):
        sexp = rinterface.globalenv.get("plot")
        ob = robjects.default_ri2py(sexp)
        self.assertTrue(isinstance(ob, 
                                   robjects.Function))

    def testMapperR2Python_environment(self):
        sexp = rinterface.globalenv.get(".GlobalEnv")
        self.assertTrue(isinstance(robjects.default_ri2py(sexp), 
                                   robjects.Environment))

    def testMapperR2Python_s4(self):
        robjects.r('setClass("A", representation(x="integer"))')
        classname = rinterface.StrSexpVector(["A", ])
        one = rinterface.IntSexpVector([1, ])
        sexp = rinterface.globalenv.get("new")(classname, 
                                               x=one)
        self.assertTrue(isinstance(robjects.default_ri2py(sexp), 
                                   robjects.RS4))

    def testMapperPy2R_integer(self):
        py = 1
        rob = robjects.default_py2ro(py)
        self.assertTrue(isinstance(rob, robjects.Vector))
        self.assertEquals(rinterface.INTSXP, rob.typeof)

    def testMapperPy2R_boolean(self):        
        py = True
        rob = robjects.default_py2ro(py)
        self.assertTrue(isinstance(rob, robjects.Vector))
        self.assertEquals(rinterface.LGLSXP, rob.typeof)

    def testMapperPy2R_str(self):        
        py = 'houba'
        rob = robjects.default_py2ro(py)
        self.assertTrue(isinstance(rob, robjects.Vector))
        self.assertEquals(rinterface.STRSXP, rob.typeof)

    def testMapperPy2R_unicode(self):        
        py = u'houba'
        self.assertTrue(isinstance(py, unicode))
        rob = robjects.default_py2ro(py)
        self.assertTrue(isinstance(rob, robjects.Vector))
        self.assertEquals(rinterface.STRSXP, rob.typeof)
        #FIXME: more tests

    def testMapperPy2R_float(self):
        py = 1.0
        rob = robjects.default_py2ro(py)
        self.assertTrue(isinstance(rob, robjects.Vector))
        self.assertEquals(rinterface.REALSXP, rob.typeof)

    def testMapperPy2R_complex(self):
        py = 1.0 + 2j
        rob = robjects.default_py2ro(py)
        self.assertTrue(isinstance(rob, robjects.Vector))
        self.assertEquals(rinterface.CPLXSXP, rob.typeof)


    def testOverride_ri2py(self):
        class Density(object):
            def __init__(self, x):
                self._x = x

        def f(obj):
            pyobj = robjects.default_ri2py(obj)
            inherits = rinterface.baseenv["inherits"]
            classname = rinterface.SexpVector(["density", ], 
                                              rinterface.STRSXP)
            if inherits(pyobj, classname)[0]:
                pyobj = Density(pyobj)
            return pyobj
        robjects.conversion.ri2py = f
        x = robjects.r.rnorm(100)
        d = robjects.r.density(x)

        self.assertTrue(isinstance(d, Density))

def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(RInstanceTestCase)
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(MappingTestCase))
    return suite

if __name__ == '__main__':
     unittest.main()
