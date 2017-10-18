#!/usr/bin/env python

import os
import re

def update_file(filename):

    f = open(filename, 'r')

    content = f.read()
    f.close()
    f = open(filename, 'w')

    content = re.sub('id = sai','id = slack', content)
    content = re.sub('[sai]','[slack]', content)
    content = re.sub('action.sai','action.slack', content)

    f.write(content)
    f.close()

    return

def traverse_dirs(cwd):
    for root, directories, filenames in os.walk('.'):
        # for directory in directories:
        #     print os.path.join(root, directory), " is a dir"
        for filename in filenames:
             update_file(filename)

def main():

    traverse_dirs('.')


if __name__ == '__main__':
    main()
