#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
from dataclasses import dataclass

from slpkg.configs import Configs
from slpkg.queries import SBoQueries
from slpkg.blacklist import Blacklist


@dataclass
class Check:
    ''' Some checks before proceed. '''
    log_packages: str = Configs.log_packages
    repo_tag: str = Configs.repo_tag

    def exists(self, slackbuilds: list):
        ''' Checking if the slackbuild exists in the repository. '''
        self.database()
        packages = []

        for sbo in slackbuilds:
            if not SBoQueries(sbo).slackbuild():
                packages.append(sbo)

        if packages:
            raise SystemExit(f'\nPackages {", ".join(packages)} '
                             'does not exists.\n')

    def unsupported(self, slackbuilds: list):
        ''' Checking for unsupported slackbuilds. '''
        for sbo in slackbuilds:
            sources = SBoQueries(sbo).sources()

            if 'UNSUPPORTED' in sources:
                raise SystemExit(f'\nPackage {sbo} unsupported by arch.\n')

    def installed(self, slackbuilds: list):
        ''' Checking for installed packages. '''

        for package in os.listdir(self.log_packages):
            for sbo in slackbuilds:

                if sbo + '-' in package and self.repo_tag in package:
                    return

        raise SystemExit('\nNot found packages for remove.\n')

    def blacklist(self, slackbuilds: list):
        ''' Checking for packages on the blacklist and removing them. '''
        black = Blacklist()

        for package in black.get():
            if package in slackbuilds:
                slackbuilds.remove(package)

        return slackbuilds

    def database(self):
        ''' Checking for empty table '''
        if not SBoQueries('').names():
            raise SystemExit('\nYou need to update the package lists first.\n'
                             'Please run slpkg update.\n')
