import os
import sys
import time
from epics import caget, caput, cainfo

hv_status = int(caget('spellmanhv/rSWITCH'))
jump_step_in_bits = 5

if hv_status == 1:  # -- HV enabled
    read_kV_bit_record = 'spellmanhv/rVSet_bit'
    this_read_kV_bit = int(caget('spellmanhv/rVSet_bit'))
    set_kV_bit_record = 'spellmanhv/setV_bit'
    
    target_bit = 0  # Always ramp to zero
    
    if this_read_kV_bit > target_bit:
        # RAMP DOWN to zero
        print("Set target voltage to zero")
        caput('spellmanhv/targetV_kV', 0.)
        print(f"Ramping DOWN from {this_read_kV_bit} to {target_bit} bits (zero)")
        while this_read_kV_bit > target_bit:
            hv_status = int(caget('spellmanhv/rSWITCH'))  # Re-check status
            if hv_status == 0:
                print("HV disabled, stopping ramp")
                break
                
            remaining_bits = this_read_kV_bit - target_bit
            if remaining_bits <= jump_step_in_bits:
                # Final step - go directly to zero
                caput(set_kV_bit_record, target_bit)
            else:
                # Normal step decrement
                caput(set_kV_bit_record, this_read_kV_bit - jump_step_in_bits)
                
            time.sleep(0.2)
            this_read_kV_bit = int(caget('spellmanhv/rVSet_bit'))
            print("this_read_kV_bit : " + str(this_read_kV_bit))
            time.sleep(0.3)
    else:
        print("Already at zero voltage")
else:
    print("HV is disabled. Cannot ramp voltage.")
