#!/bin/sh

if [ $# -ne 1 ]
then
    echo "Usage: create_alarm_topics.sh Accelerator"
    exit 1
fi

config=$1

kafkaDir=/home/acd/acdcs/2x2/EPICS/phoebus/kafka_2.13-3.9.0
host=acd-daq05-priv.fnal.gov

# Create the compacted topics.
for topic in "$1"
do
    $kafkaDir/bin/kafka-topics.sh  --bootstrap-server $host:9092 --create --replication-factor 1 --partitions 1 --topic $topic
    $kafkaDir/bin/kafka-configs.sh --bootstrap-server $host:9092 --entity-type topics --alter --entity-name $topic \
           --add-config cleanup.policy=compact,segment.ms=10000,min.cleanable.dirty.ratio=0.01,min.compaction.lag.ms=1000
done

# Create the deleted topics
for topic in "${1}Command" "${1}Talk"
do
    $kafkaDir/bin/kafka-topics.sh  --bootstrap-server $host:9092 --create --replication-factor 1 --partitions 1 --topic $topic
    $kafkaDir/bin/kafka-configs.sh --bootstrap-server $host:9092 --entity-type topics --alter --entity-name $topic \
           --add-config cleanup.policy=delete,segment.ms=10000,min.cleanable.dirty.ratio=0.01,min.compaction.lag.ms=1000,retention.ms=20000,delete.retention.ms=1000,file.delete.delay.ms=1000
done
