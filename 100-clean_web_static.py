#!/usr/bin/python3
'''Fabric script that deletes out-of-date archives'''
from fabric.api import *
import os
from datetime import datetime

env.hosts = ['100.26.53.100', '34.232.72.27']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/school'

@task
def do_clean(number=0):
    '''function to clean'''
    number = int(number)  # Convert number to integer

    # Clean local versions folder
    if number == 0 or number == 1:
        local('ls -ltr versions | head -n -1 | xargs -d "\n" rm -rf')
    else:
        local('ls -lt versions | tail -n +{} | xargs -d "\n" rm -rf'.format(number + 1))

    # Clean remote releases folder
    if number == 0 or number == 1:
        run('ls -ltr /data/web_static/releases | head -n -1 | xargs -d "\n" rm -rf')
    else:
        run('ls -lt /data/web_static/releases | tail -n +{} | xargs -d "\n" rm -rf'.format(number + 1))
