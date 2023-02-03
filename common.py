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

def isInfoTypeDependency(info: dict):
    s1: str = info['infotype']
    s2: str = s1.partition('.')[0]
    if s2 == 'dependencies':
        return True
    return False

def getInfo(res: str, start=0, end=None):
    OHEADER = f'{OHEADER_G}/getInfo()'
    mode = DebugMode(DEBUGMODE_NORMAL, gmode.mode)

    if end is None:
        end = res.__len__()
    dict1 = {}

    i = res.find('[[', start, end)
    j = res.find(']]', start, end)
    if i == -1 or j == -1:
        print_log(strings.CONTENT_INCOMPLETED)
        print_debug([strings.CONTENT_INCOMPLETED, '\'[[\' or \']]\' not found'], OHEADER, mode.isDebug())
    if i >= j:
        print_log(strings.INTERVAL_NOT_EXIST + f'[{i},{j}). ')

    i += 2

    dict1['infotype'] = res[i:j]
    print_debug(['infotype: ', dict1['infotype']], OHEADER, mode.isDebug())

    i = j + 2
    j = res.find('[[', i, end)

    raw: str
    if j == -1:
        if dict1['infotype'] == 'mods':
            # Dependencies are missing.
            print_log(strings.CONTENT_INCOMPLETED)
            print_debug([strings.CONTENT_INCOMPLETED, '\'[[\' not found after recognizing infotype'], OHEADER, mode.isDebug())
        raw = res[i:]
    else:
        raw = res[i:j]

    print_debug(['raw: ', raw], OHEADER, mode.isDebug())

    # dict1['raw'] = raw

    dict1.update(extractPairs(raw))

    # for i in dict1.keys():
    #     dict1[i] = dict1[i].strip('\r\n')

    print_debug(['dict1: ', [dict1[x] for x in dict1.keys() if x!='raw']], OHEADER, mode.isDebug())

    return dict1

def extractPairs(raw: str, start=0, end=None, identifier:str='='):
    OHEADER = f'{OHEADER_G}/extractPairs()'
    mode = DebugMode(DEBUGMODE_NORMAL, gmode.mode)

    if end is None:
        end = raw.__len__()
    # not good for dependencies, good for description
    dict1 = {}
    i = start

    while True:
        k = raw.find(identifier, i, end)
        if k == -1:
            print_log(strings.NO_MORE_ITEM)
            break

        left_1 = raw.rfind('\r', i, k) + 1
        left_2 = raw.rfind('\n', i, k) + 1
        # print_debug(['left_1, left_2: ', left_1, left_2], OHEADER, mode.isDebug())
        left_idx = max(left_1, left_2)
        if left_idx <= 0:  # (-1) + 1 = 0
            # print_log()
            # raise IndexError()
            left_idx = i
            # print_log(strings.MEET_PURE_END + strings.ON_THE_LEFT)
            print_debug([strings.MEET_PURE_END + strings.ON_THE_LEFT + f'[i, k, str]: [{i}, {k}] .', raw[i:k]], OHEADER,
                        mode.isDebug())

        left_str = raw[left_idx: k]
        # print_debug(['left_str, left_idx, k: ', left_str, left_idx, k], OHEADER, mode.isDebug())
        # strip out blankspaces
        left_str = left_str.strip('\r\n ')

        if left_str != 'description':
            right_1 = raw.find('\r', k, end)
            right_2 = raw.find('\n', k, end)
            try:
                right_idx = getNonNegativeMin(right_1, right_2)
            except ValueError:
                right_idx = end
                # print_log(strings.MEET_PURE_END + strings.ON_THE_RIGHT)
                print_debug(strings.MEET_PURE_END + strings.ON_THE_RIGHT, OHEADER, mode.isDebug())

            right_str = raw[k + 1: right_idx]
        else:
            right_1 = raw.find("\'\'\'", k, end) + 3
            right_2 = raw.find("\'\'\'", right_1, end)
            right_idx = right_2 + 3
            right_str = raw[right_1:right_2]
            print_debug(['description: ', right_str], OHEADER, mode.isDebug())

        # strip out blankspaces and \r\n
        right_str = right_str.strip('\r\n ')

        dict1[left_str] = right_str

        i = right_idx
        print_debug(['i: ', i], OHEADER, mode.isDebug())

    dict1['raw'] = raw
    return dict1

def getParts(res: str, substr: str=None):
    OHEADER = f'{OHEADER_G}/getParts()'
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
        st = res.find(']]', st, ed)
        # print_debug( f'[str, st(loc), st, ed]: [{res[loc:ed]}, {loc}, {st}, {ed}]', OHEADER, mode.isDebug())
        if st == -1:
            print_log(strings.CONTENT_INCOMPLETED)
            print_debug([strings.CONTENT_INCOMPLETED, '\']]\' not found: '], OHEADER, mode.isDebug())
            break
        st += 2
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


def versionCmp(v1: str, v2: str):
    pass