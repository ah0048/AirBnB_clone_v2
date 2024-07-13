#!/usr/bin/python3
'''Fabric script that creates and distributes an archive to your web servers'''
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
        local(f'tar cvzf {directory}/{archive_name} {dir_to_archive}')
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
        destination = f'/data/web_static/releases/{exctraction_name}'
        run(f'mkdir -p {destination}')
        run(f'sudo tar -xzf /tmp/{archive_name} -C {destination}')
        run(f'sudo rm /tmp/{archive_name}')
        run(f'sudo mv {destination}/web_static/* {destination}')
        run(f'sudo rm -rf {destination}/web_static')
        run('sudo rm -rf /data/web_static/current')
        run(f'sudo ln -s {destination} /data/web_static/current')
        print('New version deployed!')
        return True

    except Exception:
        return False


@task
def deploy():
    '''function to pack & deploy'''
    archive_path = do_pack()
    if not os.path.exists(archive_path):
        return False
    result = do_deploy(archive_path)
    return result
