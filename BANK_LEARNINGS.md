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

## CALIBRATION (audit of 23 Oct 2026, 23:15 IST) - READ BEFORE SCORING
- An independent audit of TOAS 04, 07 and 08 found the CHAPTERS, SUBTOPICS and ANSWERS good (printed keys mapped
  correctly, stray letter entries in the maths numerical blocks rightly ignored, solved answers with real working),
  but the DIFFICULTY inflated by about 2 points and drifting: S3/S4 and I1 had become the default (TOAS 07: 92 of 114
  questions S3; TOAS 08: 63 of 108 S4), e.g. a two-equation Raoult's-law question scored D6 and an elevation-of-
  boiling-point one-liner D7. Cause: factors were assigned without working the solutions out.
- Therefore: every ANCHOR line written before this audit (Score-I 12, TOAS 01-08) is VOID. Calibrate only against the
  examples below and against ANCHOR lines tagged [v2]. Every test banked before the audit carries fix_note
  "rescore difficulty": redo ONLY difficulty.tsv in the new format (chapters, subtopics, answers stay).
- The reason column must now list the concepts and the steps (see `bank_tools.py difficulty`); `apply` checks that K and
  S match the counts and rejects anything else. A step is real work (an equation set up and solved, a case, an option
  needing its own working) - reading data, substituting into a formula and one-line arithmetic are not steps.
- Calibrated examples (factors K S I C, F from the type, D):
  Chemistry  TOAS 08 p1_chem_s3_q05  1 1 0 0 F1 -> D2  concepts: elevation of boiling point | steps: dTb = i Kb m; solve i
  Chemistry  TOAS 07 p1_chem_s1_q03  1 2 0 0 F0 -> D2  concepts: Raoult's law | steps: equation for first mixture;
             equation after adding B; solve the linear pair
  Chemistry  TOAS 07 p2_chem_s4_q09  1 1 0 0 F1 -> D2  concepts: EAN counting (NO as 3e donor) | steps: EAN of
             Fe(CO)5; EAN of Fe(CO)2(NO)2
  Physics    TOAS 07 p1_phy_s4_q07   1 2 0 1 F1 -> D4  concepts: compound microscope | steps: eyepiece object distance
             for image at 25 cm; objective image distance = L - ue; objective object distance; product of magnifications
  Physics    TOAS 07 p1_phy_s1_q02   2 2 1 0 F0 -> D4  concepts: angular momentum conservation, energy with shell
             potential | steps: L about centre gives v = u/2 when grazing; energy equation at the surface; solve for u
             | I: grazing means velocity tangential at the surface
  Maths      TOAS 07 p1_math_s4_q08  2 2 0 1 F1 -> D5  concepts: tangent intercepts, related rates | steps: position at
             t = 2; intercepts of the tangent in terms of x; area A = x^(3/2)/4; differentiate and substitute
  Maths      TOAS 07 p2_math_s4_q07  1 2 1 1 F1 -> D5  concepts: derivatives of the inverse function | steps: d2x/dy2 =
             -y''/y'^3; differentiate w.r.t. x and divide by y'; compare coefficients -> k = 3
  Maths      TOAS 04 p2_math_s4_q07  1 2 1 1 F1 -> D5  concepts: telescoping alternating sum | steps: write f(94) as an
             alternating sum of squares plus f(19); pair the squares into an arithmetic series; sum; remainder 561
  Maths      TOAS 07 p1_math_s4_q07  2 3 1 0 F1 -> D6  concepts: a^3+b^3+c^3-3abc factorisation, integer case analysis
             | steps: factorise; split 4 = sum x half-sum-of-squares; cases sum 1, 2, 4; list the triples; maximise
  Maths      TOAS 07 p1_math_s4_q09  2 3 1 1 F1 -> D7  concepts: derivative of arsinh, differentiating an identity |
             steps: y'; (1+x^2) y'^2 = 4y; differentiate -> (1+x^2) y'' + x y' = 2; differentiate again; read p, q, r, s
- Very hard (8-10) needs a genuinely non-standard idea (I2) on top of a long solution (S3-S4) or three concepts; it
  should be a handful of questions per paper at most, not a tenth of it.
- New ANCHOR lines: write them as `ANCHOR [v2] <Subject> D<n>: <test> <qid>: <K S I C F>: concepts: ... | steps: ...`.

## SECOND AUDIT (24 Oct 2026, 08:30 IST) - READ BEFORE SCORING
- From about 00:00 to 00:45 UTC a session banked ~120 tests at ~2 minutes each and wrote TEMPLATE difficulty reasons
  ("concepts: standard problem in this chapter, <subtopic>, apply the relevant results | steps: apply the relevant
  results; compute"), every question S1 and the bands only Medium / Very hard. Some earlier tests also had copied
  reasons or near-uniform S/I. Chapters, subtopics and answers were re-checked (258 keyed answers against the printed
  keys incl. a scanned key, 18 chapter placements, solved working): all correct.
- bank_tools apply now ALSO rejects: generic phrases (apply the relevant results, standard problem, ...), steps that
  are only generic verbs (compute / solve / simplify ...), the same reason or the same step list for more than two
  questions, and a test whose S or I is (almost) the same for every question. A rejected line leaves the question
  without difficulty, so pack refuses. Every banked test that fails these checks has fix_note "rescore difficulty v3".
- Never generate difficulty.tsv (or chapters.tsv / answers.tsv) with a script or a template: score each question from
  its own solution. Matching sets (Q8-Q10 on one table) still need each question's own steps.
- NUMERICAL KEY RANGES: write a printed range as printed ("6.28 to 6.30"), never its midpoint (6.29). The rescore pass
  restores ranges from the key pages (answers.tsv; everything else unchanged).

## THIRD AUDIT (24 Oct 2026, 09:45 IST) - INFLATION - READ BEFORE SCORING
- The v3 rescores began well (TOAS etc.: C2 ~0%, K3 ~1%, I2 ~5-15%), then drifted UP: later tests had C2 on 40%+ of
  questions, K3 on 25%+, Very hard on 30-74% - even the Foundational SRGBT papers. Concept lists were padded to reach
  K3 and C2/I2 were given freely. Examples of the inflation (correct factors in brackets):
  - SRGBT 11 p1_chem_s1_q24 real gas A->B->C, W, dU, q: scored K3 S3 I1 C2 D9 [first law is ONE concept, W at constant
    p + dU from data + q per option: K1 S2 I0 C1 F1 -> D4]
  - SRGBT 11 p1_math_s1_q48 circle of radius 3 touching a pair of lines: scored D10 [angle between the lines, centre on
    the bisector, tangent length: K2 S2 I1 C1 F1 -> D6]
  - SRGBT 11 p1_phy_s1_q11 bobbin pulled by a string, rolling: scored D10 [torque about contact point: K2 S2 I1 C1 F1 -> D6]
- New rules in bank_tools apply: an I or C of 2 must carry "| I: <the non-standard idea>" / "| C: <what is heavy>" in
  the reason; and a test is rejected (all its scores cleared) if more than 25% of its questions get C2, 20% K3 or 30% I2.
- K counts DISTINCT laws or methods, not the quantities they produce. Typical JEE Advanced papers land mostly in
  D3-D6; D8-D10 is for the few questions that combine a non-standard idea with a long solution.
- User decision 24 Oct 09:47: finished tests are NOT rescored again (their difficulty stays approximate); the new
  rules apply to every test banked from now on.
