#!/usr/bin/env python3
# Copyright (C) 2022 Martin Paulus <m.paulus@linuxoperator.nl>
'''
command line interface to the mira133 module
'''
import argparse
import time

try:
    from mira133 import BooxMira
except ModuleNotFoundError:
    print('mira133 module not found in system location, adding current path')
    import os
    import sys
    file_path = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.dirname(file_path))
    # development workaround for virtualenv:
    sys.path.append(f'{os.path.dirname(file_path)}/venv/lib/python3.8/site-packages')
    from mira133 import BooxMira


mira = BooxMira()
parser = argparse.ArgumentParser(description='Control the Boox Mira settings')
# FIXME -s for log level critical, -v for log level debug
parser.add_argument(
    '-a', '--all',
    action='store_true',
    help='show current settings'
)
parser.add_argument(
    '-r', '--refresh',
    action='store_true',
    help='fully refresh the display'
)
parser.add_argument(
    '-c', '--cold-light',
    choices=range(0, 256), metavar='[0-255]', type=int,
    help='cold light intensity'
)
parser.add_argument(
    '-m', '--refresh-mode',
    choices=[1, 2, 3], metavar='[1-3]', type=int,
    help='refresh mode'
)
parser.add_argument(
    '-s', '--speed',
    choices=range(4, 12), metavar='[4-11]', type=int,
    help='refresh speed'
)
commands = {
    'cold_light': mira.cold_light,
    'refresh_mode': mira.refresh_mode,
    'speed': mira.speed,
    'warm_light': mira.warm_light
}
parser.add_argument(
    '-w', '--warm-light',
    choices=range(0, 256), metavar='[0-255]', type=int,
    help='warm light intensity'
)


def cli():
    '''
    entrypoint for the package which parses command line arguments
    '''
    args = parser.parse_args()
    # FIXME - remove the print statments, or replace with logging
    print(f'args: {args}')

    for cmd in commands:
        val = getattr(args, cmd)
        if isinstance(val, int):
            commands[cmd](val)
            time.sleep(0.01)

    if getattr(args, 'all'):
        print(mira.all_settings())

    if getattr(args, 'refresh'):
        mira.full_refresh()


if __name__ == '__main__':
    cli()
