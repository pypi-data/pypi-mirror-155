#!/usr/bin/python3
# -*- coding: utf-8 -*-


import os
import json

from dataclasses import dataclass


@dataclass
class Configs:

    # Programme name
    prog_name: str = 'slpkg'

    ''' Default configurations. '''
    # OS architecture by default
    os_arch: str = 'x86_64'

    # All necessary paths
    tmp_path: str = '/tmp'
    tmp_slpkg: str = f'{tmp_path}/{prog_name}'
    build_path: str = f'/tmp/{prog_name}/build'
    lib_path: str = f'/var/lib/{prog_name}'
    etc_path: str = f'/etc/{prog_name}'
    db_path: str = f'/var/lib/{prog_name}/database'
    sbo_repo_path: str = f'/var/lib/{prog_name}/repository'
    log_packages: str = '/var/log/packages'

    # Database name
    database: str = f'database.{prog_name}'

    # Repository details
    repo_version: str = '15.0'
    sbo_url: str = f'http://slackbuilds.org/slackbuilds/{repo_version}'
    sbo_txt: str = 'SLACKBUILDS.TXT'
    tar_suffix: str = '.tar.gz'
    pkg_suffix: str = '.tgz'
    repo_tag: str = '_SBo'

    # Slackware commands
    installpkg: str = 'upgradepkg --install-new'
    reinstall: str = 'upgradepkg --reinstall'
    removepkg: str = 'removepkg'

    # Other configs
    colors: str = 'on'
    wget_options = '-c -N'

    ''' Overwrite with user configuration. '''
    config_file: str = f'{etc_path}/{prog_name}.json'
    if os.path.isfile(config_file):

        with open(config_file, 'r') as conf:
            config = json.load(conf)

        # OS architecture by default
        os_arch: str = config['os_arch']

        # All necessary paths
        tmp_path: str = config['tmp_path']
        tmp_slpkg: str = config['tmp_slpkg']
        build_path: str = config['build_path']
        lib_path: str = config['lib_path']
        etc_path: str = config['etc_path']
        db_path: str = config['db_path']
        sbo_repo_path: str = config['sbo_repo_path']
        log_packages: str = config['log_packages']

        # Database name
        database: str = config['database']

        # Repository details
        repo_version: str = config['repo_version']
        sbo_url: str = config['sbo_url']
        sbo_txt: str = config['sbo_txt']
        tar_suffix: str = config['tar_suffix']
        pkg_suffix: str = config['pkg_suffix']
        repo_tag: str = config['repo_tag']

        # Slackware commands
        installpkg: str = config['installpkg']
        reinstall: str = config['reinstall']
        removepkg: str = config['removepkg']

        # Other configs
        colors: str = config['colors']
        wget_options: str = config['wget_options']

    @classmethod
    def colour(cls):
        color = {
            'RED': '',
            'GREEN': '',
            'YELLOW': '',
            'CYAN': '',
            'BLUE': '',
            'GREY': '',
            'ENDC': ''
        }

        if cls.colors in ['on', 'ON']:
            color = {
                'RED': '\x1b[91m',
                'GREEN': '\x1b[32m',
                'YELLOW': '\x1b[93m',
                'CYAN': '\x1b[96m',
                'BLUE': '\x1b[94m',
                'GREY': '\x1b[38;5;247m',
                'ENDC': '\x1b[0m'
            }

        return color
