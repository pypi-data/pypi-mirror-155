#!/usr/bin/python3
# -*- coding: utf-8 -*-


from dataclasses import dataclass

from slpkg.queries import SBoQueries


@dataclass
class Requires:
    ''' Creates a list of dependencies with
    the right order to install. '''
    name: str

    def resolve(self) -> list:
        requires = SBoQueries(self.name).requires()

        for req in requires:
            if req and req != "%README%":
                sub = SBoQueries(req).requires()
                for s in sub:
                    requires.append(s)

        requires.reverse()

        return list(dict.fromkeys(requires))
