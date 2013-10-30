#include <Python.h>

PyDoc_STRVAR(baseutils_strtoint_doc, "string to int, assert len(string) <= 8");

static PyObject * 
baseutils_strtoint(PyObject *object, PyObject *args)
{
	PyObject *str;
	int strlen;
	int extra;
	long long value;
	if (!PyArg_ParseTuple(args, "O:strtoint", &str))
		return NULL;
	if (!PyString_Check(str)) {
		PyErr_SetString(PyExc_TypeError, "expect a string");
		return NULL;
	}
	strlen = PyString_Size(str); 
	extra = (8 - strlen) * 8;
	value = *(long *)((PyStringObject *)str)->ob_sval;
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

static PyMethodDef baseutils_methods[] = {
	{"strtoint", (PyCFunction)baseutils_strtoint,
		METH_VARARGS, baseutils_strtoint_doc},
	{NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC initbaseutils(void)
{
	PyObject *m;
	m = Py_InitModule("baseutils", baseutils_methods);
	if (m == NULL)
		return;
}


