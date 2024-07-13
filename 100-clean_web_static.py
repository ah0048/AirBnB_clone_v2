#!/usr/bin/python3
"""
Deletes out-of-date archives,
using the function do_clean
"""
from fabric.api import *


env.hosts = ['100.26.53.100', '34.232.72.27']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/school'


def do_clean(number=0):
    ''' Removes out of date archives locally and remotely '''
    number = int(number)
    if number == 0:
        number = 2
    else:
        number += 1

    local('cd versions; ls -t | tail -n +{} | xargs rm -rf'
          .format(number))
    releases_path = '/data/web_static/releases'
    run('cd {}; ls -t | tail -n +{} | sudo xargs rm -rf'
        .format(releases_path, number))
