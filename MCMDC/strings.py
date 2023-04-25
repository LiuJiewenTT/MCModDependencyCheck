import constants

strings_loaded: bool
# try:
#     if strings_loaded is not None: pass
# except Exception as e:
#     strings_loaded = False
if 'strings_loaded' not in vars():
    strings_loaded = False

if strings_loaded is not True:
    strings_loaded = True

    # About section
    ABOUT_TITLE = 'About Software'
    ABOUT_PROJECT = 'Project'
    ABOUT_AUTHORS = 'Authors'
    ABOUT_PROJECTLINK = 'Project Link'
    ABOUT_LICENSE = 'License'
    ABOUT_VERSION = 'Version'
    ABOUT_CONTACTEMAIL = 'Contact Email'

    # Document section
    DOCS_MANUAL = 'Manual'

    # other
    CURRENT_FILE_PREFIX = 'Current file: '
    TARGET_FOUNDED = f'Target file exists. '
    ERROR_FILE_NOT_FOUND = 'ERROR! File not found. '
    NO_MORE_PARTS = 'End search for parts. No more parts. '
    CONTENT_INCOMPLETED = 'Something not matched. Content has some problem. '
    INTERVAL_NOT_EXIST = 'The interval does not exist. '
    NO_MORE_ITEM = 'End search for items. No more items. '
    ERROR_NO_NONNEGATIVE_VALUE = 'ERROR! No value is NON-NEGATIVE. '
    INFO_NOT_MOD = 'The infotype is not \'mods\'. '
    CREATE_MODINFO = 'ModInfo instance is created. '
    VALUETYPE_ERROR = 'Not expected value type found. '
    MEET_PURE_END = 'Meet a \'pure\' end, no \'\\r\' or \'\\n\'. '
    ON_THE_RIGHT = ': on the right side. '
    ON_THE_LEFT = ': on the left side. '
    CNT_DEPENDENCIES_1 = 'Count of dependencies: '
    CNT_DEPENDENCIES_REAL = 'Count of dependencies(real): '
    UNEXPECTED_MANDATORY_VALUE = 'The value of \'mandatory\' is not expected. '
    NO_OTHERINFO_NOW = 'No otherInfo now. '
    NO_FILEDIR = 'No filedir. '
    NO_FILENAME = 'No filename. '
    WORKING_ON_OTHERINFO = 'Working on otherinfo. '
    WORKING_ON_MODINFO = 'Working on modinfo. '
    WORKING_ON_DEPENDENCYINFO = 'Working on dependencyinfo. '
    MOD_READINFO_DONE = 'This mod\'s info has been read. Done. '
    MOD_READINFO_DONE_1 = 'This mod\'s info has been read(part1). Done. '
    MOD_READINFO_DONE_2 = 'This mod\'s info has been read(part2). Done. '
    VERSION_REDIRECTED = 'Version string is redirected. '
    CURRENT_VERSION_VALUE = 'Current value of version: '
    CORRECTED_VERSION_VALUE = 'Corrected value of version: '
    WRONG_EDGESIGN_OF_INTERVAL = 'The interval\'s edge has wrong sign. '
    EMPTY_VERSIONRANGE = 'The versionRange is empty. '
    MODS_INSUFFICIENT = 'Some mods are insufficient. '
    MODS_LACK_OF = 'Some mods are missing. '
    MODPACK_READY = 'OK! This modpack is ready to go. '
    EMPTY_FILELIST = 'The list of files is empty. '
    STR_FILEDIR = 'File directory'
    LICENSE_FILE_MISSING = 'The file of license is missing. '
    LICENSE_FROM_OUTER = 'The License is from outer and please check the content yourself! '
    ARGUMENTS_NOT_PROCESSED = 'The arguments not processed: '
    DOCSHELPER_GIVEDOC_OPENING = 'Giving Document...'

    # other(to be formatted)
    DOCSHELPER_GIVEDOC_OPENING_DEBUG = 'Giving Document with command: [{command}]'
    DOCSHELPER_GIVEDOC_WARN_UNTRUSTED_EXECUTOR = 'Warning: GiveDoc executor is changed to "{executor}"(not trusted).'
    DOCSHELPER_GIVEDOC_EXECUTOR_CHANGED_TRUSTED = 'GiveDoc will execute with "{executor}".'
    DOCSHELPER_EXECUTOR_NOT_IN_TRUSTED_LOCATION = 'Warning: executor is not in trusted location: [{executor_dir}]'

