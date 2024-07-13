#!/usr/bin/python3
'''Fabric script that distributes an archive to your web servers'''
from fabric.api import *
import os
from datetime import datetime


env.hosts = ['100.26.53.100', '34.232.72.27']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/school'


@task
def do_pack():
    '''function to archive'''
    directory = 'versions'
    dir_to_archive = 'web_static'
    time = datetime.now().strftime('%Y%m%d%H%M%S')
    archive_name = f'{dir_to_archive}_{time}.tgz'
    try:
        local(f'mkdir -p {directory}')
        local(f'tar czf {directory}/{archive_name} {dir_to_archive}')
        path = f'{directory}/{archive_name}'
        return path
    except Exception:
        return None


@task
def do_deploy(archive_path):
    '''function to deploy'''
    if not os.path.exists(archive_path):
        return False
    try:
        put(archive_path, '/tmp/')
        archive_name = os.path.basename(archive_path)
        exctraction_name = archive_name.split('.')[0]
        run(f'sudo tar -xzf /tmp/{archive_name} -C /data/web_static/releases')
        run('cd /data/web_static/releases')
        old_path = '/data/web_static/releases/web_static'
        new_path = f'/data/web_static/releases/{exctraction_name}'
        run(f'sudo mv {old_path} {new_path}')
        run(f'sudo rm -r /tmp/{archive_name}')
        run('sudo rm /data/web_static/current')
        run(f'sudo ln -s {new_path} /data/web_static/current')
        return True

    except Exception:
        return False
