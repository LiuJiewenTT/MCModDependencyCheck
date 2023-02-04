## How to setup before using:
# import DebugMode
# DebugMode.initDefault_gmode(DebugMode.DEBUGMODE_GDEBUG)
## The command must be applied to every page:
# from DebugMode import *
## then is your codes...


DEBUGMODE_NORMAL = 0
DEBUGMODE_DEBUG = 1
DEBUGMODE_GDEBUG = 2

gmode_default: int

def initDefault_gmode(val: int):
    global gmode_default
    gmode_default = val

# This initialization method avoid modules that load in common sequence can read the default.
# But it only works when using 'from DebugMode import * ' sentence.

class DebugMode:
    mode: int
    gmode: int

    ## One example for use:
    #  page or class uses gmode and functions' DebugMode instances inherited from the gmode, stores in self.gmode.
    #  functions use mode
    #
    #  All mode instances affected by gmode_default
    #  Entrance of program uses init function to initialize gmode_default.

    def __init__(self, mode=DEBUGMODE_NORMAL, gmode=DEBUGMODE_NORMAL):
        global gmode_default
        self.mode = mode
        if gmode is None:
            self.gmode = gmode_default
        else:
            self.gmode = gmode

    def isDebug(self, opt=None):
        if opt is not None:
            return opt

        global gmode_default
        flag = False
        if gmode_default > 0:
            if self.gmode > 0:
                if self.mode > 0:
                    if self.mode == DEBUGMODE_DEBUG or self.gmode == DEBUGMODE_DEBUG or gmode_default == DEBUGMODE_DEBUG:
                        flag = True
        return flag
