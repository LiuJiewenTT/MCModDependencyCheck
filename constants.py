import os.path as osp

LOGMODE_LOG_OHEADER = '[Log]: '
LOGMODE_DEBUG_OHEADER = '[Debug]: '
LOGMODE_LOADING_OHEADER = '[ProgramLoad]: '
target_path = 'META-INF/mods.toml'

RETV_ERROR = -1

basedir: str

try:
    assert basedir is not None
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