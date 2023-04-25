import os
import sys
import path

from constants import *
import strings
from DebugMode import *
from common import print_log, print_debug

OHEADER_G = f'{os.path.relpath(__file__, basedir)}'
gmode = DebugMode(DEBUGMODE_GDEBUG, None)

reserved_docNames = {'Manual': 'Manual'}
doc_langs = ['en-us', 'zh-cn']
trusted_docExecutors = ['notepad.exe']
env_trusted_paths: list
env_trusted_paths_win32 = ['C:\\windows\\system32', ]
env_trusted_paths_unix = []

# try:
#     if env_trusted_paths is not None: pass
# except Exception as e:
if 'env_trusted_paths' not in vars():
    if sys.platform == 'win32':
        env_trusted_paths = env_trusted_paths_win32
    else:
        env_trusted_paths = env_trusted_paths_unix


def LocateExecutor(executor: str):
    paths_str = os.getenv('PATH')
    if sys.platform == 'win32':
        paths = paths_str.split(';')
    else:
        paths = paths_str.split(':')
    retv = None
    for path in paths:
        if osp.exists(osp.join(path, executor)):
            retv = path
            break
    return retv


def GiveDoc(file: str, lang: str = 'en-us', executor: str = 'start', startOptions: list = []):
    OHEADER = f'{OHEADER_G}/GiveDoc()'
    mode = DebugMode(DEBUGMODE_GDEBUG, gmode.mode)
    print_log(f'Document: {file}')
    print_log(f'Doc Lang: {lang}')
    if isBuilt:
        filepath = os.path.join(basedir, 'docs', '')
    else:
        filepath = os.path.join(basedir, '..', 'docs', '')
    filepath += os.path.join(lang, file)
    if not os.path.exists(filepath):
        print_log(strings.ERROR_FILE_NOT_FOUND + f'File Path: "{filepath}".')
    else:
        # Basic Security Examination
        if executor != 'start':
            if executor.strip(' ').find('start ') == 0:
                executor_untrusted = executor.partition('start ')[-1]
            else:
                executor_untrusted = executor
            if executor_untrusted not in trusted_docExecutors:
                print_log(strings.DOCSHELPER_GIVEDOC_WARN_UNTRUSTED_EXECUTOR.format(executor=executor_untrusted))
                # May apply basic security examination here in the future.
            else:
                print_log(strings.DOCSHELPER_GIVEDOC_EXECUTOR_CHANGED_TRUSTED.format(executor=executor_untrusted))
            executor_dir = LocateExecutor(executor_untrusted)
            if executor_dir not in env_trusted_paths:
                print_log(strings.DOCSHELPER_EXECUTOR_NOT_IN_TRUSTED_LOCATION.format(executor_dir=executor_dir))

        command = f'{executor} {filepath}'
        for i in startOptions:
            command += f' {i}'
        print_log(strings.DOCSHELPER_GIVEDOC_OPENING)
        print_debug(strings.DOCSHELPER_GIVEDOC_OPENING_DEBUG.format(command=command), OHEADER, mode.isDebug())
        os.system(command)
    pass


def GiveDoc_Guide():
    file = input('Please choose a file: ').strip('" ')
    lang = input('Please choose a language: ').strip('"\' ')
    executor = input('Please choose an executor: ').strip('" ')
    GiveDoc(file, lang, executor=executor)
