# I'm not going to use this now.
import zipfile
import os

import common
import strings
from constants import *
from ModInfo import ModInfo
from DependencyInfo import DependencyInfo
from common import print_log, print_debug
from DebugMode import *

OHEADER_G = f'{os.path.relpath(__file__, basedir)}'
gmode = DebugMode(DEBUGMODE_GDEBUG, None)

class Mod:
    filename: str
    filepath: str
    filedir: str

    target1_path = 'META-INF/mods.toml'
    target2_path = 'META-INF/MANIFEST.MF'

    modinfo: ModInfo

    # for possible future development
    IMG_LOGO: list


    def __init__(self, filepath: str=None, filedir: str=None, filename: str=None):
        OHEADER = f'{OHEADER_G}/__init__()'
        mode = DebugMode(DEBUGMODE_NORMAL, gmode.mode)

        if filepath is None:
            if filedir is None:
                print_log(strings.NO_FILEDIR)
                print_debug(strings.NO_FILEDIR, OHEADER, mode.isDebug())
                raise RuntimeError(strings.NO_FILEDIR)
            if filename is None:
                print_log(strings.NO_FILENAME)
                print_debug(strings.NO_FILENAME, OHEADER, mode.isDebug())
                raise RuntimeError(strings.NO_FILENAME)

            filepath = os.path.join(filedir, filename)
        else:
            # filepath not none, but filedir or filename not completed.
            # complete those
            filedir = os.path.dirname(filepath)
            filename = os.path.basename(filepath)

        # Assign the values.
        try:
            self.filepath = filepath
            self.filename = filename
            self.filedir = filedir
        except Exception as e:
            print_log(e)
            print_debug(e, OHEADER, mode.isDebug())

        pass

    def readinfo(self):
        OHEADER = f'{OHEADER_G}/readinfo()'
        mode = DebugMode(DEBUGMODE_NORMAL, gmode.mode)

        # self.filepath = os.path.join(self.filedir, self.filename)

        # open zip and read
        with zipfile.ZipFile(self.filepath, mode='r') as file_zip:
            path_target = zipfile.Path(file_zip, at=self.target1_path)
            if (path_target.exists()):
                print_log(strings.TARGET_FOUNDED + f'target: [{self.target1_path}].')
            else:
                return [RETV_ERROR, strings.ERROR_FILE_NOT_FOUND + self.target1_path]

            # open target file to read info
            with path_target.open(mode='r') as file_target:
                # read
                content_bytes = file_target.read()
                # content_str = str(content_bytes)
                content_str = content_bytes.decode()

                print_debug(['content_str: ', content_str], OHEADER, enabled=mode.isDebug())

                # locate [[mods]]
                i = content_str.find('[[')
                # get otherinfo
                print_log(strings.WORKING_ON_OTHERINFO)
                otherInfo: dict = common.extractPairs(content_str, 0, i)
                # print_debug(['otherinfo: ', otherInfo], OHEADER, mode.isDebug())

                # get info for modinfo
                print_log(strings.WORKING_ON_MODINFO)
                info = common.getInfo(content_str)
                print_debug(['info: ', info], OHEADER, mode.isDebug())

                if (info['infotype'] == 'mods'):
                    modinfo = ModInfo(info, otherInfo=otherInfo)
                    # modinfo.otherInfo = modinfo.clearValueType(otherInfo)
                    print_debug(['otherInfo', modinfo.otherInfo], OHEADER, mode.isDebug())
                    print_log(strings.CREATE_MODINFO)
                else:
                    print_log([strings.INFO_NOT_MOD, f'infotype: {info["infotype"]}'])

                # get dependencies and info
                print_log(strings.WORKING_ON_DEPENDENCYINFO)
                parts = common.getParts(content_str)
                print_debug(['parts: ', parts], OHEADER, enabled=mode.isDebug())

                # check if real dependencyinfo
                dependenciesinfo = []
                cnt_dependencies = 0
                for part in parts:
                    print_debug(['part: ', part], OHEADER, mode.isDebug())
                    info = common.getInfo(part)
                    print_debug(['info: ', info], OHEADER, mode.isDebug())
                    # only append real ones.
                    if (common.isInfoTypeDependency(info)):
                        dependencyinfo = DependencyInfo(info)
                        dependenciesinfo.append(dependencyinfo)
                        print_debug(['dependenctinfo.datadict: ', dependencyinfo.datadict], OHEADER, mode.isDebug())
                        cnt_dependencies += 1
                    else:
                        pass
                print_log(strings.CNT_DEPENDENCIES_1 + str(
                    dependenciesinfo.__len__()) + ', ' + strings.CNT_DEPENDENCIES_REAL + str(cnt_dependencies))

                # test: to see if that's ok.
                # print_debug(['dependenciesinfo: ', vars(dependenciesinfo[0])], OHEADER, mode.isDebug())

                modinfo.dependenciesinfo = dependenciesinfo

            pass