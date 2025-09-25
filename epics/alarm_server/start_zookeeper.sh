#!/bin/bash

kafkaDir=/home/acd/acdcs/2x2/EPICS/phoebus/kafka_2.13-3.9.0/
propDir=/home/acd/acdcs/2x2/SlowControls2x2/epics/alarm_server

$kafkaDir/bin/zookeeper-server-start.sh $propDir/zookeeper.properties
