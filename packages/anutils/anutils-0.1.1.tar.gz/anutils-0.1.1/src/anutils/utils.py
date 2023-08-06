import time 
import datetime
import os
import sys

def print_with_time(string):
    print('[{}] '.format(str(datetime.datetime.now())) + string)
    sys.stdout.flush()


def silent(mode='all'):
    assert(mode in ['out', 'err', 'all'])
    def silencer(fn):
        def wrapped(*args, **kwargs):
            oo, oe = sys.stdout, sys.stderr
            with open(os.devnull, 'w') as devnull:
                if mode=='out' or mode=='all':
                    sys.stdout = devnull
                if mode=='err' or mode=='all':
                    sys.stderr = devnull
                ret = fn(*args, **kwargs)
            sys.stdout, sys.stderr = oo, oe
            return ret
        return wrapped
    return silencer


def timing(fn, show_datetime: bool = True):
    def timed(*args, **kwargs):
        start = time.time()
        ret = fn(*args, **kwargs)
        tmstr = "{} elapse: {:.3f} s".format(fn.__name__, time.time() - start)
        if show_datetime:
            tmstr = ' '.join(['['+str(datetime.datetime.now())+']', tmstr])
        print(tmstr)
        return ret
    return timed


def logging_to(target_dir: str, need_timing_in_name: bool = True):
    assert (os.path.isdir(target_dir))
    def decorator(fn):
        def logged_fn(*args, **kwargs):
            if need_timing_in_name:
                dt = datetime.datetime.now()
                txt_path = os.path.join(target_dir, "log_{:d}_{:d}_{:d}_{:d}_{:d}_{:d}.txt".format(
                    dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second))
            else:
                txt_path = os.path.join(target_dir, 'log.txt')

            with open(txt_path, 'w') as f:
                old_stdout = sys.stdout
                sys.stdout = f
                ret = fn(*args, **kwargs)
                sys.stdout = old_stdout
            return ret
        return logged_fn
    return decorator


def get_datetime_str() -> str:
    dt = datetime.datetime.now()
    dt_str = "{:d}_{:d}_{:d}_{:d}_{:d}_{:d}".format(
        dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
    return dt_str