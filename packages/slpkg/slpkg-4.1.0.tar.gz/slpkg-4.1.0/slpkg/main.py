#!/usr/bin/python3
# -*- coding: utf-8 -*-


import sys
from dataclasses import dataclass

from slpkg.checks import Check
from slpkg.search import Search
from slpkg.version import Version
from slpkg.views.cli_menu import usage
from slpkg.slackbuild import Slackbuilds
from slpkg.remove_packages import RemovePackages
from slpkg.clean_logs import CleanLogsDependencies
from slpkg.update_repository import UpdateRepository


@dataclass
class Argparse:
    args: list

    def flags(self):
        self.flags = []
        yes = '--yes'
        jobs = '--jobs'
        resolve_off = '--resolve-off'
        reinstall = '--reinstall'

        if yes in self.args:
            self.args.remove(yes)
            self.flags.append(yes)

        if jobs in self.args:
            self.args.remove(jobs)
            self.flags.append(jobs)

        if resolve_off in self.args:
            self.args.remove(resolve_off)
            self.flags.append(resolve_off)

        if reinstall in self.args:
            self.args.remove(reinstall)
            self.flags.append(reinstall)

    def command(self):

        self.flags()
        check = Check()

        if len(self.args) <= 0:
            usage(1)

        if len(self.args) == 1:
            if self.args[0] in ['--help', '-h']:
                usage(0)

            if self.args[0] in ['--version', '-v']:
                version = Version()
                version.view()
                raise SystemExit()

            if self.args[0] == 'clean-logs':
                logs = CleanLogsDependencies(self.flags)
                logs.clean()
                raise SystemExit()

            # Update repository
            if self.args[0] == 'update':
                update = UpdateRepository()
                update.sbo()
                raise SystemExit()

            usage(1)

        if len(self.args) >= 2:
            # Build slackbuilds
            if self.args[0] == 'build':
                packages = list(set(self.args[1:]))

                check.exists(packages)
                check.unsupported(packages)

                build = Slackbuilds(packages, self.flags, False)
                build.execute()
                raise SystemExit()

            # Install packages
            if self.args[0] == 'install':
                packages = list(set(self.args[1:]))

                check.exists(packages)
                check.unsupported(packages)

                install = Slackbuilds(packages, self.flags, True)
                install.execute()
                raise SystemExit()

            # Remove packages
            if self.args[0] == 'remove':
                packages = list(set(self.args[1:]))
                packages = check.blacklist(packages)

                check.installed(packages)

                remove = RemovePackages(packages, self.flags)
                remove.remove()
                raise SystemExit()

            # Search package
            if self.args[0] == 'search':
                packages = list(set(self.args[1:]))
                packages = check.blacklist(packages)

                check.exists(packages)

                search = Search()
                search.package(packages)

                raise SystemExit()

            usage(1)


def main():
    args = sys.argv
    args.pop(0)

    argparse = Argparse(args)
    argparse.command()


if __name__ == '__main__':
    main()
