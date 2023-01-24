import os
import strings
from constants import *
from DebugMode import *
from common import print_log, print_debug

OHEADER_G = f'{os.path.relpath(__file__, basedir)}'
gmode = DebugMode(DEBUGMODE_GDEBUG, None)

class DependencyInfo:
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

        self.clearValueType()

        self.modId = self.datadict['modId']
        self.versionRange = self.datadict['versionRange']
        self.ordering = self.datadict['ordering']
        self.side = self.datadict['side']
        self.mandatory = self.datadict['mandatory']

        self.raw = self.datadict['raw']
        return

    def clearValueType(self):
        OHEADER = f'{OHEADER_G}/clearValueType()'
        mode = DebugMode(DEBUGMODE_NORMAL, gmode.mode)

        for key in self.datadict.keys():
            if key != 'raw':
                s1 = self.datadict[key].strip('\'" ')
                if self.datadict[key] != s1:
                    self.datadict[key] = s1
                if key == 'mandatory':
                    if s1 == 'true':
                        self.datadict['mandatory'] = True
                    elif s1 == 'false':
                        self.datadict['mandatory'] = False
                    else:
                        print_log([strings.UNEXPECTED_MANDATORY_VALUE + f': {self.datadict["mandatory"]}. '])
                        print_debug([strings.UNEXPECTED_MANDATORY_VALUE + f': {self.datadict["mandatory"]}. '], OHEADER, mode.isDebug())