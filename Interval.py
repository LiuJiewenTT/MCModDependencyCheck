import os

from common import print_log, print_debug
import strings
from constants import *
from DebugMode import *
from Version import Version

OHEADER_G = f'{os.path.relpath(__file__, basedir)}'
gmode = DebugMode(DEBUGMODE_GDEBUG, None)

class Interval:
    INF = 'INF'
    interval: list

    def __init__(self, arg: str=None):
        OHEADER = f'{OHEADER_G}/__init__()'
        mode = DebugMode(DEBUGMODE_DEBUG, gmode.mode)

        if arg is None:
            self.interval = ['[', '0', '1', ')']
        else:
            s1 = arg[1:-1]
            # remove possible multiple spaces
            s1 = s1.replace(' ', '')
            t1 = s1.split(sep=',')
            t1 = [x if x != '' else Interval.INF for x in t1]
            if t1.__len__() == 1:
                t1.append(t1[0])
            self.interval = [arg[0], t1[0], t1[1], arg[-1]]
        print_debug(self.interval, OHEADER, mode.isDebug())

        return

    def compareLeft(self, arg: str, func=None):
        # Return True if arg is larger or equal, cases depends.

        OHEADER = f'{OHEADER_G}/compareLeft()'
        mode = DebugMode(DEBUGMODE_DEBUG, gmode.mode)

        retv = False
        sign = self.interval[0]
        if func is None:
            if self.interval[1] == self.INF:
                retv = True
            elif sign == '[':
                # retv = (self.interval[1] <= arg)
                retv = (Version.versionCompare(self.interval[1], arg) != Version.VER_DECREASING)
            elif sign == '(':
                # retv = (self.interval[1] < arg)
                retv = (Version.versionCompare(self.interval[1], arg) == Version.VER_INCREASING)
            else:
                print_log(strings.WRONG_EDGESIGN_OF_INTERVAL)
                print_debug([strings.WRONG_EDGESIGN_OF_INTERVAL, sign], OHEADER, mode.isDebug())
                raise RuntimeError(strings.WRONG_EDGESIGN_OF_INTERVAL)
        else:
            retv = func.__call__(self.interval[1], arg, sign)

        return retv

    def compareRight(self, arg: str, func=None):
        # Return True if arg is smaller or equal, cases depends.

        OHEADER = f'{OHEADER_G}/compareRight()'
        mode = DebugMode(DEBUGMODE_DEBUG, gmode.mode)

        retv = False
        sign = self.interval[-1]
        if func is None:
            if self.interval[2] == self.INF:
                retv = True
            elif sign == ']':
                # retv = (self.interval[2] >= arg)
                retv = (Version.versionCompare(self.interval[2], arg) != Version.VER_INCREASING)
            elif sign == ')':
                # retv = (self.interval[2] > arg)
                retv = (Version.versionCompare(self.interval[2], arg) == Version.VER_DECREASING)
            else:
                print_log(strings.WRONG_EDGESIGN_OF_INTERVAL)
                print_debug([strings.WRONG_EDGESIGN_OF_INTERVAL, sign], OHEADER, mode.isDebug())
                raise RuntimeError(strings.WRONG_EDGESIGN_OF_INTERVAL)
        else:
            retv = func.__call__(self.interval[2], arg, sign)

        return retv

    def query_in_list(self, arg: list):
        pass

    def query_in_number(self, arg, func=None):
        retv = False
        a = self.compareLeft(arg, func)
        b = self.compareRight(arg, func)
        if a==True and b==True:
            retv = True
        return retv

    def query_in_Interval(self, arg):
        pass


