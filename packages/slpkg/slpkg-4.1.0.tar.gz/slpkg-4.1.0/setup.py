#!/usr/bin/python3
# -*- coding: utf-8 -*-


from setuptools import setup
from slpkg.version import Version


install_requires = ['SQLAlchemy>=1.4.36']


setup(
    name='slpkg',
    packages=['slpkg', 'slpkg/models', 'slpkg/views'],
    scripts=['bin/slpkg'],
    version=Version.version,
    description='Packaging tool that interacts with the SBo repository',
    long_description=open('README.rst').read(),
    keywords=['slackware', 'slpkg', 'update', 'build', 'install', 'remove',
              'slackpkg', 'tool'],
    author='dslackw',
    url='https://dslackw.gitlab.io/slpkg/',
    package_data={'': ['LICENSE.txt', 'README.rst', 'ChangeLog.txt']},
    data_files=[('/etc/slpkg', ['configs/slpkg.json']),
                ('/etc/slpkg', ['configs/blacklist.json']),
                ('/var/lib/slpkg/database', []),
                ('/var/lib/slpkg/repository', []),
                ('/tmp/slpkg/build', [])],
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Unix Shell',
        'Topic :: Software Development :: Build Tools',
        'Topic :: System :: Archiving :: Packaging',
        'Topic :: System :: Software Distribution',
        'Topic :: System :: Installation/Setup',
        'Topic :: System :: Systems Administration',
        'Topic :: System :: Software Distribution',
        'Topic :: Utilities'],
    python_requires='>=3.9'
)
