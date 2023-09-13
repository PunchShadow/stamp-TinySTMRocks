import time
import os
import argparse
import csv
import re
import subprocess
import tempfile
import math
import sys
import signal
import errno
import functools
from tqdm import tqdm


cmds = {
    "bayes": "./bayes.stm -v32 -r4096 -n10 -p40 -i2 -e8 -s1 -t",
    "genome": "./genome.stm -g16384 -s64 -n16777216 -t",
    "intruder": "./intruder.stm -a10 -l128 -n262144 -s1 -t",
    "kmeans_high": "./kmeans.stm -m15 -n15 -t0.00001 -i inputs/random-n65536-d32-c16.txt -p",
    "kmeans_low": "./kmeans.stm -m40 -n40 -t0.00001 -i inputs/random-n65536-d32-c16.txt -p",
    "labyrinth": "./labyrinth.stm -i inputs/random-x512-y512-z7-n512.txt -t",
    "ssca2": "./ssca2.stm -s20 -i1.0 -u1.0 -l3 -p3 -t",
    "vacation_high": "./vacation.stm -n4 -q60 -u90 -r1048576 -t4194304 -c",
    "vacation_low": "./vacation.stm -n2 -q90 -u98 -r1048576 -t4194304 -c",
    "yada": "./yada.stm -a15 -i inputs/ttimeu1000000.2 -t"
}

dic = ['bayes', 'genome', 'intruder', 'kmeans', 'labyrinth', 'ssca2', 'vacation', 'yada']
cmds_index = ['bayes', 'genome', 'intruder', 'kmeans_high', 'kmeans_low', 'labyrinth', 'ssca2', 'vacation_high', 
             'vacation_low', 'yada']

ROOT = os.path.abspath(os.getcwd())


if __name__ == "__main__":
    Romeo_path = '/home/sylab/PunchShadow/TM/TinySTMRocks'
    STAMP_path = '/home/sylab/PunchShadow/TM/stamp-TinySTMRocks'
    param_path = '/home/sylab/PunchShadow/TM/TinySTMRocks/include'

    Romeo_make_cmd = "make clean && make"
    STAMP_cmd = "python3 bash_run.py -r 50 --max_thread 32 -e -st"
    bayes_file_name = "/home/sylab/PunchShadow/TM/stamp-TinySTMRocks/Romeo_raw_data/0328/retry_time/bayes_1-32_retry"

    
    bayes_60_cmd = "python3 bash_run.py -o Romeo_raw_data/0328/retry_time/bayes_retry60_1-32.txt -r 25 --min_thread 2 --max_thread 32 -s bayes -e"
    bayes_120_cmd = "python3 bash_run.py -o Romeo_raw_data/0328/retry_time/bayes_retry120_1-32.txt -r 25 --min_thread 2 --max_thread 32 -s bayes -e"
    bayes_240_cmd = "python3 bash_run.py -o Romeo_raw_data/0328/retry_time/bayes_retry240_1-32.txt -r 25 --min_thread 2 --max_thread 32 -s bayes -e"

    kmeans_60_cmd = "python3 bash_run.py -o Romeo_raw_data/0328/retry_time/kmeans_high_retry60_1-32.txt -r 25 --min_thread 2 --max_thread 32 -s kmeans_high -e"
    kmeans_120_cmd = "python3 bash_run.py -o Romeo_raw_data/0328/retry_time/kmeans_high_retry120_1-32.txt -r 25 --min_thread 2 --max_thread 32 -s kmeans_high -e"
    kmeans_240_cmd = "python3 bash_run.py -o Romeo_raw_data/0328/retry_time/kmeans_high_retry240_1-32.txt -r 25 --min_thread 2 --max_thread 32 -s kmeans_high -e"
    
    # retry = 60
    os.chdir(Romeo_path)
    os.system(Romeo_make_cmd)
    os.chdir(STAMP_path)
    os.system(kmeans_60_cmd)

    # retry = 120
    os.chdir(param_path)
    os.remove("param.h")
    os.rename("param120.h", "param.h")
    os.chdir(Romeo_path)
    os.system(Romeo_make_cmd)
    os.chdir(STAMP_path)
    os.system(kmeans_120_cmd)
    os.system(bayes_120_cmd)

    # retry 240
    os.chdir(param_path)
    os.remove("param.h")
    os.rename("param240.h", "param.h")
    os.chdir(Romeo_path)
    os.system(Romeo_make_cmd)
    os.chdir(STAMP_path)
    os.system(kmeans_240_cmd)
    os.system(bayes_240_cmd)

    