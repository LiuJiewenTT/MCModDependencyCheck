import sys
import os.path as osp
import MCMDC
from MCMDC.constants import *
# if isBuilt:
#     MCMDC.constants.basedir = basedir = osp.normpath(osp.join(basedir, '..'))
#     print(f'{LOGMODE_LOADING_OHEADER}Basedir is set to [{basedir}].')
# LOGMODE_LOADING_OHEADER = '[ProgramLoad]: '

if __name__ == "__main__":
    from MCMDC import DebugMode
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
    MCMDC.DebugMode.initDefault_gmode(ifDebug)
    pass
# initDefault_gmode(DEBUGMODE_GDEBUG)

print(f'{LOGMODE_LOADING_OHEADER}Haven\'t import all.')
# sys.path.append(osp.normpath(osp.join(osp.dirname(__file__), 'MCMDC')))
from MCMDC.pkg_init import *
# import MCMDC
# from MCMDC import *
print(f'{LOGMODE_LOADING_OHEADER}Import all done.')
from MCMDC.DebugMode import *

# print(globals())

if __name__ == "__main__":

    args: dict = main.processArgs(sys.argv)
    main.applyArgs(args)
    main.filedir = args.get('dir')

    # print('exists: ', os.path.exists(filedir))
    # print('isSetDir: ', isSetDir)

    main.responseArgs()

    # 忽略默认
    # toIgnore = True
    # IgnoreList = ['forge', 'minecraft']

    main.main(main.filedir)