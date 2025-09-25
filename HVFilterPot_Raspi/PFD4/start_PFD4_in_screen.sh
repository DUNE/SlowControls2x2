
#   Start the monitoring of the voltage values pushed to influxdb in a screen session

#   Last modified:  2025-09-25
#   by:             Nicolas Sallin, nicolas.sallin@unibe.ch

screen -dmS "PFD4" bash -c 'python3 /home/pi/SlowControls2x2/HVFilterPot_Raspi/PFD4/src/PFD4.py; exec sh'
