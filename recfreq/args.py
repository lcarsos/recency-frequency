"""Sets up argparse"""

from argparse import ArgumentParser


def init():
    parser = ArgumentParser(description='Quickly figure out how many (remote) branches  have certain characteristics')

    parser.add_argument('command', nargs='+', help='Command that should return 0 if true to filter branches')
    parser.add_argument('-d', '--days', help='How many days to check in history')
    parser.add_argument('-r', '--remote', default='origin', help='Which remote to check')

    return parser
