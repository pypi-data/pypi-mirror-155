#!/usr/bin/python3
# -*- coding: utf-8 -*-


import os
import json
from dataclasses import dataclass

from slpkg.configs import Configs


@dataclass
class Blacklist:
    ''' Reads and returns the blacklist. '''
    etc_path: str = Configs.etc_path

    def get(self):
        file = f'{self.etc_path}/blacklist.json'
        if os.path.isfile(file):
            with open(file, 'r') as black:
                return json.load(black)['blacklist']
