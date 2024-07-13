#!/usr/bin/python3
'''Fabric script that distributes an archive to your web servers'''
from fabric.api import *
import os


env.hosts = ['100.26.53.100', '34.232.72.27']



def do_deploy(archive_path):
    '''function to deploy'''
    if not os.path.exists(archive_path):
        return False
    try:
        for host in env.hosts:
            put(archive_path, '/tmp/')
            archive_name = os.path.basename(archive_path)
            exctraction_name = archive_name.split('.')[0]
            run(f'sudo tar -xzf /tmp/{archive_name} -C /data/web_static/releases')
            run('cd /data/web_static/releases')
            run(f'mv /data/web_static/releases/web_static /data/web_static/releases/{exctraction_name}')
            run(f'sudo rm -r /tmp/{archive_name}')
            run('sudo rm /data/web_static/current')
            run(f'sudo ln -s /data/web_static/releases/{exctraction_name} /data/web_static/current')
            return True

    except Exception:
        return False
