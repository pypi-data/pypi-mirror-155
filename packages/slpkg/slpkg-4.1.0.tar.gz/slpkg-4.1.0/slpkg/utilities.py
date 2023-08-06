#!/usr/bin/python3
# -*- coding: utf-8 -*-


import os
import re
import tarfile

from dataclasses import dataclass

from slpkg.configs import Configs


@dataclass
class Utilities:
    log_packages: str = Configs.log_packages

    def build_tag(self, path: str, name: str):
        ''' Opens the .SlackBuild file and reads the BUILD TAG. '''
        folder = f'{path}/{name}'
        slackbuild = f'{name}.SlackBuild'

        if os.path.isfile(f'{folder}/{slackbuild}'):
            with open(f'{folder}/{slackbuild}', 'r', encoding='utf-8') as sbo:
                lines = sbo.readlines()

            for line in lines:
                if line.startswith('BUILD'):
                    return re.findall(r'\d+', line)

    def untar_archive(self, path: str, archive: str, ext_path: str):
        ''' Untar the file to the build folder. '''
        tar_file = f'{path}/{archive}'
        untar = tarfile.open(tar_file)
        untar.extractall(ext_path)
        untar.close()

    def is_installed(self, package: str):
        ''' Returns True if a package is installed. '''
        for pkg in os.listdir(self.log_packages):
            if package in pkg:
                return True
