import os
import strings
from constants import *
from DebugMode import *

OHEADER_G = f'{os.path.relpath(__file__, basedir)}'
# print(__file__)

gmode = DebugMode(DEBUGMODE_GDEBUG, None)

def print_log(para):
    print(LOGMODE_LOG_OHEADER, end='')
    print(para)

def print_debug(para, location='unknown', enabled=True):
    if enabled is False:
        return
    print(LOGMODE_DEBUG_OHEADER + f'in [{location}]: ', end='')
    print(para)

def getNonNegativeMin(a, b):
    if a < 0 and b >= 0:
        return b
    elif b < 0 and a >= 0:
        return a
    elif a >= 0 and b >= 0:
        return min(a, b)
    else:
        print_log(strings.ERROR_NO_NONNEGATIVE_VALUE + f': min[{a}, {b}] >= 0')
        raise ValueError(strings.ERROR_NO_NONNEGATIVE_VALUE + f': min[{a}, {b}] >= 0')


def getInfo(res: str, start=0, end=None):
    OHEADER = f'{OHEADER_G}/getInfo()'
    global gmode
    mode = DebugMode(DEBUGMODE_GDEBUG, gmode.mode)

    end = res.__len__()
    dict1 = {}

    i = res.find('[[', start, end) + 2
    j = res.find(']]', start, end)
    if i == -1 or j == -1:
        print_log(strings.CONTENT_INCOMPLETED)
    if i >= j:
        print_log(strings.INTERVAL_NOT_EXIST + f'[{i},{j}). ')

    dict1['infotype'] = res[i:j]
    # print(dict1['infotype'])

    i = j + 2
    j = res.find('[[', i, end)
    if j == -1:
        print_log(strings.CONTENT_INCOMPLETED)

    raw: str = res[i:j]
    print_debug(['raw: ', raw], OHEADER, mode.isDebug())

    # dict1['raw'] = raw

    # not good for description
    while True:
        k = raw.find('=', i, end)
        if k == -1:
            print_log(strings.NO_MORE_ITEM)
            break

        left_1 = raw.rfind('\\r', i, k) + 2
        left_2 = raw.rfind('\\n', i, k) + 2
        left_idx = max(left_1, left_2)
        if left_idx < 0:
            # print_log()
            raise IndexError()

        left_str = raw[left_idx: k]
        # strip out blankspaces
        left_str = left_str.strip()

        if left_str != 'description':
            right_1 = raw.find('\\r', k, end)
            right_2 = raw.find('\\n', k, end)
            right_idx = getNonNegativeMin(right_1, right_2)
            right_str = raw[k + 1: right_idx]
        else:
            right_1 = raw.find("\\\'\\\'\\\'", k, end) + 3
            right_2 = raw.find("\\\'\\\'\\\'", right_1, end)
            right_idx = right_2
            right_str = raw[right_1:right_2]
            print_debug(['description: ', right_str], OHEADER, mode.isDebug())

        # strip out blankspaces
        right_str = right_str.strip()

        dict1[left_str] = right_str

        i = right_idx + 2

    print_debug(['dict1: ', dict1], OHEADER, mode.isDebug())
    dict1['raw'] = raw


def getParts(res: str, substr: str=None):
    OHEADER = f'{OHEADER_G}/getParts()'
    if substr is None:
        substr = PART_LOCATOR

    parts_raw = getParts_raw(res, substr)

    # should return some object
    return parts_raw

def getParts_raw(res: str, substr: str=None):
    OHEADER = f'{OHEADER_G}/getParts_raw()'
    global gmode
    mode = DebugMode(DEBUGMODE_NORMAL, gmode.mode)

    if substr is None:
        substr = PART_LOCATOR
    lst1 = []
    lst2 = []
    st = 0
    ed = res.__len__()
    while st < ed:
        # print_debug(st, OHEADER)
        loc = res.find(substr, st, ed)
        if loc == -1:
            print_log(strings.NO_MORE_PARTS)
            break
        st = loc
        st = res.find(']]', st, ed) + 2
        if st == -1:
            print_log(strings.CONTENT_INCOMPLETED)
            break
        # print(loc, res[st], res[st+1])
        # break
        lst1.append(loc)
    print_debug(lst1, OHEADER, mode.isDebug())
    i = 0
    j = 1
    a = b = 0
    while True:
        str_part = ''
        try:
            a = lst1[i]
        except IndexError:
            break
        except Exception as e:
            print_debug(e, OHEADER, mode.isDebug())

        try:
            b = lst1[j]
            print_debug(b, OHEADER, mode.isDebug())
            str_part = res[a:b]
        except:
            print_debug(lst2, OHEADER, mode.isDebug())
            str_part = res[a:]

        lst2.append(str_part)
        i += 1
        j += 1

    return lst2