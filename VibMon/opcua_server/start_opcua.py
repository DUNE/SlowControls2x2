#!/usr/bin/python
import time, math, json
import datetime 
import subprocess
import asyncio 
from asyncua import Server, ua 
import socket 
import os 
from pytz import timezone 

async def main():

    ''' This script starts a OPCUA server.
    The server creates variables for vibrations monitoring on the 2x2 cryostat
    that can be accessed by other devices connected to the same
    network like ignition.Values will be written by a separate
    measurement script.
    '''
    PORT = 4840

    # Create server instance
    server = Server() 
    # Set server endpoint
    await server.init()
    server.set_endpoint(f"opc.tcp://0.0.0.0:{PORT}/freeopcua/server/")
    
    # Setup server namespaces
    uri = "http://examples.freeopcua.github.io"
    idx = await server.register_namespace(uri)

    # Get the Objects node, which is the root node for our server
    objects = server.nodes.objects
    
    # Add a new object to the server
    myobj = await objects.add_object(idx, "VibrationSet")
    
    # Add a variables to store vibrations data
    date_var = await myobj.add_variable(idx, "DateVar", 0, ua.String)

    # Vibration variables for Channel 1 (different frequency ranges)
    ch1_20_200_hz = await myobj.add_variable(idx,"Ch1_20_200_Hz",0.0,ua.Float)
    ch1_200_2000_hz = await myobj.add_variable(idx,"Ch1_200_2000_Hz",0.0,ua.Float)
    ch1_2000_20000_hz = await myobj.add_variable(idx,"Ch1_2000_20000_Hz",0.0,ua.Float)
    
    # Vibration variables for Channel 2 (different frequency ranges)
    ch2_20_200_hz = await myobj.add_variable(idx,"Ch2_20_200_Hz",0.0,ua.Float)
    ch2_200_2000_hz = await myobj.add_variable(idx,"Ch2_200_2000_Hz",0.0,ua.Float)
    ch2_2000_20000_hz = await myobj.add_variable(idx,"Ch2_2000_20000_Hz",0.0,ua.Float)

    # Make the variables writable by clients
    await date_var.set_writable()
    await ch1_20_200_hz.set_writable()
    await ch1_200_2000_hz.set_writable()
    await ch1_2000_20000_hz.set_writable()
    await ch2_20_200_hz.set_writable()
    await ch2_200_2000_hz.set_writable()
    await ch2_2000_20000_hz.set_writable()

    # Start the server
    await server.start()
    print("OPC UA Vibration Server is running...")
    print("Available variables:")
    print("  - VibrationSet.DateVar")
    print("  - VibrationSet.Ch1_20_200_Hz")
    print("  - VibrationSet.Ch1_200_2000_Hz")
    print("  - VibrationSet.Ch1_2000_20000_Hz")
    print("  - VibrationSet.Ch2_20_200_Hz")
    print("  - VibrationSet.Ch2_200_2000_Hz")
    print("  - VibrationSet.Ch2_2000_20000_Hz")    

    try:
        # Update the timestamp in a loop
        while True:
            # Format the date as a string
            chicago_time = timezone("America/Chicago")
            time_now = datetime.datetime.now(chicago_time)
            date_string = time_now.strftime("%Y-%m-%d-%H-%M-%S")
            await date_var.write_value(date_string)

            await asyncio.sleep(10)  # Sleep for 10 seconds
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the server
        await server.stop()
        print("OPC UA Server has stopped.")


if __name__ == "__main__":
    asyncio.run(main())
