#!/usr/bin/python3
# -*- coding: utf-8 -*-


from dataclasses import dataclass

from slpkg.configs import Configs
from slpkg.models.models import SBoTable
from slpkg.models.models import session as Session


@dataclass
class CreateData:
    ''' Reads the SLACKBUILDS.TXT file and inserts them into the database. '''

    db_path: str = Configs.db_path
    sbo_txt: str = Configs.sbo_txt
    sbo_repo_path: str = Configs.sbo_repo_path
    session: str = Session

    def insert_sbo_table(self):
        sbo_tags = [
            "SLACKBUILD NAME:",
            "SLACKBUILD LOCATION:",
            "SLACKBUILD FILES:",
            "SLACKBUILD VERSION:",
            "SLACKBUILD DOWNLOAD:",
            "SLACKBUILD DOWNLOAD_x86_64:",
            "SLACKBUILD MD5SUM:",
            "SLACKBUILD MD5SUM_x86_64:",
            "SLACKBUILD REQUIRES:",
            "SLACKBUILD SHORT DESCRIPTION:"
        ]

        sbo_file = self.read_file(f"{self.sbo_repo_path}/SLACKBUILDS.TXT")

        cache = []  # init cache

        print('Creating the database... ', end='', flush=True)

        for i, line in enumerate(sbo_file, 1):

            for tag in sbo_tags:
                if line.startswith(tag):
                    line = line.replace(tag, "").strip()
                    cache.append(line)

            if (i % 11) == 0:
                data = SBoTable(name=cache[0], location=cache[1].split('/')[1],
                                files=cache[2], version=cache[3],
                                download=cache[4], download64=cache[5],
                                md5sum=cache[6], md5sum64=cache[7],
                                requires=cache[8], short_description=cache[9])
                self.session.add(data)

                cache = []  # reset cache after 11 lines

        print('Done')

        self.session.commit()

    def read_file(self, file: str):
        with open(file, "r", encoding="utf-8") as f:
            return f.readlines()
