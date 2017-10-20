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
    excluded_files = ['build.py', 'build_all.sh', '.travis.yml', 'README.md']
    for root, _, filenames in os.walk('.'):
        for filename in filenames:
            if filename in excluded_files or os.path.join(root,filename).split('/')[1] == ".git":
                continue
            else:
                update_file(os.path.join(root,filename))

def main():
    traverse_dirs('.')


if __name__ == '__main__':
    main()
