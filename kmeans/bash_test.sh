#!/bin/bash

#until ./kmeans.stm -m40 -n40 -t0.05 -i inputs/random-n2048-d16-c16.txt -p8 > /dev/null ; [ $? -eq 139 ]; do printf '.'; done

while true
do
    ./kmeans.stm -m40 -n40 -t0.05 -i inputs/random-n2048-d16-c16.txt -p16 > /dev/null
done
