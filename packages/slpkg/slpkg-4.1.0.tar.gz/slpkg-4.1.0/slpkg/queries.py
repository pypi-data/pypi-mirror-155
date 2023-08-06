#!/usr/bin/python3
# -*- coding: utf-8 -*-


from dataclasses import dataclass

from slpkg.configs import Configs
from slpkg.blacklist import Blacklist
from slpkg.models.models import SBoTable
from slpkg.models.models import session as Session


@dataclass
class SBoQueries:
    ''' Queries class for the sbo repository. '''
    name: str
    session: str = Session
    os_arch: str = Configs.os_arch

    def __post_init__(self):
        self.black = Blacklist()
        if self.name in self.black.get():
            self.name = ''

    def names(self):
        return list(self._names_grabbing())

    def slackbuild(self):
        sbo = self.session.query(
            SBoTable.name).filter(SBoTable.name == self.name).first()

        if sbo:
            return sbo
        return ''

    def location(self):
        location = self.session.query(
            SBoTable.location).filter(SBoTable.name == self.name).first()

        if location:
            return location[0]
        return ''

    def sources(self):
        source, source64 = self.session.query(
            SBoTable.download, SBoTable.download64).filter(
                SBoTable.name == self.name).first()

        if source or source64:
            return self._chose_arch(source, source64)
        return ''

    def requires(self):
        requires = self.session.query(
            SBoTable.requires).filter(
                SBoTable.name == self.name).first()

        if requires:
            requires = requires[0].split()
            for req in requires:
                if req in self.black.get():
                    requires.remove(req)
            return requires
        return ''

    def version(self):
        version = self.session.query(
            SBoTable.version).filter(
                SBoTable.name == self.name).first()

        if version:
            return version[0]
        return ''

    def checksum(self):
        md5sum, md5sum64, = [], []
        mds5, md5s64 = self.session.query(
            SBoTable.md5sum, SBoTable.md5sum64).filter(
                SBoTable.name == self.name).first()

        if mds5:
            md5sum.append(mds5)
        if md5s64:
            md5sum64.append(md5s64)

        if md5sum or md5sum64:
            return self._chose_arch(md5sum, md5sum64)
        return ''

    def description(self):
        desc = self.session.query(
            SBoTable.short_description).filter(
                SBoTable.name == self.name).first()

        if desc:
            return desc[0]
        return ''

    def files(self):
        files = self.session.query(
            SBoTable.files).filter(
                SBoTable.name == self.name).first()

        if files:
            return files[0]
        return ''

    def _chose_arch(self, arch, arch64):
        if self.os_arch and arch64:
            return arch64
        return arch

    def _names_grabbing(self):
        names = self.session.query(SBoTable.name).all()
        for n in names:
            yield n[0]
