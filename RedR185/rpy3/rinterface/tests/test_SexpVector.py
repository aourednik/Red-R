import unittest
import sys
import rpy2.rinterface as ri

ri.initr()
def evalr(string):
    rstring = ri.StrSexpVector((string, ))
    res = ri.baseenv["parse"](text = rstring)
    res = ri.baseenv["eval"](res)
    return res

def floatEqual(x, y, epsilon = 0.00000001):
    return abs(x - y) < epsilon


class WrapperSexpVectorTestCase(unittest.TestCase):
    def testInt(self):
        sexp = ri.IntSexpVector([1, ])
        isInteger = ri.globalenv.get("is.integer")
        ok = isInteger(sexp)[0]
        self.assertTrue(ok)

    def testFloat(self):
        sexp = ri.IntSexpVector([1.0, ])
        isNumeric = ri.globalenv.get("is.numeric")
        ok = isNumeric(sexp)[0]
        self.assertTrue(ok)

    def testStr(self):
        sexp = ri.StrSexpVector(["a", ])
        isStr = ri.globalenv.get("is.character")
        ok = isStr(sexp)[0]
        self.assertTrue(ok)

    def testBool(self):
        sexp = ri.BoolSexpVector([True, ])
        isBool = ri.globalenv.get("is.logical")
        ok = isBool(sexp)[0]
        self.assertTrue(ok)

    def testComplex(self):
        sexp = ri.ComplexSexpVector([1+2j, ])
        is_complex = ri.globalenv.get("is.complex")
        ok = is_complex(sexp)[0]
        self.assertTrue(ok)

class NAValuesTestCase(unittest.TestCase):
    def testRtoNAInteger(self):
        na_int = ri.NAIntegerType()
        r_na_int = evalr("NA_integer_")[0]
        self.assertTrue(r_na_int is na_int)

    def testNAIntegertoR(self):
        na_int = ri.NAIntegerType()
        self.assertEquals(True, ri.baseenv["is.na"](na_int)[0])

    def testNAIntegerBinaryfunc(self):
        na_int = ri.NAIntegerType()
        self.assertTrue((na_int + 2) is na_int)

    def testNAIntegerInVector(self):
        na_int = ri.NAIntegerType()
        x = ri.IntSexpVector((1, na_int, 2))
        self.assertTrue(x[1] is na_int)
        self.assertEquals(1, x[0])
        self.assertEquals(2, x[2])

    def testNAIntegerRepr(self):
        na_int = ri.NAIntegerType()
        self.assertEquals("NA_integer_", repr(na_int))

    def testRtoNALogical(self):
        na_lgl = ri.NALogicalType()
        r_na_lgl = evalr("NA")[0]
        self.assertTrue(r_na_lgl is na_lgl)

    def testNALogicaltoR(self):
        na_lgl = ri.NALogicalType()
        self.assertEquals(True, ri.baseenv["is.na"](na_lgl)[0])

    def testNALogicalInVector(self):
        na_bool = ri.NALogicalType()
        x = ri.BoolSexpVector((True, na_bool, False))
        self.assertTrue(x[1] is na_bool)
        self.assertEquals(True, x[0])
        self.assertEquals(False, x[2])

    def testNAIntegerRepr(self):
        na_bool = ri.NALogicalType()
        self.assertEquals("NA", repr(na_bool))

    def testRtoNAReal(self):
        na_real = ri.NARealType()
        r_na_real = evalr("NA_real_")[0]
        self.assertTrue(r_na_real is na_real)

    def testNARealtoR(self):
        na_real = ri.NARealType()
        self.assertEquals(True, ri.baseenv["is.na"](na_real)[0])

    def testNARealBinaryfunc(self):
        na_real = ri.NARealType()
        self.assertTrue((na_real + 2.0) is na_real)

    def testNARealInVector(self):
        na_float = ri.NARealType()
        x = ri.FloatSexpVector((1.1, na_float, 2.2))
        self.assertTrue(x[1] is na_float)
        self.assertEquals(1.1, x[0])
        self.assertEquals(2.2, x[2])

    def testNARealRepr(self):
        na_float = ri.NARealType()
        self.assertEquals("NA_real_", repr(na_float))

    def testRtoNACharacter(self):
        na_character = ri.NACharacterType()
        r_na_character = evalr("NA_character_")[0]
        self.assertTrue(r_na_character is na_character)
        
    def testNACharactertoR(self):
        na_character = ri.NACharacterType()
        self.assertEquals(True, ri.baseenv["is.na"](ri.StrSexpVector((na_character, )))[0])
        
    def testNACharacterInVector(self):
        na_str = ri.NACharacterType()
        x = ri.StrSexpVector(("ab", na_str, "cd"))
        self.assertTrue(x[1] is na_str)
        self.assertEquals("ab", x[0])
        self.assertEquals("cd", x[2])

    def testNACharacterRepr(self):
        na_str = ri.NACharacterType()
        self.assertEquals("NA_character_", repr(na_str))

class SexpVectorTestCase(unittest.TestCase):

    def testMissinfType(self):
        self.assertRaises(ValueError, ri.SexpVector, [2, ])

#FIXME: end and initializing again causes currently a lot a trouble...
    def testNewWithoutInit(self):
        if sys.version_info[0] == 2 and sys.version_info[1] < 6:
            self.assertTrue(False) # cannot be tested with Python < 2.6
            return None
        import multiprocessing
        def foo(queue):
            import rpy2.rinterface as rinterface
            rinterface.endr(1)
            try:
                tmp = ri.SexpVector([1,2], ri.INTSXP)
                res = (False, None)
            except RuntimeError, re:
                res = (True, re)
            except Exception, e:
                res = (False, e)
            queue.put(res)
        q = multiprocessing.Queue()
        p = multiprocessing.Process(target = foo, args = (q,))
        p.start()
        res = q.get()
        p.join()
        self.assertTrue(res[0])

    def testNewBool(self):
        sexp = ri.SexpVector([True, ], ri.LGLSXP)
        isLogical = ri.globalenv.get("is.logical")
        ok = isLogical(sexp)[0]
        self.assertTrue(ok)
        self.assertTrue(sexp[0])

        sexp = ri.SexpVector(["a", ], ri.LGLSXP)
        isLogical = ri.globalenv.get("is.logical")
        ok = isLogical(sexp)[0]
        self.assertTrue(ok)
        self.assertTrue(sexp[0])

    def testNewInt(self):
        sexp = ri.SexpVector([1, ], ri.INTSXP)
        isInteger = ri.globalenv.get("is.integer")
        ok = isInteger(sexp)[0]
        self.assertTrue(ok)

        sexp = ri.SexpVector(["a", ], ri.INTSXP)
        isNA = ri.globalenv.get("is.na")
        ok = isNA(sexp)[0]
        self.assertTrue(ok)

    def testNewReal(self):
        sexp = ri.SexpVector([1.0, ], ri.REALSXP)
        isNumeric = ri.globalenv.get("is.numeric")
        ok = isNumeric(sexp)[0]
        self.assertTrue(ok)

        sexp = ri.SexpVector(["a", ], ri.REALSXP)
        isNA = ri.globalenv.get("is.na")
        ok = isNA(sexp)[0]
        self.assertTrue(ok)

    def testNewComplex(self):
        sexp = ri.SexpVector([1.0 + 1.0j, ], ri.CPLXSXP)
        isComplex = ri.globalenv.get("is.complex")
        ok = isComplex(sexp)[0]
        self.assertTrue(ok)

    def testNewString(self):
        sexp = ri.SexpVector(["abc", ], ri.STRSXP)
        isCharacter = ri.globalenv.get("is.character")
        ok = isCharacter(sexp)[0]
        self.assertTrue(ok)

        sexp = ri.SexpVector([1, ], ri.STRSXP)
        isCharacter = ri.globalenv.get("is.character")
        ok = isCharacter(sexp)[0]
        self.assertTrue(ok)

    def testNewUnicode(self):
        sexp = ri.SexpVector([u'abc', ], ri.STRSXP)
        isCharacter = ri.globalenv.get("is.character")
        ok = isCharacter(sexp)[0]
        self.assertTrue(ok)
        self.assertEquals('abc', sexp[0])

    def testNewList(self):
        vec = ri.ListSexpVector([1,'b',3,'d',5])
        ok = ri.baseenv["is.list"](vec)[0]
        self.assertTrue(ok)
        self.assertEquals(5, len(vec))
        self.assertEquals(1, vec[0][0])
        self.assertEquals('b', vec[1][0])

    def testNewVector(self):
        sexp_char = ri.SexpVector(["abc", ], 
                                          ri.STRSXP)
        sexp_int = ri.SexpVector([1, ], 
                                         ri.INTSXP)
        sexp = ri.SexpVector([sexp_char, sexp_int], 
                                     ri.VECSXP)
        isList = ri.globalenv.get("is.list")
        ok = isList(sexp)[0]
        self.assertTrue(ok)

        self.assertEquals(2, len(sexp))


    def testNew_InvalidType_NotAType(self):
        self.assertRaises(ValueError, ri.SexpVector, [1, ], -1)
        self.assertRaises(ValueError, ri.SexpVector, [1, ], 250)

    def testNew_InvalidType_NotAVectorType(self):
        self.assertRaises(ValueError, ri.SexpVector, [1, ], ri.ENVSXP)

    def testNew_InvalidType_NotASequence(self):
        self.assertRaises(ValueError, ri.SexpVector, 1, ri.INTSXP)

    def testGetItem(self):
        letters_R = ri.globalenv.get("letters")
        self.assertTrue(isinstance(letters_R, ri.SexpVector))
        letters = (('a', 0), ('b', 1), ('c', 2), 
                   ('x', 23), ('y', 24), ('z', 25))
        for l, i in letters:
            self.assertTrue(letters_R[i] == l)

        Rlist = ri.globalenv.get("list")
        seq_R = ri.globalenv.get("seq")

        mySeq = seq_R(ri.SexpVector([0, ], ri.INTSXP),
                      ri.SexpVector([10, ], ri.INTSXP))

        myList = Rlist(s=mySeq, l=letters_R)
        idem = ri.globalenv.get("identical")

        self.assertTrue(idem(mySeq, myList[0]))
        self.assertTrue(idem(letters_R, myList[1]))

        letters_R = ri.globalenv.get("letters")
        self.assertEquals('z', letters_R[-1])


    def testGetItemLang(self):
        formula = ri.baseenv.get('formula')
        f = formula(ri.StrSexpVector(['y ~ x', ]))
        y = f[0]
        self.assertEquals(ri.SYMSXP, y.typeof)

    def testGetItemExpression(self):
        expression = ri.baseenv.get('expression')
        e = expression(ri.StrSexpVector(['a', ]),
                       ri.StrSexpVector(['b', ]))
        y = e[0]
        self.assertEquals(ri.STRSXP, y.typeof)

    def testGetItemPairList(self):
        pairlist = ri.baseenv.get('pairlist')
        pl = pairlist(a = ri.StrSexpVector([1, ]))
        y = pl[0]
        self.assertEquals(ri.LISTSXP, y.typeof)

    def testGetItemNegativeOutOfBound(self):
        letters_R = ri.globalenv.get("letters")
        self.assertRaises(IndexError, letters_R.__getitem__,
                          -100)

    def testGetItemOutOfBound(self):
        myVec = ri.SexpVector([0, 1, 2, 3, 4, 5], ri.INTSXP)
        self.assertRaises(IndexError, myVec.__getitem__, 10)
        if (sys.maxint > ri.R_LEN_T_MAX):
            self.assertRaises(IndexError, myVec.__getitem__, 
                              ri.R_LEN_T_MAX+1)

    def testGetSliceFloat(self):
        vec = ri.FloatSexpVector([1.0,2.0,3.0])
        vec = vec[0:2]
        self.assertEquals(2, len(vec))
        self.assertEquals(1.0, vec[0])
        self.assertEquals(2.0, vec[1])

    def testGetSliceInt(self):
        vec = ri.IntSexpVector([1,2,3])
        vec = vec[0:2]
        self.assertEquals(2, len(vec))
        self.assertEquals(1, vec[0])
        self.assertEquals(2, vec[1])

    def testGetSliceIntNegative(self):
        vec = ri.IntSexpVector([1,2,3])
        vec = vec[-2:-1]
        self.assertEquals(1, len(vec))
        self.assertEquals(2, vec[0])

    def testGetSliceBool(self):
        vec = ri.BoolSexpVector([True,False,True])
        vec = vec[0:2]
        self.assertEquals(2, len(vec))
        self.assertEquals(True, vec[0])
        self.assertEquals(False, vec[1])

    def testGetSliceStr(self):
        vec = ri.StrSexpVector(['a','b','c'])
        vec = vec[0:2]
        self.assertEquals(2, len(vec))
        self.assertEquals('a', vec[0])
        self.assertEquals('b', vec[1])

    def testGetSliceComplex(self):
        vec = ri.ComplexSexpVector([1+2j,2+3j,3+4j])
        vec = vec[0:2]
        self.assertEquals(2, len(vec))
        self.assertEquals(1+2j, vec[0])
        self.assertEquals(2+3j, vec[1])

    def testGetSliceList(self):
        vec = ri.ListSexpVector([1,'b',True])
        vec = vec[0:2]
        self.assertEquals(2, len(vec))
        self.assertEquals(1, vec[0][0])
        self.assertEquals('b', vec[1][0])

    def testAssignItemDifferentType(self):
        c_R = ri.globalenv.get("c")
        myVec = c_R(ri.SexpVector([0, 1, 2, 3, 4, 5], ri.INTSXP))
        self.assertRaises(ValueError, myVec.__setitem__, 0, 
                          ri.SexpVector(["a", ], ri.STRSXP))

    def testAssignItemOutOfBound(self):
        c_R = ri.globalenv.get("c")
        myVec = c_R(ri.SexpVector([0, 1, 2, 3, 4, 5], ri.INTSXP))
        self.assertRaises(IndexError, myVec.__setitem__, 10, 
                          ri.SexpVector([1, ], ri.INTSXP))

    def testAssignItemInt(self):
        c_R = ri.globalenv.get("c")
        myVec = c_R(ri.SexpVector([0, 1, 2, 3, 4, 5], ri.INTSXP))
        myVec[0] = ri.SexpVector([100, ], ri.INTSXP)
        self.assertTrue(myVec[0] == 100)

        myVec[3] = ri.SexpVector([100, ], ri.INTSXP)
        self.assertTrue(myVec[3] == 100)

        myVec[-1] = ri.SexpVector([200, ], ri.INTSXP)
        self.assertTrue(myVec[5] == 200)

    def testAssignItemReal(self):
        c_R = ri.globalenv.get("c")
        myVec = c_R(ri.SexpVector([0.0, 1.0, 2.0, 3.0, 4.0, 5.0], 
                                          ri.REALSXP))
        myVec[0] = ri.SexpVector([100.0, ], ri.REALSXP)
        self.assertTrue(floatEqual(myVec[0], 100.0))

        myVec[3] = ri.SexpVector([100.0, ], ri.REALSXP)
        self.assertTrue(floatEqual(myVec[3], 100.0))

    def testAssignItemLogical(self):
        c_R = ri.globalenv.get("c")
        myVec = c_R(ri.SexpVector([True, False, True, True, False], 
                                  ri.LGLSXP))
        myVec[0] = ri.SexpVector([False, ], ri.LGLSXP)
        self.assertFalse(myVec[0])

        myVec[3] = ri.SexpVector([False, ], ri.LGLSXP)
        self.assertFalse(myVec[3])

    def testAssignItemComplex(self):
        c_R = ri.globalenv.get("c")
        myVec = c_R(ri.SexpVector([1.0+2.0j, 2.0+2.0j, 3.0+2.0j, 
                                   4.0+2.0j, 5.0+2.0j], 
                                  ri.CPLXSXP))
        myVec[0] = ri.SexpVector([100.0+200.0j, ], ri.CPLXSXP)
        self.assertTrue(floatEqual(myVec[0].real, 100.0))
        self.assertTrue(floatEqual(myVec[0].imag, 200.0))

        myVec[3] = ri.SexpVector([100.0+200.0j, ], ri.CPLXSXP)
        self.assertTrue(floatEqual(myVec[3].real, 100.0))
        self.assertTrue(floatEqual(myVec[3].imag, 200.0))

    def testAssignItemList(self):
        myVec = ri.SexpVector([ri.StrSexpVector(["a", ]), 
                               ri.IntSexpVector([1, ]),
                               ri.IntSexpVector([3, ])], 
                              ri.VECSXP)

        myVec[0] = ri.SexpVector([ri.FloatSexpVector([100.0, ]), ], 
                                 ri.VECSXP)
        self.assertTrue(floatEqual(myVec[0][0][0], 100.0))

        myVec[2] = ri.SexpVector([ri.StrSexpVector(["a", ]), ], 
                                 ri.VECSXP) 
        self.assertTrue(myVec[2][0][0] == "a")

    def testAssignItemString(self):
        letters_R = ri.SexpVector("abcdefghij", ri.STRSXP)
        self.assertRaises(ValueError, letters_R.__setitem__, 0, 
                          ri.SexpVector([1, ], 
                                        ri.INTSXP))

        letters_R[0] = ri.SexpVector(["z", ], ri.STRSXP)
        self.assertTrue(letters_R[0] == "z")

    def testSetSliceFloat(self):
        vec = ri.FloatSexpVector([1.0,2.0,3.0])
        vec[0:2] = ri.FloatSexpVector([11.0, 12.0])
        self.assertEquals(3, len(vec))
        self.assertEquals(11.0, vec[0])
        self.assertEquals(12.0, vec[1])
        self.assertEquals(3.0, vec[2])

    def testSetSliceInt(self):
        vec = ri.IntSexpVector([1,2,3])
        vec[0:2] = ri.IntSexpVector([11,12])
        self.assertEquals(3, len(vec))
        self.assertEquals(11, vec[0])
        self.assertEquals(12, vec[1])

    def testSetSliceIntNegative(self):
        vec = ri.IntSexpVector([1,2,3])
        vec[-2:-1] = ri.IntSexpVector([33,])
        self.assertEquals(3, len(vec))
        self.assertEquals(33, vec[1])

    def testSetSliceBool(self):
        vec = ri.BoolSexpVector([True,False,True])
        vec[0:2] = ri.BoolSexpVector([False, False])
        self.assertEquals(3, len(vec))
        self.assertEquals(False, vec[0])
        self.assertEquals(False, vec[1])

    def testSetSliceStr(self):
        vec = ri.StrSexpVector(['a','b','c'])
        vec[0:2] = ri.StrSexpVector(['d','e'])
        self.assertEquals(3, len(vec))
        self.assertEquals('d', vec[0])
        self.assertEquals('e', vec[1])

    def testSetSliceComplex(self):
        vec = ri.ComplexSexpVector([1+2j,2+3j,3+4j])
        vec[0:2] = ri.ComplexSexpVector([11+2j,12+3j])
        self.assertEquals(3, len(vec))
        self.assertEquals(11+2j, vec[0])
        self.assertEquals(12+3j, vec[1])

    def testSetSliceList(self):
        vec = ri.ListSexpVector([1,'b',True])
        vec[0:2] = ri.ListSexpVector([False, 2])
        self.assertEquals(3, len(vec))
        self.assertEquals(False, vec[0][0])
        self.assertEquals(2, vec[1][0])


    def testMissingRPreserveObjectBug(self):
        rgc = ri.baseenv['gc']
        xx = range(100000)
        x = ri.SexpVector(xx, ri.INTSXP)
        rgc()    
        self.assertEquals(0, x[0])

def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(SexpVectorTestCase)
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(WrapperSexpVectorTestCase))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(NAValuesTestCase))
    return suite

if __name__ == '__main__':
    tr = unittest.TextTestRunner(verbosity = 2)
    tr.run(suite())
    
