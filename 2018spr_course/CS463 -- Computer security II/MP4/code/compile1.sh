#!/bin/bash

COMP="javac"
BITCOINLIB="./libs/api-1.1.0.jar"
JSON="./libs/gson-2.2.jar"
CLASSPATH=".:$BITCOINLIB:$JSON"
OUTDIR="./bin"

EXTRA=""

FILES="src/main/*.java src/test/*.java"

mkdir "$OUTDIR" 2> /dev/null

cmd=`echo "$COMP" "$EXTRA" -classpath "$CLASSPATH" -d "$OUTDIR" "$FILES"`
echo "Compilation command: \"$cmd\" ";

echo "-------------------------------"

$cmd

if [ $? -eq 0 ]; then
	echo "Compilation succeeded!";
else
	echo "Compilation failed!";
fi
