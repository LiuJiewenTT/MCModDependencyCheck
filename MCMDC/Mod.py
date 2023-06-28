import zipfile
import os

from . import common
from . import strings
from .constants import *
from .ModInfo import ModInfo
from .DependencyInfo import DependencyInfo
from .Version import Version
from .common import print_log, print_debug
from .DebugMode import *

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
    IMG_LOGO: list  # e.g.: np.ndarray


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
        mode = DebugMode(DEBUGMODE_GDEBUG, gmode.mode)

        self.modinfo = None
        retvs = self.readinfo1()
        if type(retvs) == 'list':
            retv, error_message = retvs
        if retvs is None and self.modinfo.version != VERSION_REDIRECTED_SIGN:
            self.resolveVersion()
            return
        # Version might be redirected.
        if self.modinfo is None:
            print_log(strings.MOD_INCOMPLETE_NOINFO)
            print_debug(strings.MOD_INCOMPLETE_NOINFO, OHEADER, mode.isDebug())
            return

        print_log(strings.VERSION_REDIRECTED)
        self.readinfo2()
        print_log(strings.MOD_READINFO_DONE + f'mod: [{self.modinfo.getModName()}]')
        self.resolveVersion()

    def readinfo1(self):
        OHEADER = f'{OHEADER_G}/readinfo1()'
        mode = DebugMode(DEBUGMODE_NORMAL, gmode.mode)

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
                try:
                    content_str = content_bytes.decode()
                except UnicodeDecodeError as ude:
                    print_log(f'UnicodeDecodeError: {ude}')
                    content_str = content_bytes.decode(errors='ignore')

                print_debug(['content_str: ', content_str], OHEADER, enabled=mode.isDebug())

                # get otherinfo
                print_log(strings.WORKING_ON_OTHERINFO)
                # locate [[mods]]
                i = content_str.find('[[')


                otherInfo: dict = common.extractPairs(content_str, 0, i)
                # print_debug(['otherinfo: ', otherInfo], OHEADER, mode.isDebug())

                # get info for modinfo
                print_log(strings.WORKING_ON_MODINFO)
                info = common.getInfo(content_str)
                print_debug(['info: ', info], OHEADER, mode.isDebug())

                if (info.get('infotype') == 'mods'):
                    modinfo = ModInfo(info, otherInfo=otherInfo)
                    # modinfo.otherInfo = modinfo.clearValueType(otherInfo)
                    print_debug(f'modinfo.modId: {modinfo.modId}', OHEADER, mode.isDebug())
                    print_debug(['otherInfo', modinfo.otherInfo], OHEADER, mode.isDebug())
                    print_log(strings.CREATE_MODINFO)
                else:
                    print_log([strings.INFO_NOT_MOD, f'infotype: {info.get("infotype")}'])

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
                    print_debug(['info: ', info], OHEADER, mode.isDebug(True))
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

            # work is done, assign modinfo to self.modinfo
            self.modinfo = modinfo
            print_log(strings.MOD_READINFO_DONE_1 + f'mod: [{self.modinfo.getModName()}]')
        return

    def readinfo2(self):
        OHEADER = f'{OHEADER_G}/readinfo2()'
        mode = DebugMode(DEBUGMODE_NORMAL, gmode.mode)

        # open zip and read
        with zipfile.ZipFile(self.filepath, mode='r') as file_zip:
            path_target = zipfile.Path(file_zip, at=self.target2_path)
            if (path_target.exists()):
                print_log(strings.TARGET_FOUNDED + f'target: [{self.target2_path}].')
            else:
                return [RETV_ERROR, strings.ERROR_FILE_NOT_FOUND + self.target2_path]

            # open target file to read info
            with path_target.open(mode='r') as file_target:
                # read
                content_bytes = file_target.read()
                # content_str = str(content_bytes)
                # content_str = content_bytes.decode()
                try:
                    content_str = content_bytes.decode()
                except UnicodeDecodeError as ude:
                    print_log(f'UnicodeDecodeError: {ude}')
                    content_str = content_bytes.decode(errors='ignore')

                print_debug(['content_str: ', content_str], OHEADER, enabled=mode.isDebug())

                info = common.extractPairs(content_str, identifier=':')
                print_debug(['.MF, info: ', info], OHEADER, mode.isDebug())

                self.modinfo.version = info.get('Implementation-Version')

        print_log(strings.MOD_READINFO_DONE_2 + f'mod: [{self.modinfo.getModName()}]')
        pass

    def resolveVersion(self):
        OHEADER = f'{OHEADER_G}/resolveVersion()'
        mode = DebugMode(DEBUGMODE_NORMAL, gmode.mode)

        version = self.modinfo.version
        print_log(strings.CURRENT_VERSION_VALUE + version)
        # Check if there are multiple versions
        a = version.find('-')
        # NO, it's single
        if a == -1:
            self.modinfo.version_Version = Version(self.modinfo.version)
            return
        # YES, it's multiple
        # Going to load rules and match
        print_log('Gonna process the version string further with some technics. modId: [{modId}]'.format(modId=self.modinfo.modId))
        print_log('version check is not online for now. [In Designing Stage]')
        pass

        # Finish.
        print_log(strings.CORRECTED_VERSION_VALUE + version)
        pass