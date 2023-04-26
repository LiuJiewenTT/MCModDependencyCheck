import sys
from MCMDC.constants import *

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
    DebugMode.initDefault_gmode(ifDebug)
    pass
from MCMDC.DebugMode import *
# initDefault_gmode(DEBUGMODE_GDEBUG)

from MCMDC import *