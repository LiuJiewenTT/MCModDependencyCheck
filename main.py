import zipfile
import os

import constants
from constants import *
import strings
from common import *

OHEADER_G = f'{os.path.basename(__file__)}'

def main():
    OHEADER = f'{OHEADER_G}/main()'
    filedir = 'testres/'
    filelist = os.listdir(filedir)

    # print(filelist)

    for filename in filelist:
        # do something
        pass

    # temp filename
    filename = 'mcvine_wat_1.18.2_0.1.2.jar'
    path_zip = os.path.join(filedir, filename)
    print_log(path_zip)

    with zipfile.ZipFile(path_zip, mode='r') as file_zip:
        path_target = zipfile.Path(file_zip, at=target_path)
        if( path_target.exists() ):
            print_log(strings.TARGET_FOUNDED)
        else:
            return [ RETV_ERROR , strings.FILE_NOT_FOUND + constants.target_path ]

        with path_target.open(mode='r') as file_target:
            content_bytes = file_target.read()
            content_str = str(content_bytes)
            # print_debug(lines[0].__class__, OHEADER)
            # print_debug(lines, OHEADER)
            # for i in lines:
            #     print_debug(i, OHEADER)
            print_debug(content_str, OHEADER)

            parts = getPart(content_str)
            print_debug(parts, OHEADER)

        pass



if __name__ == "__main__":
    main()