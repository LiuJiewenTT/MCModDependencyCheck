import os
import strings
from constants import *
from DebugMode import *
from common import print_log, print_debug

class DependencyInfo:
    modId: str
    versionRange: str
    ordering: str
    side: str
    mandatory: str

    raw: str
    datadict: dict

    def __init__(self, dict_info: dict):
        if isinstance(dict_info, dict) is False:
            print_log(strings.VALUETYPE_ERROR)
            return
        self.datadict = dict_info
        pass

    def resolveDict(self):
        self.modId = self.datadict['modId']
        self.versionRange = self.datadict['versionRange']
        self.ordering = self.datadict['ordering']
        self.side = self.datadict['side']
        self.mandatory = self.datadict['mandatory']

        self.raw = self.datadict['raw']
        return
