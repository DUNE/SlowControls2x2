record(ai, "$(crate)_ch$(channel)/outputMeasurementCurrent")
{
    field(DTYP,"Snmp")
    field(INP,"@$(HOST) $(COMMUNITY) $(W)::outputMeasurementCurrent.u$(channel) Float: 100 Fn")
    field(SCAN,".2 second")
    field(EGU,"A")
    field(DESC,"current")
    field(MDEL,"0.001")
    field(ADEL,"0.01")
    field(PREC, "3")
    field(HIHI,"${Ihihi}")
    field(HIGH,"${Ihigh}")
    field(LOW,"${Ilow}")
    field(LOLO,"${Ilolo}")
    field(LLSV, "${Illsv}")
    field(LSV, "${Ilsv}")
    field(HSV, "${Ihsv}")
    field(HHSV, "${Ihhsv}")
}

record(ai, "$(crate)_ch$(channel)/outputMeasurementSenseVoltage")
{
    field(DTYP,"Snmp")
    field(INP,"@$(HOST) $(COMMUNITY) $(W)::outputMeasurementSenseVoltage.u$(channel) Float: 100")
    field(SCAN,".2 second")
    field(EGU,"V")
    field(DESC,"Channel sense voltage read")
    field(MDEL,"0.01")
    field(ADEL,"0.01")
    field(PREC, "3")
    field(HIHI,"${Vhihi}")
    field(HIGH,"${Vhigh}")
    field(LOW,"${Vlow}")
    field(LOLO,"${Vlolo}")
    field(LLSV, "${Vllsv}")
    field(LSV, "${Vlsv}")
    field(HSV, "${Vhsv}")
    field(HHSV, "${Vhhsv}")
}

record(ao, "$(crate)_ch$(channel)/outputVoltage")
{
    field(DTYP,"Snmp")
    field(OUT,"@$(HOST) $(COMMUNITY) $(W)::outputVoltage.u$(channel) Float: 100 Fn")
    field(SCAN,"Passive")
    field(EGU,"V")
    field(DESC,"Channel output voltage setting")
    field(MDEL,"0")
    field(ADEL,"0")
    field(PREC, "3")
}

record(ao, "$(crate)_ch$(channel)/outputCurrent")
{
    field(DTYP,"Snmp")
    field(OUT,"@$(HOST) $(COMMUNITY) $(W)::outputCurrent.u$(channel) Float: 100 Fn")
    field(SCAN,"Passive")
    field(EGU,"A")
    field(DESC,"Channel Current limit set")
    field(MDEL,"0")
    field(ADEL,"0")
    field(PREC, "3")
}

record(longout, "$(crate)_ch$(channel)/outputSupervisionBehavior")
{
    field(DTYP,"Snmp")
    field(OUT,"@$(HOST) $(COMMUNITY) $(W)::outputSupervisionBehavior.u$(channel) INTEGER: 100 i")
    field(SCAN,"Passive")
    field(EGU,"mask")
    field(DESC,"Channel Supervision Behavior")
    field(MDEL,"0")
    field(ADEL,"0")
}

#record(stringin, "$(crate)_ch$(channel)/outputSwitchStatus")
#{
#    field(DTYP,"Snmp")
#    field(INP,"@$(HOST) $(COMMUNITY) $(W)::outputSwitch.u$(channel) BITS:__ 100 I")
#    field(SCAN,".5 second")
#    field(DESC,"Output Switch Status")
#}

record(longout, "$(crate)_ch$(channel)/outputSwitch")
{
    field(DTYP,"Snmp")
    field(OUT,"@$(HOST) $(COMMUNITY) $(W)::outputSwitch.u$(channel) ( 100 i")
    field(SCAN,"Passive")
    field(DESC,"Output Switch Setting")
    field(MDEL,"0")
    field(ADEL,"0")
    field(HIHI,"2")
    field(HIGH,"2")
    field(LOW,"0")
    field(LOLO,"0")
    field(LLSV, MAJOR)
    field(LSV, MINOR)
    field(HSV, MINOR)
    field(HHSV, MAJOR)
}

record(stringin, "$(crate)_ch$(channel)/outputStatus")
{
    field(DTYP,"Snmp")
    field(INP,"@$(HOST) $(COMMUNITY) $(W)::outputStatus.u$(channel) BITS:__ 100")
    field(SCAN,".5 second")
    field(DESC,"Output Status")
    field(FLNK,"")
}

record(ao, "$(crate)_ch$(channel)/outputSupervisionMaxCurrent")
{
    field(DTYP,"Snmp")
    field(OUT,"@$(HOST) $(COMMUNITY) $(W)::outputConfigMaxCurrent.u$(channel) Float: 100 Fn")
    field(SCAN,"Passive")
    field(EGU,"A")
    field(DESC,"Max Sense Current SW")
    field(MDEL,"0")
    field(ADEL,"0")
}

record(ao, "$(crate)_ch$(channel)/outputSupervisionMaxTerminalVoltage")
{
    field(DTYP,"Snmp")
    field(OUT,"@$(HOST) $(COMMUNITY) $(W)::outputSupervisionMaxTerminalVoltage.u$(channel) Float: 100 F")
    field(SCAN,"Passive")
    field(EGU,"V")
    field(DESC,"Max Terminal Voltage SW")
    field(MDEL,"0")
    field(ADEL,"0")
}

record(ao, "$(crate)_ch$(channel)/outputSupervisionMaxPower")
{
    field(DTYP,"Snmp")
    field(OUT,"@$(HOST) $(COMMUNITY) $(W)::outputSupervisionMaxTerminalVoltage.u$(channel) Float: 100 F")
    field(SCAN,"Passive")
    field(EGU,"W")
    field(DESC,"Max Power SW")
    field(MDEL,"0")
    field(ADEL,"0")
}

