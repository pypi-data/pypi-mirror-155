#!/usr/bin/python3
# -*- coding: utf-8 -*-


from slpkg.configs import Configs


def usage(status: int):
    args = [f'Usage: {Configs.prog_name} [OPTIONS] [packages]\n',
            '  Packaging tool that interacts with the SBo repository.\n',
            'Options:',
            '  update              Update the package lists.',
            '  build               Build only the packages.',
            '  install             Build and install the packages.',
            '  remove              Remove installed packages.',
            '  search              Search packages by name.',
            '  clean-logs          Purge logs of dependencies.\n',
            '  --yes               Answer Yes to all questions.',
            '  --jobs              Set it for multicore systems.',
            '  --resolve-off       Turns off dependency resolving.',
            '  --reinstall         Use this option if you want to upgrade.\n',
            '  -h, --help          Show this message and exit.',
            '  -v, --version       Print version and exit.\n',
            'If you need more information try to use slpkg manpage.']

    for opt in args:
        print(opt)
    raise SystemExit(status)
