import opentuner
import argparse
import re
import os
from opentuner import ConfigurationManipulator
from opentuner import EnumParameter
from opentuner import IntegerParameter
from opentuner import FloatParameter
from opentuner import MeasurementInterface
from opentuner import Result

dic = ['bayes', 'genome', 'intruder', 'kmeans', 'labyrinth', 'ssca2', 'vacation', 'yada']
cmds_index = ['bayes', 'genome', 'intruder', 'kmeans_high', 'kmeans_low', 'labyrinth', 'ssca2', 'vacation_high', 
             'vacation_low', 'yada']


# parser = argparse.ArgumentParser()

# parser.add_argument("-t", "--thread_num",
#                     default='1',
#                     help="Please enter the thread number.")









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

FLOAT_CONFIG = []
INT_CONFIG = []

ROMEO_CONFIG_INT = [
    ('MAX_ENTRY_SIZE', 1, 10),
    ('scheduler_type', 0, 1)
]


ROMEO_CONFIG_FLOAT = [
    ('ci_alpha', 0, 1),
    ('CI_THRESHOLD', 0, 1)
]

# Manipulator only need to modify this dictionary
ROMEO_CONFIG = {
    'MAX_ENTRY_SIZE': 1,
    'scheduler_type': 0,
    'ci_alpha': 0,
    'CI_THRESHOLD': 0
}








class RomoeConfigTuner(MeasurementInterface):
    
    def manipulator(self):
        # Define the search space by creating a ConfigurationManipulator
        manipulator = ConfigurationManipulator()
        for param, min_val, max_val in ROMEO_CONFIG_INT:
            manipulator.add_parameter(
                IntegerParameter(param, min_val, max_val))
            INT_CONFIG.append(param)
        for param, min_val, max_val in ROMEO_CONFIG_FLOAT:
            manipulator.add_parameter(
                FloatParameter(param, min_val, max_val))
            FLOAT_CONFIG.append(param)
        return manipulator

    def ModifyParam(self, path):
        # Modify param.h by ROMEO_CONFIG dic
        assert(FLOAT_CONFIG != [])
        assert(INT_CONFIG != [])

        flag = 0
        temp_path = path + 'temp'
        inputfile = open(path, "r")
        output = open(temp_path, "a")
        for line in inputfile:
            for key, value in ROMEO_CONFIG.items():
                if(re.search(r'%s' % key, line) != None):
                    if key in FLOAT_CONFIG:
                        output.write(re.sub(r'\d+.\d+', str(ROMEO_CONFIG[key]), str(line)))
                        flag = 1
                        continue
                    elif key in INT_CONFIG:
                        output.write(re.sub(r'\d+', str(ROMEO_CONFIG[key]), str(line)))
                        flag = 1
                        continue
                    else:
                        assert(0)
                    continue
            if flag == 0:
                output.write(line)
            else:
                flag = 0

        inputfile.close()
        output.close()

        # Replace path with new temp_path
        os.remove(path)
        os.rename(temp_path, path)

    def save_config_each_iter(self, config_dic, config_path):
        f = open(config_path, "a")
        f.write(str(config_dic)+'\n')
        f.close()


    def run(self, desired_result, input, limit):
        # Compile and run a given configuration then return performance
        cfg = desired_result.configuration.data
        repeat_times = 20
        avg_exe_time = 0
        specific_bench = self.args.specific
        thread_num = self.args.thread_num
        # Romeo library path
        Romeo_path = '/home/sylab/PunchShadow/TM/TinySTMRocks'
        # STAMP library path
        STAMP_path = '/home/sylab/PunchShadow/TM/stamp-TinySTMRocks' + '/' + specific_bench.split("_")[0]

        # First find Romeo library's path and modify param.h
        romeo_gcc_cmd = 'make clean && make'
        stamp_gcc_cmd = 'make -f Makefile.stm clean && make -f Makefile.stm'

        stamp_exe_cmd = cmds[specific_bench] + thread_num

        # Change param.h
        for key, value in ROMEO_CONFIG.items():
            ROMEO_CONFIG[key] = cfg[key]
        print(ROMEO_CONFIG)
        self.save_config_each_iter(ROMEO_CONFIG, cur_path+'/'+self.args.config_file)
        self.ModifyParam(Romeo_path+'/include/param.h')
        

        os.chdir(Romeo_path)
        compile_result = self.call_program(romeo_gcc_cmd)
        assert compile_result['returncode'] == 0
        os.chdir(STAMP_path)
        compile_result = self.call_program(stamp_gcc_cmd)
        assert compile_result['returncode'] == 0
        for i in range(repeat_times):
            run_result = self.call_program(stamp_exe_cmd)
            assert run_result['returncode'] == 0
            avg_exe_time += float(run_result['time'])
        
        return Result(time=(avg_exe_time/repeat_times))


if __name__ == '__main__':
    cur_path = os.getcwd()
    argparser = opentuner.default_argparser()
    argparser.add_argument('--config-file',
                           help="Configuration file path.")
    argparser.add_argument("-s", "--specific",
                           default="No",
                           help="Only test the specific benchmark (default: all).")
    argparser.add_argument("--thread-num",
                           default='1',
                           help="Thread number of STAMP benchmarks (default: 1)")
    args = argparser.parse_args()
    if (args.specific != "No"):
        assert args.specific in cmds_index, "Specific benchmark name error! [bayes, genome, intruder, kmeans_high, kmeans_low, labyrinth, ssca2, vacation_high, vacation_low, ssca2]"
        specific_bench = args.specific
    else:
        assert(0)  
    RomoeConfigTuner.main(argparser.parse_args())
