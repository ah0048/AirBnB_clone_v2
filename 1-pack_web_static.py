#!/usr/bin/python3
'''Fabric script that generates a .tgz archive of the web_static'''
from fabric.api import *
from datetime import datetime


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
