#!../../bin/linux-x86_64/VME

#- You may have to change wiener to something else
#- everywhere it appears in this file

< envPaths

cd "${TOP}"

## Register all support components
dbLoadDatabase "dbd/VME.dbd"
VME_registerRecordDeviceDriver pdbbase

## Load record instances VME records
devSnmpSetParam("DebugLevel",1)
devSnmpSetParam("SessionTimeout", "100000000")
epicsEnvSet("WIENER_SNMP","COMMUNITY=guru,W=WIENER-CRATE-MIB")
epicsEnvSet("ADC_crate", "HOST=192.168.197.78,crate=ADC_crate")
epicsEnvSet("VGA_crate01","HOST=192.168.197.80,crate=VGA_crate01")
epicsEnvSet("VGA_crate23","HOST=192.168.197.79,crate=VGA_crate23")

## Crate
dbLoadRecords("db/crate.db","${ADC_crate},${WIENER_SNMP}")
dbLoadRecords("db/crate.db","${VGA_crate01},${WIENER_SNMP}")
dbLoadRecords("db/crate.db","${VGA_crate23},${WIENER_SNMP}")

## sensor temperatures
dbLoadTemplate("db/temp_sensor.sub","${ADC_crate},${WIENER_SNMP}")
dbLoadTemplate("db/temp_sensor.sub","${VGA_crate01},${WIENER_SNMP}")
dbLoadTemplate("db/temp_sensor.sub","${VGA_crate23},${WIENER_SNMP}")

## channels
dbLoadTemplate("db/adc_crate_channel.sub","${ADC_crate},${WIENER_SNMP}")
dbLoadTemplate("db/vga_crate01_channel.sub","${VGA_crate01},${WIENER_SNMP}")
dbLoadTemplate("db/vga_crate23_channel.sub","${VGA_crate23},${WIENER_SNMP}")

#cd "${TOP}/iocBoot/${IOC}"
iocInit

## Start any sequence programs
#seq sncxxx,"user=dunecet"
