# -*- coding: utf-8 -*-
import pwd
import os
from pathlib import Path


def get_username():
    return pwd.getpwuid(os.getuid())[0]


def get_home_dir():
    return str(Path.home())


##  find the complete path for a file
#
#   return value is usually str, but any value can
#   be returned as specified in not_found
def find_file_path(
    filename: str,
    rootpath: str,
    path_only: bool = False,
    not_found='{filename} not found in {rootpath}',
    verbose=False
) -> str:

    if rootpath.startswith('~'):
        rootpath = get_home_dir() + rootpath[1:]

    for root, dirs, files in os.walk(rootpath):
        if verbose:
            print(root)
        for name in files:
            if name == filename:
                if path_only:
                    return root
                return os.path.join(root, filename)

    return not_found.format(
        filename=filename,
        rootpath=rootpath)
