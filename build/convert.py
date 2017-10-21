#!/usr/bin/env python

import os
import re

def update_file(filename):
    f = open(filename, 'r')
    content = f.read()
    f.close()
    f = open(filename, 'w')

    if filename == './sai/default/alert_actions.conf':
        content = re.sub('\[sai\]','[slack]', content)
    elif filename == './sai/default/app.conf':
        content = re.sub('id = sai','id = slack', content)
    elif filename == './sai/default/restmap.conf' or filename == './sai/default/data/ui/alerts/sai.html':
        content = re.sub('action.sai','action.slack', content)
    elif filename == './sai/default/setup.xml':
        content = re.sub('sai','slack', content)
    else:
        pass

    f.write(content)
    f.close()

    return

def traverse_dirs(cwd):
    excluded_files = ['build.py', 'build_all.sh', '.travis.yml', 'README.md']
    for root, _, filenames in os.walk('./sai/'):
        for filename in filenames:
            if filename in excluded_files or os.path.join(root,filename).split('/')[1] == ".git":
                continue
            else:
                update_file(os.path.join(root,filename))
                if os.path.join(root,filename) == './sai/bin/sai.py' or os.path.join(root,filename) == './sai/default/data/ui/alerts/sai.html':
                    if os.path.join(root,filename) == './sai/bin/sai.py':
                         os.rename('./sai/bin/sai.py','./sai/bin/slack.py')
                    else:
                         os.rename('./sai/default/data/ui/alerts/sai.html','./sai/default/data/ui/alerts/slack.html')

def main():
    traverse_dirs('.')
    os.rename('sai','slack')


if __name__ == '__main__':
    main()
