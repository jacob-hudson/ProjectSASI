#!/usr/bin/env python

import os
import re

def update_file(filename):
    return

def traverse_dirs(cwd):
    for root, directories, filenames in os.walk('.'):
        # for directory in directories:
        #     print os.path.join(root, directory), " is a dir"
        for filename in filenames:
             print os.path.join(root,filename), " is a file"

def main():

    # regexes
    heading = re.compile('[sai]')
    id = re.compile ('id = sai')
    html = re.compile ('action.sai')

    traverse_dirs('.')


if __name__ == '__main__':
    main()
