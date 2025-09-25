#!/usr/bin/env python
#  -*- coding: utf-8 -*-
"""
    MCC 134 HAT Temp reader

    Purpose:
        Read voltage values from raspi hat, push to influxdb and to a OPC UA server

    Last modified : 2025-09-03
    by:             Nicolas Sallin, nicolas.sallin@unibe.ch

"""

from __future__ import print_function
import time
from sys import stdout
import sys, os
#sys.path.append('/home/pi/daqhats')
from daqhats import mcc134,mcc118, OptionFlags, HatIDs, HatError, TcTypes
from daqhats_utils import select_hat_device, enum_mask_to_string, tc_type_to_string
import subprocess

import asyncio
from asyncua import Server, ua
import socket

import configparser

from datetime import datetime
import pytz
from influxdb import InfluxDBClient

async def main():
    conf = configparser.ConfigParser()
    conf.read('/home/pi/SlowControls2x2/HVFilterPot_Raspi/config.ini')

    db = conf["DATABASE"]
    meta = conf["METADATA"]
    para = conf["PARAMETERS"]

    #Read device IP
    ips = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ips.connect((db["PINGIP"], 80))
    ip = ips.getsockname()[0]
    ips.close()

    # Constants
    CURSOR_BACK_2 = '\x1b[2D'
    ERASE_TO_END_OF_LINE = '\x1b[0K'
    OFFSET_SENS_A = 0.0
    OFFSET_SENS_B = 0.0
    OFFSET_SENS_C = 0.0
    # ped = [146.1,152.4,147.3,147.3]
    # kv = [0.01106,0.01098,0.01094,0.01092]

    # New calib values, 2025-08-27, elog 6905
    ped = [0, -1.7572, -1.7115, -1.7129, -1.7556]
    kv = [0, 10.9639, 10.8981, 10.8949 ,10.9030]

    client = InfluxDBClient(host = db["IP"], port = int(db["PORT"]), database = db["NAME"])

    tc_type = TcTypes.TYPE_K   # change this to the desired thermocouple type
    channels_tc = {0}
    channels_adc = {0,1,2,3,4}

    #Setup OPC UA server
    s = Server()
    await s.init()
    opc_port = "4841"
    s.set_endpoint("opc.tcp://"+ip+":"+opc_port)
    idx = await s.register_namespace("http://"+ip+":"+opc_port)
    uaobj = await s.nodes.objects.add_object(idx,db["OPCSERVERNAME"])
    uavar = []
    for chan_adc in channels_adc:
        uavar.append(await uaobj.add_variable(idx,"hvchan%02d" % chan_adc,0.0))
        await uavar[-1].set_writable()
    for chan_tc in channels_tc:
        uavar.append(await uaobj.add_variable(idx,"hvtc%02d" % chan_tc,0.0))
        await uavar[-1].set_writable()

    try:
        # Get an instance of the selected hat device object.
        address_tc = select_hat_device(HatIDs.MCC_134)
        address_adc = select_hat_device(HatIDs.MCC_118)
        hat_tc = mcc134(address_tc)
        hat_adc = mcc118(address_adc)
        for channel in channels_tc:
            hat_tc.tc_type_write(channel, tc_type)
        print('    Offset constants: OFFSET_SENS_A = {}, OFFSET_SENS_B = {}, OFFSET_SENS_C = {}'.format(OFFSET_SENS_A, OFFSET_SENS_B, OFFSET_SENS_C))
        print('    PED constants: PED_0 = {}, PED_1 = {}, PED_2 = {}, PED_3 = {}, PED_4 = {}'.format(ped[0], ped[1], ped[2], ped[3], ped[4]))
        print('    KV cosntants: KV_0 = {}, KV_1 = {}, KV_2 = {}, KV_3 = {}, KV_4 = {}'.format(kv[0], kv[1], kv[2], kv[3], kv[4]))
        print('    Thermocouple type: ' + tc_type_to_string(tc_type))
        print('\nAcquiring data ... Press Ctrl-C to abort')

        # Display the header row for the data table.
        print('\n  Sample', end='')
        for channel in channels_tc:
            print('       TC ', channel, end='')
        for channel in channels_adc:
            print('\n\n        kV',channel, end='')
            print('        ADC', channel,end='')
            print('        Raw_value', channel,end='')
            #print('        Raw_value*1000-PED', channel,end='')
        print('')
        
        try:
            samples_per_channel = 0
            json_payload = []
            
            async with s:
                while True:
                    # Display the updated samples per channel count
                    samples_per_channel += 1
                    print('\r        \033[14A{:8d}'.format(samples_per_channel))
                    
                    # Read TCs
                    values_tc = []
                    for channel in channels_tc:
                        value_tc = hat_tc.t_in_read(channel)
                        
                        #corr = (hat_tc.cjc_read(channel)-24.3)*1.7
                        #value=value - corr + 4.5
                        #value = hat_tc.a_in_read(channel)*1000
                        #if channel == 0:
                            #position = "A"
                            #value += OFFSET_SENS_A
                        
                        if value_tc == mcc134.OPEN_TC_VALUE:
                            print('     Open     ', end='')
                        elif value_tc == mcc134.OVERRANGE_TC_VALUE:
                            print('     OverRange', end='')
                        elif value_tc == mcc134.COMMON_MODE_TC_VALUE:
                            print('   Common Mode', end='')
                        else:
                            print('\r\033[2B{:12.2f} '.format(value_tc))

                        values_tc.append(value_tc)
                                                
                    # Read ADC
                    values_adc = []
                    for channel in channels_adc:
                        value_adc = hat_adc.a_in_read(channel)
                        print('\r\033[34G\033[2B{:.3f}'.format(value_adc), end = '') #raw [V]
                        value_adc = value_adc* kv[channel] + ped[channel]
                        #print('\r\033[58G{:.4f}'.format(value_adc), end='')
                        #value_adc *= kv[channel]
                        print('\r\033[7G {:.3f}'.format(value_adc), end='') #HV [kV]
                        ADC_value = hat_adc.a_in_read(channel, options=OptionFlags.NOSCALEDATA)
                        print('\r\033[19G{:.0f} '.format(ADC_value), end='') # ADC value []
                        values_adc.append(value_adc)
                        
                    # Get correct time for influx
                    utc_timezone = datetime.utcnow()
                    fermi_timezone = pytz.timezone('America/Chicago')
                    fermi_time = utc_timezone.astimezone(fermi_timezone)
                    fermi_time_str = fermi_time.strftime('%Y-%m-%d %H:%M:%S.%f') 
                    
                    # Write data to json payload and send to InfluxDB
                    # Build Data fields
                    fields = {}

                    # Add all TC values
                    for i, val in enumerate(values_tc):
                        fields[f"Temperature{i}"] = val

                    # Add all ADC values
                    for j, val in enumerate(values_adc):
                        fields[f"CH{j}"] = val

                    # Wrap everything into your data dict
                    data = {
                        # Table name
                        "measurement": "Raspi",
                        # Time Stamp
                        "time": fermi_time_str,
                        # Data Fields
                        "fields": fields
                    }

                    json_payload.append(data)
                    client.write_points(json_payload)
                    json_payload.clear()
                    stdout.flush()

                    for i in range(len(channels_adc)):
                        await uavar[i].write_value(values_adc[i])
                    for j in range(len(channels_adc),len(channels_adc)+len(channels_tc)):
                        await uavar[j].write_value(value_tc[j])

                    # Wait the specified interval between reads.
                    await asyncio.sleep(int(para["CTIME"]))

        except KeyboardInterrupt:
            # Clear the '^C' from the display.
            print(CURSOR_BACK_2, ERASE_TO_END_OF_LINE, '\n')

    except (HatError, ValueError) as error:
        print('\n', error)


if __name__ == '__main__':
    # This will only be run when the module is called directly.
    asyncio.run(main(), debug=True)
