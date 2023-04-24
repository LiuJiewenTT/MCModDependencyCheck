import os
from constants import *
import strings
from DebugMode import *
from common import print_log, print_debug

OHEADER_G = f'{os.path.relpath(__file__, basedir)}'
gmode = DebugMode(DEBUGMODE_GDEBUG, None)

reserved_docNames = {'Manual': 'Manual'}
doc_langs = ['en-us', 'zh-cn']

def GiveDoc(file: str, lang: str = 'en-us'):
    OHEADER = f'{OHEADER_G}/GiveDoc_Markdown()'
    mode = DebugMode(DEBUGMODE_GDEBUG, gmode.mode)
    print_log(f'Document: {file}')
    print_log(f'Doc Lang: {lang}')
    filepath = os.path.join('docs', '')
    filepath += os.path.join(lang, file)
    if not os.path.exists(filepath):
        print_log(strings.ERROR_FILE_NOT_FOUND + f'File Path: "{filepath}".')
    else:
        command = f'start {filepath}'
        os.system(command)
    pass

def GiveDoc_Guide():
    file = input('Please choose a file: ').strip('" ')
    lang = input('Please choose a language: ').strip('"\' ')
    GiveDoc(file, lang)
