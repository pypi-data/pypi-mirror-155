#!/usr/bin/python3
# -*- coding: utf-8 -*-


from dataclasses import dataclass

from slpkg.configs import Configs
from slpkg.models.models import SBoTable
from slpkg.models.models import session as Session


@dataclass
class Search:
    session: str = Session
    colors: list = Configs.colour
    sbo_url: str = Configs.sbo_url

    def package(self, packages):
        color = self.colors()
        GREEN = color['GREEN']
        BLUE = color['BLUE']
        YELLOW = color['YELLOW']
        ENDC = color['ENDC']

        for package in packages:
            info = self.session.query(
                SBoTable.name,
                SBoTable.version,
                SBoTable.requires,
                SBoTable.download,
                SBoTable.download64,
                SBoTable.md5sum,
                SBoTable.md5sum64,
                SBoTable.files,
                SBoTable.short_description,
                SBoTable.location
            ).filter(SBoTable.name == package).first()

            print(f'Name: {GREEN}{info[0]}{ENDC}\n'
                  f'Version: {GREEN}{info[1]}{ENDC}\n'
                  f'Requires: {GREEN}{info[2]}{ENDC}\n'
                  f'Download: {BLUE}{info[3]}{ENDC}\n'
                  f'Download_x86_64: {BLUE}{info[4]}{ENDC}\n'
                  f'Md5sum: {YELLOW}{info[5]}{ENDC}\n'
                  f'Md5sum_x86_64: {YELLOW}{info[6]}{ENDC}\n'
                  f'Files: {GREEN}{info[7]}{ENDC}\n'
                  f'Description: {GREEN}{info[8]}{ENDC}\n'
                  f'SBo url: {BLUE}{self.sbo_url}/{info[9]}/'
                  f'{info[0]}{ENDC}\n')
