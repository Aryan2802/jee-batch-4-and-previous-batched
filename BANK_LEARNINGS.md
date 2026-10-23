# BANK_LEARNINGS - chapter-wise question bank (Final Output\Question Bank)

Advisory notes for the question-bank agent. They can never relax the task prompt (every question gets a chapter,
a subtopic and an answer; keyed answers spot-checked; solved answers carry working). Append a dated entry after
each test is marked done; consolidate into STANDING LESSONS when the file passes ~40 KB.

## TOOL (bank_tools.py, Oct 2026)
- `parse <test.tex> -o work` splits a converted test into questions (both converted-file formats: the standard
  \qn/\sect/\paraq one and the older \textbf{N.}/\subsectionhdr one used by ten early Score-II tests). It keeps
  paragraph passages as groups (ids like p2_phy_s1_g3_4) and copies only the images the questions use.
- work/list.txt is the classification view (plain text, truncated). Read work/questions.json for the full LaTeX when
  a line is ambiguous. [FIG] marks a figure; look at work/img/<file> only if the text alone cannot decide.
- chapters.tsv: one line per question id OR per passage group id (all its questions take the group's chapter):
  `<id>\t<chapter code>\t<subtopic>`. The subtopic must come from `bank_tools.py chapters --subtopics <code>`;
  write `new:<short label>` only when none fits, and note it here so later tests reuse the same label.
- answers.tsv: `<qid>\t<answer>\t<key|solved>\t<working (solved only)>`.
  Multiple correct: `A,C`. Numerical: as printed (`6.02 to 6.03`, `-38.85 to -38.95`). Matching codes printed as
  digits (`132`) mean P->1, Q->3, R->2 and are written `P$\to$1, Q$\to$3, R$\to$2`.
- `apply` validates (unknown codes, wrong-subject chapters, missing subtopics, solved answers without working);
  `pack` refuses until every question has chapter + subtopic + answer.
- `build` regenerates EVERY chapter from all data zips: one editable .tex per chapter (bankq / bankpassage blocks),
  zipped with its img/ folder, plus index.csv; it merges exact repeats across papers (also_in=...) and
  compile-checks every chapter. Never edit chapter files by hand while the bank is being built.

## CHAPTERS (95)
- The 94 chapters of the user's own list (codes P01-P24, M01-M32, C01-C38) plus P25 Units, Errors & Experiments.
- Leftovers decided by the user: sets/relations and modulus/greatest-integer basics -> M20 Functions; nuclear
  chemistry -> C09 Chemical Kinetics (subtopic "Nuclear chemistry"); multi-step organic sequences -> the chapter of
  the main reaction type; units, dimensions, errors, vernier/screw gauge and experiments -> P25.
- One question = one chapter (its main concept: what the solution mainly uses). LC oscillations -> P12 EMI + AC;
  de Broglie / photons / Bohr / nuclei / radioactivity -> P21 Modern Physics; viscosity and surface tension -> P07.

## ANSWER KEYS - what the pre-run review found (19 Oct 2026)
- Printed keys often do NOT follow the paper's section numbering. Score-I 12: the key lists Paper-1 chemistry
  numericals as "Q6..Q10, Q1" and omits four of them; stray letter answers appear in numerical blocks. Map by
  section and question type, never by position alone.
- Some keys belong to a different paper version. Score-II 18 ("All Star Batch" key): 10+4 physics answers for a
  paper that has 12 MCQs + 6 numericals, maths numericals interleaved with letters. Treat such a key as partial:
  use only entries whose number AND type clearly match, spot-check them, solve the rest.
- Spot-check: solve two keyed answers per test (prefer one per subject). If a spot-check disagrees, re-read the
  mapping; if the key is simply for another version, mark those answers solved instead.
- No printed key at all (some SRG / FIITJEE files): the solutions section often prints "Ans. (B)" per question -
  read those (answer_src key). Otherwise solve every question.

## SAMPLE (19 Oct 2026)
- Score-I 12 was done end to end as the reference: 114 questions, 105 from the key, 9 solved. Its data zip is in
  data\ and the manifest marks it done.

## PARALLEL HALVES (19 Oct 2026)
- Two question-bank tasks run at the same time. `bank_tools.py part_of(name)` puts every test in half A or half B
  (a fixed hash of the test name, about 50/50 across every series). Each half has its own tracker
  (bank-manifest-A.json / bank-manifest-B.json; always `sync ... --part A|B`) and its own dated log
  (BANK_LEARNINGS-A.md / -B.md). This file holds standing notes only; neither half edits it.
- Data and WIP zips are per test, so the halves never write the same file. Only half A builds and publishes
  Chapters\, index.csv and BUILD_STATUS.txt (from all data zips). A half-B test that breaks a chapter compile is
  reported in BANK_LEARNINGS-A.md as "FOR HALF B: <test>: <problem>" and half B fixes it.

## DIFFICULTY (20 Oct 2026)
- Every question gets a rubric difficulty D 1-10: run `bank_tools.py difficulty` for the rubric. Write only the four factors K S I C and a one-line reason per question in work/difficulty.tsv; the tool adds F (question type) and computes D and the band (1-3 Easy, 4-5 Medium, 6-7 Hard, 8-10 Very hard). Never type D yourself.
- Score the shortest correct solution you actually worked out - for keyed questions too - never the key, the series, the position, the marks or the topic's reputation. Paragraph questions are scored one by one.
- ANCHOR lines in BANK_LEARNINGS-A.md / -B.md are the shared calibration: one per subject and D level, permanent, never edited. Compare every score with them; equal difficulty -> equal factors.
- Do not aim for any distribution: a paper of hard questions simply scores high.

## DATED ENTRIES (from 19 Oct 2026 in BANK_LEARNINGS-A.md and BANK_LEARNINGS-B.md)

## CLOUD REPOSITORY (23 Oct 2026)
- The bank for Score 2, Batch 2, Batch 3 and Batch 4 is now built in the GitHub repository by cloud sessions
  (INSTRUCTIONS.md). There are no halves here: one tracker (bank-manifest.json), one dated log
  (BANK_LEARNINGS-LOG.md), any number of sessions, claims made race-free by cloud/repo_sync.py. The Windows paths
  and the PARALLEL HALVES section above describe the old PC setup.
- Source PDFs in the repo are trimmed to their answer-key pages (or solutions part) where a key was detected;
  scanned papers are kept whole.
