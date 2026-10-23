#!/usr/bin/env python3
"""export_to_pc.py - bring the question-bank progress made in this repository back to the PC layout.

Run it in any clone of this repository (a Claude session does this when the cloud credit runs out):

  python3 cloud/export_to_pc.py --pc-a <PC bank-manifest-A.json> --pc-b <PC bank-manifest-B.json> \
        --pc-log-a <PC BANK_LEARNINGS-A.md> -o <out dir>

It reads the LATEST state of the shared branch (claude/qbank-shared) and writes, under <out dir>, files whose paths
are relative to "D:\\Aryan DOWNLOADS\\Final Output" (copy each to the same place on the PC):

  Question Bank/bank-manifest-A.json, -B.json   the PC trackers with every repo test merged in, split by part_of:
                                               done stays done (note, fix_note kept); a test in progress in the
                                               cloud becomes pending with a note to resume from its WIP zip
  Question Bank/data/<Test>.zip                 every finished test's data zip
  Question Bank/WIP/<Test>-work.zip             checkpoints of unfinished tests (the PC prompt resumes from them)
  Question Bank/BANK_LEARNINGS-A.md             the PC half-A log + an "IMPORTED FROM CLOUD REPO" section holding
                                               the repo log (dated entries and ANCHOR lines); re-running replaces
                                               that section instead of duplicating it
  Question Bank/tools/bank_tools.py, subtopics.json, BANK_LEARNINGS.md   the repo's current tool and standing notes
  Question Bank/BUILD_STATUS.txt                "tests in build: 0" so the PC half-A task rebuilds the chapters
  commit-list.txt                              every file above, one per line
It also prints a summary and warns about other claude/* branches holding commits that are not on the shared branch
(sessions that could not push to the shared branch).
"""
import argparse, collections, hashlib, io, json, os, re, shutil, subprocess, sys, tarfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHARED = "claude/qbank-shared"
FO_ROOT = "D:\\Aryan DOWNLOADS\\Final Output\\"
MARK = "## IMPORTED FROM CLOUD REPO (Aryan2802/jee-batch-4-and-previous-batched)"


def git(*a, check=True):
    r = subprocess.run(["git", "-C", ROOT, *a], capture_output=True)
    if check and r.returncode:
        sys.exit(f"git {' '.join(a)} failed: {r.stderr.decode(errors='replace')}")
    return r


def part_of(name):
    return "AB"[int(hashlib.sha1(name.encode("utf-8")).hexdigest(), 16) % 2]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pc-a", required=True); ap.add_argument("--pc-b", required=True)
    ap.add_argument("--pc-log-a", required=True); ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--ref", default=None, help="git ref to export (default: origin/" + SHARED + ")")
    a = ap.parse_args()

    if a.ref:
        ref = a.ref
    else:
        git("fetch", "-q", "origin", f"+refs/heads/{SHARED}:refs/remotes/origin/{SHARED}")
        ref = f"origin/{SHARED}"

    # A session that could not push to the shared branch worked on its own claude/* branch (repo_sync fallback).
    # If exactly one such branch is ahead of the shared branch and contains it, it is the newest state: export it.
    ahead = []
    for line in git("ls-remote", "--heads", "origin").stdout.decode().splitlines():
        sha, r = line.split("\t"); b = r[len("refs/heads/"):]
        if b in (SHARED, "main") or not b.startswith("claude/") or a.ref:
            continue
        git("fetch", "-q", "origin", f"+{r}:refs/remotes/origin/{b}", check=False)
        n = git("rev-list", "--count", f"{ref}..origin/{b}", check=False).stdout.decode().strip()
        if n and n != "0":
            contains = git("merge-base", "--is-ancestor", ref, f"origin/{b}", check=False).returncode == 0
            ahead.append((b, n, contains))
            print(f"NOTE: branch {b} has {n} commit(s) not on {SHARED}" + ("" if contains else " and has diverged from it"))
    if len(ahead) == 1 and ahead[0][2]:
        ref = f"origin/{ahead[0][0]}"
        print(f"  -> exporting {ref} instead (it contains everything on {SHARED} plus its own work)")
    elif ahead:
        print(f"WARNING: several branches hold unshared work - exporting {SHARED} only; merge the others by hand "
              f"(or re-run with --ref) before trusting this export")
    tip = git("rev-parse", "--short", ref).stdout.decode().strip()
    snap = os.path.join(a.out, "_snapshot")
    shutil.rmtree(snap, ignore_errors=True); os.makedirs(snap)
    paths = [p for p in ("bank-manifest.json", "BANK_LEARNINGS-LOG.md", "BUILD_STATUS.txt", "data", "WIP",
                       "tools", "BANK_LEARNINGS.md")
             if git("cat-file", "-e", f"{ref}:{p}", check=False).returncode == 0]
    tarfile.open(fileobj=io.BytesIO(git("archive", "--format=tar", ref, *paths).stdout)).extractall(snap, filter="data")

    repo = json.load(open(os.path.join(snap, "bank-manifest.json"), encoding="utf-8"))
    bs = lambda p: p.replace("/", "\\")
    pcs = {"A": json.load(open(a.pc_a, encoding="utf-8")), "B": json.load(open(a.pc_b, encoding="utf-8"))}
    idx = {k: {t["name"]: t for t in m["tests"]} for k, m in pcs.items()}
    wips = set(os.listdir(os.path.join(snap, "WIP"))) if os.path.isdir(os.path.join(snap, "WIP")) else set()
    count = collections.Counter()
    for t in repo["tests"]:
        k = part_of(t["name"])
        e = idx[k].get(t["name"])
        if e is None:
            e = dict(name=t["name"], status="pending"); pcs[k]["tests"].append(e); idx[k][t["name"]] = e
        e.update(tex_rel=bs(t["tex_rel"]), img_rel=bs(t["img_rel"]), src_rel=[bs(s) for s in t["src_rel"]],
                 conv_note=t.get("conv_note", e.get("conv_note", "")))
        for f in ("started_at", "claimed_by", "progress_note", "fix_note", "note"):
            e.pop(f, None)
        if t["status"] == "done" or t.get("fix_note"):
            # a fix_note test (e.g. "add difficulty") claimed in the cloud stays done + fix_note: the PC only re-fixes it
            e["status"] = "done"
            for f in ("note", "fix_note"):
                if t.get(f): e[f] = t[f]
        else:
            e["status"] = "pending"
            w = f"{t['name']}-work.zip"
            note = t.get("progress_note") or t.get("note") or ""
            if w in wips:
                e["note"] = f"cloud WIP: resume from QB\\WIP\\{w}" + (f" ({note})" if note else "")
        count[(k, e["status"])] += 1

    qb = os.path.join(a.out, "Question Bank")
    os.makedirs(os.path.join(qb, "data"), exist_ok=True)
    files = []
    for k in "AB":
        p = os.path.join(qb, f"bank-manifest-{k}.json")
        json.dump(pcs[k], open(p, "w", encoding="utf-8"), indent=1, ensure_ascii=False); files.append(p)
    for sub in ("data", "WIP"):
        d = os.path.join(snap, sub)
        if os.path.isdir(d):
            os.makedirs(os.path.join(qb, sub), exist_ok=True)
            for f in sorted(os.listdir(d)):
                if f.endswith(".zip"):
                    shutil.copy(os.path.join(d, f), os.path.join(qb, sub, f)); files.append(os.path.join(qb, sub, f))
    log_a = open(a.pc_log_a, encoding="utf-8").read()
    if MARK in log_a:
        log_a = log_a[:log_a.index(MARK)].rstrip("\n") + "\n"
    cloud_log = open(os.path.join(snap, "BANK_LEARNINGS-LOG.md"), encoding="utf-8").read()
    body = cloud_log.split("\n## ", 1)[1] if "\n## " in cloud_log else cloud_log
    p = os.path.join(qb, "BANK_LEARNINGS-A.md")
    open(p, "w", encoding="utf-8").write(log_a.rstrip("\n") + f"\n\n{MARK}\nExported from {SHARED} @ {tip}. "
                                         "Dated entries and ANCHOR lines written by the cloud sessions (they count as "
                                         "anchors for both halves).\n\n## " + body.rstrip("\n") + "\n")
    files.append(p)
    # the tool and the standing notes evolve in the repo (e.g. the 23 Oct difficulty audit): the PC gets the same
    os.makedirs(os.path.join(qb, "tools"), exist_ok=True)
    for f in ("bank_tools.py", "subtopics.json"):
        shutil.copy(os.path.join(snap, "tools", f), os.path.join(qb, "tools", f)); files.append(os.path.join(qb, "tools", f))
    shutil.copy(os.path.join(snap, "BANK_LEARNINGS.md"), os.path.join(qb, "BANK_LEARNINGS.md"))
    files.append(os.path.join(qb, "BANK_LEARNINGS.md"))
    p = os.path.join(qb, "BUILD_STATUS.txt")
    open(p, "w").write("last build: none on the PC since the cloud import (the half-A task rebuilds)\n"
                       "tests in build: 0\nquestions: 0\nduplicates merged: 0\ndone-since-build: 0\n")
    files.append(p)
    open(os.path.join(a.out, "commit-list.txt"), "w").write("\n".join(os.path.relpath(f, a.out) for f in files) + "\n")
    shutil.rmtree(snap)
    print(f"exported {ref} @ {tip}: {len(files)} files")
    print("  half A:", {s: n for (k, s), n in count.items() if k == "A"}, " half B:", {s: n for (k, s), n in count.items() if k == "B"})
    print("  data zips:", sum(1 for f in files if os.sep + "data" + os.sep in f), " WIP zips:", sum(1 for f in files if os.sep + "WIP" + os.sep in f))


if __name__ == "__main__":
    main()
