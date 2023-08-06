# -*- coding: utf-8 -*-
import datetime
import re
import sys

import time


def check_sharedmemory_support():
    return sys.version_info >= (3, 8)


def formatter_st(v, default=None) -> time.struct_time:
    if v is None:
        v = default
    if type(v) == time.struct_time:
        return v
    elif type(v) == str and re.match(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', v):
        return time.strptime(v, '%Y-%m-%d %H:%M:%S')
    if type(v) == str and re.match(r'\d{14}', v):
        return time.strptime(v, '%Y%m%d%H%M%S')
    elif type(v) == str and re.match(r'\d{4}-\d{2}-\d{2}', v):
        return time.strptime(v, '%Y-%m-%d')
    elif type(v) == str and re.match(r'\d{8}', v):
        return time.strptime(v, '%Y%m%d')
    elif type(v) == str and re.match(r'\d{2}:\d{2}:\d{2}', v):
        return time.strptime(v, '%H:%M:%S')
    elif type(v) == str and re.match(r'\d{6}', v):
        return time.strptime(v, '%H%M%S')
    elif type(v) == datetime.time:
        return time.strptime(v.strftime('%H:%M:%S'), '%H:%M:%S')
    elif type(v) == datetime.datetime or type(v) == datetime.date:
        return v.timetuple()
    else:
        raise ValueError('the value must be str, struct_time or datetime.')


def formatter_list(v, default=None) -> list:
    if v is None:
        v = default
    if type(v) is list:
        return v
    elif v is None:
        return []
    else:
        return [v]
