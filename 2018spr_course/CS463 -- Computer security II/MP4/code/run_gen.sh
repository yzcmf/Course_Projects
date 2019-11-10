#!/bin/bash
RUN="java"
BITCOINLIB="./libs/api-1.1.0.jar"
JSON="./libs/gson-2.2.jar"
CLASSPATH=".:$BITCOINLIB:$JSON"
OUTDIR="./bin"

CLASSPATH=".:$OUTDIR:$BITCOINLIB:$JSON"

EXTRA=""

MAINCLASS="test/DatasetGeneratorTest"

if [ ! -d "$OUTDIR" ]; then
    echo "Class files directory does not exist: run 'compile2.sh' first, exiting...";
    exit 1;
fi


cmd=`echo "$RUN" "$EXTRA" -classpath "$CLASSPATH" "$MAINCLASS"`
echo "Run command: \"$cmd\" ";

echo "--------------------------";

$cmd

echo "--------------------------"; echo "";