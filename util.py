import os
import traceback
from datetime import datetime


def get_logfile_path(filename):
    try:
        os.mkdir(os.getcwd() + r'/logs/')
    except:
        pass
    return os.getcwd() + r'/logs/' + filename + ' ' + datetime.now().strftime('%y%m%d') + '.txt'


def log(msg: str):
    with open(get_logfile_path('log'), 'a', encoding='utf-8') as f:
        f.write('\n' + str(msg))
    return


def error():
    with open(get_logfile_path('error'), 'a', encoding='utf-8') as f:
        f.write('\n[' + datetime.now().strftime('%H:%M:%S') + '] ' + str(traceback.format_exc()))
    return
