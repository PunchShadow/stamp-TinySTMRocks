# ./kmeans -m15 -n15 -t0.00001 -p 4 -i inputs/random-n2048-d16-c16.txt
# Parameters
declare -a P_NUM=("1" "2" "4" "8" "16")
M=15
N=15
T=0.00001
CYCLE=$1
INPUT_FILE="inputs/random-n65536-d32-c16.txt"
OUPUT_DIR="result_log/high_contention_pcm/$(date '+%Y_%m_%d_%H_%M_%S')"


mkdir -p ${OUPUT_DIR}
echo "m=${M}, n=${N}, t=${T}, p_max=${P_MAX}, cycle=${CYCLE}, input_file=${INPUT_FILE}" > ${OUPUT_DIR}/parameters 

for i in "${P_NUM[@]}"; do
    mkdir ${OUPUT_DIR}/${i}
    for ((j=0; j<${CYCLE}; j++)); do
        sudo ./kmeans.stm -m${M} -n${N} -t${T} -p${i} -i ${INPUT_FILE} | tail -n 1 >> ${OUPUT_DIR}/${i}/t.log
    done
    echo -n -e "p=${i}:" >> ${OUPUT_DIR}/rst
    echo -n -e "p=${i}:" >> ${OUPUT_DIR}/toast
    cat ${OUPUT_DIR}/${i}/t.log | awk -F" " '{sum+=$2} END {print sum/NR}' >> ${OUPUT_DIR}/rst
    cat ${OUPUT_DIR}/${i}/t.log | awk -F" " 'BEGIN{ORS=","}{print $2}' >> ${OUPUT_DIR}/toast
    echo -e '\n' >> ${OUPUT_DIR}/toast
done

