# BANK_LEARNINGS-LOG - dated entries and ANCHOR lines of every question-bank session

Advisory; read together with BANK_LEARNINGS.md (standing notes). Append only with `python3 cloud/repo_sync.py learn <file>`. ANCHOR lines are permanent calibration points: never edit or delete one.

## 2026-10-23 repository created
- 214 converted tests (Batch 4, Score 2, Batch 3, Batch 2) moved from the PC to this repo for cloud sessions. The PC logs BANK_LEARNINGS-A.md / -B.md had no dated entries yet. Score-I 12 (reference sample, 19 Oct) carries fix_note "add difficulty".

## 2026-10-23 Score-I - Test 12 (09 Mar 2022) - difficulty added (fix_note "add difficulty")
- 114 questions scored from the rubric: D2:7 D3:13 D4:12 D5:28 D6:28 D7:22 D8:3 D9:1; bands Easy 20, Medium 40, Hard 50, Very hard 4. Chapters, subtopics and answers unchanged.
- Paper-2 "combination" tables (Column I/II/III, single correct): each option needs its own check, so S is 3-4 and F=0; the table's shared computations are counted in every question that depends on them.
- If repo_sync.py first fails with "couldn't find remote ref", merge origin/claude/qbank-shared (the shared branch) into your session branch.
ANCHOR Physics D2: Score-I - Test 12 p1_phy_s2_q05: 1 1 0 0 F1: work-energy theorem with W=F.d, one line
ANCHOR Physics D5: Score-I - Test 12 p2_phy_s2_q03: 2 2 1 0 F1: circular path in B, R^2=a^2+(R-d)^2 then p=qBR
ANCHOR Physics D8: Score-I - Test 12 p2_phy_s2_q04: 2 3 2 1 F1: alpha and recoil ion in B field, equal radii circles, angular-speed ratio 24 gives meeting at 2pi*24/25
ANCHOR Chemistry D3: Score-I - Test 12 p2_chem_s2_q01: 1 2 0 0 F1: recall count of essential amino acids
ANCHOR Chemistry D7: Score-I - Test 12 p1_chem_s1_q06: 2 4 0 1 F1: AgCl solubility in water, AgNO3, NH3 (Ksp*Kf), four options each worked
ANCHOR Mathematics D4: Score-I - Test 12 p1_math_s3_q10: 1 2 1 0 F1: area of [x][y]=2 as four unit squares
ANCHOR Mathematics D8: Score-I - Test 12 p1_math_s3_q09: 2 4 1 1 F1: differentiability of piecewise function with [x^2] and tan(pi[x^2]); continuity and derivative match at x=1

## 2026-10-23 TOAS - Test 01 (30 Jan 2022)
- 147 questions (the conversion note says 168; the .tex has 147: P1 19+19+19, P2 30+30+30). 126 from key, 21 solved. Difficulty: Easy 53, Medium 64, Hard 27, Very hard 3.
- Key layout (one page, 2 papers): MCQ rows Q1-Q10 (P1) / Q1-Q20 (P2) and a numeric row per subject. P1 numeric rows list section-II passage questions and section-II(ii) questions together; Physics P1 omits passage Q1, Q3, Q5, and the P2 Chemistry numerics list only Q2 and Q5, P2 Mathematics numerics are missing altogether, so those were solved. One stray letter ("Q4 A") sits in the P1 Mathematics numeric row: ignore it.
- Key vs paper: p2_math_s1_q03 prints "<0" but the key (D, sum 8) needs "<=0" (conversion lost the equal sign); p1_chem_s2_q05 option A prints PQ3S4R3 but R4S3 is what counts (key A kept); the printed key value "205.00 to 210..." of p1_phy_s3_q02 is truncated (computed 207).
- Subtopic labels used as-is; no new ones. Passage groups need ONE chapter in chapters.tsv (apply refuses mixed chapters in a group).
- Spot checks done: all P1 MCQ and numeric key entries re-derived, P2 physics and chemistry MCQs re-derived; no disagreement.
ANCHOR Physics D1: TOAS - Test 01 p1_phy_s1_q02: 1 1 0 0 F0: PE of SHM oscillates at twice the frequency
ANCHOR Physics D6: TOAS - Test 01 p1_phy_s2_q10: 2 3 1 0 F1: ball in accelerated liquid, effective gravity and relative acceleration 3 g_eff, geometry gives a and t
ANCHOR Chemistry D2: TOAS - Test 01 p1_chem_s4_q08: 1 1 0 0 F1: radius ratio 0.837 gives coordination number 8
ANCHOR Chemistry D5: TOAS - Test 01 p1_chem_s2_q07: 2 3 0 0 F1: four B2 configurations judged against aufbau, Hund, Pauli and s-p mixing
ANCHOR Mathematics D2: TOAS - Test 01 p2_math_s1_q08: 1 2 0 0 F0: a1 and a2 of (1-x^2+x^3)(1+x)^n substituted into a1^2-a1-2a2
ANCHOR Mathematics D6: TOAS - Test 01 p1_math_s2_q07: 1 3 1 1 F1: sum r C(100,r)^2 by r C(n,r)=n C(n-1,r-1) and Vandermonde, option A rewritten

## 2026-10-23 TOAS - Test 02 (13 Feb 2022)
- 54 questions (one paper, 18 per subject: s1 6 single, s2 6 multiple, s3 6 numerical). 37 from key, 17 solved. Difficulty: Easy 5, Medium 21, Hard 26, Very hard 2.
- Key (one page): Physics complete. Chemistry lists only s1 Q1-Q6 and numeric Q2 (53.25): the 6 multiple-correct and 5 numericals were solved. Mathematics: s1 Q1-Q6 and s2 Q7-Q12 usable (re-derived several), but the numeric block prints letters (C A B D B) instead of numbers: ignored, all six numericals solved.
- Ambiguities settled and noted in working: chemistry s3 q01 reads "face centres not opposite to each other" as three mutually adjacent faces (density 40); phy s2 q07 P is the pole of the curved face in (i) and the flat face in (ii) (only A true).
ANCHOR Physics D4: TOAS - Test 02 p1_phy_s1_q04: 2 3 0 0 F0: Snell at top face then TIR condition at vertical face
ANCHOR Physics D7: TOAS - Test 02 p1_phy_s3_q03: 2 3 1 1 F1: prism with delta=i=2 alpha gives e=alpha, two Snell relations eliminated to cos^2 alpha=(mu^2-1)/8
ANCHOR Chemistry D1: TOAS - Test 02 p1_chem_s1_q02: 1 1 0 0 F0: pure silicon is an intrinsic semiconductor
ANCHOR Chemistry D6: TOAS - Test 02 p1_chem_s1_q06: 2 4 1 0 F0: count stereoisomers (incl. linkage isomers) of four octahedral complexes
ANCHOR Mathematics D5: TOAS - Test 02 p1_math_s1_q02: 2 3 1 0 F0: range [-4,3) of (3x^2+ax+b)/(x^2+1) via discriminant, a=0 forced because 3 is excluded
ANCHOR Mathematics D7: TOAS - Test 02 p1_math_s1_q01: 2 4 1 1 F0: rectangular hyperbola, tangents of slope 2, asymptote intersections, quadrilateral area

## 2026-10-23 TOAS - Test 03 (27 Feb 2022)
- 108 questions (P1 and P2, 18 per subject each). 100 from key, 8 solved. Difficulty: Easy 16, Medium 56, Hard 34, Very hard 2.
- Key (one page) is complete except Physics P1 s3 Q4, Q5 (solved: 2 and g/3=3.33) and Chemistry P2 s2 (only Q3 keyed; Q1, Q2, Q4, Q5, Q6 solved). In Paper 2 the key prints the SECTION-III integer block BEFORE the SECTION-II decimal block (Physics: 6 9 3 7 3 9 then 2.40 ...; Mathematics: 0.50 ... then 8 1 2 ...): mapped by content, not position.
- Key disagreement: p1_math_s3_q06 prints 2.00 but with real a, b, c the constraint b <= -3/2 gives 2.25 (key ignores the realness condition); stored 2.25 as solved with working. p1_math_s3_q02 prints no value for k (domain question), key 4.00 kept unverified.
- Spot checks done on all P1 and P2 mathematics, P1 physics and chemistry numericals and many MCQs; only the item above disagreed.
ANCHOR Physics D3: TOAS - Test 03 p1_phy_s1_q02: 1 2 1 0 F0: SHM PE proportional to displacement squared so sqrt(E)=sqrt(E1)+sqrt(E2)
ANCHOR Chemistry D4: TOAS - Test 03 p1_chem_s2_q12: 1 3 0 0 F1: Fajans' rules applied to four solubility / thermal stability statements
ANCHOR Mathematics D3: TOAS - Test 03 p1_math_s1_q02: 1 2 1 0 F0: |tan^-1 x|+|cot^-1 x|=pi/2 holds only for x>=0

## 2026-10-23 TOAS - Test 04 (15 Mar 2022)
- 114 questions (19 per subject per paper, 24 passage groups, sections up to s4 = SECTION-II(ii)). 110 from key, 4 solved. Difficulty: Easy 8, Medium 27, Hard 71, Very hard 8.
- Key page complete except Chemistry P2 s3 Q1, Q2, Q5, Q6 (solved: 3, 8, 1, 2). Stray letters in numeric rows (Physics none; Mathematics P1 "Q3 C, Q4 B"; Mathematics P2 "Q2 B,C,D / Q3 A,C / Q4 A,C,D / Q5 A,C") were ignored; the MCQ entries printed in the main MCQ row were re-derived and match.
- Conversion typos worth knowing: p1_math_s1_q02 prints sqrt(x - sqrt(lambda)) where the source has sqrt(x)-sqrt(lambda) (key B with lambda=2 matches the source form); p2_chem_s4_q08 prints "0.4 meV" but the key (13) needs 0.4 MeV.
- Judgement calls: p2_chem_s3_q06 treats benzyl alcohol as reacting immediately with Lucas reagent (statement (i) false), so answer 2.
ANCHOR Physics D9: TOAS - Test 04 p2_phy_s4_q07: 3 3 2 1 F1: particle leaves the circle at B, projectile returns to string-taut point C diametrically opposite; speed condition at A
ANCHOR Chemistry D8: TOAS - Test 04 p1_chem_s2_q07: 2 4 1 1 F1: three gases with equal masses and movable pistons: mole ratios, final pressures and piston positions, four statements
