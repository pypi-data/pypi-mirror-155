#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import shutil
import subprocess
import multiprocessing

from dataclasses import dataclass
from collections import OrderedDict

from slpkg.downloader import Wget
from slpkg.checksum import Md5sum
from slpkg.configs import Configs
from slpkg.queries import SBoQueries
from slpkg.utilities import Utilities
from slpkg.dependencies import Requires
from slpkg.views.views import ViewMessage
from slpkg.models.models import LogsDependencies
from slpkg.models.models import session as Session


@dataclass
class Slackbuilds:
    ''' Download build and install the SlackBuilds. '''
    slackbuilds: str
    flags: list
    install: bool
    session: str = Session
    utils: str = Utilities()
    build_path: str = Configs.build_path
    sbo_url: str = Configs.sbo_url
    build_path: str = Configs.build_path
    tmp_slpkg: str = Configs.tmp_slpkg
    tmp_path: str = Configs.tmp_path
    tar_suffix: str = Configs.tar_suffix
    os_arch: str = Configs.os_arch
    repo_tag: str = Configs.repo_tag
    pkg_suffix: str = Configs.pkg_suffix
    installpkg: str = Configs.installpkg
    reinstall: str = Configs.reinstall

    def execute(self):
        ''' Starting build or install the slackbuilds. '''
        self.install_order = []
        self.dependencies = []
        self.creating_dictionary()

        if '--resolve-off' not in self.flags:
            self.creating_dependencies_for_build()
        self.creating_main_for_build()

        self.view_before_build()

        self.download_slackbuilds_and_build()

    def view_before_build(self):
        ''' View slackbuilds before proceed. '''
        view = ViewMessage(self.flags)

        if self.install:
            view.install_packages(self.slackbuilds, self.dependencies)
        else:
            view.build_packages(self.slackbuilds, self.dependencies)

        del self.dependencies  # no more needed

        view.question()

    def creating_dictionary(self):
        ''' Dictionary with the main slackbuilds and dependencies. '''
        self.sbos = {}
        for sbo in self.slackbuilds:
            self.sbos[sbo] = Requires(sbo).resolve()

    def creating_dependencies_for_build(self):
        ''' List with the dependencies. '''
        for deps in self.sbos.values():
            for dep in deps:
                if dep not in self.slackbuilds:
                    self.dependencies.append(dep)
        # Remove duplicate packages and keeps the order.
        self.dependencies = list(OrderedDict.fromkeys(self.dependencies))
        self.install_order.extend(self.dependencies)

    def creating_main_for_build(self):
        ''' List with the main slackbuilds. '''
        for main in self.sbos.keys():
            self.install_order.append(main)

    def download_slackbuilds_and_build(self):
        ''' Downloads files and sources and starting the build. '''
        wget = Wget()

        for sbo in self.install_order:
            file = f'{sbo}{self.tar_suffix}'

            self.remove_file_if_exists(self.tmp_slpkg, file)
            self.remove_folder_if_exists(self.build_path, sbo)

            location = SBoQueries(sbo).location()
            url = f'{self.sbo_url}/{location}/{file}'

            wget.download(self.tmp_slpkg, url)

            self.utils.untar_archive(self.tmp_slpkg, file, self.build_path)

            sources = SBoQueries(sbo).sources()
            self.download_sources(sbo, sources)

            self.execute_the_script(self.build_path, sbo)

            if self.install:

                package = self.creating_package_for_install(sbo)
                self.install_package(package)

                if '--resolve-off' not in self.flags:
                    self.logging_installed_dependencies(sbo)

    def logging_installed_dependencies(self, name: str):
        ''' Logging installed dependencies and used for remove. '''
        exist = self.session.query(LogsDependencies.name).filter(
            LogsDependencies.name == name).first()

        requires = Requires(name).resolve()

        # Update the dependencies if exist else create it.
        if exist:
            self.session.query(
                LogsDependencies).filter(
                    LogsDependencies.name == name).update(
                        {LogsDependencies.requires: ' '.join(requires)})

        elif requires:
            deps = LogsDependencies(name=name, requires=' '.join(requires))
            self.session.add(deps)
        self.session.commit()

    def install_package(self, package: str):
        ''' Install the packages that before created in the tmp directory. '''
        execute = self.installpkg
        if ('--reinstall' in self.flags and
                self.utils.is_installed(package[:-4])):
            execute = self.reinstall
        command = f'{execute} {self.tmp_path}/{package}'
        subprocess.call(command, shell=True)

    def creating_package_for_install(self, name: str):
        ''' Creating a list with all the finished packages for
            installation.
        '''
        build_tag = self.utils.build_tag(self.build_path, name)
        version = SBoQueries(name).version()
        return (f'{name}-{version}-{self.os_arch}-{build_tag[0]}'
                f'{self.repo_tag}{self.pkg_suffix}')

    def execute_the_script(self, path: str, name: str):
        ''' Run the .SlackBuild script. '''
        folder = f'{path}/{name}/'
        slackbuild = f'./{name}.SlackBuild'
        execute = folder + slackbuild

        if '--jobs' in self.flags:
            self.set_makeflags()

        stdout = subprocess.call(execute)
        if stdout > 0:
            raise SystemExit(stdout)

    def set_makeflags(self):
        ''' Set number of processors. '''
        cpus = multiprocessing.cpu_count()
        os.environ['MAKEFLAGS'] = f'-j {cpus}'

    def download_sources(self, name: str, sources: str):
        ''' Download the sources. '''
        wget = Wget()
        path = f'{self.build_path}/{name}'
        checksums = SBoQueries(name).checksum()

        for source, checksum in zip(sources.split(), checksums[0].split()):
            wget.download(path, source)
            md5sum = Md5sum(self.flags)
            md5sum.check(source, checksum, name)

    def remove_file_if_exists(self, path: str, file: str):
        ''' Clean the the old files. '''
        archive = f'{path}/{file}'
        if os.path.isfile(archive):
            os.remove(archive)

    def remove_folder_if_exists(self, path: str, folder: str):
        ''' Clean the the old folders. '''
        directory = f'{path}/{folder}'
        if os.path.isdir(directory):
            shutil.rmtree(directory)
