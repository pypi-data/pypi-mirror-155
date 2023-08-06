#ifndef MCSSTRUCT
#define MCSSTRUCT

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "structures.h"
#include "common.h"



PyObject *create_mcs(
    const MCSStruct *const mcs_struct,
    const int32_t *const  mcsevent_struct,
    const EventStruct *const event_struct,
    const BEEventStruct *const beevent_struct,
    const CCFEventStruct *const ccfevent_struct,
    const MODEventStruct *const modevent_struct,
    const uint_fast32_t count,
    const char *encoding);

#endif /* MCSSTRUCT */
