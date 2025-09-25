
#   Start the monitoring of the voltage values pushed to influxdb and to a OPC UA server 
#   in a screen session

#   Last modified:  2025-09-25
#   by:             Nicolas Sallin, nicolas.sallin@unibe.ch

screen -dmS "PFD4" bash -c 'python3 /home/pi/Dune2x2_SlowControl/PFD4/src/20250903_PFD4_opcua.py; exec sh'
