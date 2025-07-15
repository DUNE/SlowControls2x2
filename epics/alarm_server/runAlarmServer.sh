#!/bin/sh

source /home/acd/acdcs/2x2/EPICS/setup_EPICS.sh

#/usr/bin/screen -dmS alarmServer
screen -dmS alarmServer /home/acd/acdcs/2x2/EPICS/2x2_Slow_Controls/epics/alarm_server/startAlarmServer.sh
