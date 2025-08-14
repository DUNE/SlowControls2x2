import os
import sys
import time
from epics import caget, caput, cainfo

target_bit = int(caget('spellmanhv/targetV_bit'))
hv_status = int(caget('spellmanhv/rSWITCH'))

if hv_status == 1: # -- HV enabled
    read_kV_bit_record = 'spellmanhv/rVSet_bit'
    this_read_kV_bit = int(caget('spellmanhv/rVSet_bit'))

    set_kV_bit_record = 'spellmanhv/setV_bit'
    if this_read_kV_bit != 0:
        caput(set_kV_bit_record, 0)
        time.sleep(0.2)
        
    this_read_kV_bit = int(caget('spellmanhv/rVSet_bit'))

    while this_read_kV_bit < target_bit:
        if hv_status == 0:
            continue
        caput(set_kV_bit_record, this_read_kV_bit + 5)
        time.sleep(0.2)
        this_read_kV_bit = int(caget('spellmanhv/rVSet_bit'))
        print("this_read_kV_bit : " + str(this_read_kV_bit))
        time.sleep(0.3)


