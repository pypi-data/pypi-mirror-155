#ifndef RESSUMMARYMISCSTRUCT
#define RESSUMMARYMISCSTRUCT

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <fcntl.h>
 
typedef struct 
{
    int32_t iDummy[10];
    double fDummy[10];
    char cDummy[10][20];
}__attribute__ ((__packed__)) ResSummaryMiscStruct;

extern PyTypeObject ResSummaryMiscType;
extern PyStructSequence_Desc ResSummaryMiscType_desc;

PyObject *create_ResSummaryMisc(ResSummaryMiscStruct *misc_struct);



#endif /* RESSUMMARYMISCSTRUCT */
