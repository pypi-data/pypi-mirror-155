#ifndef COMMON
#define COMMON
#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <datetime.h>

PyObject *DateTimeFromString(char *str);

const size_t trim(const char *str, size_t len);
#endif /* COMMON */
