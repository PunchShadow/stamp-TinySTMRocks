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



# Timeout decorator
class TimeoutError(Exception):
    pass

def timeout(seconds=10, error_message=os.strerror(errno.ETIME)):
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wrapper

    return decorator


@timeout(5)
def exe_func(args):
    print("arg_func: ", args, " sec")
    time.sleep(args)



def safe_exe_func(args):
    try:
        exe_func(args)
    except TimeoutError:
        print("Timeout !!!!")
        exe_func(args)


if __name__ == "__main__":
    for i in range(10):
        safe_exe_func(i)
    