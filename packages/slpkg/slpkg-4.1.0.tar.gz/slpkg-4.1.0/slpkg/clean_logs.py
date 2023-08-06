#!/usr/bin/python3
# -*- coding: utf-8 -*-


from dataclasses import dataclass

from slpkg.views.views import ViewMessage
from slpkg.models.models import LogsDependencies
from slpkg.models.models import session as Session


@dataclass
class CleanLogsDependencies:
    ''' Cleans the logs from packages. '''
    flags: str
    session: str = Session

    def clean(self):
        dependencies = self.session.query(
            LogsDependencies.name, LogsDependencies.requires).all()

        if dependencies:
            view = ViewMessage(self.flags)
            view.logs_packages(dependencies)
            view.question()

            self.session.query(LogsDependencies).delete()
            self.session.commit()
        else:
            print('\nNothing to clean.\n')
