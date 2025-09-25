#!/bin/bash

kafkaDir=/home/acd/acdcs/2x2/EPICS/phoebus/kafka_2.13-3.9.0
propDir=/home/acd/acdcs/2x2/EPICS/2x2_Slow_Controls/epics/alarm_server

$kafkaDir/bin/kafka-server-start.sh $propDir/kafka.properties
