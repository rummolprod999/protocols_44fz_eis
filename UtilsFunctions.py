import datetime
import operator
import shutil
from functools import reduce

from VarExecut import file_log


def logging_parser(*messages):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"{timestamp} {' '.join(str(msg) for msg in messages)}\n\n"

    try:
        with open(file_log, 'a') as log_file:
            log_file.write(log_entry)
    except IOError as e:
        print(f"Failed to write to log file: {e}")


def check_yeld(h) -> bool:
    flag = False
    for i in h:
        if i:
            flag = True
    return flag


def get_from_dict(data_dict, map_list):
    return reduce(operator.getitem, map_list, data_dict)


def generator_univ(c):
    if c == "":
        raise StopIteration
    if type(c) == list:
        for i in c:
            yield i
    else:
        yield c


def get_el(d, *kwargs):
    try:
        res = get_from_dict(d, kwargs)
    except Exception:
        res = ''
    if res is None:
        res = ''
    if type(res) is str:
        res = res.strip()
    return res


def get_el_list(d, *kwargs):
    try:
        res = get_from_dict(d, kwargs)
    except Exception as ex:
        res = []
    if res is None:
        res = []
    return res


unic_files = []


def unic(f, path):
    global unic_files
    begin_file_list = f.split('_')
    if not begin_file_list[0] in unic_files:
        unic_files.append(begin_file_list[0])
        file_ex = path + '/' + f
        file_target = f'./ParserProtocols/unic_protocol/{f}'
        shutil.copy(file_ex, file_target)


def copy_new_file(f, path):
    file_ex = path + '/' + f
    file_target = f'./ParserProtocols/unic_protocol/{f}'
    shutil.copy(file_ex, file_target)
