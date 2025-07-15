import os

def start_group(filename, groupname, tier):
    f = open(filename,'a')
    this_line = ""
    for i in range (0, tier):
        this_line = this_line + "  "
    this_line = this_line + '''<component name=\"{groupname}\">
'''.format(groupname=groupname)
    f.write(this_line)
    f.close()
    
def end_group(filename, tier):
    f = open(filename,'a')
    this_line = ""
    for i in range (0, tier):
        this_line = this_line + "  "
    this_line = this_line + '''</component>
'''
    f.write(this_line)
    f.close()
    
def add_pv(filename, pvname, enabled, latching, annunciating, tier):
    f = open(filename,'a')
    this_line = ""
    for i in range (0, tier):
        this_line = this_line + "  "
    this_line = this_line + '''<pv name=\"{pvname}\"><description>{pvname}</description><enabled>{enabled}</enabled><latching>{latching}</latching><annunciating>{annunciating}</annunciating></pv>
'''.format(pvname=pvname, enabled=enabled, latching=latching, annunciating=annunciating)
    f.write(this_line)
    f.close()    

def add_pv_with_delay(filename, pvname, enabled, latching, annunciating, delay, count, tier):
    f = open(filename,'a')
    this_line = ""
    for i in range (0, tier):
        this_line = this_line + "  "
    this_line = this_line + '''<pv name=\"{pvname}\"><description>{pvname}</description><enabled>{enabled}</enabled><latching>{latching}</latching><annunciating>{annunciating}</annunciating><delay>{delay}</delay><count>{count}</count></pv>
'''.format(pvname=pvname, enabled=enabled, latching=latching, annunciating=annunciating, delay=delay, count=count)
    f.write(this_line)
    f.close()

#### == Write an .sql file
filename = 'AC_alarm_config_20250714.xml'    
f = open(filename,'w')
f.write('<?xml version="1.0" encoding="UTF-8"?>')
f.write(
'''
<config name="ACDCS">
'''
    )
f.close()

#################################
### == add MPODs
#################################
channel_pvs = ["outputMeasurementCurrent", "outputMeasurementSenseVoltage", "outputMeasurementTerminalVoltage"]
start_group(filename, "MPOD", 1)
for module in range(0, 4):
    this_module = "Mod" + str(module)
    start_group(filename, this_module, 2)
    ## -- Add VGA
    for vga in range(1, 5):
        this_vga = this_module + "-VGA_Card_" + str(vga)
        for channel_pv in channel_pvs:
            this_pv = this_vga + "/" + channel_pv
            add_pv(filename, this_pv, "true", "true", "true", 3)
    ## -- Add RTD
    if module == 0:
        for rtds in range(1, 3):
            this_rtd = this_module + "-RTD_" + str(rtds)
            for channel_pv in channel_pvs:
                this_pv = this_rtd  + "/" + channel_pv
                add_pv(filename, this_pv, "true", "true", "true", 3)
    else:
        this_rtd = this_module + "-RTD"
        for channel_pv in channel_pvs:
            this_pv = this_rtd  + "/" + channel_pv
            add_pv(filename, this_pv, "true", "true", "true", 3)

    ## -- Add PACFAN & PACMAN
    for tpc in range(1, 3):
        this_tpc = this_module + "-TPC" + str(tpc)

        ## -- PACFAN & PACMAN
        for channel_pv in channel_pvs:
            this_pv = this_tpc  + "_pacFAN/" + channel_pv
            add_pv(filename, this_pv, "true", "true", "true", 3)
            this_pv = this_tpc  + "_PACMAN/" + channel_pv
            add_pv(filename, this_pv, "true", "true", "true", 3)

    ## interlock
    if module != 2:
        this_interlock = this_module + "-Interlock"
        for channel_pv in channel_pvs:
            this_pv = this_interlock  + "/" + channel_pv
            add_pv(filename, this_pv, "true", "true", "true", 3)
    end_group(filename, 2)
end_group(filename, 1)


f = open(filename,'a')
f.write('</config>')
f.close()
