import datetime
import operator
from functools import reduce

from parser_prot import file_log


def logging_parser(*kwargs):
    s_log = f'{datetime.datetime.now()} '
    for i in kwargs:
        s_log += f'{i} '
    s_log += '\n\n'
    with open(file_log, 'a') as flog:
        flog.write(s_log)


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
    except Exception:
        res = []
    if res is None:
        res = []
    return res
