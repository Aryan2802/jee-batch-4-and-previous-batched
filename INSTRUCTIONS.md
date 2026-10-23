# Question bank - cloud session instructions (Score 2, Batch 2, Batch 3, Batch 4)

You are continuing a multi-session job: building a chapter-wise QUESTION BANK from the user's converted JEE test
papers in this repository. Every question of every converted test gets one chapter, one subtopic, an answer and a
rubric difficulty score (1-10), and is published in one editable LaTeX file per chapter (with its figures) plus an
index. Several cloud sessions may run at the same time on this repository; all shared state lives in the repo and is
changed ONLY through `cloud/repo_sync.py`, which makes claims and log entries race-free. This session has no memory
of earlier runs.

## RUN UNTIL USAGE RUNS OUT - FULLY AUTONOMOUS
No per-session limit: finish a test, claim the next, until nothing is left or the session is cut off. Never stop
voluntarily, never ask questions, never wait for input: make the most reasonable decision, note it in the test's
manifest note / the learnings log, and keep going. You can be cut off at any moment, so save constantly (WIP zip
after every step, manifest note after every step). Do not create or modify scheduled tasks. Never push with
`git push --force`, never rewrite history, never edit files that belong to another session's claimed test.

## REPOSITORY LAYOUT (paths relative to the repo root)
- `tools/bank_tools.py`, `tools/subtopics.json` - the bank tool (`python3 tools/bank_tools.py -h`)
- `bank-manifest.json` - the tracker: one entry per converted test (name, tex_rel, img_rel, src_rel, status ...).
  214 tests: Batch 4 (ALLEN series) first, then Score 2, Batch 3, Batch 2. Edit it ONLY with `cloud/repo_sync.py`.
- Converted tests: `<Batch> Converted/.../<Test Name>.tex` + `<Test Name>-img/` (tex_rel / img_rel). Read-only.
- Sources: `<Batch>/Source/.../<Test Name>.pdf` (src_rel). Read-only. To keep the repo small most of these hold ONLY
  the printed answer-key pages (or the solutions part) of the original paper - page numbers therefore start at 1.
  PDFs without a detectable key (scanned papers, e.g. SRGBT, several Score Advanced) are kept complete.
  The question text itself is always in the converted .tex.
- `<Batch>/progress-manifest.json` - conversion trackers (read-only; their notes describe each paper).
- `BANK_LEARNINGS.md` - standing notes (read it; never edit it). `BANK_LEARNINGS-LOG.md` - dated entries and ANCHOR
  lines of every session (read all of it; append only through `repo_sync.py learn`).
- `data/<Test Name>.zip` - per-test results (questions.json with chapter/subtopic/answer/difficulty + the images used)
- `WIP/<Test Name>-work.zip` - partial work dir of a claimed test (incl. chapters.tsv / answers.tsv / difficulty.tsv)
- Published bank: `Chapters/Physics|Chemistry|Mathematics/<code title>/` (the chapter .tex + img/, stored UNZIPPED so
  unchanged images are not re-stored on every build), `index.csv`, `BUILD_STATUS.txt`; `build-lock.json` = build lock.

## SETUP (once per session)
1. `bash cloud/setup.sh` (installs pymupdf, scipy, pillow, pdflatex if missing; prints a check).
2. Do all scratch work in `/tmp/qb/` (never inside the repo, except the files you save on purpose).
3. Read `BANK_LEARNINGS.md` (TOOL, CHAPTERS, ANSWER KEYS and DIFFICULTY sections first; its PARALLEL HALVES section
   and Windows paths describe the old PC setup and do not apply here), run `python3 tools/bank_tools.py difficulty`
   and read the rubric, then read all of `BANK_LEARNINGS-LOG.md` including every ANCHOR line. All of it is advisory
   and can never relax these instructions.

## SHARED-STATE RULES
- Claim: `python3 cloud/repo_sync.py claim-next` -> prints the entry and `CLAIMED <Test Name>` (or NONE). It takes
  fix_note tests first, then abandoned in_progress tests (started_at >= 40 min old), then pending ones. Never work
  on a test you did not claim.
- Every manifest edit: `python3 cloud/repo_sync.py set "<Test Name>" key=value ...` (exact full name as printed by
  CLAIMED; `started_at=now` for the current time; `-key` removes a field). Keep `started_at` fresh: re-set
  `started_at=now` together with each progress note (at least every 30 min), or another session will reclaim the test.
- Files: `python3 cloud/repo_sync.py save -m "<msg>" <paths...>` commits and pushes them; `remove` deletes them.
- Learnings: write the entry to a file and `python3 cloud/repo_sync.py learn <file>`.
- `python3 cloud/repo_sync.py show` prints the counts and every unfinished entry.

## PIPELINE FOR ONE TEST
1. CLAIM (above). If the entry already has `data/<Test Name>.zip` complete in the repo and no fix_note, the file is
   the truth: mark it done and claim the next. Fix_note "rescore difficulty" (tests banked before the 23 Oct audit,
   see BANK_LEARNINGS.md CALIBRATION) and fix_note "add difficulty" (e.g. Score-I 12, packed before 20 Oct
   2026): unzip its data zip into an empty `/tmp/qb/work` (it holds questions.json + img/), do step 5b only, then `apply --difficulty`, `pack`, save the zip and
   mark done with `-fix_note` - chapters, subtopics and answers stay as they are.
2. RESUME: if `WIP/<Test Name>-work.zip` exists, unzip it into `/tmp/qb` (`python3 -m zipfile -e "WIP/<Test Name>-work.zip" /tmp/qb`; it holds a `work/` folder) and continue from where it stopped. Otherwise start from an empty `/tmp/qb/work` (`rm -rf /tmp/qb/work /tmp/qb/key`).
3. PARSE: `python3 tools/bank_tools.py parse "<tex_rel>" -o /tmp/qb/work --img "<img_rel>"`. Check the printed
   question counts per paper/subject against the converted test (read the .tex section headers and the conversion
   note in `<Batch>/progress-manifest.json`; the note may count paragraph questions differently - the .tex is the
   truth). "missing images" must be empty.
4. CLASSIFY: read work/list.txt (and work/questions.json for full text, the images only when needed). Write
   work/chapters.tsv: one line per question id or per passage group id: `<id>\t<chapter code>\t<subtopic>`. Codes:
   `python3 tools/bank_tools.py chapters --subtopics`. One chapter per question = the concept its solution mainly
   uses (see BANK_LEARNINGS CHAPTERS for the agreed placements). Subtopic from that chapter's list; `new:<label>`
   only when nothing fits. Save WIP: `mkdir -p WIP && rm -f "WIP/<Test Name>-work.zip" && python3 -m zipfile -c "WIP/<Test Name>-work.zip" /tmp/qb/work` (run from the repo root) then
   `repo_sync.py save -m "WIP <Test>" "WIP/<Test Name>-work.zip"`, and set a manifest note.
5. ANSWERS: `python3 tools/bank_tools.py keyprep "<src_rel>" -o /tmp/qb/key --work /tmp/qb/work`. View each
   key/page-N.png once. Write work/answers.tsv `<qid>\t<answer>\t<key|solved>\t<working>`:
   - use the printed key only where it clearly belongs to this paper - map by paper, subject, section and question
     type, never by position alone (keys skip, reorder and mislabel sections; see BANK_LEARNINGS ANSWER KEYS).
     key/proposed_answers.tsv, when written, is a starting point to verify line by line, not a result;
   - scanned sources (no text layer, keyprep finds nothing): render the last pages yourself
     (`pdftoppm -r 110 -f <n> -png`) and look for the key or "Ans." lines before deciding to solve everything;
   - SPOT-CHECK: solve two keyed answers per test (one per subject where possible). On disagreement re-check the
     mapping; if the key is for another version of the paper, stop using it for the affected part;
   - if the paper prints "Ans." in a solutions section instead of a key table, those are key answers;
   - every question without a usable key answer: SOLVE it carefully (it is the real answer the user will study
     from) and give answer_src=solved plus one or two lines of working (LaTeX allowed). Matching codes like 132
     become `P$\to$1, Q$\to$3, R$\to$2`.
   Save WIP again.
5b. DIFFICULTY - rigorous and uniform, from the rubric only (`python3 tools/bank_tools.py difficulty`). Read the
   CALIBRATION section of BANK_LEARNINGS.md first: an audit found scores assigned without working the solutions out.
   The reason column must list `concepts: ... | steps: ...` and `apply` checks K and S against those lists. Speed is
   not a goal: a 100-question paper honestly worked takes far longer than a few minutes. Score EVERY
   question, keyed ones too: for a keyed question work out the shortest correct solution route yourself (enough to
   be sure of every factor) - never score from the key, the source series, the question's position, its marks or
   the topic's reputation. Write work/difficulty.tsv `<qid>\t<K S I C>\t<one-line reason naming concepts: a, b | steps:
   s1; s2; s3 ...>` (one line per question, passage questions scored one by one; F, D and the band are computed by the
   tool from the question type - never type D yourself). Factors: K concepts 1-3, S non-trivial steps 1 (1-2) /
   2 (3-4) / 3 (5-7) / 4 (8+), I insight 0 direct / 1 known technique / 2 non-standard idea, C computation 0 light /
   1 moderate / 2 heavy. CALIBRATE: compare every score with the CALIBRATION examples in BANK_LEARNINGS.md and
   the ANCHOR [v2] lines of the same subject in BANK_LEARNINGS-LOG.md (older anchors are void) - a question clearly harder than an anchor must not get a lower D, and an equally hard one
   gets the same factors; when two readings are possible, count the step or concept the shortest solution really
   cannot skip. Never shift scores towards a target distribution. CONSISTENCY CHECK: after the file is written,
   re-derive the four factors for three questions (one per subject) from their solution without looking at the
   file; if a D differs by more than 1, re-examine that whole section. Save WIP again.
6. APPLY + PACK: `python3 tools/bank_tools.py apply /tmp/qb/work --chapters work/chapters.tsv --answers
   work/answers.tsv --difficulty work/difficulty.tsv` - fix every ERROR and rerun until it is clean; then
   `python3 tools/bank_tools.py pack /tmp/qb/work -o "data/<Test Name>.zip"` (refuses while any chapter, subtopic,
   answer or difficulty is missing) and `repo_sync.py save -m "data: <Test>" "data/<Test Name>.zip"`.
7. MARK DONE: `repo_sync.py set "<Test Name>" status=done note="<N questions; K from key, S solved; difficulty bands
   Easy/Medium/Hard/Very hard counts; chapters touched>" -started_at -claimed_by -progress_note -fix_note`.
   Then append a short dated entry with `repo_sync.py learn`: `## <date> <Test Name>` + key quirks of this series,
   subtopic labels you added, anything the next test should know, plus ANCHOR lines: for every subject and every D
   level that has no [v2] anchor yet in the log, add one `ANCHOR [v2] <Physics|Chemistry|Mathematics> D<n>: <test>
   <qid>: <K S I C F>: concepts: ... | steps: ...` (at most 6 per test, from questions whose factors you are most sure of). Anchors are
   permanent: never edit or delete one. Finally `repo_sync.py remove -m "WIP done <Test>" "WIP/<Test Name>-work.zip"`.
8. BUILD: BUILT = "tests in build" in BUILD_STATUS.txt (0 if missing); DONE = done tests in bank-manifest.json
   (after `repo_sync.py pull`). Build when DONE - BUILT >= 10, or when claim-next returns NONE and DONE > BUILT:
   - `repo_sync.py claim-build`; on BUSY skip the build (another session is building) and go on;
   - `repo_sync.py pull`, `rm -rf /tmp/qb/out`, `python3 tools/bank_tools.py build data -o /tmp/qb/out` - it must report all chapters ok (it compile-checks
     each one); if a chapter fails, fix the offending test's data zip (re-parse, apply, pack) and re-run;
   - replace the published chapters: `rm -rf Chapters && mkdir Chapters`, then unzip every
     /tmp/qb/out/<Subject>/<code title>.zip into `Chapters/<Subject>/` (each zip already holds a `<code title>/`
     folder with the .tex and img/, e.g. `python3 -m zipfile -e "<zip>" "Chapters/<Subject>"`); copy
     /tmp/qb/out/index.csv to `index.csv`; write `BUILD_STATUS.txt` (date, tests in build, questions, duplicates
     merged, done-since-build 0);
   - `repo_sync.py save -m "build: N tests" Chapters index.csv BUILD_STATUS.txt` (it also records chapter files
     that disappeared), then
     `repo_sync.py release-build "built N tests"`.
9. Claim the next test (step 1).

## QUALITY BAR (never relaxed)
Every question of the test is in the bank exactly once, with its figures; the chapter is the question's main
concept; the subtopic comes from the list; every answer is either a correctly mapped printed key answer or a careful
solution with working; every question has a rubric difficulty (K S I C with a reason) consistent with the anchors;
chapter files always compile.

## WHEN NOTHING IS LEFT
When claim-next prints NONE: build if DONE > BUILT (step 8), then write `ALL_DONE.txt` (date + counts) with
`repo_sync.py save`, and stop.
