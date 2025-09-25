import os
import sys
import time
from epics import caget, caput, cainfo

target_bit = int(caget('spellmanhv/targetV_bit'))
hv_status = int(caget('spellmanhv/rSWITCH'))
jump_step_in_bits = 5

if hv_status == 1:  # -- HV enabled
    read_kV_bit_record = 'spellmanhv/rVSet_bit'
    this_read_kV_bit = int(caget('spellmanhv/rVSet_bit'))
    set_kV_bit_record = 'spellmanhv/setV_bit'

    # Bidirectional ramping logic
    if this_read_kV_bit < target_bit:
        # RAMP UP
        print(f"Ramping UP from {this_read_kV_bit} to {target_bit} bits")
        while this_read_kV_bit < target_bit:
            hv_status = int(caget('spellmanhv/rSWITCH'))  # Re-check status
            if hv_status == 0:
                print("HV disabled, stopping ramp")
                break

            remaining_bits = target_bit - this_read_kV_bit
            if remaining_bits <= jump_step_in_bits:
                # Final step - go directly to target
                caput(set_kV_bit_record, target_bit)
            else:
                # Normal step increment
                caput(set_kV_bit_record, this_read_kV_bit + jump_step_in_bits)

            time.sleep(0.2)
            this_read_kV_bit = int(caget('spellmanhv/rVSet_bit'))
            print("this_read_kV_bit : " + str(this_read_kV_bit))
            time.sleep(0.3)

    elif this_read_kV_bit > target_bit:
        # RAMP DOWN
        print(f"Ramping DOWN from {this_read_kV_bit} to {target_bit} bits")
        while this_read_kV_bit > target_bit:
            hv_status = int(caget('spellmanhv/rSWITCH'))  # Re-check status
            if hv_status == 0:
                print("HV disabled, stopping ramp")
                break
            remaining_bits = this_read_kV_bit - target_bit
            if remaining_bits <= jump_step_in_bits:
                # Final step - go directly to target
                caput(set_kV_bit_record, target_bit)
            else:
                # Normal step decrement
                caput(set_kV_bit_record, this_read_kV_bit - jump_step_in_bits)
            time.sleep(0.2)
            this_read_kV_bit = int(caget('spellmanhv/rVSet_bit'))
            print("this_read_kV_bit : " + str(this_read_kV_bit))
            time.sleep(0.3)

    else:
        print(f"Already at target voltage: {target_bit} bits")

else:
    print("HV is disabled. Cannot ramp voltage.")

