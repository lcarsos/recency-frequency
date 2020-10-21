#!/usr/bin/env python3

"""Script entrypoint for recyfreqy, in case you aren't using the package"""

import datetime
from contextlib import contextmanager
from datetime import datetime, timedelta
from itertools import filterfalse
from os import chdir
import os.path as op
import subprocess
from tempfile import TemporaryDirectory

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


# This is not the canonical way to do this. This shadows all kinds of metadata, and clobbers docstrings
def on_false(action):
    def inner(f):
        def wrapped(*args, **kwargs):
            ret = f(*args, **kwargs)
            if not bool(ret):
                action(*args, **kwargs)
            return ret
        return wrapped
    return inner


@on_false(lambda head: print(f"{datetime.utcfromtimestamp(head.commit.authored_date)}\t{head}"))
def check_branch(head):
    """Create a temporary worktree to check if this branch has the thing we're looking for"""
    global g
    global init_pwd
    global cmd_args
    try:
        with TemporaryDirectory() as directory:
            with git_worktree(directory, head):
                chdir(directory)
                result = subprocess.run(cmd_args.command, stdin=None, stderr=None, capture_output=True)
                return result.returncode != 0
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
    # print(cmd_args.command)

    recently = timedelta(days=cmd_args.days)

    r = Repo(op.curdir)
    g = git.cmd.Git(op.curdir)

    # print(f"work dir: {r.working_dir}")
    # print(f"git_dir: {r.git_dir}")

    heads = list(reversed(sorted((x for x in r.remotes[cmd_args.remote].refs
                                 if now - utcfromtimestamp(x.commit.committed_date) < recently),
                                 key=lambda x: x.commit.authored_date)))
    total_branches = len(heads)
    heads_with_change = list(filterfalse(check_branch, heads))
    filtered_branches = len(heads_with_change)

    if filtered_branches > 0:
        print('----')
    print(f"{filtered_branches}/{total_branches} branches pass the check")


if __name__ == '__main__':
    print('script invocation')
    main()
