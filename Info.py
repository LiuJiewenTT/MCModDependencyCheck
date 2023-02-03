import os
import strings
from constants import *
from DebugMode import *
from common import print_log, print_debug

OHEADER_G = f'{os.path.relpath(__file__, basedir)}'
gmode = DebugMode(DEBUGMODE_GDEBUG, None)

class Info:
    raw: str

    def __init__(self, dict_info: dict):
        if isinstance(dict_info, dict) is False:
            print_log(strings.VALUETYPE_ERROR)
            return
        self.datadict = dict_info
        self.resolveDict()

    def resolveDict(self):
        OHEADER = f'{OHEADER_G}/resolveDict()'
        mode = DebugMode(DEBUGMODE_NORMAL, gmode.mode)

        self.datadict = self.clearValueType()

        try:
            self.raw = self.datadict['raw']
        except KeyError as ke:
            print_debug([f'KeyError: {ke}. Keys: ', self.datadict.keys()], OHEADER, mode.isDebug())
            raise ke
        return

    def clearValueType(self, mdict: dict=None):
        OHEADER = f'{OHEADER_G}/clearValueType()'
        mode = DebugMode(DEBUGMODE_NORMAL, gmode.mode)

        if mdict is None:
            mdict = self.datadict

        for key in mdict.keys():
            if key != 'raw':
                idx = mdict[key].find('#')
                if idx != -1:
                    s1 = mdict[key][:idx]
                else:
                    s1 = mdict[key]
                print_debug(s1, OHEADER, mode.isDebug())
                s1 = s1.strip('\'" ')
                if mdict[key] != s1:
                    print_debug([f'neq: [key, str, s1]: [{key}, {mdict[key]}, {s1}]'], OHEADER, mode.isDebug())
                    # print_debug([f'raw: ', self.datadict['raw']], OHEADER, mode.isDebug())
                    mdict[key] = s1
                else:
                    # print_debug([f'eq: [key, str, s1]: [{key}, {self.datadict[key]}, {s1}]'], OHEADER, mode.isDebug())
                    pass

        return mdict