#!/usr/bin/env python3
"""repo_sync.py - safe git operations for several question-bank cloud sessions sharing this repo.

Every change to a shared file (bank-manifest.json, BANK_LEARNINGS-LOG.md, build-lock.json) is made on the LATEST
remote copy and pushed; if another session pushed first, the change is thrown away locally and re-applied on the new
copy. So two sessions can never overwrite each other's claims or log entries.

  python3 cloud/repo_sync.py pull
        fast-forward to the remote (keeps your uncommitted files)

  python3 cloud/repo_sync.py claim-next
        on the latest copy, claim the next free test (fix_note entries first, then in_progress older than 40 min
        or without started_at, then pending, in manifest order) and push the claim. Prints the entry as JSON,
        then CLAIMED <Test Name>, or NONE when nothing is left. Two sessions can never claim the same test.

  python3 cloud/repo_sync.py set "<Test Name>" key=value [key=value ...] [-key ...]
        on the latest copy, edit that test's manifest entry (exact full name, e.g. "TOAS - Test 07 (01 May 2022)"):
        key=value sets a field (value "now" = current UTC time), -key removes a field. Commits and pushes.

  python3 cloud/repo_sync.py show
        pull, then print counts and every entry that is not done (or has a fix_note)

  python3 cloud/repo_sync.py claim-build / release-build "<message>"
        build lock (build-lock.json): claim-build prints CLAIMED-BUILD or BUSY (another session's lock < 60 min old);
        release-build clears it.

  python3 cloud/repo_sync.py learn <file-with-entry.md>
        append the file's text to BANK_LEARNINGS-LOG.md on the latest copy, commit, push (retries)

  python3 cloud/repo_sync.py save -m "message" <path> [<path> ...]
        commit these paths (data zips, WIP checkpoints, chapters) and push (retries). Paths relative to the repo root.

  python3 cloud/repo_sync.py remove -m "message" <path> [<path> ...]
        delete these tracked paths (e.g. a finished test's WIP zip), commit and push (retries)
"""
import os, subprocess, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = "bank-manifest.json"
LEARN = "BANK_LEARNINGS-LOG.md"
LOCK = "build-lock.json"
TRIES = 8


def git(*args, check=True, quiet=False):
    r = subprocess.run(["git", "-C", ROOT, *args], capture_output=True, text=True)
    if check and r.returncode != 0:
        if not quiet:
            sys.stderr.write(f"git {' '.join(args)} failed:\n{r.stdout}{r.stderr}")
        raise RuntimeError(r.stderr.strip() or r.stdout.strip())
    return r


def branch():
    return git("rev-parse", "--abbrev-ref", "HEAD").stdout.strip()


def ensure_identity():
    if not git("config", "user.email", check=False).stdout.strip():
        git("config", "user.email", "qbank-cloud@users.noreply.github.com")
        git("config", "user.name", "Question bank cloud session")


def pull():
    """rebase local commits on the remote; uncommitted tracked changes are stashed and restored"""
    for i in range(TRIES):
        r = git("pull", "--rebase", "--autostash", "origin", branch(), check=False)
        if r.returncode == 0:
            return
        git("rebase", "--abort", check=False)
        time.sleep(3 + 3 * i)
    raise RuntimeError("git pull failed repeatedly:\n" + r.stdout + r.stderr)


def push():
    r = git("push", "origin", f"HEAD:{branch()}", check=False)
    return r.returncode == 0


def head():
    return git("rev-parse", "--short", "HEAD").stdout.strip()


def shared_change(path, apply, message):
    """apply() edits `path` on the latest copy; commit only that file; push; on rejection undo and redo."""
    ensure_identity()
    for i in range(TRIES):
        pull()
        out = apply()
        if not git("status", "--porcelain", "--", path).stdout.strip():
            return out, None                      # nothing changed (e.g. manifest show / verify)
        git("add", "--", path)
        git("commit", "-m", message, "--", path)
        if push():
            return out, head()
        # someone pushed first: drop our commit, restore the file, retry on the new remote state
        git("reset", "--mixed", "HEAD~1")
        git("checkout", "--", path)
        time.sleep(2 + 2 * i)
    raise RuntimeError(f"could not push {path} after {TRIES} tries")


def _load():
    import json
    return json.load(open(os.path.join(ROOT, MANIFEST), encoding="utf-8"))


def _dump(m):
    import json
    p = os.path.join(ROOT, MANIFEST)
    json.dump(m, open(p + ".tmp", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    os.replace(p + ".tmp", p)


def _now():
    import datetime
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def cmd_set(args):
    import json
    if len(args) < 2:
        sys.exit('usage: set "<Test Name>" key=value ... -key ...')
    name, ops = args[0], args[1:]
    out = {}

    def apply():
        m = _load()
        e = [t for t in m["tests"] if t["name"] == name]
        if len(e) != 1:
            sys.exit(f"no manifest entry named exactly {name!r}")
        e = e[0]
        for o in ops:
            if o.startswith("-") and "=" not in o:
                e.pop(o[1:], None)
            else:
                k, v = o.split("=", 1)
                e[k] = _now() if v == "now" else v
        _dump(m)
        out.update(e)
    _, c = shared_change(MANIFEST, apply, f"manifest: {name} {' '.join(o for o in ops if o.startswith('status='))}".strip())
    print(json.dumps(out, ensure_ascii=False))
    print(f"PUSHED {c}" if c else "UNCHANGED")


def cmd_show(args):
    import collections, json
    pull()
    m = _load()
    print(dict(collections.Counter(t["status"] for t in m["tests"])))
    for t in m["tests"]:
        if t["status"] != "done" or t.get("fix_note"):
            print("  " + json.dumps({k: t.get(k) for k in ("name", "status", "started_at", "claimed_by", "note", "fix_note") if t.get(k)}, ensure_ascii=False))


def cmd_build_lock(args, release=False):
    import datetime, json
    res = {}

    def apply():
        p = os.path.join(ROOT, LOCK)
        cur = json.load(open(p)) if os.path.exists(p) else {}
        if release:
            cur = {"holder": "", "since": "", "last": " ".join(args) or "released", "released_at": _now()}
        else:
            if cur.get("holder") and cur["holder"] != session_id():
                st = datetime.datetime.strptime(cur["since"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.timezone.utc)
                if (datetime.datetime.now(datetime.timezone.utc) - st).total_seconds() < 3600:
                    res["busy"] = cur
                    return
            cur = dict(cur, holder=session_id(), since=_now())
        json.dump(cur, open(p, "w"), indent=1)
    _, c = shared_change(LOCK, apply, f"build lock: {'release' if release else 'claim'} by {session_id()}")
    if release:
        print(f"RELEASED {c}")
    elif "busy" in res:
        print(f"BUSY {json.dumps(res['busy'])}")
    else:
        print(f"CLAIMED-BUILD {c}")


def session_id():
    """stable id of this cloud session (one container), so two sessions' claim commits can never be identical"""
    if os.environ.get("QBANK_SESSION_ID"):
        return os.environ["QBANK_SESSION_ID"]
    p = "/tmp/.qbank_session_id"
    try:
        return open(p).read().strip()
    except OSError:
        import secrets, socket
        sid = f"{socket.gethostname()[:12]}-{secrets.token_hex(4)}"
        open(p, "w").write(sid)
        return sid


def _claimable(t, now, minutes=40):
    import datetime
    if t["status"] == "pending":
        return True
    if t["status"] == "done" and t.get("fix_note"):
        return True
    if t["status"] == "in_progress":
        s = t.get("started_at")
        if not s:
            return True
        try:
            st = datetime.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.timezone.utc)
        except ValueError:
            return True
        return (now - st).total_seconds() >= minutes * 60
    return False


def cmd_claim_next(args):
    """claim the next free test in manifest order (fix_note entries first) on the latest remote copy"""
    import datetime, json
    picked = {}

    def apply():
        p = os.path.join(ROOT, MANIFEST)
        m = json.load(open(p, encoding="utf-8"))
        now = datetime.datetime.now(datetime.timezone.utc)
        order = [t for t in m["tests"] if t["status"] == "done" and t.get("fix_note")] + \
                [t for t in m["tests"] if t["status"] in ("in_progress", "pending")]
        cand = next((t for t in order if _claimable(t, now)), None)
        picked.clear()
        if cand is None:
            return None
        reclaim = cand["status"] == "in_progress"
        prev_note = cand.get("progress_note", "")
        cand["status"] = "in_progress"
        cand["started_at"] = now.strftime("%Y-%m-%dT%H:%M:%SZ")
        cand["claimed_by"] = session_id()
        cand["progress_note"] = (f"reclaimed (previous note: {prev_note})" if reclaim else
                                 ("fix: " + cand["fix_note"]) if cand.get("fix_note") else "starting")
        tmp = p + ".tmp"
        json.dump(m, open(tmp, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        os.replace(tmp, p)
        picked.update(cand)
        return cand
    _, c = shared_change(MANIFEST, apply, f"manifest: claim by {session_id()}")
    if not picked:
        print("NONE - no pending, reclaimable or fix_note test left")
        return
    print(json.dumps(picked, ensure_ascii=False))
    print(f"CLAIMED {picked['name']}")
    print(f"PUSHED {c}")


def cmd_learn(args):
    text = open(args[0], encoding="utf-8").read()

    def apply():
        p = os.path.join(ROOT, LEARN)
        cur = open(p, encoding="utf-8").read() if os.path.exists(p) else ""
        with open(p, "a", encoding="utf-8") as f:
            f.write(("" if cur.endswith("\n") or not cur else "\n") + text.rstrip("\n") + "\n")
    _, c = shared_change(LEARN, apply, "learnings: append entry")
    print(f"PUSHED {c}")


def cmd_save(args, remove=False):
    if "-m" not in args:
        sys.exit("save/remove need -m 'message'")
    k = args.index("-m")
    msg, paths = args[k + 1], args[:k] + args[k + 2:]
    if not paths:
        sys.exit("no paths given")
    ensure_identity()
    if remove:
        git("rm", "-r", "-q", "--ignore-unmatch", "--", *paths)
    else:
        git("add", "--", *paths)
    if not git("diff", "--cached", "--name-only").stdout.strip():
        print("nothing to commit")
        return
    git("commit", "-q", "-m", msg)
    for i in range(TRIES):
        if push():
            print(f"PUSHED {head()}")
            return
        pull()
        time.sleep(2 + 2 * i)
    raise RuntimeError("push failed repeatedly")


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    c, a = sys.argv[1], sys.argv[2:]
    if c == "pull":
        pull(); print(f"up to date at {head()}")
    elif c == "set":
        cmd_set(a)
    elif c == "show":
        cmd_show(a)
    elif c == "claim-build":
        cmd_build_lock(a)
    elif c == "release-build":
        cmd_build_lock(a, release=True)
    elif c == "claim-next":
        cmd_claim_next(a)
    elif c == "learn":
        cmd_learn(a)
    elif c == "save":
        cmd_save(a)
    elif c == "remove":
        cmd_save(a, remove=True)
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
