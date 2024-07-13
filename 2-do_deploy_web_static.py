#!/usr/bin/python3
'''Fabric script that distributes an archive to your web servers'''
from fabric.api import *
import os
from fabric import Connection


env.hosts = ['100.26.53.100', '34.232.72.27']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/school'


def do_deploy(archive_path):
    '''function to deploy'''
    if not os.path.exists(archive_path):
        return False
    try:
        for host in env.hosts:
            conn = Connection(host=host, user=env.user, connect_kwargs={'key_filename': env.key_filename})
            conn.put(archive_path, '/tmp/')
            archive_name = os.path.basename(archive_path)
            exctraction_name = archive_name.split('.')[0]
            conn.run(f'cd /tmp/{archive_name}')
            conn.run(f'sudo tar -xzf {archive_name} -C /data/web_static/releases')
            conn.run('cd /data/web_static/releases')
            conn.run(f'mv web_static {exctraction_name}')
            conn.run(f'sudo rm -r /tmp/{archive_name}')
            conn.run('sudo rm /data/web_static/current')
            conn.run(f'sudo ln -s /data/web_static/releases/{exctraction_name} /data/web_static/current')
            return True

    except Exception:
        return False