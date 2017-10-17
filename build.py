#!/usr/bin/env python

import os
import re

def traverse_dirs(cwd):


def main():

    # regexes
    heading = re.compile('[sai]')
    id = re.compile ('id = sai')
    html = re.compile ('action.sai')

    traverse_dirs('.')


if __name__ == '__main__':
    main()
