# OPC UA Server

This directory contains an OPC UA server for monitoring cryostat vibration data across multiple frequency bands and channels.

## Overview
The server creates 6 vibration monitoring variables:

* Channel 1: Ch1_20_200_Hz, Ch1_200_2000_Hz, Ch1_2000_20000_Hz
* Channel 2: Ch2_20_200_Hz, Ch2_200_2000_Hz, Ch2_2000_20000_Hz

All variables are writable and can be updated by external measurement scripts.

## Virtual Environment

A virtual python environment is needed to run this server. For instructions on how to setup your raspberry pi proxy connection for github please refer to: https://cdcvs.fnal.gov/redmine/projects/argoncube-2x2-demonstrator/wiki/AC2x2-proxy-config

```bash
python3 -m venv opcua_env
source opcua_env/bin/activate
pip install --proxy http://192.168.197.49:3128 asyncua pytz
```
## Start Server in Screen Session
```bash
./start_opcua_in_screen.sh
```

## Connection Information
* **Endpoint:** opc.tcp://0.0.0.0:4840/freeopcua/server/
* **Namespace:** http://examples.freeopcua.github.io
* **Main Object:** VibrationSet

## Troubleshooting
If you get "address already in use" errors:

```bash
# Find process using port 4840
sudo lsof -i :4840

# Kill the process
sudo kill -9 <PID>

# Restart server
./start_opcua_in_screen.sh
```

## For External Clients

* **Connect to:** opc.tcp://<raspberry-pi-ip>:4840/freeopcua/server/
* Browse to: Objects > VibrationSet
* Write vibration values to the appropriate frequency band variables
