import os
import strings
from constants import *
from DebugMode import *
from common import print_log, print_debug
from Info import Info
from DependencyInfo import DependencyInfo

OHEADER_G = f'{os.path.relpath(__file__, basedir)}'
gmode = DebugMode(DEBUGMODE_GDEBUG, None)

class ModInfo(Info):
    # info above [[mods]]
    otherInfo: dict

    # info under [[mods]]
    modId: str
    version: str
    displayName: str
    authors: str
    description: str

    raw: str
    datadict: dict

    # info under [[dependencies.*]]
    dependenciesinfo: list

    def __init__(self, dict_info: dict, dependencies_info = [], otherInfo = {}):
        if isinstance(dict_info, dict) is False:
            print_log(strings.VALUETYPE_ERROR)
            return
        self.datadict = dict_info
        self.dependenciesinfo = dependencies_info
        self.otherInfo = otherInfo

    def resolveDict(self):
        OHEADER = f'{OHEADER_G}/resolveDict()'
        mode = DebugMode(DEBUGMODE_NORMAL, gmode.mode)

        try:
            self.otherInfo = self.clearValueType(self.otherInfo)
            print_debug(['otherInfo', self.otherInfo], OHEADER, mode.isDebug())
        except AttributeError as ae:
            print_debug(strings.NO_OTHERINFO_NOW + f': [{ae}]', OHEADER, mode.isDebug())

        self.datadict = self.clearValueType()

        try:
            self.raw = self.datadict['raw']

            self.modId = self.datadict['modId']
            self.version = self.datadict['version']
            self.displayName = self.datadict['displayName']
            self.authors = self.datadict['authors']
            self.description = self.datadict['description']
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
                s1 = mdict[key].strip('\'" ')
                if mdict[key] != s1:
                    # print_debug([f'neq: [key, str, s1]: [{key}, {self.datadict[key]}, {s1}]'], OHEADER, mode.isDebug())
                    # print_debug([f'raw: ', self.datadict['raw']], OHEADER, mode.isDebug())
                    mdict[key] = s1
                else:
                    # print_debug([f'eq: [key, str, s1]: [{key}, {self.datadict[key]}, {s1}]'], OHEADER, mode.isDebug())
                    pass

        return mdict