#!/usr/bin/python3
# -*- coding: utf-8 -*-


import hashlib
from dataclasses import dataclass

from slpkg.configs import Configs
from slpkg.views.views import ViewMessage


@dataclass
class Md5sum:
    ''' Checksum the sources. '''
    flags: str
    build_path: str = Configs.build_path

    def check(self, source: str, checksum: str, name: str):
        path = f'{self.build_path}/{name}'
        filename = f'{path}/{source.split("/")[-1]}'

        md5 = self.read_file(filename)

        file_check = hashlib.md5(md5).hexdigest()

        if file_check not in checksum:
            print('\nExpected:', ''.join(checksum))
            print('Found:', file_check)
            print(f'\nMD5SUM check for {name} FAILED.')

            view = ViewMessage()
            view.question(self.flags)

    def read_file(self, filename: str):
        with open(filename, 'rb') as f:
            return f.read()
