import os.path as osp

APP_NAME = 'MCModDependencyCheck'
APP_NAME_DISPLAY = 'Minecraft Mod Dependency Check'
APP_NAME_ABBR = 'MCMDC'
APP_VERSION = '1.0.0'
AUTHORS = ['LiuJiewenTT']
PROJECT_LINK = 'https://github.com/LiuJiewenTT/MCModDependencyCheck'
LICENSE = 'GPL-3.0'
LICENSE_PATH = 'LICENSE'

LOGMODE_LOG_OHEADER = '[Log]: '
LOGMODE_DEBUG_OHEADER = '[Debug]: '
LOGMODE_LOADING_OHEADER = '[ProgramLoad]: '
# target_path = 'META-INF/mods.toml'

RETV_ERROR = -1

basedir: str

try:
    # anything that has variable 'basedir' is ok, except assignment sentence.
    if basedir is None: pass;
except Exception as e:
    # print(e)
    basedir = osp.dirname(__file__)
    print(f'{LOGMODE_LOADING_OHEADER}Basedir is set to [{basedir}].')


# # filename_constants = 'constants.py'
# try:
#     PROJDIR = PROJDIR
# except:
#     PROJDIR:str = osp.dirname(__file__)
#     # PROJDIR = PROJDIR.replace(filename_constants, '')
#     print(PROJDIR)

PART_LOCATOR = '[[dependencies.'
VERSION_REDIRECTED_SIGN = '${file.jarVersion}'