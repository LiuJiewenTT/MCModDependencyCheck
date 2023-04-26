import time
from importlib import resources
import os.path
import sys

from typing import List

import constants
from constants import *

ifDebug: int

if __name__ == "__main__":
    import DebugMode
    ifDebug = DebugMode.DEBUGMODE_NORMAL
    for i in sys.argv:
        if i == '-enableGlobalDebug':
            ifDebug = DebugMode.DEBUGMODE_GDEBUG
            sys.argv.remove('-enableGlobalDebug')
            print(f'{LOGMODE_LOADING_OHEADER}Debug Mode is set to "Global Debug".')
        if i == '-enableDebug':
            ifDebug = DebugMode.DEBUGMODE_DEBUG
            sys.argv.remove('-enableDebug')
            print(f'{LOGMODE_LOADING_OHEADER}Debug Mode is set to "Debug".')
    DebugMode.initDefault_gmode(ifDebug)
    pass
from DebugMode import *
# initDefault_gmode(DEBUGMODE_GDEBUG)

from docs_helper import *
from common import *
from Mod import Mod

OHEADER_G = f'{os.path.relpath(__file__, basedir)}'
# print(__file__)

gmode = DebugMode(DEBUGMODE_GDEBUG, None)

toIgnore: bool
IgnoreList: list
isSetDir: bool
showLicense: str
onlyAbout: bool
forceMandatory: bool
displayVersionOnly: bool
GiveDoc_Name: str
DocLang: None
GiveDoc_PauseExit: bool
GiveDoc_SleepExit: int
ifChooseDoc: bool
devpause: bool

def main(filedir: str=None):
    OHEADER = f'{OHEADER_G}/main()'

    global gmode
    mode = DebugMode(DEBUGMODE_GDEBUG, gmode.mode)

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
    print(strings.ABOUT_CONTACTEMAIL + ': ' + CONTACT_EMAIL)
    return

def license_print():
    OHEADER = f'{OHEADER_G}/license_print()'
    mode = DebugMode(DEBUGMODE_GDEBUG, gmode.mode)

    if os.path.exists(LICENSE_PATH) is False:
        print_log(strings.LICENSE_FILE_MISSING)
        print_debug([strings.LICENSE_FILE_MISSING, LICENSE_PATH], OHEADER, mode.isDebug())

        if os.path.exists(LICENSE_PATH_NOT_BUILDED):
            # Now accept outer license file.
            print_log(strings.LICENSE_FROM_OUTER)
            filedir = LICENSE_PATH_NOT_BUILDED
        else:
            print_log(strings.LICENSE_FILE_MISSING)
            print_debug([strings.LICENSE_FILE_MISSING, LICENSE_PATH], OHEADER, mode.isDebug())
            return
    else:
        filedir = LICENSE_PATH

    with open(filedir, mode='r', encoding='utf-8') as file:
        content = file.read()
        print(content)
    return

def readmods_dir(filedir: str):
    # read mods from directory
    OHEADER = f'{OHEADER_G}/readmods_dir()'
    mode = DebugMode(DEBUGMODE_GDEBUG, gmode.mode)

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
                if toIgnore is True and dependencyinfo.modId in IgnoreList:
                    continue
                if dependencyinfo.modId not in modIds_lack_of:
                    if forceMandatory is True or dependencyinfo.mandatory is True:
                        modIds_lack_of.append(dependencyinfo.modId)
                flag = True
        if flag is True:
            mods_insufficient.append(mod)

    return [mods_insufficient, modIds_lack_of]

def processArgs(argv: list):
    # Manual
    # -toIgnore [true/false] -dir ["testres/"]

    OHEADER = f'{OHEADER_G}/processArgs()'
    mode = DebugMode(DEBUGMODE_GDEBUG, gmode.mode)

    print_debug(f'Args: {argv}', OHEADER, mode.isDebug())

    argv: List[str]
    argc = argv.__len__()
    retv = {}
    unset_args = []

    # 默认设置
    # 忽略默认
    retv['toIgnore'] = True
    retv['IgnoreList'] = ['forge', 'minecraft']
    retv['dir'] = 'testres/'
    retv['isSetDir'] = False
    retv['license'] = 'hide'
    retv['onlyAbout'] = False
    retv['forceMandatory'] = False
    retv['version'] = False
    retv['GiveDoc_Name'] = None
    retv['DocLang'] = None
    retv['GiveDoc_PauseExit'] = False
    retv['GiveDoc_SleepExit'] = 1
    retv['ChooseDoc'] = False
    retv['devpause'] = False

    flag = True
    i = None
    try:
        i = 1
        while i < argc:
            if argv[i] == '-toIgnore':
                if argv[i+1].lower() == 'false':
                    retv['toIgnore'] = False
                    i += 1
                elif argv[i + 1].lower() == 'true':
                    i += 1
            elif argv[i] == '-IgnoreList':
                s: str = argv[i+1].strip(' ')
                s = s[1:-1]
                l = s.split(sep=',')
                l = [x.strip('"\' ') for x in l]
                retv['IgnoreList'] = l
                i += 1
            elif argv[i] == '-dir':
                retv['dir'] = argv[i+1].strip('" ')
                retv['isSetDir'] = True
                i += 1
            elif argv[i] == '-license':
                retv['license'] = 'show'
            elif argv[i] == '-onlyAbout':
                retv['onlyAbout'] = True
            elif argv[i] == '-forceMandatory':
                retv['forceMandatory'] = True
            elif argv[i] == '--version':
                retv['version'] = True
            elif argv[i] == '-GiveDoc':
                if retv['GiveDoc_Name'] is None:
                    retv['GiveDoc_Name'] = []
                if i+1 < argc \
                        and not argv[i+1].startswith('-'):
                    retv['GiveDoc_Name'].append(argv[i+1])
                    i += 1
                else:
                    retv['GiveDoc_Name'].append(DEFAULT_DOC)
            elif argv[i] == '-DocLang':
                retv['DocLang'] = argv[i+1].strip('"\' ')
                i += 1
            elif argv[i] == '-GiveDoc_PauseExit':
                retv['GiveDoc_PauseExit'] = True
            elif argv[i] == '-GiveDoc_SleepExit':
                if i+1 < argc \
                        and not argv[i+1].startswith('-'):
                    if argv[i+1].isdigit():
                        retv['GiveDoc_SleepExit'] = eval(argv[i+1])
            elif argv[i] == '-ChooseDoc':
                retv['ChooseDoc'] = True
            elif argv[i] == '--devpause':
                retv['devpause'] = True
                if gmode.isDebug():
                    input('paused')
            else:
                flag = False
                unset_args.append(argv[i])
            i += 1
    except Exception as e:
        print(f'{LOGMODE_LOADING_OHEADER}ERROR when processing "{argv[i]}". ', end='')
        print(e)
        raise e

    if flag is False:
        print_debug(LOGMODE_LOADING_OHEADER+strings.ARGUMENTS_NOT_PROCESSED+unset_args.__str__(), OHEADER, mode.isDebug())
        if unset_args.__len__() == 1:
            s: str = unset_args[-1].strip('"\' ')
            retv['dir'] = s
            retv['isSetDir'] = True
    return retv

def applyArgs(args: dict):
    OHEADER = f'{OHEADER_G}/applyArgs()'
    mode = DebugMode(DEBUGMODE_NORMAL, gmode.mode)

    global toIgnore, IgnoreList, showLicense, isSetDir, onlyAbout, forceMandatory, displayVersionOnly,\
        GiveDoc_Name, DocLang, GiveDoc_PauseExit, GiveDoc_SleepExit, ifChooseDoc, devpause
    toIgnore = args.get('toIgnore')
    IgnoreList = args.get('IgnoreList')
    showLicense = args.get('license')
    isSetDir = args.get('isSetDir')
    onlyAbout = args.get('onlyAbout')
    forceMandatory = args.get('forceMandatory')
    displayVersionOnly = args.get('version')
    GiveDoc_Name = args.get('GiveDoc_Name')
    DocLang = args.get('DocLang')
    GiveDoc_PauseExit = args.get('GiveDoc_PauseExit')
    GiveDoc_SleepExit = args.get('GiveDoc_SleepExit')
    ifChooseDoc = args.get('ChooseDoc')
    devpause = args.get('devpause')
    return

def responseArgs():
    OHEADER = f'{OHEADER_G}/responseArgs()'
    mode = DebugMode(DEBUGMODE_GDEBUG, gmode.mode)

    constants.devpause = devpause

    if displayVersionOnly is True:
        print(APP_VERSION)
        sys.exit(0)

    if onlyAbout is True:
        # print('onlyAbout')
        about_print()
        sys.exit(0)

    if showLicense == 'show':
        # print('show license')
        # contents_bytes = resources.read_text(, 'LICENSE', encoding='UTF-8')
        # print(contents_bytes)
        license_print()
        pass

    if ifChooseDoc is True:
        GiveDoc_Guide()
        if GiveDoc_PauseExit:
            input('Paused, Enter to resume. ')
        else:
            time.sleep(GiveDoc_SleepExit)
        sys.exit(0)
    elif GiveDoc_Name is not None:
        global DocLang

        if DocLang is None:
            print_debug(f'Will use default first language in list.', OHEADER, mode.isDebug())
            DocLang = doc_langs[0]

        if DocLang not in doc_langs:
            if DocLang is not None:
                print_log(f'Doc language "{DocLang}" is not supported.')
            else:
                print_log(f'Doc language is None, which is unexpected to occur. Can\'t continue.')
        else:
            for Doc_Name in GiveDoc_Name:
                GiveDoc(Doc_Name, DocLang)
        if GiveDoc_PauseExit:
            input('Paused, Enter to resume. ')
        else:
            time.sleep(GiveDoc_SleepExit)
        sys.exit(0)

    if os.path.exists(filedir) is False:
        if isSetDir is True:
            print_log(strings.NO_FILEDIR)
            print_debug(strings.NO_FILEDIR + f'{strings.STR_FILEDIR}: [{filedir}]', OHEADER_G, gmode.isDebug())
            sys.exit(strings.NO_FILEDIR)
        else:
            sys.exit(0)
    elif os.listdir(filedir) == []:
        print_log(strings.EMPTY_FILELIST)
        print_debug(strings.EMPTY_FILELIST + f'{strings.STR_FILEDIR}: [{filedir}]', OHEADER_G, gmode.isDebug())
        sys.exit(strings.EMPTY_FILELIST)


if __name__ == "__main__":

    args: dict = processArgs(sys.argv)
    applyArgs(args)
    filedir = args.get('dir')

    # print('exists: ', os.path.exists(filedir))
    # print('isSetDir: ', isSetDir)

    responseArgs()

        # 忽略默认
    # toIgnore = True
    # IgnoreList = ['forge', 'minecraft']

    main(filedir)


