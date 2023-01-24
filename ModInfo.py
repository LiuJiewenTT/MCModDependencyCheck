import os
import strings
from constants import *
from DebugMode import *
from common import print_log, print_debug
from DependencyInfo import DependencyInfo

OHEADER_G = f'{os.path.relpath(__file__, basedir)}'
gmode = DebugMode(DEBUGMODE_DEBUG, None)

class ModInfo:
    otherInfo: dict

    modId: str
    version: str
    displayName: str
    authors: str
    description: str

    dependenciesinfo: DependencyInfo

    raw: str
    datadict: dict

    def __init__(self, dict_info: dict, dependencies_info = []):
        if isinstance(dict_info, dict) is False:
            print_log(strings.VALUETYPE_ERROR)
            return
        self.datadict = dict_info
        self.resolveDict()
        self.dependenciesinfo = dependencies_info

    def resolveDict(self):
        OHEADER = f'{OHEADER_G}/resolveDict()'
        mode = DebugMode(DEBUGMODE_NORMAL, gmode.mode)

        self.clearValueType()
        try:
            self.modId = self.datadict['modId']
            self.version = self.datadict['version']
            self.displayName = self.datadict['displayName']
            self.authors = self.datadict['authors']
            self.description = self.datadict['description']

            self.raw = self.datadict['raw']
        except KeyError as ke:
            print_debug([f'KeyError: {ke}. Keys: ', self.datadict.keys()], OHEADER, mode.isDebug())
            raise ke
        return

    def clearValueType(self):
        OHEADER = f'{OHEADER_G}/clearValueType()'
        mode = DebugMode(DEBUGMODE_NORMAL, gmode.mode)

        for key in self.datadict.keys():
            if key != 'raw':
                s1 = self.datadict[key].strip('\'" ')
                if self.datadict[key] != s1:
                    # print_debug([f'neq: [key, str, s1]: [{key}, {self.datadict[key]}, {s1}]'], OHEADER, mode.isDebug())
                    # print_debug([f'raw: ', self.datadict['raw']], OHEADER, mode.isDebug())
                    self.datadict[key] = s1
                else:
                    # print_debug([f'eq: [key, str, s1]: [{key}, {self.datadict[key]}, {s1}]'], OHEADER, mode.isDebug())
                    pass