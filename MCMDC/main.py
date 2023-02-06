import os.path
import sys

from DebugMode import *
initDefault_gmode(DEBUGMODE_GDEBUG)

from common import *
from Mod import Mod

OHEADER_G = f'{os.path.relpath(__file__, basedir)}'
# print(__file__)

gmode = DebugMode(DEBUGMODE_GDEBUG, None)

toIgnore: bool
IgnoreList: list
isSetDir: bool
showLicense: str

def main(filedir: str=None):
    OHEADER = f'{OHEADER_G}/main()'

    global gmode
    mode = DebugMode(DEBUGMODE_NORMAL, gmode.mode)

    # print_debug([toIgnore, IgnoreList], OHEADER, mode.isDebug())

    about_print()

    if filedir is None:
        filedir = 'testres/'
        if os.path.exists(filedir) is False or os.listdir(filedir) == []:
            return

    # print_debug(f'isSetDir: {isSetDir}', OHEADER, True)

    # print(filelist)

    mods = readmods_dir(filedir)
    if mods == []:
        return

    mods_insufficient, modIds_lack_of = checkModIds(mods)
    modIds_insufficient = [x.modinfo.modId for x in mods_insufficient]

    if modIds_lack_of == []:
        print_log(strings.MODPACK_READY)
    else:
        print_log([strings.MODS_INSUFFICIENT, modIds_insufficient])
        print_log([strings.MODS_LACK_OF, modIds_lack_of])

def about_print():
    print(strings.ABOUT_TITLE)
    print(APP_NAME_DISPLAY + f' ({APP_NAME_ABBR})')
    print(strings.ABOUT_VERSION + f': v{APP_VERSION}')
    print(strings.ABOUT_AUTHORS + ': ', end='')
    for i in AUTHORS:
        print(i, end='; ')
    print('')
    print(strings.ABOUT_PROJECT + ': ' + APP_NAME)
    print(strings.ABOUT_LICENSE + ': ' + LICENSE)
    print(strings.ABOUT_PROJECTLINK + ': ' + PROJECT_LINK)
    return

def readmods_dir(filedir: str):
    # read mods from directory
    OHEADER = f'{OHEADER_G}/readmods_dir()'
    mode = DebugMode(DEBUGMODE_NORMAL, gmode.mode)

    filelist_temp = os.listdir(filedir)

    filelist = []
    for file in filelist_temp:
        if os.path.isfile(os.path.join(filedir, file)):
            filelist.append(file)

    # print_debug(['filelist: ', filelist, filelist_temp], OHEADER, mode.isDebug())

    # temp
    # filelist = ['mcvine_wat_1.18.2_0.1.2.jar']
    # filelist = ['createdeco-1.2.9-1.18.2.jar']

    if filelist == []:
        print_log(strings.EMPTY_FILELIST)
        print_debug(strings.EMPTY_FILELIST + f'{strings.STR_FILEDIR}: [{filedir}]', OHEADER, mode.isDebug())
        return []

    mods = readmods( filelist, filedir)
    return mods

def readmods(filelist: list, filedir: str=None):
    # read mods from list
    mods = []
    for filename in filelist:
        # do something
        if filedir is None:
            path_zip = filename
        else:
            path_zip = os.path.join(filedir, filename)
        print_log(strings.CURRENT_FILE_PREFIX + '[' + str(path_zip) + ']')
        mod = Mod(filename=filename, filedir=filedir)
        mod.readinfo()
        mods.append(mod)
    return mods

def checkModIds(mods: list):
    # check modId
    modIds = []
    mods_insufficient = []
    modIds_lack_of = []

    for mod in mods:
        mod: Mod
        modIds.append(mod.modinfo.modId)

    for mod in mods:
        mod: Mod
        flag = False
        for dependencyinfo in mod.modinfo.dependenciesinfo:
            if dependencyinfo.modId not in modIds:
                if toIgnore is True:
                    if dependencyinfo.modId not in IgnoreList:
                        if dependencyinfo.modId not in modIds_lack_of:
                            modIds_lack_of.append(dependencyinfo.modId)
                else:
                    if dependencyinfo.modId not in modIds_lack_of:
                        modIds_lack_of.append(dependencyinfo.modId)
                flag = True
        if flag is True:
            mods_insufficient.append(mod)

    return [mods_insufficient, modIds_lack_of]

def processArgs(argv: list):
    # Manual
    # -toIgnore [true/false] -dir ["testres/"]

    OHEADER = f'{OHEADER_G}/processArgs()'
    mode = DebugMode(DEBUGMODE_NORMAL, gmode.mode)

    print_debug(['Args: ', argv], OHEADER, mode.isDebug())

    argc = argv.__len__()
    retv = {}

    # 默认设置
    # 忽略默认
    retv['toIgnore'] = True
    retv['IgnoreList'] = ['forge', 'minecraft']
    retv['dir'] = 'testres/'
    retv['isSetDir'] = False
    retv['license'] = 'hide'

    flag = True
    try:
        for i in range(0, argc):
            if argv[i] == '-toIgnore':
                if argv[i+1].lower() == 'false':
                    retv['toIgnore'] = False
            elif argv[i] == '-IgnoreList':
                s: str = argv[i+1].strip(' ')
                s = s[1:-1]
                l = s.split(sep=',')
                l = [x.strip('"\' ') for x in l]
                retv['IgnoreList'] = l
            elif argv[i] == '-dir':
                retv['dir'] = argv[i+1].strip('" ')
                retv['isSetDir'] = True
            elif argv[i] == '-license':
                retv['license'] = 'show'
            else:
                flag = False
    except Exception as e:
        print(f'{LOGMODE_LOADING_OHEADER}', end='')
        print(e)
    if flag is False:
        if argc == 2:
            s: str = argv[-1].strip('"\' ')
            if os.path.isdir(s) is True:
                retv['dir'] = argv[-1]
                retv['isSetDir'] = True
    return retv

def applyArgs(args: dict):
    OHEADER = f'{OHEADER_G}/processArgs()'
    mode = DebugMode(DEBUGMODE_NORMAL, gmode.mode)

    global toIgnore, IgnoreList, showLicense, isSetDir
    toIgnore = args.get('toIgnore')
    IgnoreList = args.get('IgnoreList')
    showLicense = args.get('license')
    isSetDir = args.get('isSetDir')
    return

if __name__ == "__main__":

    args: dict = processArgs(sys.argv)
    applyArgs(args)
    filedir = args.get('dir')

    # print('exists: ', os.path.exists(filedir))
    # print('isSetDir: ', isSetDir)

    if os.path.exists(filedir) is False:
        if isSetDir is True:
            print_log(strings.NO_FILEDIR)
            print_debug(strings.NO_FILEDIR + f'{strings.STR_FILEDIR}: [{filedir}]', OHEADER_G, gmode.isDebug())
            sys.exit(strings.NO_FILEDIR)
        else:
            sys.exit(0)
    elif os.listdir(filedir) == []:
        if isSetDir is True:
            print_log(strings.EMPTY_FILELIST)
            print_debug(strings.EMPTY_FILELIST + f'{strings.STR_FILEDIR}: [{filedir}]', OHEADER_G, gmode.isDebug())
            sys.exit(strings.NO_FILEDIR)
        else:
            sys.exit(0)

        # 忽略默认
    # toIgnore = True
    # IgnoreList = ['forge', 'minecraft']

    main(filedir)


