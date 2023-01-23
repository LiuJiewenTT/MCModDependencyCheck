import os
import strings
from constants import *
from DebugMode import *
from common import print_log, print_debug

OHEADER_G = f'{os.path.relpath(__file__, basedir)}'
gmode = DebugMode(DEBUGMODE_DEBUG, None)

class ModInfo:
    modId: str
    version: str
    displayName: str
    authors: str
    description: str

    raw: str
    datadict: dict

    def __init__(self, dict_info: dict):
        if isinstance(dict_info, dict) is False:
            print_log(strings.VALUETYPE_ERROR)
            return
        pass

    def resolveDict(self):
        self.modId = self.datadict['modId']
        self.version = self.datadict['version']
        self.displayName = self.datadict['displayName']
        self.authors = self.datadict['authors']
        self.description = self.datadict['description']

        self.raw = self.datadict['raw']
        return