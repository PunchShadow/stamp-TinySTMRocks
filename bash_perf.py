import time
import os
import argparse
import csv
import re
import subprocess
import tempfile
import math


dic = ['bayes', 'genome', 'intruder', 'kmeans', 'labyrinth', 'ssca2', 'vacation', 'yada']
cmds_index = ['bayes', 'genome', 'intruder', 'kmeans_high', 'kmeans_low', 'labyrinth', 'ssca2', 'vacation_high', 
             'vacation_low', 'yada']
# Non-simulated commands
cmds = {
    "bayes": "./bayes.stm -v32 -r4096 -n10 -p40 -i2 -e8 -s1 -t8",
    "genome": "./genome.stm -g16384 -s64 -n16777216 -t8",
    "intruder": "./intruder.stm -a10 -l128 -n262144 -s1 -t8",
    "kmeans_high": "./kmeans.stm -m15 -n15 -t0.00001 -i inputs/random-n65536-d32-c16.txt -p8",
    "kmeans_low": "./kmeans.stm -m40 -n40 -t0.00001 -i inputs/random-n65536-d32-c16.txt -p8",
    "labyrinth": "./labyrinth.stm -i inputs/random-x512-y512-z7-n512.txt -t8",
    "ssca2": "./ssca2.stm -s20 -i1.0 -u1.0 -l3 -p3 -t8",
    "vacation_high": "./vacation.stm -n4 -q60 -u90 -r1048576 -t4194304 -c8",
    "vacation_low": "./vacation.stm -n2 -q90 -u98 -r1048576 -t4194304 -c8",
    "yada": "./yada.stm -a15 -i inputs/ttimeu1000000.2 -t8"
}

cmds_sim = {
    "bayes": "./bayes.stm -v32 -r1024 -n2 -p20 -s0 -i2 -e2 -t",
    "genome": "./genome.stm -g256 -s16 -n16384 -t",
    "intruder": "./intruder.stm -a10 -l4 -n2038 -s1 -t",
    "kmeans_high": "./kmeans.stm -m15 -n15 -t0.05 -i inputs/random-n2048-d16-c16.txt -p",
    "kmeans_low": "./kmeans.stm -m40 m40 -n40 -t0.05 -i inputs/random-n2048-d16-c16.txt -p",
    "labyrinth": "./labyrinth.stm -i inputs/random-x32-y32-z3-n96.txt -t",
    "ssca2": "./ssca2.stm -s13 -i1.0 -u1.0 -l3 -p3 -t",
    "vacation_high": "./vacation.stm -n4 -q60 -u90 -r16384 -t4096 -c",
    "vacation_low": "./vacation.stm -n2 -q90 -u98 -r16384 -t4096 -c",
    "yada": "./yada.stm -a20 -i inputs/633.2 -t"
}

# Get Root path of current path
ROOT = os.path.abspath(os.getcwd())

# # Re-compile each benchmarks
# for ele in dic:
#     print('cd '+ele)
#     #os.system('cd '+ele)
#     os.chdir(ele)
#     os.system('make -f Makefile.stm clean')
#     os.system('make -f Makefile.stm')
#     os.chdir(ROOT)


# Export Flamegraph scripts to path
os.system("export PATH=$PATH:/home/sylab/PunchShadow/FlameGraph")

# Execute perf record
for cmd in cmds_index:

    # Find and switch to proper dic
    dir_name = cmd.split("_")[0]
    os.chdir(dir_name)
    print("Switch to ", dir_name)

    exe_cmd = cmds[cmd]
    data_file = cmd + ".data"
    perf_file = cmd + ".perf"
    folded_file = cmd + ".folded"
    svg_file = cmd + ".svg"

    perf_exe_cmd = "sudo perf record -aR -g -o " + data_file + " " + exe_cmd 
    perf_script_cmd = "sudo perf script -i " + data_file + " > " + perf_file
    folding_cmd = "stackcollapse-perf.pl " + perf_file + " > " + folded_file
    svg_cmd = "flamegraph.pl " + folded_file + " > " + svg_file


    # Execute cmd
    print("-----------<< %s >>--------" % perf_exe_cmd)
    os.system(perf_exe_cmd)
    time.sleep(0.5)
    print("-----------<< %s >>--------" % perf_script_cmd)
    os.system(perf_script_cmd)
    time.sleep(0.5)
    print("-----------<< %s >>--------" % folding_cmd)
    os.system(folding_cmd)
    time.sleep(0.5)
    print("-----------<< %s >>--------", svg_cmd)
    os.system(svg_cmd)

    # Clear up temporal file
    clean_up_cmd = "sudo rm " + data_file + " " + perf_file + " " + folded_file
    os.system(clean_up_cmd)

    os.chdir(ROOT)

print("All Finish!!!!")









