import time
import subprocess
from configparser import ConfigParser
from Source.tti_library_old import ttiPsu
import sys
from datetime import datetime

ips = ['192.168.197.55','192.168.197.57','192.168.197.76','192.168.197.77']

# NOTE: if program is cannceled during ramp up procedure it may not write the final state to the log file!!!
def write():
    """
    f = open("Historical.log", "a")
    f.write(str(datetime.now()) + "\n")
    for TTIn in [0]:# [0,1,2,3]:
        ip = ips[TTIn]
        tti = ttiPsu(ip,1)
        f.write("Module "+str(TTIn) + "\t" + str(tti.getOutputIsEnabled()) + "\t" + str(tti.readOutputVolts()) + " V\t" +str (tti.readOutputAmps()) + " I\n")
    f.close()
    """
    a = 1

def ramp_up(ip,V_start,V0):
    status = True
    #print("Starting ttiPsu")
    tti = ttiPsu(ip,1)
    #print("Done with ttiPsu")
    #   Makes sure output is turned off 
    try:
        tti.setOutputEnable(False)
    except:
        failure(ip, "Ramp up, setOutputEnable(False)")
        return False
    
    #   Turns output on
    try:
        tti.setOutputEnable(True)
    except:
        failure(ip, "Ramp up, setOutputEnable(True)")
        return False
    
    #	Test to ensure we can read voltages
    try:
        print("The current Voltage is: " ,tti.readOutputVolts() ,"V")
    except:
        failure(ip, "Ramp up, readOutputVolts")
        return False
    
    #   Sets max current to 7.5 mA
    tti.setMaxAmps(0.0075)
    tti.setTripAmps(0.01) 
    tti.setTripVolts(110) 
    #   Sets voltage step size
    tti.setStepSizeVolts(1)
    #   Begins ramping up voltage
    if V0 > 6:
        print("starting ramp")
        #   Slow at the beginning
        while tti.readOutputVolts() < 6:
            #   Stops if incrimentation fails
            try:
                tti.incrementVoltage()
                print("The current Voltage is: " ,tti.readOutputVolts() ,"V")
                #write()
            except:
                failure(ip, "Ramp up, readOutputVolts 2")
                status = False
                break
                
        #   Breaks ends the function if there was an issue in incrimentation
        if status == False:
            failure(ip, "Incrementation Issue")
            return False
        
        #   Speeds up incrimentation
        fast_step = 6
        tti.setStepSizeVolts(fast_step)
        
        #   Same as above but now to V0
        while tti.readOutputVolts() < V0-fast_step:
                try:    
                    tti.incrementVoltage()
                    print("The current Voltage is: " ,tti.readOutputVolts() ,"V")
                    #write()
                except:
                    failure(ip, "Ramp up, incrementVoltage")
                    status = False
                    break
                if status == False:
                    failure(ip, "Ramp up, incrementVoltage status=False")
                    return False
        
        tti.setMaxVolts(V0)
        print("The current Voltage is: " ,tti.readOutputVolts() ,"V")

    #   If voltage is lower than threshold to speed up then just do normally
    elif V0 < 7: 
        while tti.readOutputVolts() < 7:
            try:
                tti.incrementVoltage()
                print("The current Voltage is: " ,tti.readOutputVolts() ,"V")
            except: 
                failure(ip, "Ramp up, incrementVoltage with V0 < 7")
                break

    tti.setStepSizeVolts(0)
    tti.setMaxVolts(V0)            
    return True
        
def ramp_down(ip):
    tti = ttiPsu(ip,1)
        
    #   Prints the voltage it starts at
    print("The current Voltage is: " ,tti.readOutputVolts() ,"V")
    write() 
    #   initializes the voltage step size to 1
    tti.setStepSizeVolts(6)
    dec_iter = 0
    #   Lowers the voltage (reverse of before)
    #while tti.readOutputVolts() > 0.1:
    while tti.readOutputVolts() > 0.1:
        if tti.readOutputVolts() < 7:
            if dec_iter > 7:
                break
            elif dec_iter < 0.01:
                break
            if tti.getOutputIsEnabled() == True:
                while dec_iter < 7:
                    try:
                        tti.setStepSizeVolts(1)
                        dec_iter += 1
                    except:
                        failure(ip, "Ramp down, setStepSizeVolts")        
            else:
                try:
                    tti.setStepSizeVolts(1)
                except:
                    failure(ip, "Ramp down, setStepSizeVolts") 
        try:
            tti.decrementVoltage()
            print("The current Voltage is: " ,tti.readOutputVolts() ,"V")
        except:
            failure(ip, "Ramp down, decrementVoltage")
        
    #   Sets voltage to zero and turns off output
    tti.setMaxVolts(0)
    print("The current Voltage is: " ,tti.readOutputVolts() ,"V")
    tti.setOutputEnable(False)
  
#   Ramp voltage down to zero and turn off
def failure(ip, function=None):
    print("Failure with ip: "+str(ip)+" in function: "+function)
    log = open("Historical.log", "a")
    log.write("ENTERING FAILURE MODE!\n")
    #write()
    tti = ttiPsu(ip,1)
    ramp_down(ip)
    tti.setOutputEnable(False)
    log.write("Failure Protocol Succesfully executed")
    log.close()
  

"""
Controls
"""

def validate_TTIn(TTIn):
	if TTIn == 0 or TTIn == 1 or TTIn == 2 or TTIn == 3:
		return TTIn, True
	else:
		return TTIn, False

if __name__ == '__main__':
    try:
        tutorial = str(sys.argv[1])
        if tutorial == "-n":
            tutorial = True
        else:
            tutorial = False
    except:
        tutorial = False
        

    if tutorial == False:
        
        write()
        TTIn = int(input("What TTI would you like to control (0,1,2,3) "))
        
        while validate_TTIn(TTIn)[1] == False:
            print(validate_TTIn(TTIn))
            TTIn = int(input("What TTI would you like to control (0,1,2,3) "))
        ip = ips[TTIn]
        #print("starting ttiPsu")
        tti = ttiPsu(ip,1)
        #print("done")

        #   Start voltage so that if connection is lost things dont blow up 
        V_start = tti.readOutputVolts()

        # Converts boolean into a more sensible string
        def getoutput():
            status = tti.getOutputIsEnabled()
            if status == True:
                return "On"
            else:
                return "Off"

        # valdiates the users input and converts a near string into the right one
        def validate_out_v_power(s):
            if  s == "Output" or s == "out" or s == "OUTPUT" or s == "o" or s == "O" or s == "output":
                s = "Output"
                return s, True
            elif s == "Power" or s == "POWER" or s == "power" or s == "p" or s == "P":
                s = "Power"
                return s, True
            else:
                print("Invalid input, valid inputs are Output or Power")
                return s, False
        
        # valdiates the users input and converts a near string into the right one
        def validate_ONOFF(s):
            if s == "On" or s == "on" or s == "ON":
                s = "On"
                return s, True
            elif s == "Off" or s == "OFF" or s == "off" or s == "of" or s == "Of" or s == "OF":
                s = "Off"
                return s, True
            else:
                print("Invalid input, valid inputs are On or Off")
                return s, False

        # Gets current configuration of Power Supply
        #print("Looking for output")
        status = getoutput()
        print("The current voltage on the TTI is: ", V_start, "\t V\nCurrently the output is: ", status, "\nThe current limit on the TTI is: ", tti.getMaxAmps())
        
        # Gets the user to tell it if it wants to configure the output of the channel or if you would like to change the voltage on the channels
        out_v_power = input("Would you like to configure Output or Power? ")
        validate = validate_out_v_power(out_v_power)
        while validate[1] == False:
            out_v_power = input("Would you like to configure Output or Power? ")
            validate = validate_out_v_power(out_v_power)
        out_v_power = validate[0]

        # If you want to change the power being output get instructions then execute
        if out_v_power == "Power":
        
            ONOFF = input("Would you like the SiPM bias PS On or Off? ")
            validate = validate_ONOFF(ONOFF)
            while validate[1] == False:
                ONOFF = input("Would you like the SiPM bias PS On or Off? ")
                validate = validate_ONOFF(ONOFF)
            ONOFF = validate[0]
        
            if ONOFF == "On":
                ramp_up(ip,0,100)
                write()
            elif ONOFF == "Off":
                ramp_down(ip)
                write()
            else:
                print("Invalid input")
        
        # If you want to change the output status of the channel get instructions and do it 
        elif out_v_power == "Output":
        
            ONOFF = input("Would you like to turn the output On or Off? ")
            validate = validate_ONOFF(ONOFF)
            while validate[1] == False:
                ONOFF = input("Would you like the output On or Off? ")
                validate = validate_ONOFF(ONOFF)
            ONOFF = validate[0]
        
            if ONOFF == "On":
                if status == "On":
                    print("Output already on")
                else:
                    tti.setOutputEnable(True)
                    print("The output is: ",getoutput())
                    write()
            else:
                tti.setOutputEnable(False)
                print("The output is: ",getoutput())
                write()

    else:
            print("Your first prompt will be to enter the number of the TTI")
            print("This will tell the program which IP address to use")
            print("0 corresponds to the TTI controlling module 0")
            print("TTI 1 -> Module 1 ...")
            print("Any inputs besides 0,1,2, or 3 will be rejected")
            print("\n")
            dummy = input("Press Enter to continue")

            print("\n")
            print("There will be a short pause and then you should see something like this:")
            print("\tUsing port 9221")
            print("\tusing IP 192.168.196.33")
            print("\tThe current voltage on the TTI is:  0.0 	 V")
            print("\tCurrently the output is:  On")
            print("If you do not see this come up, there might be an issue with the network connection")
            print("\n")

            dummy = input("Press Enter to continue")

            print("\n")
            print("Your next prompt will be: Would you like to configure Output or Power?")
            print("CONFIGURE")
            print("\tThe Output option will allow you to turn on or off the output of the channel")
            print("POWER")
            print("\tIf turned on it will ramp up to the appropriate voltage setting")
            print("\tIf turned down it will ramp down to zero")
            print("\tWhen turned on they will be set according the Slow Controls Settings spreadsheet (DocDB 28372)")
            print("\tIf there a channel is misconfigured consult the manuals (DocDB 28372) or contact Tom (thmurphy@syr.edu)")
            dummy = input("Press Enter to continue")

            print("\n")
            print("For more details about each of the functions see TTI_library.py")
            print('\n')
