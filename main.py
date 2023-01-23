import zipfile
import os

from DebugMode import *
initDefault_gmode(DEBUGMODE_GDEBUG)

import constants
from constants import *
import strings
from common import *
from ModInfo import ModInfo
from DependencyInfo import DependencyInfo


OHEADER_G = f'{os.path.relpath(__file__, basedir)}'
# print(__file__)

gmode = DebugMode(DEBUGMODE_GDEBUG, None)

def main():
    OHEADER = f'{OHEADER_G}/main()'

    global gmode
    mode = DebugMode(DEBUGMODE_DEBUG, gmode.mode)

    filedir = 'testres/'
    filelist = os.listdir(filedir)

    # print(filelist)

    for filename in filelist:
        # do something
        pass

    # temp filename
    filename = 'mcvine_wat_1.18.2_0.1.2.jar'
    path_zip = os.path.join(filedir, filename)
    print_log(path_zip)

    with zipfile.ZipFile(path_zip, mode='r') as file_zip:
        path_target = zipfile.Path(file_zip, at=target_path)
        if( path_target.exists() ):
            print_log(strings.TARGET_FOUNDED)
        else:
            return [ RETV_ERROR , strings.ERROR_FILE_NOT_FOUND + constants.target_path ]

        with path_target.open(mode='r') as file_target:
            content_bytes = file_target.read()
            # content_str = str(content_bytes)
            content_str = content_bytes.decode()

            print_debug(['content_str: ', content_str], OHEADER, enabled=mode.isDebug())

            info = getInfo(content_str)
            if( info['infotype'] == 'mods'):
                modinfo = ModInfo(info)
                print_log(strings.CREATE_MODINFO)
            else:
                print_log([strings.INFO_NOT_MOD, f'infotype: {info["infotype"]}'])

            parts = getParts(content_str)
            print_debug(['parts: ', parts], OHEADER, enabled=mode.isDebug())

            dependenciesinfo = []
            for part in parts:
                print_debug(['part: ', part], OHEADER, mode.isDebug())
                info = getInfo(part)
                print_debug(['info: ', info], OHEADER, mode.isDebug())
                if( isInfoTypeDependency(info) ):
                    dependencyinfo = DependencyInfo(info)
                    dependenciesinfo.append(dependencyinfo)
                else:
                    pass

        pass



if __name__ == "__main__":
    main()