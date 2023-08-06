#!/usr/bin/python3
# -*- coding: utf-8 -*-


from dataclasses import dataclass

from slpkg.configs import Configs


@dataclass
class Version:
    prog_name: str = Configs.prog_name
    version_info: tuple = (4, 1, 0)
    version: str = '{0}.{1}.{2}'.format(*version_info)
    license: str = 'MIT License'
    author: str = 'dslackw'
    homepage: str = 'https://dslackw.gitlab.io/slpkg'

    def view(self):
        print(f'{self.prog_name} version: {self.version}\n'
              f'Homepage: {self.homepage}')
