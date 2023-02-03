import os
import strings
from constants import *
from DebugMode import *
from common import print_log, print_debug
from Info import Info

OHEADER_G = f'{os.path.relpath(__file__, basedir)}'
gmode = DebugMode(DEBUGMODE_GDEBUG, None)

class DependencyInfo(Info):
    modId: str
    versionRange: str
    ordering: str
    side: str
    mandatory: bool

    raw: str
    datadict: dict

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

            self.modId = self.datadict['modId']
            self.versionRange = self.datadict['versionRange']
            self.ordering = self.datadict['ordering']
            self.side = self.datadict['side']
            self.mandatory = self.datadict['mandatory']
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
                s1 = s1.strip('\'" ')
                if mdict[key] != s1:
                    mdict[key] = s1
                # s1 = mdict[key]
                if key == 'mandatory':
                    if s1 == 'true':
                        mdict['mandatory'] = True
                    elif s1 == 'false':
                        mdict['mandatory'] = False
                    else:
                        print_log([strings.UNEXPECTED_MANDATORY_VALUE + f': {mdict["mandatory"]}. '])
                        print_debug([strings.UNEXPECTED_MANDATORY_VALUE + f': {mdict["mandatory"]}. '], OHEADER, mode.isDebug())
                    print_debug(['mandatory', mdict['mandatory']], OHEADER, mode.isDebug())

        return mdict