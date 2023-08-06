#!/usr/bin/python3
# -*- coding: utf-8 -*-


import subprocess
from dataclasses import dataclass

from slpkg.configs import Configs


@dataclass
class Wget:
    ''' Wget donwloader. '''
    wget_options: str = Configs.wget_options

    def download(self, path: str, url: str):
        subprocess.call(f'wget {self.wget_options} --directory-prefix={path}'
                        f' {url}', shell=True)
