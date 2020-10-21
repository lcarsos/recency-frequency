"""Sets up argparse"""

from argparse import ArgumentParser


def init():
    parser = ArgumentParser(description='Quickly figure out how many (remote) branches  have certain characteristics')

    parser.add_argument('command', nargs='+', help='Command that should return 0 if true to filter branches')
    parser.add_argument('-d', '--days', default=7, type=int, help='How many days to check in history')
    parser.add_argument('-r', '--remote', default='origin', help='Which remote to check')
    parser.add_argument('-v', '--verbose', action='count', default=0, help='Provide more information. default output is intended for further scripting')

    return parser
