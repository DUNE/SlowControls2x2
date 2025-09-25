
#   Start the monitoring of the voltage values pushed to influxdb and to a OPC UA server 
#   in a screen session

#   Last modified:  2025-09-25
#   by:             Nicolas Sallin, nicolas.sallin@unibe.ch

screen -dmS "PFD4_opcua" bash -c 'python3 /home/pi/SlowControls2x2/HVFilterPot_Raspi/PFD4/src/PFD4_opcua.py; exec sh'
