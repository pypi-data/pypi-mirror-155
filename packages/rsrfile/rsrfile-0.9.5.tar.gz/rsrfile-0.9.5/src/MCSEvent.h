#ifndef MCSEVENT
#define MCSEVENT

#define PY_SSIZE_T_CLEAN
#include <Python.h>

extern PyTypeObject MCSEventType;
extern PyStructSequence_Field MCSEventType_fields[];
extern PyStructSequence_Desc MCSEventType_desc;

#endif /* MCSEVENT */
