TOP=../..
include $(TOP)/configure/CONFIG
#----------------------------------------
#  ADD MACRO DEFINITIONS AFTER THIS LINE
#=============================

#USR_CFLAGS += -I/usr/local/include        #Path to snmp if ness.
USR_CFLAGS += `net-snmp-config --cflags`
USR_CFLAGS += -DNETSNMP_NO_INLINE

USR_LDFLAGS += `net-snmp-config --libs`
PROD_LDLIBS += `net-snmp-config --libs`

USR_CFLAGS += $(shell $(PERL) ../getNetSNMPversion.pl)
USR_CPPFLAGS += $(shell $(PERL) ../getNetSNMPversion.pl)

#==================================================
# Build an IOC support library
LIBRARY_IOC += devSnmp

# xxxRecord.h will be created from xxxRecord.dbd
#DBDINC += xxxRecord
# install devXxxSoft.dbd into <top>/dbd
DBD += devSnmp.dbd

# The following are compiled and added to the Support library

devSnmp_SRCS += snmpRegister.cpp
devSnmp_SRCS += snmpSessShow.c
devSnmp_SRCS += devSnmp.cpp

devSnmp_LIBS += $(EPICS_BASE_IOC_LIBS)

#=============================
# build an ioc application

PROD_IOC = VME
# snmp.dbd will be created and installed
DBD += VME.dbd

# snmp.dbd will be made up from these files:
VME_DBD += base.dbd
VME_DBD += devSnmp.dbd

# <name>_registerRecordDeviceDriver.cpp will be created from <name>.dbd
VME_SRCS += VME_registerRecordDeviceDriver.cpp
VME_SRCS_DEFAULT += VMEMain.cpp
VME_SRCS_vxWorks += -nil-

# The following adds support from base/src/vxWorks
VME_OBJS_vxWorks += $(EPICS_BASE_BIN)/vxComLibrary

VME_LIBS += devSnmp

# NOTE: To build SNL programs, SNCSEQ must be defined
# in the <top>/configure/RELEASE file

ifneq ($(SNCSEQ),)
    # This builds sncExample as a component of snmp
    VME_SNCFLAGS += +r
    VME_DBD += sncExample.dbd
    VME_SRCS += sncExample.stt
    VME_LIBS += seq pv

    # The following builds sncProgram as a standalone application
    PROD_HOST += sncProgram
    sncProgram_SNCFLAGS += +m
    sncProgram_SRCS += sncProgram.st
    sncProgram_LIBS += seq pv
    sncProgram_LIBS += $(EPICS_BASE_HOST_LIBS)
endif

VME_LIBS += $(EPICS_BASE_IOC_LIBS)

#===========================

include $(TOP)/configure/RULES
#----------------------------------------
#  ADD RULES AFTER THIS LINE

