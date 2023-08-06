#!/usr/bin/python3
# -*- coding: utf-8 -*-


import subprocess
from dataclasses import dataclass

from slpkg.configs import Configs
from slpkg.views.views import ViewMessage
from slpkg.models.models import LogsDependencies
from slpkg.models.models import session as Session


@dataclass
class RemovePackages:
    ''' Removes installed packages. '''
    packages: str
    flags: list
    session: str = Session
    removepkg: str = Configs.removepkg

    def remove(self):
        ''' Removes package with dependencies. '''
        self.installed_packages = []
        self.dependencies = []

        view = ViewMessage(self.flags)

        self.installed_packages, self.dependencies = view.remove_packages(
            self.packages)

        view.question()

        self.remove_packages()
        self.delete_main_logs()

        if self.dependencies and '--resolve-off' not in self.flags:
            self.delete_deps_logs()

    def remove_packages(self):
        ''' Run Slackware command to remove the packages. '''
        for package in self.installed_packages:
            command = f'{self.removepkg} {package}'
            subprocess.call(command, shell=True)

    def delete_main_logs(self):
        ''' Deletes main packages from logs. '''
        for pkg in self.packages:
            self.session.query(LogsDependencies).filter(
                LogsDependencies.name == pkg).delete()
        self.session.commit()

    def delete_deps_logs(self):
        ''' Deletes depends packages from logs. '''
        for pkg in self.dependencies[0].split():
            self.session.query(LogsDependencies).filter(
                LogsDependencies.name == pkg).delete()
        self.session.commit()
