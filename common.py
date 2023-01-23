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