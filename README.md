# Recency-Frequency

A CLI tool to check how many branches in the remote pass a check.

It's a glorified foreach, but it's exactly the tool I wanted.

Ricky checks out branches to a temporary worktree that have been recently pushed to in your remote (defaults to `origin`) and then runs the command you specify, if it returns
`0` then we include that branch.

### What's a worktree?

Oh you noticed that. `git-worktree(1)` is a feature of git. Go learn about it.

Ricky creates a temporary directory, and makes that a separate worktree and does the checkout there, so you don't have to
worry about your working directory being dirty, or you don't want it changed for some reason.
