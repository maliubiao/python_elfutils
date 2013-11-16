#include <Python.h>

PyDoc_STRVAR(baseutils_string_to_signed_doc, "string to signed int");

static PyObject * 
baseutils_string_to_signed(PyObject *object, PyObject *args)
{
	PyObject *str;
	int strlen;
	int extra;
	signed long value;
	if (!PyArg_ParseTuple(args, "O:string_to_signed", &str))
		return NULL;
	if (!PyString_Check(str)) {
		PyErr_SetString(PyExc_TypeError, "expect a string");
		return NULL;
	}
	strlen = PyString_Size(str); 
	extra = (8 - strlen) * 8;
	value = *(signed long *)((PyStringObject *)str)->ob_sval;
	if (strlen == 0) {
		PyErr_SetString(PyExc_AssertionError, "len(string) != 0");
		return NULL;
	} 
	if (strlen > 8) {
		PyErr_SetString(PyExc_AssertionError, "len(string) <= 8");
		return NULL;
	} 
	return PyInt_FromLong(value<<extra>>extra);
}


PyDoc_STRVAR(baseutils_string_to_unsigned_doc, "string to unsigned int");

static PyObject * 
baseutils_string_to_unsigned(PyObject *object, PyObject *args)
{
	PyObject *str;
	int strlen;
	int extra;
	unsigned long value;
	if (!PyArg_ParseTuple(args, "O:string_to_unsigned", &str))
		return NULL;
	if (!PyString_Check(str)) {
		PyErr_SetString(PyExc_TypeError, "expect a string");
		return NULL;
	}
	strlen = PyString_Size(str); 
	extra = (8 - strlen) * 8;
	value = *(unsigned long *)((PyStringObject *)str)->ob_sval;
	if (strlen == 0) {
		PyErr_SetString(PyExc_AssertionError, "len(string) != 0");
		return NULL;
	} 
	if (strlen > 8) {
		PyErr_SetString(PyExc_AssertionError, "len(string) <= 8");
		return NULL;
	} 
	return PyInt_FromLong(value<<extra>>extra);
}

PyDoc_STRVAR(baseutils_get_types_length_doc, "get default sizes of basic typs");

static PyObject *
baseutils_get_types_length(PyObject *object, PyObject *args)
{
	PyObject *types;	
	types = PyDict_New();
	PyDict_SetItemString(types, "char", PyInt_FromLong(sizeof(char)));
	PyDict_SetItemString(types, "short", PyInt_FromLong(sizeof(short)));
	PyDict_SetItemString(types, "int", PyInt_FromLong(sizeof(int)));
	PyDict_SetItemString(types, "long", PyInt_FromLong(sizeof(long)));
	PyDict_SetItemString(types, "longlong", PyInt_FromLong(sizeof(long long)));
	PyDict_SetItemString(types, "float", PyInt_FromLong(sizeof(float)));
	PyDict_SetItemString(types, "double", PyInt_FromLong(sizeof(double)));
	PyDict_SetItemString(types, "longdouble", PyInt_FromLong(sizeof(long double)));
	return types;
} 

static PyMethodDef baseutils_methods[] = {
	{"string_to_unsigned", (PyCFunction)baseutils_string_to_unsigned,
		METH_VARARGS, baseutils_string_to_unsigned_doc},
	{"string_to_signed", (PyCFunction)baseutils_string_to_signed,
		METH_VARARGS, baseutils_string_to_signed_doc},
	{"get_types_length", (PyCFunction)baseutils_get_types_length,
	METH_VARARGS, baseutils_get_types_length_doc}, 
	{NULL, NULL, 0, NULL}
};


PyMODINIT_FUNC initbaseutils(void)
{
	PyObject *m;
	m = Py_InitModule("baseutils", baseutils_methods);
	if (m == NULL)
		return;
}


