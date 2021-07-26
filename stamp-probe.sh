#!/bin/bash
# Automatically make each benchmarks and insert perf uprobe to each one

echo $#
if [ $# -ge 1 ]
then
    suffix=$1
    shift
else 
    echo "format: stamp-probe.sh (seq | stm) ..."
    exit
fi


# Automatically make

for dir in \
    bayes \
    genome \
    intruder \
    kmeans \
    labyrinth \
    ssca2 \
    vacation \
    yada
do

cd ${dir}
make -f Makefile.${suffix} clean
make -f Makefile.${suffix}
cd ..

done

# Automatically insert probe ( stm_start, stm_abort__return, stm_commit__return)

# First clear out all probes
perf probe --del=*

for file in \
    bayes \
    genome \
    intruder \
    kmeans \
    labyrinth \
    ssca2 \
    vacation \
    yada
do

cd ${file}
perf probe -f -x ./${file}.stm ${file}_stm_start_entry=stm_start
perf probe -f -x ./${file}.stm ${file}_stm_commit_entry=stm_commit
perf probe -f -x ./${file}.stm ${file}_stm_commit_exit=stm_commit%return
perf probe -f -x ./${file}.stm ${file}_stm_abort_exit=stm_abort%return
perf probe -f -x ./${file}.stm ${file}_stm_rollback_exit=stm_rollback%return
perf probe -f -x ./${file}.stm ${file}_stm_rollback_entry=stm_rollback
cd ..

done

exit

