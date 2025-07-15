#! /bin/sh

alarmserverDir=/home/acd/acdcs/2x2/EPICS/phoebus/phoebus/services/alarm-server
host=acd-daq05-priv.fnal.gov
alarmConfigDir=/home/acd/acdcs/2x2/EPICS/2x2_Slow_Controls/epics/alarm_server/alarm_config/

cd $alarmserverDir

./alarm-server.sh -server $host:9092 -config ACDCS -import $alarmConfigDir/AC_alarm_config_20250714.xml

#$alarmserverDir/alarm-server.sh -help

