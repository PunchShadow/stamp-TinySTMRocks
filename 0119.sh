#!/bin/bash

python3 bash_run.py -o Romeo_bayes_CIT85_ALPHA95_20.txt -r20 --max_thread 32 -e -st -s bayes

python3 bash_run.py -o Romeo_intruder_CIT85_ALPHA95_20.txt -r20 --max_thread 32 -e -st -s intruder

python3 bash_run.py -o Romeo_labyrinth_CIT85_ALPHA95_20.txt -r20 --max_thread 32 -e -st -s labyrinth


python3 bash_run.py -o Romeo_genome_CIT85_ALPHA95_20.txt -r20 --max_thread 32 -e -st -s genome
