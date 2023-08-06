#!/usr/bin/python3
# -*- coding: utf-8 -*-


import os

from os import path
from dataclasses import dataclass

from slpkg.downloader import Wget
from slpkg.configs import Configs
from slpkg.create_data import CreateData
from slpkg.models.models import SBoTable
from slpkg.models.models import session as Session


@dataclass
class UpdateRepository:
    ''' Deletes and install the data. '''
    sbo_repo_path: str = Configs.sbo_repo_path
    url: str = Configs.sbo_url
    sbo_txt: str = Configs.sbo_txt
    db_path: str = Configs.db_path
    database: str = Configs.database
    session: str = Session

    def sbo(self):
        print('Updating the package list...\n')
        self.delete_file(self.sbo_repo_path, self.sbo_txt)
        self.delete_sbo_data()

        sbo_url = f'{self.url}/{self.sbo_txt}'

        wget = Wget()
        wget.download(self.sbo_repo_path, sbo_url)

        data = CreateData()
        data.insert_sbo_table()

    def delete_file(self, dir: str, txt_file: str):
        file = f'{dir}/{txt_file}'
        if path.exists(file):
            os.remove(file)

    def delete_sbo_data(self):
        self.session.query(SBoTable).delete()
        self.session.commit()
