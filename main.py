import zipfile
import os

from DebugMode import *
initDefault_gmode(DEBUGMODE_GDEBUG)

import constants
from constants import *
import strings
from common import *
from Mod import Mod
from ModInfo import ModInfo
from DependencyInfo import DependencyInfo


OHEADER_G = f'{os.path.relpath(__file__, basedir)}'
# print(__file__)

gmode = DebugMode(DEBUGMODE_GDEBUG, None)

def main():
    OHEADER = f'{OHEADER_G}/main()'

    global gmode
    mode = DebugMode(DEBUGMODE_NORMAL, gmode.mode)

    filedir = 'testres/'
    filelist = os.listdir(filedir)
    # print(filelist)

    # temp
    # filelist = ['mcvine_wat_1.18.2_0.1.2.jar']
    filelist = ['createdeco-1.2.9-1.18.2.jar']

    for filename in filelist:
        # do something
        path_zip = os.path.join(filedir, filename)
        print_log(strings.CURRENT_FILE_PREFIX + '[' + str(path_zip) + ']')
        mod = Mod(filename=filename, filedir=filedir)
        mod.readinfo()

        pass



if __name__ == "__main__":
    main()