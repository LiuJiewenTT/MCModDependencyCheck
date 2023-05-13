import difflib
import os
import sys
import time

import shlex

import psutil

from MCMDC.constants import *
from MCMDC import strings
from MCMDC.DebugMode import *
from MCMDC.common import print_log, print_debug
# from main import devpause
devpause: bool

OHEADER_G = f'{os.path.relpath(__file__, basedir)}'
gmode = DebugMode(DEBUGMODE_GDEBUG, None)

reserved_docNames = {'Manual': 'Manual'}
doc_langs = ['en-us', 'zh-cn']

# If you want to trust "./...", don't just write "..." but "./..." instead.
trusted_docExecutors = ['notepad.exe']
env_trusted_paths: list
env_trusted_paths_win32: list
env_trusted_paths_unix: list


def __moreimport__(slient: bool=False):
    OHEADER = f'{OHEADER_G}/__moreimport__()'
    mode = DebugMode(DEBUGMODE_GDEBUG, gmode.mode)

    global devpause
    from . import constants
    if 'devpause' not in vars() and 'devpause' in vars(constants):
        from .constants import devpause
        print_debug('devpause is imported.', OHEADER, mode.isDebug() and not slient)
        # input('imp')
        # devpause = main.devpause
    print_debug(['devpause' not in vars(), 'devpause' in vars(constants)], OHEADER, mode.isDebug(False))


def env_trusted_paths_win32_init():
    global env_trusted_paths_win32
    env_trusted_paths_win32 = []
    env_trusted_paths_win32.append(osp.join(os.getenv('windir'), 'system32'))


def env_trusted_paths_unix_init():
    global env_trusted_paths_unix
    env_trusted_paths_unix = []


def env_trusted_paths_init():
    global env_trusted_paths
    # try:
    #     if env_trusted_paths is not None: pass
    # except Exception as e:
    if 'env_trusted_paths' not in vars():
        if sys.platform == 'win32':
            env_trusted_paths_win32_init()
            env_trusted_paths = env_trusted_paths_win32
        else:
            env_trusted_paths_unix_init()
            env_trusted_paths = env_trusted_paths_unix
        # print(env_trusted_paths)


env_trusted_paths_init()


def yieldDocName(doc: str):
    ext = []
    ext_md = ['.md', '.markdown']
    ext_text = ['.txt', '.log']
    ext.extend(ext_md)
    ext.extend(ext_text)

    retv = doc
    yield retv
    for i in ext:
        retv = doc + i
        yield retv

def GetActualDocName(doc: str):
    OHEADER = f'{OHEADER_G}/GetActualDocName()'
    mode = DebugMode(DEBUGMODE_GDEBUG, gmode.mode)

    # if osp.exists(doc):
    #     return doc
    for name in yieldDocName(doc):
        print_debug(name, OHEADER, mode.isDebug())
        if osp.exists(name):
            return name
    # Leave it
    print_debug('Cannot get actual doc name. Return: "{name}"'.format(name=doc), OHEADER, mode.isDebug())
    return doc


def GetActualExecutorName(executor: str, locator=None):
    OHEADER = f'{OHEADER_G}/GetActualExecutorName()'
    mode = DebugMode(DEBUGMODE_GDEBUG, gmode.mode)

    __moreimport__(slient=True)

    if sys.platform == 'win32':
        priority_list = ['.com', '.exe', '.bat']
        if osp.splitext(executor)[-1] in priority_list:
            return executor
        for i in priority_list:
            te = executor + i
            if locator is not None:
                if mode.isDebug() and devpause:
                    print_debug(locator)
                    input('paused')
                te2 = locator(te)
                print_debug(f'Locator retv: {te2}', OHEADER, mode.isDebug())
                if te2 is None:
                    te2 = te
                else:
                    te2 = osp.join(te2, te)
                if mode.isDebug() and devpause:
                    input('paused')
            else:
                te2 = te
            if osp.exists(te2):
                return te
        # No legal executable name.
        return executor
    else:
        return executor


def LocateExecutor(executor: str):
    OHEADER = f'{OHEADER_G}/LocateExecutor()'
    mode = DebugMode(DEBUGMODE_GDEBUG, gmode.mode)

    retv = None
    if osp.exists(executor):
        retv = osp.dirname(osp.normpath(executor))
        return retv
    paths_str = os.getenv('PATH')
    # if sys.platform == 'win32':
    #     paths = paths_str.split(';')
    # else:
    #     paths = paths_str.split(':')
    paths = paths_str.split(osp.pathsep)
    # print_debug(paths)
    paths.extend(env_trusted_paths)
    # print_debug(paths)
    for path_i in paths:
        tp = GetActualExecutorName(osp.join(path_i, executor))
        if osp.exists(tp):
            print_debug(tp, OHEADER, mode.isDebug())
            retv = path_i
            break
    return retv


def GiveDoc(file: str, lang: str = 'en-us', executor: str = 'start', startOptions: list = [], disableReserves: bool = False):
    OHEADER = f'{OHEADER_G}/GiveDoc()'
    mode = DebugMode(DEBUGMODE_GDEBUG, gmode.mode)

    __moreimport__()

    # if isBuilt and BuildType == BuildTypeDirectory:
    #     librarydir = basedir_folder
    # else:
    #     librarydir = basedir
    librarydir = basedir

    if isBuilt:
        filepath = os.path.join(librarydir, 'docs')
    else:
        filepath = os.path.join(librarydir, '..', 'docs')
        filepath = os.path.normpath(filepath)

    print_debug(file, enabled=False)

    if disableReserves is False:
        if file in reserved_docNames.keys():
            print_debug('Filename is reserved. Replace it with: {newfilename}'
                        .format(newfilename=reserved_docNames[file]), OHEADER, mode.isDebug())
            file = reserved_docNames[file]

    file_ActualName = GetActualDocName(osp.join(filepath, lang, file))
    # print_debug('Actual Doc Name: {name}'.format(name=file_ActualName), OHEADER, mode.isDebug())

    if not file_ActualName.endswith(file):
        file_ext = osp.splitext(file_ActualName)[-1]
        file = file + file_ext
        print_debug('Found file with expansion mode: {file}. '.format(file=file), OHEADER, mode.isDebug())

    print_log(f'Document: {file}')
    print_log(f'Doc Lang: {lang}')

    filepath = os.path.join(filepath, lang, file)
    if not os.path.exists(filepath):
        print_log(strings.ERROR_FILE_NOT_FOUND + f'File Path: "{filepath}".')
        return False
    else:
        executor = executor.strip(' ')
        # Basic Security Examination
        if executor != 'start':
            if executor.find('start ') == 0:
                executor_untrusted = executor.partition('start ')[-1]
            else:
                executor_untrusted = executor
            executor_untrusted = GetActualExecutorName(executor_untrusted.strip('"'), locator=LocateExecutor)
            if mode.isDebug() and devpause:
                input('paused')
            if osp.exists(executor_untrusted) and osp.basename(executor_untrusted) == executor_untrusted:
                executor_untrusted = osp.join('.', executor_untrusted)
            if executor_untrusted not in trusted_docExecutors:
                print_log(strings.DOCSHELPER_GIVEDOC_WARN_UNTRUSTED_EXECUTOR.format(executor=executor_untrusted))
                # May apply basic security examination here in the future.
            else:
                print_log(strings.DOCSHELPER_GIVEDOC_EXECUTOR_CHANGED_TRUSTED.format(executor=executor_untrusted))
            executor_dir = LocateExecutor(executor_untrusted)
            if executor_dir is None:
                print_log('Executor cannot be located. ')
                if sys.platform == 'win32':
                    print_debug('Executor cannot be located. '
                                + 'You may check with "{command}"'
                                .format(command='echo %PATH% | findstr "{executor}"'
                                        .format(executor=osp.basename(executor_untrusted))),
                                OHEADER, mode.isDebug())
                else:
                    print_debug('Executor cannot be located. '
                                + 'You may check with "{command}"'
                                .format(command='echo $PATH | grep "{executor}"'
                                        .format(executor=osp.basename(executor_untrusted))),
                                OHEADER, mode.isDebug())
                return False
            elif executor_dir not in env_trusted_paths:
                print_log(strings.DOCSHELPER_EXECUTOR_NOT_IN_TRUSTED_LOCATION.format(executor_dir=executor_dir))
            else:
                print_log('Executor located at (trusted)"{place}". '.format(place=executor_dir))

        if executor.lstrip(' ').find('start') == 0:
            if sys.platform == 'win32':
                executor = executor.replace('start', 'cmd.exe /c start', 1)
            else:
                executor = executor.replace('start', 'sh', 1)

        # command = f'{executor} {filepath}'
        # for i in startOptions:
        #     command += f' {i}'
        if startOptions != [] and startOptions is not None:
            option_str = shlex.join(startOptions)
        else:
            option_str = ''
        command = f'{executor} {option_str} {filepath}'
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
    return True


def GiveDoc_Guide():
    __moreimport__()

    # print_debug(env_trusted_paths)
    # print_debug(env_trusted_paths_win32)
    # print_debug(env_trusted_paths_unix)

    file = input('Please choose a file: ').strip('" ')
    lang = input('Please choose a language: ').strip('"\' ')
    executor = input('Please choose an executor: ').strip(' ')
    options_str = input('Please input options: ')
    options = shlex.split(options_str, posix=(sys.platform != 'win32'))
    retv = GiveDoc(file, lang, executor=executor, startOptions=options)
    if retv is False:
        print_log('GiveDoc Failed. ')
    else:
        print_log('GiveDoc Might Succeed. ')
