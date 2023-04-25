import difflib
import os
import sys
import time

import path
import shlex, subprocess

import psutil

from constants import *
import strings
from DebugMode import *
from common import print_log, print_debug
# from main import devpause
devpause: bool

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

def __moreimport__():
    OHEADER = f'{OHEADER_G}/__moreimport__()'
    mode = DebugMode(DEBUGMODE_GDEBUG, gmode.mode)

    global devpause
    import constants
    if 'devpause' not in vars() and 'devpause' in vars(constants):
        from constants import devpause
        print_debug('devpause is imported.', OHEADER, mode.isDebug())
        # input('imp')
        # devpause = main.devpause
    print_debug(['devpause' not in vars(), 'devpause' in vars(constants)], OHEADER, mode.isDebug(False))


def LocateExecutor(executor: str):
    paths_str = os.getenv('PATH')
    if sys.platform == 'win32':
        paths = paths_str.split(';')
    else:
        paths = paths_str.split(':')
    retv = None
    # Here needs more operations.
    for path in paths:
        if osp.exists(osp.join(path, executor)):
            retv = path
            break
    return retv


def GiveDoc(file: str, lang: str = 'en-us', executor: str = 'start', startOptions: list = []):
    OHEADER = f'{OHEADER_G}/GiveDoc()'
    mode = DebugMode(DEBUGMODE_GDEBUG, gmode.mode)

    __moreimport__()

    print_log(f'Document: {file}')
    print_log(f'Doc Lang: {lang}')
    if isBuilt:
        filepath = os.path.join(basedir, 'docs')
    else:
        filepath = os.path.join(basedir, '..', 'docs')
        filepath = os.path.normpath(filepath)
    filepath = os.path.join(filepath, lang, file)
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
        # os.system(command)
        # sp_ret = subprocess.run(command, shell=True)
        # sp_ret = subprocess.call(command, shell=True)


        # sp_args = shlex.split(command, posix=(os.name=='posix'))
        # print_debug(sp_args, OHEADER, mode.isDebug())
        sp_args = command
        # sp = subprocess.Popen(sp_args)
        # sp_info = psutil.Process(sp.pid)
        sp = psutil.Popen(sp_args)
        sp.suspend()
        sp_info = sp
        if mode.isDebug() and devpause:
            input('paused')

        timeout_basic = 5
        timeout_extended = 0
        timeout_incrementStep = 1
        send_started = False
        file_opened = False
        send_ok_certainly = False
        len_pre = len_now = 0
        oflist_names = []
        oflist_names_pre = []
        differ = difflib.Differ()
        t0 = time.time()
        while (not send_started or file_opened):
            # print_debug('read states')
            try:
                oflist = [list(x) for x in sp_info.open_files()]
                if sp.status() == 'stopped':
                    sp.resume()
                    pass
            except psutil.NoSuchProcess as pnsp:
                print_log('The process is stopped. (pid={pid})'.format(pid=sp_info.pid))
                break
            len_now = oflist.__len__()
            if len_now != len_pre:
                print_debug('Process Supervisor: new count: {pre}=>{now}.'
                            .format(pre=len_pre, now=len_now), OHEADER, mode.isDebug())
                if len_now > len_pre and len_pre:
                    timeout_extended += timeout_incrementStep
            if mode.isDebug():
                oflist_names = [x[0] for x in oflist]
                difflist = list(differ.compare(oflist_names_pre, oflist_names))
                for item in difflist:
                    if item[0] != ' ':
                        print_debug('difflist: {item}'.format(item=item), OHEADER, mode.isDebug())

            for item in oflist:
                # print(filepath, item)
                if filepath in item:
                    print_debug(oflist, OHEADER, mode.isDebug())
                    file_opened = True
                    send_started = True
                elif send_started:
                    file_opened = False
            # time.sleep(0.1)
            len_pre = len_now
            if mode.isDebug():
                oflist_names_pre = oflist_names
            if time.time() - t0 >= timeout_basic + timeout_extended:
                print_log('Process Supervision timeout: Over {timeout} seconds. '.format(timeout=timeout_basic+timeout_extended))
                print_debug('Process Supervision timeout: Over {timeout_basic}+{timeout_extended} seconds. '
                          .format(timeout_basic=timeout_basic, timeout_extended=timeout_extended), OHEADER, mode.isDebug())
                break
        # sp.kill() # Should not kill unless it is suspended.
        if sp.is_running() and sp.status() == 'stopped':
            print_log('Kill suspended subprocess. (pid={pid}'.format(pid=sp.pid))
            sp.kill()

        if send_started is True and file_opened is False:
            # When send_ok_certainly is False, it doesn't mean a failure.
            send_ok_certainly = True
    pass


def GiveDoc_Guide():
    __moreimport__()

    file = input('Please choose a file: ').strip('" ')
    lang = input('Please choose a language: ').strip('"\' ')
    executor = input('Please choose an executor: ').strip('" ')
    GiveDoc(file, lang, executor=executor)
