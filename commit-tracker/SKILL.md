---
name: commit-tracker
description: "Track every file you create or modify during a session and check them into the appropriate git repo before finishing. Prevents lost work from forgotten commits."
version: 1.0.0
author: Hermes Agent
license: MIT
---

# Commit Tracker

When you create or modify files during a session, track them and check them in before the session ends. This skill enforces the discipline of **never leaving work in limbo**.

## Why This Exists

- Sessions end. Work disappears. Files vanish from `/tmp`, from scratchpads, from hidden folders.
- You create something useful (a script, a config, a draft) and forget to commit it.
- Next session: "where did that go?" -- it's gone.

## The Rules

### Rule 1: Track as You Go

Every time you create or meaningfully modify a file, add it to the session's tracking list:

```
TRACKED: /path/to/file -- brief description
```

Or use the `commit-tracker-track` command below.

### Rule 2: Check In Before Session End

Before the session wraps up, check in every tracked file to its appropriate repo. If a repo doesn't exist yet, create it.

### Rule 3: Never Commit to the Wrong Repo

Know which repo each file belongs to:

| File Location | Repo |
|---|---|
| `~/.hermes/skills/` | `HermesSkills` (git@github.com:davidleepotter/HermesSkills.git) |
| `~/projects/` or project dirs | Project's own repo |
| `~/.hermes/scripts/` | `HermesScripts` (if it exists) or `HermesSkills` |
| `/tmp/` scratch files | Delete or ask user before committing |
| Config files (~/.bashrc, etc.) | User's dotfiles repo (if any) |

### Rule 4: Small, Frequent Commits

- One logical change per commit.
- Commit messages describe **what** and **why**, not just "update".
- If you made 5 changes to 3 files, that's 3 commits minimum.

## Commands

### Track a file

```bash
# Add to the session tracking list (append to ~/.hermes/commit-tracker/active.txt)
echo "/path/to/file -- description" >> ~/.hermes/commit-tracker/active.txt
```

### Check in all tracked files

```bash
# For each tracked file:
# 1. Determine the correct repo
# 2. git add, commit, push
# 3. Remove from active list
```

### Clear the tracker

```bash
# Clear all tracked files
> ~/.hermes/commit-tracker/active.txt
```

## Workflow

### When Creating Files

1. Create the file.
2. If it belongs in a repo, add it to the tracker.
3. If it's the only change, commit immediately.
4. If more changes are coming, wait until they're done.

### Before Session End

1. Read `~/.hermes/commit-tracker/active.txt` (create it if missing).
2. For each entry:
   a. Verify the file still exists.
   b. Determine the correct repo.
   c. `git add`, `git commit -m "description"`, `git push`.
   d. If the push fails, note it and warn the user.
3. Clear the tracker.

### When Modifying Files

1. If modifying a tracked file, update the tracker entry.
2. If the change is significant, commit the change immediately.
3. If the change is part of a larger task, wait for the task to complete.

## Repo Mapping

Current known repos:

| Repo | URL | Purpose |
|---|---|---|
| `HermesSkills` | `git@github.com:davidleepotter/HermesSkills.git` | All custom skills |
| `ToolKit-V1` | `git@github.com:davidleepotter/ToolKit-V1.git` | ComfyUI custom nodes |
| `HermesScripts` | `git@github.com:davidleepotter/HermesScripts.git` | Hermes utility scripts |

If a repo doesn't exist, create it first:

```bash
gh repo create <name> --public
git clone git@github.com:davidleepotter/<name>.git
```

## Pitfalls

1. **Empty commits** -- if `git status` shows nothing to commit, skip. Don't force an empty commit.
2. **Conflicts** -- if a push fails due to conflicts, pull first, resolve, then push. Report to the user.
3. **Large files** -- don't commit binary files, model weights, or huge datasets. Use `.gitignore`.
4. **Sensitive data** -- never commit API keys, passwords, or tokens. Check `.gitignore` before committing.
5. **Missing remote** -- if `git remote -v` shows nothing, the clone failed. Verify the URL and retry.
6. **Offline** -- if the network is down, note the files to commit and warn the user. Don't lose the work.

## Verification

After checking in, verify:

```bash
# Confirm the file is in the repo
git log --oneline --all | head -5

# Confirm it's pushed
git status
# Should show "nothing to commit, working tree clean"
```

## Integration with Other Skills

- **HermesSkills repo**: When creating or modifying skills, always check them in to `HermesSkills`.
- **ToolKit-V1 repo**: When creating or modifying ComfyUI nodes, always check them in to `ToolKit-V1`.
- **Any new repo**: When creating a new repo, update the repo mapping table above.

## Quick Reference

```bash
# Track a file
echo "/path/to/file -- description" >> ~/.hermes/commit-tracker/active.txt

# Check in all
bash ~/.hermes/scripts/commit-all.sh

# Clear
> ~/.hermes/commit-tracker/active.txt

# Check a specific file
git -C /path/to/repo log --oneline -- /path/to/file
```
