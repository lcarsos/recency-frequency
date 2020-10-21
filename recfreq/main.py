#!/usr/bin/env python3

"""Script entrypoint for recyfreqy, in case you aren't using the package"""

import datetime
from contextlib import contextmanager
from datetime import datetime, timedelta
from itertools import dropwhile
from os import chdir
import os.path as op
import subprocess
from tempfile import TemporaryDirectory

import logger

from git import Repo
import git

import recfreq.args as argparse

global g
global init_pwd
global cmd_args


@contextmanager
def git_worktree(directory, head):
    g.worktree(['add', directory, head])
    try:
        yield
    finally:
        g.worktree(['remove', directory])


def check_branch(head):
    """Create a temporary worktree to check if this branch has the thing we're looking for"""
    global g
    global init_pwd
    try:
        with TemporaryDirectory() as directory:
            with git_worktree(directory, head):
                chdir(directory)
                return subprocess.call(command)
    finally:
        chdir(init_pwd)


def main():
    """entrypoint"""
    global g
    global init_pwd
    global cmd_args

    init_pwd = op.curdir
    utcfromtimestamp = datetime.utcfromtimestamp
    now = datetime.now()

    arg_parse = argparse.init()
    cmd_args = arg_parse.parse_args()
    print(cmd_args.command)

    recently = timedelta(days=7)

    r = Repo(op.curdir)
    g = git.cmd.Git(op.curdir)

    print(f"work dir: {r.working_dir}")
    print(f"git_dir: {r.git_dir}")

    for line in g.worktree('list').splitlines():
        print(f"{line}")

    heads = list(reversed(sorted((x for x in r.remotes.cban.refs
                                 if now - utcfromtimestamp(x.commit.committed_date) < recently),
                                 key=lambda x: x.commit.authored_date)))
    total_branches = len(heads)
    for head in heads:
        print(f"{utcfromtimestamp(head.commit.authored_date)}\t{head}")
    heads_with_change = list(dropwhile(check_branch, heads))
    filtered_branches = len(heads_with_change)


if __name__ == '__main__':
    print('script invocation')
    main()
