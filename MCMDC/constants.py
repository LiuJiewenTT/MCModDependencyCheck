import os.path as osp

LOGMODE_LOG_OHEADER = '[Log]: '
LOGMODE_DEBUG_OHEADER = '[Debug]: '
LOGMODE_LOADING_OHEADER = '[ProgramLoad]: '

basedir: str

try:
    # anything that has variable 'basedir' is ok, except assignment sentence.
    if basedir is None: pass;
except Exception as e:
    # print(e)
    basedir = osp.dirname(__file__)
    print(f'{LOGMODE_LOADING_OHEADER}Basedir is set to [{basedir}].')

APP_NAME = 'MCModDependencyCheck'
APP_NAME_DISPLAY = 'Minecraft Mod Dependency Check'
APP_NAME_ABBR = 'MCMDC'
APP_VERSION = '1.0.0'
AUTHORS = ['LiuJiewenTT']
CONTACT_EMAIL = 'liuljwtt@163.com'
PROJECT_LINK = 'https://github.com/LiuJiewenTT/MCModDependencyCheck'
LICENSE = 'GPL-3.0'

# target_path = 'META-INF/mods.toml'

RETV_ERROR = -1

LICENSE_FILENAME = 'LICENSE'
LICENSE_PATH = osp.join(basedir, LICENSE_FILENAME)
LICENSE_PATH_NOT_BUILDED = osp.join(osp.join(basedir, '..'), LICENSE_FILENAME)


# # filename_constants = 'constants.py'
# try:
#     PROJDIR = PROJDIR
# except:
#     PROJDIR:str = osp.dirname(__file__)
#     # PROJDIR = PROJDIR.replace(filename_constants, '')
#     print(PROJDIR)

PART_LOCATOR = '[[dependencies.'
VERSION_REDIRECTED_SIGN = '${file.jarVersion}'