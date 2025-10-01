PFD4

ssh into any server of your pleasing, this tutorial will use daq05 as an example,

```bash
ssh -J <user>@acd-gw05.fnal.gov <user>@acd-daq05.fnal.gov
```

From here, you must ssh into the filter pot raspi,

```bash
ssh pi@<IP>
```
The ip address can be found here, https://cdcvs.fnal.gov/redmine/projects/argoncube-2x2-demonstrator/wiki/Ac2x2-network-configurations_ , under the HV section.

You will be prompted to enter a password.

After you are in the raspi enter:

```bash
cd SlowControls2x2/HVFilterPot_Raspi/PFD4/
```

After you are in this directory, start the monitoring in a screen that push the data to influxdb and to a OPC UA server 

```bash
./start_PFD4_in_screen_opcua.sh
```
or push data only to influxdb

```bash
./start_PFD4_in_screen.sh
```

Recall to see the list of screen session

```bash
screen -ls
```
to attach to a session
```bash
screen -r <session_name>
```
to detach a session (aka to quit the session but leave it active in the background):
ctrl+a then d

to kill a session (aka to quit the session and kill it at the same time):
ctrl+a then :quit
