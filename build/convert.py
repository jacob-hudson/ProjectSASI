#!/usr/bin/env python

import os
import re

def update_file(filename):
    f = open(filename, 'r')
    content = f.read()
    f.close()
    f = open(filename, 'w')

    if filename == '../default/alert_actions.conf':
        content = re.sub('\[sai\]','[slack]', content)
    elif filename == '../default/app.conf':
        content = re.sub('id = sai','id = slack', content)
    elif filename == '../default/restmap.conf' or filename == '../default/data/ui/alerts/sai.html':
        content = re.sub('action.sai','action.slack', content)
    elif filename == '../default/setup.xml':
        content = re.sub('sai','slack', content)
    else:
        pass

    f.write(content)
    f.close()

    return

def traverse_dirs(cwd):
    excluded_files = ['build.py', 'build_all.sh', '.travis.yml', 'README.md']
    for root, _, filenames in os.walk('../'):
        for filename in filenames:
            if filename in excluded_files or os.path.join(root,filename).split('/')[1] == ".git":
                continue
            else:
                update_file(os.path.join(root,filename))
                if os.path.join(root,filename) == '../bin/sai.py' or os.path.join(root,filename) == '../default/data/ui/alerts/sai.html':
                    if os.path.join(root,filename) == '../bin/sai.py':
                         os.rename('../bin/sai.py','../bin/slack.py')
                    else:
                         os.rename('../default/data/ui/alerts/sai.html','../default/data/ui/alerts/slack.html')

def main():
    traverse_dirs('.')


if __name__ == '__main__':
    main()
