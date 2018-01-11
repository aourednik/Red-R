/* conversion package for rpy3.  This will take a SEXP obect and convert to a python object of the expected class as would be seen in rpy1
Modifications made on or before 12 November 2010.
This module is derived from the functions that appeared in rpy1 with changes by Kyle R Covington (KRC).  The orriginal licence block is reproduced below.*/

/*
 * $Id: rpymodule.c 510 2008-05-09 21:16:59Z warnes $
 * Implementation of the module '_rpy' and the 'Robj' type.
 */

/* ***** BEGIN LICENSE BLOCK *****
 * Version: MPL 1.1/GPL 2.0/LGPL 2.1
 *
 * The contents of this file are subject to the Mozilla Public License Version
 * 1.1 (the "License"); you may not use this file except in compliance with
 * the License. You may obtain a copy of the License at
 * http://www.mozilla.org/MPL/
 *
 * Software distributed under the License is distributed on an "AS IS" basis,
 * WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
 * for the specific language governing rights and limitations under the
 * License.
 *
 * The Original Code is the RPy python module.
 *
 * The Initial Developer of the Original Code is Walter Moreira.
 * Portions created by the Initial Developer are Copyright (C) 2002
 * the Initial Developer. All Rights Reserved.
 *
 * Contributor(s): Note that this section has been changed from the original.
 *    Kyle R Covington <kyle@red-r.org> (Maintainer)// orriginally Gregory R. Warnes <greg@warnes.net> (Maintainer)
 *
 * Alternatively, the contents of this file may be used under the terms of
 * either the GNU General Public License Version 2 or later (the "GPL"), or
 * the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
 * in which case the provisions of the GPL or the LGPL are applicable instead
 * of those above. If you wish to allow use of your version of this file only
 * under the terms of either the GPL or the LGPL, and not to allow others to
 * use your version of this file under the terms of the MPL, indicate your
 * decision by deleting the provisions above and replace them with the notice
 * and other provisions required by the GPL or the LGPL. If you do not delete
 * the provisions above, a recipient may use your version of this file under
 * the terms of any one of the MPL, the GPL or the LGPL.
 *
 * ***** END LICENSE BLOCK ***** */
 

//#include <R.h>
//#include <Rinternals.h>
#include <Python.h>
#include <Rdefines.h> // for definitions of functions
# define RPY_SEXP(obj) (((obj)->sObj)->sexp) // from rpy_rinterface.h in rpy2 this provides conversion with the tools needed to handle a conversion
#define NO_CONVERSION 0
#define VECTOR_CONVERSION 1
#define BASIC_CONVERSION 2
#define CLASS_CONVERSION 3
#define PROC_CONVERSION 4
/* Representation of R objects (instances) as instances in Python.
 */

/*these are used for debugging only

// static PyObject *my_callback = NULL; // for the callback
// PyObject *argslist;
// static PyObject *
// test_set_callback(PyObject *dummy, PyObject *args)
// {
    // PyObject *result = NULL;
    // PyObject *temp;
    
    // if (PyArg_ParseTuple(args, "O:set_callback", &temp)) {
        // if (!PyCallable_Check(temp)) {
            // PyErr_SetString(PyExc_TypeError, "parameters must be callable");
            // return NULL;
        // }
        // Py_XINCREF(temp);
        // Py_XDECREF(my_callback);
        // my_callback = temp;
        
        // Py_INCREF(Py_None);
        // result = Py_None;
    // }
    // return result;
// }

*/
PyObject *to_Pyobj_with_mode(SEXP, int);
typedef struct {
  Py_ssize_t count;
  //unsigned short int rpy_only;
  SEXP sexp;
} SexpObject;


typedef struct {
  PyObject_HEAD 
  SexpObject *sObj;
  //SEXP sexp;
} PySexpObject;



/* Convert a R named vector or list to a Python dictionary */
static PyObject *
to_PyDict(PyObject *obj, SEXP names)
{
  int len, i;
  PyObject *it, *dict, *tmp;
  const char *name;

    // if(my_callback){
        // argslist = Py_BuildValue("(O)", Py_BuildValue("(s)", "in dict conversion"));
        // PyObject_CallObject(my_callback, argslist);
    // }
  if ((len = PySequence_Length(obj)) < 0)
        {
            // if(my_callback){
                // argslist = Py_BuildValue("(O)", Py_BuildValue("(s)", "error in obj len"));
                // PyObject_CallObject(my_callback, argslist);
            // }
        // tmp = Py_BuildValue("s", "PySequence_Length(obj) < 0!!!");  // we are at least getting an robj
        
        // return tmp;
        return -1;
        }

  dict = PyDict_New();
  for (i=0; i<len; i++) {
    if (!(it = PyList_GetItem(obj, i)))
      
        {
            // if(my_callback){
                // argslist = Py_BuildValue("(O)", Py_BuildValue("(s)", "could not get the item"));
                // PyObject_CallObject(my_callback, argslist);
            // }
        // tmp = Py_BuildValue("s", "failed in (it = PyList_GetItem(obj, i))!!!");  // we are at least getting an robj
        
        // return tmp;
        return -1;
        }
    name = CHAR(STRING_ELT(names, i));
    if ((PyDict_SetItemString(dict, name, it)) < 0) {
        {
            // if(my_callback){
                // argslist = Py_BuildValue("(O)", Py_BuildValue("(ss)", "could not set item string", name));
                // PyObject_CallObject(my_callback, argslist);
            // }
        // tmp = Py_BuildValue("s", "failed in PyDict_SetItemString(dict, name, it)) < 0!!!");  // we are at least getting an robj
        
        // return tmp;
        return -1;
        }
      //return NULL;
    }
  }

  return dict;
}

/* We need to transpose the list because R makes array by the
 * fastest index */
static PyObject *
ltranspose(PyObject *list, int *dims, int *strides,
             int pos, int shift, int len)
{
  PyObject *nl, *it;
  int i;

  if (!(nl = PyList_New(dims[pos])))
    return NULL;

  if (pos == len-1) {
    for (i=0; i<dims[pos]; i++) {
      if (!(it = PyList_GetItem(list, i*strides[pos]+shift)))
        return NULL;
      Py_INCREF(it);
      if (PyList_SetItem(nl, i, it) < 0)
        return NULL;
    }
    return nl;
  }

  for (i=0; i<dims[pos]; i++) {
    if (!(it = ltranspose(list, dims, strides, pos+1, shift, len)))
      return NULL;
    if (PyList_SetItem(nl, i, it) < 0)
      return NULL;
    shift += strides[pos];
  }

  return nl;
}
      
/* Convert a Python list to a Python array (in the form of
 * list of lists of ...) */
static PyObject *
to_PyArray(PyObject *obj, int *dims, int l)
{
  PyObject *list;
  int i, c, *strides;

  strides = (int *)PyMem_Malloc(l*sizeof(int));
  if (!strides)
    PyErr_NoMemory();

  c = 1;
  for (i=0; i<l; i++) {
    strides[i] = c;
    c *= dims[i];
  }

  list = ltranspose(obj, dims, strides, 0, 0, l);
  PyMem_Free(strides);

  return list;
}

/* Convert an R object to a 'vector' Python object (mode 1) */
/* NOTE: R vectors of length 1 will yield a python list of length 1*/
int
to_Pyobj_vector(SEXP robj, PyObject **obj, int mode)
{
  PyObject *it, *tmp;
  SEXP names, dim;
  int len, *integers, i, type;
  const char *strings, *thislevel;
  double *reals;
  Rcomplex *complexes;
#ifdef WITH_NUMERIC
  PyObject *array;
#endif

  if (!robj)
    {
    // return -1;                  /* error */
    // if(my_callback){
        // argslist = Py_BuildValue("(O)", Py_BuildValue("(s)", "robj does not exist"));
        // PyObject_CallObject(my_callback, argslist);
    // }
    return 1;
    }
  if (robj == R_NilValue) {
    Py_INCREF(Py_None);
    *obj = Py_None;
    return 1;                   /* succeed */
  }

  len = GET_LENGTH(robj);
  tmp = PyList_New(len);
  type = TYPEOF(robj);

    // if(my_callback){
        // argslist = Py_BuildValue("(O)", Py_BuildValue("(si)", "robj length is ", len));
        // PyObject_CallObject(my_callback, argslist);
    // }
    
  /// break for checking the R length and other aspects
  for (i=0; i<len; i++) {
    switch (type)
      {
      case LGLSXP:
            // if(my_callback){
                // argslist = Py_BuildValue("(O)", Py_BuildValue("(s)", "In LGLSXP"));
                // PyObject_CallObject(my_callback, argslist);
            // }
         integers = INTEGER(robj);
         if(integers[i]==NA_INTEGER) /* watch out for NA's */
           {
             if (!(it = PyInt_FromLong(integers[i])))
             //return -1;
             tmp = Py_BuildValue("s", "failed in the PyInt_FromLong");  // we are at least getting an robj
             *obj = tmp;
             return 1;
             //it = Py_None;
           }
         else if (!(it = PyBool_FromLong(integers[i])))
            {
            tmp = Py_BuildValue("s", "failed in the PyBool_FromLong");  // we are at least getting an robj
             *obj = tmp;
             return 1;
           //return -1;
           }
         break;
      case INTSXP:
            // if(my_callback){
                // argslist = Py_BuildValue("(O)", Py_BuildValue("(s)", "In INTSXP"));
                // PyObject_CallObject(my_callback, argslist);
            // }
        integers = INTEGER(robj);
        if(isFactor(robj)) {
          /* Watch for NA's! */
          if(integers[i]==NA_INTEGER)
            it = PyString_FromString(CHAR(NA_STRING));
          else
            {
              thislevel = CHAR(STRING_ELT(GET_LEVELS(robj), integers[i]-1));
              if (!(it = PyString_FromString(thislevel)))
                {
                tmp = Py_BuildValue("s", "failed in the PyString_FromString");  // we are at least getting an robj
                *obj = tmp;
                return 1;
                }
                //return -1;
            }
        }
        else {
          if (!(it = PyInt_FromLong(integers[i])))
            {
            tmp = Py_BuildValue("s", "failed in the PyInt_FromLong");  // we are at least getting an robj
                *obj = tmp;
                return 1;
            //return -1;
            }
        }
        break;
      case REALSXP:
            // if(my_callback){
                // argslist = Py_BuildValue("(O)", Py_BuildValue("(s)", "In REALSXP"));
                // PyObject_CallObject(my_callback, argslist);
            // }
        reals = REAL(robj);
        if (!(it = PyFloat_FromDouble(reals[i])))
        {
        // tmp = Py_BuildValue("s", "failed in the PyFloat_FromDouble");  // we are at least getting an robj
                // *obj = tmp;
                // return 1;
         return -1;
        }
        break;
      case CPLXSXP:
            // if(my_callback){
                // argslist = Py_BuildValue("(O)", Py_BuildValue("(s)", "In CPLXSXP"));
                // PyObject_CallObject(my_callback, argslist);
            // }
        complexes = COMPLEX(robj);
        if (!(it = PyComplex_FromDoubles(complexes[i].r,
                                         complexes[i].i)))
          {
            
            // tmp = Py_BuildValue("s", "failed in PyComplex_FromDoubles!!!");  // we are at least getting an robj
            // *obj = tmp;
            // return 1;
            return -1;
            }
        break;
      case STRSXP:
            // if(my_callback){
                // argslist = Py_BuildValue("(O)", Py_BuildValue("(s)", "In STRSXP"));
                // PyObject_CallObject(my_callback, argslist);
            // }
        if(STRING_ELT(robj, i)==R_NaString)
          it = PyString_FromString(CHAR(NA_STRING));
        else
          {
            strings = CHAR(STRING_ELT(robj, i));
            if (!(it = PyString_FromString(strings)))
              {
            
                // tmp = Py_BuildValue("s", "failed in PyString_FromString!!!");  // we are at least getting an robj
                // *obj = tmp;
                // return 1;
                return -1;
                }
          }
        break;
      case LISTSXP:
            // if(my_callback){
                // argslist = Py_BuildValue("(O)", Py_BuildValue("(s)", "In LISTSXP"));
                // PyObject_CallObject(my_callback, argslist);
            // }
        if (!(it = to_Pyobj_with_mode(elt(robj, i), mode)))
            {
            
            // tmp = Py_BuildValue("s", "failed in to_Pyobj_with_mode LISTSXP!!!");  // we are at least getting an robj
            // *obj = tmp;
            // return 1;
            return -1;
            }
        break;
      case VECSXP:
            // if(my_callback){
                // argslist = Py_BuildValue("(O)", Py_BuildValue("(s)", "In VECSXP"));
                // PyObject_CallObject(my_callback, argslist);
            // }
        if (!(it = to_Pyobj_with_mode(VECTOR_ELT(robj, i), mode)))
            {
            return -1;
            }
        break;
      default:
        Py_DECREF(tmp);
        return 0;                 /* failed */
    }
    
    if (PyList_SetItem(tmp, i, it) < 0) // there was a failure in setting the item
            {
            
            // tmp = Py_BuildValue("s", "failed in PyList_SetItem!!!");  // we are at least getting an robj
            // *obj = tmp;
            // return 1;
            return -1;
            }
  }

  dim = GET_DIM(robj);
  if (dim != R_NilValue) {
// #ifdef WITH_NUMERIC
    // if(use_numeric)
      // {
        // array = to_PyNumericArray(tmp, dim);
        // if (array) {                /* If the conversion to Numeric succeed.. */
          // *obj = array;             /* we are done */
          // Py_DECREF(tmp);
          // return 1;
        // }
        // PyErr_Clear();
      // }
// #endif
    len = GET_LENGTH(dim);
    *obj = to_PyArray(tmp, INTEGER(dim), len);
    Py_DECREF(tmp);
    return 1;
  }
    // if(my_callback){
                // argslist = Py_BuildValue("(O)", Py_BuildValue("(O)", tmp));
                // PyObject_CallObject(my_callback, argslist);
            // }
  names = GET_NAMES(robj);
  if (names == R_NilValue)
    {
    *obj = tmp;
        // if(my_callback){
                // argslist = Py_BuildValue("(O)", Py_BuildValue("(s)", "returning as list (of lists)"));
                // PyObject_CallObject(my_callback, argslist);
            // }
    }
  else {
    *obj = to_PyDict(tmp, names);
        // if(my_callback){
                // argslist = Py_BuildValue("(O)", Py_BuildValue("(s)", "returning as dict"));
                // PyObject_CallObject(my_callback, argslist);
            // }
    Py_DECREF(tmp);
  }
  return 1;
}

/* Convert an R object to a 'basic' Python object (mode 2) */
/* NOTE: R vectors of length 1 will yield a python scalar */
int
to_Pyobj_basic(SEXP robj, PyObject **obj)
{
  int status;
  PyObject *tmp;
      // if(my_callback){
            // argslist = Py_BuildValue("(O)", Py_BuildValue("(s)", "in to_Pyobj_basic"));
            // PyObject_CallObject(my_callback, argslist);
        // }
  status = to_Pyobj_vector(robj, &tmp, BASIC_CONVERSION);
    // if(my_callback){
            // argslist = Py_BuildValue("(O)", Py_BuildValue("(si)", "to_Pyobj_vector complete with value", status));
            // PyObject_CallObject(my_callback, argslist);
        // }
  if(status==1 && PyList_Check(tmp) && PyList_Size(tmp) == 1)
    {
      *obj = PyList_GetItem(tmp, 0);
      Py_XINCREF(*obj);
      Py_DECREF(tmp);
    }
  else
    *obj = tmp;
  
  return status;
}

PyObject *
to_Pyobj_with_mode(SEXP robj, int mode)  // only basic conversion is supported at this time
{

  PyObject *obj;
  int i;

  // if(my_callback){
        // argslist = Py_BuildValue("(O)", Py_BuildValue("(s)", "in to_Pyobj_with_mode"));
        // PyObject_CallObject(my_callback, argslist);
    // }
  // commented by KRC
  // switch (mode)
    // {
    // case PROC_CONVERSION:
      // i = to_Pyobj_proc(robj, &obj);
      // if (i<0) return NULL;
      // if (i==1) break;
    // case CLASS_CONVERSION:
      // i = to_Pyobj_class(robj, &obj);
      // if (i<0) return NULL;
      // if (i==1) break;
    // case BASIC_CONVERSION:
      i = to_Pyobj_basic(robj, &obj);
      // if(my_callback){
        // argslist = Py_BuildValue("(O)", Py_BuildValue("(si)", "to_Pyobj_basic complete with result", i));
        // PyObject_CallObject(my_callback, argslist);
        // }
      if (i<0) return NULL;
      //if (i==1) break;
    // case VECTOR_CONVERSION:
      // i = to_Pyobj_vector(robj, &obj, mode=VECTOR_CONVERSION);
      // if (i<0) return NULL;
      // if (i==1) break;
    // default:
      // obj = (PyObject *)Robj_new(robj, TOP_MODE);
  // }
    
  return obj;
}

// the convert_to_py function is used to convert a PySexpObject to a SEXP and then perform the conversion.  This function was created by KRC
static PyObject *
convert_to_py(PyObject * self, PyObject * args)
{
    PyObject * obj;             // init a new py obj
    SEXP * robj;                // make a holder for the SEXP obj
    PySexpObject * rpyObj;      // make a holder for the PySexpObject
    
    // if(my_callback){
        // argslist = Py_BuildValue("(O)", Py_BuildValue("(s)", "converter initialized"));
        // PyObject_CallObject(my_callback, argslist);
    // }
    
    if (!PyArg_ParseTuple(args, "O", &rpyObj)) // parse the args to set the PySexpObject to the incomming PySexpObject
        {
            // if(my_callback){
            // argslist = Py_BuildValue("(O)", Py_BuildValue("(s)", "conversion to rpyobj failed"));
            // PyObject_CallObject(my_callback, argslist);
            // }
        // return Py_BuildValue("s", "conversion failed to set O ln 306");
        return NULL;
        }
    robj = RPY_SEXP(rpyObj);        // extract the SEXP from the PySexpObject    
    obj = to_Pyobj_with_mode(robj, BASIC_CONVERSION);           // perform the conversion
    return obj;                     // return the new obj
}
static PyMethodDef RConvert[] = {
    //...
    {"convert", convert_to_py, METH_VARARGS,
        "Convert using the basic conversion."},
     // {"setCallback", test_set_callback, METH_VARARGS,
     // "Sets the callback for this session."},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};
PyMODINIT_FUNC
init_conversion(void)
{
    (void) Py_InitModule("_conversion", RConvert);
}

