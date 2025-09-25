#! /bin/sh

alarmserverDir=/home/acd/acdcs/2x2/EPICS/phoebus/phoebus/services/alarm-server
host=acd-daq05-priv.fnal.gov

cd $alarmserverDir

./alarm-server.sh -server $host:9092 -config ACDCS
