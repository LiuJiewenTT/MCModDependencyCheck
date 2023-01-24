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
    mode = DebugMode(DEBUGMODE_NORMAL, gmode.mode)

    filedir = 'testres/'
    filelist = os.listdir(filedir)

    # print(filelist)

    for filename in filelist:
        # do something
        pass

    # temp filename
    filename = 'mcvine_wat_1.18.2_0.1.2.jar'
    path_zip = os.path.join(filedir, filename)
    print_log(strings.CURRENT_FILE_PREFIX + '[' + str(path_zip) + ']')

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

            i = content_str.find('[[')
            otherInfo: dict = extractPairs(content_str, 0, i)

            # This is good.
            info = getInfo(content_str)
            print_debug(['info: ', info], OHEADER, mode.isDebug())

            if( info['infotype'] == 'mods'):
                modinfo = ModInfo(info)
                modinfo.otherInfo = otherInfo
                print_log(strings.CREATE_MODINFO)
            else:
                print_log([strings.INFO_NOT_MOD, f'infotype: {info["infotype"]}'])

            parts = getParts(content_str)
            print_debug(['parts: ', parts], OHEADER, enabled=mode.isDebug())

            dependenciesinfo = []
            cnt_dependencies = 0
            for part in parts:
                print_debug(['part: ', part], OHEADER, mode.isDebug())
                info = getInfo(part)
                print_debug(['info: ', info], OHEADER, mode.isDebug())
                if( isInfoTypeDependency(info) ):
                    dependencyinfo = DependencyInfo(info)
                    dependenciesinfo.append(dependencyinfo)
                    cnt_dependencies += 1
                else:
                    pass
            print_log(strings.CNT_DEPENDENCIES_1 + str(dependenciesinfo.__len__()) + ', ' + strings.CNT_DEPENDENCIES_REAL + str(cnt_dependencies))

            # test: to see if that's ok.
            # print_debug(['dependenciesinfo: ', vars(dependenciesinfo[0])], OHEADER, mode.isDebug())

            modinfo.dependenciesinfo = dependenciesinfo

        pass



if __name__ == "__main__":
    main()