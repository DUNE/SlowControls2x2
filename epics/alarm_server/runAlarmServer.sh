#!/bin/sh

source /home/acd/acdcs/2x2/EPICS/setup_EPICS.sh

#/usr/bin/screen -dmS alarmServer
screen -dmS alarmServer /home/acd/acdcs/2x2/SlowControls2x2/epics/alarm_server/startAlarmServer.sh
