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

## 2026-10-23 TOAS - Test 05 (03 Apr 2022)
- 144 questions (P1: 8 multi + 4 single/matching + 6 numeric per subject; P2: 20 single MCQ + 10 numeric per subject). 133 from key, 11 solved. Difficulty: Easy 26, Medium 60, Hard 51, Very hard 7.
- Key page: complete for all MCQs; numerics missing for Physics P2 Q7 and Chemistry P2 Q1-3, Q10 (solved), and the whole Mathematics P2 numeric block prints letters (Q3 A, Q4 D, Q5 C, ...) except Q1=7, Q2=2, Q7=8, Q10=7: kept those four, solved the other six; the extra letter row for Q12-Q20 in that block was ignored. Mathematics P1 has stray "Q7 B,C / Q8 A,D" after the numeric row (the MCQ row already gives Q7 A, Q8 A,B,C,D; Q7 re-derived as A).
- Solved answers where a judgement was needed: chemistry P2 s2 q02 counts enantiomers (4), q01 treats benzylic and cyclopropyl-carbinyl alcohols as immediate Lucas positives (5).

## 2026-10-23 TOAS - Test 06 (17 Apr 2022)
- 54 questions (one paper: 4 single, 8 multiple, 6 numeric per subject). 49 from key, 5 solved. Difficulty bands as stored in the data zip.
- Key: complete for Physics and all MCQs; Chemistry numerics only Q1, Q2 keyed (Q3-Q6 solved: 5, 4, 0.17, 3); Mathematics numeric Q4 prints a letter (solved: 1); Mathematics Q5 key "1.87 or 1.88" kept as printed.
- Physics s3 q01 only makes sense with the two sources on opposite sides of the lens (real image of one = virtual image of the other): 18 + 6 = 24 cm.
ANCHOR Chemistry D9: TOAS - Test 06 p1_chem_s2_q12: 2 4 2 1 F1: stereoisomer and geometrical-isomer count of [Co(gly)2(CN)Br]+ including linkage of CN
ANCHOR Mathematics D9: TOAS - Test 06 p1_math_s2_q07: 2 4 2 1 F1: two pairs of lines with common bisectors form a kite/rhombus; range of its area over K

## 2026-10-23 TOAS - Test 07 (01 May 2022)
- 114 questions, all 114 from key (one-page key complete; each paper's numeric rows are in section order s3 then s4). Stray letters in the Mathematics numeric rows (P1 "Q3 D, Q4 C"; P2 "Q4 B,C / Q5 A,C / Q6 A") ignored. Re-derived: Physics P1 s3 q01-02 (1.2 s, 48 m), chemistry p1 s1 q03/q04 and s3 q03/q04, mathematics p1 s1 q01, s3 q03/q04.
- Difficulty scores for this test were assigned in one pass from the question statements; solution-level re-derivation was done for the spot checks only.

## 2026-10-23 TOAS - Test 08 (15 May 2022)
- 108 questions (18 per subject per paper: 6 multiple, 4 passage-based single, 8 numeric). 98 from key, 10 solved (chem P1 q06/q07, math P1 s3 q02-q06 (the key prints letters there), math Paper 1 q05... see data zip). Difficulty scores are single-pass estimates from the statements; many questions are multi-statement and score S4.
- Judgement calls: chem p1 s3 q06 counts only aldehydes giving a racemic alcohol from an achiral carbonyl (3); math p1 s3 q02 lower bound 11 roots gives 11/3 = 3.67 (key letter row unusable).
## 2026-10-23 TOAS - Test 09 (30 May 2022)
- Key: one page for both papers; P2 numeric rows had junk letters and several omitted items (solved 30 numerics). P2 chem s2 q09 key says 1 but solving gives 0.50 (stored solved value).
- Difficulty was assigned with section defaults plus manual overrides; reasons are generic, recheck if rescoring.
## 2026-10-23 23:20 AUDIT - difficulty re-score
- Independent audit (TOAS 04, 07, 08): chapters, subtopics, answers OK; difficulty inflated ~2 points and defaulting to S3/S4, I1. All ANCHOR lines above this entry are VOID. Read BANK_LEARNINGS.md CALIBRATION. bank_tools apply now requires reasons "concepts: ... | steps: ..." and checks K and S against them. Every test banked so far has fix_note "rescore difficulty". New anchors: ANCHOR [v2] ...
## 2026-10-23 build notes
- Build compile failures seen: unescaped % in diff_note (comments out the closing brace; write "percent"), bare x^2 outside $ in a working, and `\[\begin{aligned}&` (use `\begin{aligned}{}&` or inline math). Check these before pack.
## 2026-10-23 rescoring pass (TOAS 01-09, Score-I 12)
- All ten banked tests were rescored under the CALIBRATION rules (concepts | steps format). Bands now run roughly Easy 55-75 / Medium 20-30 / Hard 2-8 / Very hard 0 per paper; do not inflate to hide this.
- Write reasons without % or | characters; build breaks on unescaped % in the note (use the word percent).
- Anchor-style identical questions recur across tests (e.g. cyclic functional equations, silvered lenses, HOMO symmetry, EAN counting): keep their factors equal.
## 2026-10-23 TOAS - Test 10 (12 Jun 2022)
- One paper only (60 q: per subject 8 multi + 4 paragraph + 8 numeric). Key is one page; math numeric rows print junk letters (Q3, Q5-Q8): solved those. Phys numeric Q7 missing from the key: solved from the figure.
- Key mismatches found: chem numeric Q8 (key 4, solved 3), math paragraph Q10 (key A,B,C, solved A,B,C,D), Q11 (key B,C,D, solved B).
## 2026-10-23 TOAS - Test 11 (27 Jun 2022)
- Two papers; key one page with Paper-1 and Paper-2 sections per subject; P2 math key row has a stray "Q8 B,C" after the numerics (ignored). Phys P1 numeric Q3 was missing from the key: solved from the figure (8 V). All other keys spot-checked against solutions (a slip of mine on math P1 numeric Q2 turned out to be the key being right: minimum of (x-3)e^x is -e^2).
## 2026-10-23 TOAS - Test 12 (10 Jul 2022)
- Two papers, key one page. Paper 1 phys numeric Q8 missing from the key (solved: 0.48). Paper 2 math numeric Q2-Q6 print junk letters (B A D C D plus repeated MCQ rows): solved 5, 6, 0.41, 2, 2.11; numeric Q1 1.00 is printed.
- p1_phy_s2_q05 (rotating charged disc, 5 m on the axis, R = sqrt39 m): printed key 17.66 pT, but the standard on-axis formula gives 10.6 pT (stored as solved).
## 23 Oct 2026 TOAS - Test 13 (24 Jul 2022)
- Key is one page for both papers. P1 maths numeric row prints letters for Q3-Q6 (junk) - those four solved (0.95, 8, 1, 0). P2 maths numeric block keeps only Q1-Q3 (1600, 1, 10.00) and then letters; Q3 10.00 is wrong (A+B = 1/3), so Q3-Q10 were solved. P2 chemistry numeric row is labelled Q1-Q7 and Q10 only: Q8 and Q9 solved. Key values 3, 13 and 6 are nearest-integer roundings of 3.1, 12.5 and 6.3.
- Spot checks (phys P1 Q5 and numeric Q5, chem P2 Q1, maths P1 numeric Q2) all agreed with the key.
- New subtopic label: P17 "Superposition of SHMs" (used for p2_phy_s1_q13).
- Placements: Rosenmund + Cannizzaro, Grignard + nitrile, Dieckmann sequences go to the chapter of the main reaction type (C20, C16, C21).
ANCHOR [v2] Physics D1: TOAS - Test 13 p2_phy_s1_q06: 1 1 0 0 F0: concepts: SHM energy | steps: displacement at T/6 is A/2; KE:PE = 3:1
ANCHOR [v2] Chemistry D2: TOAS - Test 13 p2_chem_s1_q01: 1 2 0 0 F0: concepts: Hess law | steps: reverse and halve the first equation; double the second; add
ANCHOR [v2] Mathematics D2: TOAS - Test 13 p2_math_s1_q03: 1 1 1 0 F0: concepts: second derivative of the inverse function | steps: d2x/dy2 = -y''/y'^3; evaluate at x = 1
ANCHOR [v2] Physics D5: TOAS - Test 13 p1_phy_s2_q08: 2 2 1 0 F1: concepts: work-energy with friction, motion under a magnetic force | steps: path length from the energy; time; spiral not circle; stopping displacement depends on B
ANCHOR [v2] Chemistry D6: TOAS - Test 13 p2_chem_s2_q02: 2 3 1 0 F1: concepts: depression of freezing point, relative lowering of vapour pressure | steps: molality; moles of sugar; remaining water from 700 torr; ice moles and grams
ANCHOR [v2] Mathematics D6: TOAS - Test 13 p1_math_s3_q01: 2 2 1 1 F1: concepts: pencil of conics through four points, parabola condition | steps: family from two line pairs; h^2 = ab; perfect-square quadratic part; axis slope
## 23 Oct 2026 TOAS - Test 14 (07 Aug 2022)
- Single paper (60 questions: 20 per subject), key one page. Math key blocks are printed out of order (the section-III values 1,2,6,5,3,1 come before the section-II values 0.50, 4.00, 49.50, 0.35 or 0.36, 1009.00, 6054.00) and a stray "Q8 A,B,D" row sits between them; all twelve numerics and the eight MCQ were re-solved and matched the key by content, the stray row ignored (math Q8 is A,B).
- Chemistry Q8 (MnO4- + Mn2+): key prints A,B,C but option A calls it disproportionation, which it is not (comproportionation); banked as solved B,C with the reason.
- Chem section III Q3 (HBr entropy, digit sum): delta U = delta H - delta n RT = 104490 J gives 348, digit sum 15 -> 6, matching the key.
ANCHOR [v2] Physics D3: TOAS - Test 14 p1_phy_s3_q06: 1 1 1 0 F1: concepts: motional emf in the field of a straight current | steps: v cross B along z is perpendicular to the wire so no emf
ANCHOR [v2] Chemistry D4: TOAS - Test 14 p1_chem_s2_q02: 1 2 0 1 F1: concepts: buffer pH from the Henderson equation | steps: moles of acid and acetate after reaction; pKa from Ka; log ratio
ANCHOR [v2] Mathematics D8: TOAS - Test 14 p1_math_s2_q04: 2 3 2 1 F1: concepts: symmetry of a composition, property of definite integrals | steps: f(1-x) = 1 - f(x); f(f(1-x)) = 1 - f(f(x)); pairs sum to 1 over a symmetric interval; half the length
## 23 Oct 2026 correction (TOAS - Test 14 anchors)
- The anchor line "ANCHOR [v2] Mathematics D8: TOAS - Test 14 p1_math_s2_q04: 2 3 2 1 F1" is VOID: the stored factors are 2 2 2 1 (four steps listed) = D7. Use instead: ANCHOR [v2] Mathematics D7: TOAS - Test 14 p1_math_s2_q04: 2 2 2 1 F1: concepts: symmetry of a composition, property of definite integrals | steps: f(1-x) = 1 - f(x); f(f(1-x)) = 1 - f(f(x)); pairs sum to 1 over a symmetric interval; half the length
- Lesson: copy anchor factors from the applied work/questions.json (diff_kSIC, difficulty), not from the diff file, because mk.py recomputes S from the step count.
## 23 Oct 2026 correction (TOAS - Test 13 anchor)
- The anchor line "ANCHOR [v2] Chemistry D6: TOAS - Test 13 p2_chem_s2_q02: 2 3 1 0 F1" is VOID: stored factors are 2 2 1 0 (four steps) = D5. Use instead: ANCHOR [v2] Chemistry D5: TOAS - Test 13 p2_chem_s2_q02: 2 2 1 0 F1: concepts: depression of freezing point, relative lowering of vapour pressure | steps: molality; moles of sugar; remaining water from 700 torr; ice moles and grams
## 23 Oct 2026 TOAS - Test 15 (22 Aug 2022)
- Key page for both papers is incomplete: P2 physics section I lists only Q1-Q2 (Q3-Q6 solved: A,B,D / A,B,D / A,B / B,C); P2 chemistry section I MCQ are missing entirely (all six solved) and section II Q3 is missing (solved 7). Numeric blocks of P2 are printed in the order section III then II (e.g. phys 1,5,1,3,2,1 then 0.37,...), mapped by solving. P1 maths numeric Q3-Q6 are letters (junk): solved 5, 0.74 (2/e), 0.74 (2/e), 0.
- P1 chemistry Q5 ("which set is correct", key B) reads as an INCORRECT-type question (Hall-Heroult is electrolysis); key kept as printed.
- P2 chemistry S1 Q1 (HVZ) taken as multi-correct (B,C) since both acids have an alpha hydrogen.
## 23 Oct 2026 TOAS - Test 16 (04 Sep 2022)
- Passage test with sections I(i), I(ii), II(i), II(ii) in each paper. Key is one page; the numeric blocks skip entries (P1 phys Q5 of the third block, P1 chem S3 Q1-Q3 and Q5, P2 phys S3 Q1/Q3/Q5, P2 chem S3 Q3): all solved. Stray letter entries inside the maths numeric rows (P1 "Q3 D Q4 A", P2 "Q2 A,C,D Q4 B,C Q5 A,D Q6 B,C,D") are junk and were ignored; the numeric values were re-solved and match.
- P1 physics Q4 (solenoid tensile limit): derived I_max = sqrt(2F0/(mu0 n R)) (option D) from p = mu0 n^2 I^2 / 2; the printed key A lacks the factor 2; banked as solved D.
- P1 chem S3 Q2 (nitroprusside linkage isomers) banked as 1 from two linkage isomers of NOS; no key printed.
## 23 Oct 2026 TOAS - Test 17 (18 Sep 2022)
- Key page fully usable for MCQ (matching-type questions are keyed as letters). Maths P2 section II numerics Q5-Q8 and Q10 print letters (junk): solved 15, 9 (P1 not affected), 12, 120, 1; P2 chemistry section II key skips Q2, Q7, Q9, Q10 (CO2 count 4 and the three abc matches 321, 213, 321 solved). The stray row "Q11 D Q12 C ..." after the maths numerics is junk.
- P1 maths numerics: key prints a sixth entry "Q6 A,C,D" for a five-question section: ignored.
## 23 Oct 2026 TOAS - Test 18 (30 Oct 2022)
- The answer-key page is headed PAPER-2 and holds only Paper 2 (4 single + 6 multi MCQ, 8 numerics per subject); Paper 1 has no key at all: all 54 Paper 1 answers were solved (marked solved with working). Paper 2 answers were taken from the key after spot checks in all three subjects (chem Q2 0.5 K, phys Q3 B, maths numerics Q1 1, Q4 4, Q7 2 all agree). A stray "Q7 B,C Q8 A,B,C,D Q9 A,B,C Q10 A,C" row after the P2 maths numerics duplicates MCQ labels and was ignored.
- Judgement calls in the solved Paper 1: phys Q3 (errors) comes to about 11 percent so C and D are false (banked A only); chem s3 Q1 uses the 4 Cr=O, 2 Cr-O- structure of dichromate (44); chem s3 Q2 borax counted with the 8 water molecules (9.5).
## 23 Oct 2026 TOAS - Test 19 (05 Feb 2023)
- The key page lists two papers and only the PAPER-2 block belongs to this converted test (one paper of 54 questions: 8 multi + 4 matching + 6 numeric per subject); the PAPER-1 block is a different paper (20 MCQ per subject). Identified by structure and by the numerics (chem 5.35, 173.20, 34.04, 21.95; phys 2.25, 0, 6, 10) matching solved values. Maths numerics Q5-Q6 and the trailing letters in that row are junk: solved 5 and 50.
- Disagreements: phys Q12 (key C, banked solved D after recomputing: a = 6, T1 = 12, T2 = 8); chem Q4 key A,C kept as printed (my hydrolysis count gives D as incorrect too).
## 23 Oct 2026 build of 20 tests
- Build failed on 7 chapters with "Missing $ inserted": working and diff_note are written raw into the .tex, so a bare _ or ^ outside $...$ breaks the compile. Fixed by escaping _ and ^ outside math in questions.json of every data zip (done once for all 19 affected tests). When writing working text, put every formula in $...$ or avoid _ and ^ entirely; mk.py does not escape them.
## 23 Oct 2026 TAAS - Test 01 (18 Jun 2023)
- Key page again carries both papers; the converted test (12 MCQ + 6 numerics per subject, single-correct section first) is the PAPER-1 block (phys Q1 B = 7.43 s checked). Phys numerics Q5 and Q6 are missing from the key (solved 3 and 0.2). Maths PAPER-2 numeric row carries junk letters.
## 23 Oct 2026 TAAS - Test 02 (30 Jul 2023)
- Both papers of the test are converted (102 questions); key page carries both blocks and every section maps cleanly (P1: 4 single, 3 multi, 4 matching, 6 numerics per subject; P2: 4 single, 3 multi, 10 numerics). The P2 maths numeric row has three stray letters (D, A, B) inside it; the ten numerics were read around them (1, 2, 0.5, 2, 17, 3, 0, 1, 11, 6). Spot checks (phys P1 Q numerics, chem P1 occupancy 96, maths P1 lambda 8, P2 maths Q3 0.5, P2 phys 9) agreed with the key.
## TOPS - Test 01 (31 Jul 2022)
- Key page did not auto-match; answers entered by hand from the key (52 key, 2 solved: maths S3 q5 answer 1 by AM-GM equality, q6 = 44/9 = 4.89).
- Mostly constraint and friction mechanics, bonding and sequence/log maths. Passage groups need one chapter each (P02, P01, C30, M01, M03).
- Pitfall: finish.sh ran after a failed `apply` (wrong tools path) and marked the test done without a zip. Always run apply from the repo root with tools/bank_tools.py and check "difficulty missing 0" before finish.sh.
## TOPS - Test 02 (28 Aug 2022)
- Two papers (108 q). The key prints Paper-2 numerics with Section III before Section II; matched by solving (air time 3.60 and Section II values 12/286 on the maths side). Verify the section order against a worked numeric before banking.
- Missing numeric keys solved: p1 phys s3 q4 (1.20), q6 (7.07), p2 phys s2 q2 (16.67), p2 math s2 q5 (1.80).
- mk.py writes nothing if any KMISMATCH appears: fix K in the diff file to the concept count and rerun, then confirm work/difficulty.tsv exists before apply.
## TOPS - Test 03 (20 Nov 2022)
- Key rows for Paper 2 numerics again list Section III before Section II: confirmed by solving (math s2 q1 = 0.50 via telescoping; phys s2 q6 work = 0.50 J). Paper 1 key has no entries for physics s3 passage numerics and math s3 q1, q2: solved (physics: plate k, bicycle chain, wedge blocks; maths: 3 and 3).
- Chem p1 s3 q3 key 70.32 is degrees and minutes (70 deg 32 min = 70.53 degrees).
- Passage group ids go in chapters.tsv alongside the question ids.
## TOPS - Test 04 (18 Dec 2022)
- 147 questions, 15 passage groups; Paper 2 is 20 single-correct plus 10 numerics per subject. The key lists only some numerics (and prints letters in a numeric row): solved the missing ones (phys 6, chem 5, maths 4).
- p1_chem_s4_q09 key prints 0 but the list has at least 8 non-existent species; banked solved 8. Repeats of TOPS 03 question (determinant T n) exist: duplicates merge in the build.
- I must be 0-2 in the diff file; mk.py silently writes nothing on a K mismatch, and apply reports 'difficulty missing' for I=3 rows.
## TOPS - Test 05 (14 Jan 2023)
- Maths Paper 1 Section II key printed letters in numeric slots (Q3-Q6); those four were solved (15, 0.25, 1.5, 1.58). Matching-type questions are banked as single option letters from the key.
- p1_phy_s3_q08 key 4.22 mm does not fit the stated alpha (11e-6 gives 3.96 mm); banked solved.
- Difficulty tip: I is 0-2, not 3; keep I=2 for genuinely hard insight steps only (this paper's I values were rated generously).
## TEAS - Test 01 (16 Apr 2023)
- Key page holds two papers (Paper 1 main style, Paper 2 advanced style); the converted test is the advanced-style Paper 2 (6 MCQ + 4 passage + 8 numeric per subject): use the second block.
- Missing chem numerics solved (X/Y = 2; isomers of Pt complex = 14; froth flotation = 3 with CuSO4 as the only activator; reactions matched = 5).
## TMAS - Test 01 (09 Jul 2023)
- Single-correct Paper 1 (20 MCQ + 10 numeric per subject) plus a Paper 2 with matching passages (3-column tables, three questions per passage). Key lists all MCQ letters and some numerics; solved the missing physics (4) and chemistry (7) numerics.
- Chem p1 s2 q10 (identify A from the picture only): the picture shows just a chloroketone; banked 132.5 as solved and unverified. p1_chem_s2_q07 key 8 implies the cell volume unit 1e-28 m3, not 1e-27 as printed.
- Reading budget: this test cost far more than earlier ones (144 questions); keep each diff entry short.
## TMAS - Test 02 (06 Aug 2023)
- The key page covered Paper 1 only (plus one Paper 2 maths item); all 57 Paper 2 questions were solved by hand with working. Matching/passage answers were derived by solving each row of the table.
- p2_chem_s3_q04 (figure sequence) is a best-effort reading (3) and should be treated as lower confidence.
## Build note (30 tests)
- LaTeX build failure: a stem with `\begin{aligned}&\sqrt{...}` or `&\underbrace{...}` (an `&` directly after `\begin{aligned}`) fails with "Missing control sequence inserted". Fixed in data/TOPS - Test 01 by removing that leading `&`. If a chapter fails, extract its zip from the build output, compile it, and look at the line named in the error.
## TMAS - Test 03 (10 Sep 2023)
- Physics-only test with 35 questions and no answer key at all: every answer solved with working. Subtopics must come from the chapter list (`new:<label>` only when none fits); P18 uses 'Waves on a string', 'Standing waves' etc.
- p1_phy_s3_q06 depends on the figure (block directions assumed as drawn, same direction); p2_phy_s2_q10 and p2_phy_s4 answers rely on reading the figures.
## TMAS - Test 04 (19 Nov 2023)
- Two-paper layout (Paper 2: 6 MCQ + 6 + 6 numerics per subject) with key rows listing only some numerics; missing numerics solved (phys 4, chem 2, p2 phys 5).
- Process fix: `apply` prints "ERROR ... subtopic not in list" for labels outside tools/subtopics.json yet still writes them; always read ALL output lines of apply before packing. 39 earlier questions with off-list labels were remapped (e.g. C20 Aldehydes to Nucleophilic addition, M24 Tangents to Tangents and normals, M23 Rolle's theorem moved to M24 Mean value theorems).
## TNAS - Test 01 (05 Feb 2023)
- 144 questions (JEE Main style Paper 1: 20 single-correct + 10 numeric per subject; Paper 2: advanced style with matching tables). Several numeric keys missing (chem Paper 1: 7); solved with working. A few stray letter entries after the numeric rows of the maths key (Q14, Q15, Q17, Q20) do not match the MCQ answers and were ignored after verifying Q14 by direct count.
- p1_chem_s2_q05 key 72 means the maximum pressure (vdW with a=2, V free); p2_math_s3_q05 key row had two stray letter groups; solved.
## TNAS - Test 02 (07 May 2023)
- Key page is complete for MCQ and most numerics; solved the missing physics ones (mirror speed factors, tunnel time 800 pi s, capacitor work, grounding heat). Stray letter groups after numeric rows again ignored.
- Group chapter lines can be generated from the first question of each group (script mk33.py pattern) to save effort.
## TNAS - Test 03 (28 May 2023)
- Efficiency tool (reusable): match each new question against banked questions (bank_tools.fingerprint + similar, same numbers and figure count, similarity >= 0.93) and reuse the stored chapter, subtopic, answer, working and difficulty. 42 of 144 questions here (almost all maths) were inherited this way; the rest were keyed from the printed key or solved. Cross-check inherited answers against the printed key.
- Key quirks: stray capital letters in numeric rows (D, C, D for maths) are ignored when the question is inherited or solvable.
TNAS Test 04 (18 Jun 2023): the physics numeric key rows were incomplete (only two of six printed), so four numerics were solved by hand. The P2 maths numeric row mixes in stray letter answers (junk). Printed a^3 in the shell-conduction question is a misprint for a^2. 35 of 108 questions were reused from banked duplicates.
TNAS Test 05 (09 Jul 2023): the key lists numerics only for Q1-3 of Paper 1 Chemistry section II, so four were solved by hand (p1_chem_s2 q04, q07, q09, q10). The P1 maths numeric row carries stray letters for Q7-Q10 (junk), so q08 and q09 were solved. p2_phy_s3_q01 key says 0 (zero tension at A); banked as keyed. Printed a^3 style misprints were not present. 43 of 144 questions were reused from banked duplicates.
TNAS Test 06 (30 Jul 2023): the key page is scrambled and truncated for Paper 1 (about 20 answers missing in physics and chemistry, and Q4/Q5 of physics section IV). Missing ones were solved by hand: p1_phy s1_q03, s3_q09-q11, s4_q04-q05; p1_chem s1_q01, s1_q04, s3_q08-q11 and s4_q01-q06. Paper 2 maths was entirely reused from banked duplicates (35 of 102 matched). Stray letters (Q2 D, Q3 C) among the Paper 2 maths numerics are junk.
TNAS Test 07 (20 Aug 2023): Paper 1 numerics were partly missing from the key (physics Q1-2, chemistry Q1-3, Q8, Q10, maths Q5-7 and Q10 carry stray letters or nothing), and Paper 2 maths numerics Q4-6 were missing. All were solved by hand. Only 4 of 144 questions matched earlier banked tests.
Star Review (Other) Test 01 (12 Sep 2022): key page labels are shuffled in the numeric rows (a row can start at Q7 or skip numbers) and some letter answers appear among numerics (junk). Missing numerics solved by hand: p1_phy_s3_q03, p2_phy_s2_q05, and p2 chemistry Q5-Q10 and p2 maths Q3-Q8, Q10. p2_math_s2_q10 is printed as nested cube roots ending in a product; read as the nested cube root of (3 times the next radical) giving y=3. Only 3 of 147 questions matched earlier tests.
Star Review (Other) Test 02 (10 Oct 2022): the key omits p1_phy_s3_q08, p1_chem_s3_q05 and q08 (solved by hand). Key ranges (8.98 to 9.00, 3.46 to 3.47, 55.61 to 55.66, 1.57 to 1.58) were banked as midpoints. Only 2 of 108 questions matched earlier tests.
Star Review (Other) Test 03 (04 Dec 2023): key was complete for all questions. It lists stray letter answers (P2 maths Q4-Q6) next to the numeric row; they disagree with the main row (the vector triple product item is zero, so A,B,C,D) and were ignored. Key ranges (163 to 165, 1.85 to 1.95, 0.28 to 0.29, 0.13 to 0.14, 0.66 or 0.67) were banked as midpoints. Only 4 of 114 questions matched earlier tests.
Internal Test 01 (05 Aug 2020): the duplicate matcher wrongly matched two figure-only chemistry questions (p1_chem_s1_q02 and q03) to older tests; the figures differ, so the older answers disagreed with this key. They were re-banked from this key and solved by reading the figures. Be careful with duplicate matches on questions whose text is only figures: compare the figures before reusing an answer. Key was complete for this test.
Internal Test 02 (07 Jul 2021): the source PDF is a full solutions paper with no key table (keyprep prints "no key table, but solution pages exist"); the answers were read as the printed "Ans." lines in order (text extraction with pymupdf, grep Ans) and checked against several solutions. dup.py now skips figure-only questions with short text, because they gave false duplicate matches. 0 of 54 questions matched earlier tests.
Internal Test 03 (08 Sep 2021): keyprep warns that the key text has 3 runs of 6 values; answers were written by hand from the text rows (12 letters + 6 numerics per subject) and spot checked by solving p1_phy_s1_q04 and p1_math_s2_q10. Key was complete. 0 of 54 questions matched earlier tests.
Nurture SRG Test 02 (06 Dec 2023): the key file holds only ONE subject (18 answers, physics); chemistry and mathematics (36 questions) were solved by hand, with Python counts for the combinatorics (rooms 2220, triplets 46, nine digit numbers 1960, GP count 39, trailing zeros 1). The one duplicate match (p1_chem_s2_q06 vs Score-I 12 p1_chem_s1_q06) differs in option A (mole/litre here, gm/litre there), so its answer was re-solved as A,C,D; the matcher ignores such word changes, so check options of matched chemistry questions with numbers or units.
Nurture SRG Test 03 (04 Feb 2024): the printed key page is a scrambled union of different subjects (rows of physics Paper 1, chemistry Paper 1, maths Paper 2 and unattributed numerics) with no subject headings. Rows were attributed by solving: P1 physics Q1-10 and chemistry singles matched; P2 maths letters (singles Q1-4, multi Q5-12) matched; numerics of Paper 2 maths only matched for Q1=8 and Q2=161. Everything else (physics Paper 2, chemistry Paper 2, maths Paper 1, chemistry numerics) was solved by hand. Where the printed rows disagree with a worked solution the solved answer was banked: p1_phy_s3_q01 (1.5, key 15), q02 (11, key 13), p1_chem_s2_q09 (B,C,D, key A,B), p2_math_s1_q04 (D, key B), p2_math_s2_q12 (C, key B,C,D). Duplicate matcher found only 1 of 108.
Nurture (General) Test 01: no key and no solutions, so every answer is solved by hand. Paper 1 maths s2 q04 (greatest-integer table) has no strictly correct option (true match is (I),(i),(R)); banked B as the nearest. Paper 2 phys s3 q02 prints "1 mm" for the slab but the options only fit 1 micron. Group row chapters come from the first question of the group; qids in this test restart at q01 inside each section, so the group ids (g8_10 etc.) do not map to qids by number.
Nurture (General) Test 03: the key page holds physics only (20 MCQ + 10 numeric; the lower Q11-Q20 row repeats the MCQ answers, junk), so chemistry and maths are solved by hand. Maths s2 q01 prints 8x^9 in the numerator, for which no rational f exists; the standard problem has 5x^9 (f=x^10/2), banked 8. Chemistry s2 q07 headline says "oxidation electrode" but notations mix A,C (reduction form) and B,D (oxidation form); read per notation.
Nurture (General) Test 04: no key, no solutions; all solved by hand. p1_phy_s1_q04 options A and C are identical text (W=-(1/2)(1-n)n mg l), banked A. p1_chem_s2_q08 (bond length like C-O) and q10 (buffer pairs) are judgement calls from the stated chemistry; q08 banked A,B (aromatic zwitterion character).
Build warning: a working string containing a backslash followed by an apostrophe (e.g. f\') is read by LaTeX as an accent macro and broke the M22 chapter build. Write "f prime" or a plain apostrophe in working strings, never backslash-apostrophe.
Enthusiast Pre-Score Test 01: key page 1 is a clean combined key for Papers 1 and 2 (page 2 is a partial text copy). In Paper 1 the two sub-sections of Section-I run q01-06 (s1) and q07-12 (s2) in the key, Section-II numerics are s3. p1_math_s3_q01 asks |k/10| but the key prints 44.50 (=|k|); banked solved 4.45. Ranges "4.80 to 4.90" and "0.16 TO 0.17" banked as midpoints 4.85 and 0.165.
Duplicate matcher can false-match two different questions (Enthusiast Pre-Score 02 p1_phy_s2_q08 tunnel vs TOAS 09 satellite, same qid and same figure file name). After show.py, run `python3 /tmp/qb/chkpre.py` to compare the first 80 characters of each matched question against its source and drop any DIFF from pre_c/pre_a/pre_d before applying.
Score Advanced Test 02: no key, all solved by hand. Judgement calls: p2_math_s1_q06 (I_m/J_n integer parts) gives 1, 2, 4, 3 numerically, none of the printed options is right, banked D as nearest. p1_phy_s1_q02 uses a string angle of 1.8 deg from the vertical (printed horizontal); p1_phy_s1_q04 chem. p2_chem_s1_q07 banked A,C,D (strong heating of NaNO3 counted as two gases).
Score Advanced Test 03: no key; all 144 solved. The duplicate matcher false-matched three generic matching questions ("Which of the following options is the only CORRECT combination", options only (I)(i)(P) style) because the tables live in the group text, which the fingerprint ignores, and one figure-led gas question; all four were dropped and solved fresh (e.g. p1_math_s2_q06 is B here, C in the TOAS source). Whenever a matched id has generic or table-only text, drop the match. Gas-matching items p1_chem_s2_q01-03: the density data do not hit any printed P/RT value, so options were judged on Z=Vm P/RT alone. p2_math_s3 style: numeric answers entered as decimals (16/3 as 5.33).
Score Advanced Test 04: no key; all 144 solved (the three duplicate-matcher hits were dropped and solved fresh). Notes: p1_phy_s1_q09 water-jet force is 4.8 N (neither 1.2 nor 2.4 is offered; only D holds). p1_phy_s1_q07 option C is a judgement call. p1_phy_s3_q01 scenario T (ring with charged particle) matches none of the four statements. p1_math_s1_q03 only option A is a valid equally-inclined plane. A context compaction lost the unsaved answers once: save the answers table to a file as soon as a test is solved, not at the end.
Score Advanced Test 05: printed key on page 1 (text is clean, one row per subject section), banked as answer_src=key after spot-checking about 60 items by calculation. One mismatch: p1_math_s1_q02 asks for tan(beta)/tan(alpha) but the key D=24 equals the square of the true ratio (2*sqrt6); banked as D per key. build_t.py writes 'solved' rows: for a keyed test rewrite the third column to 'key' with sed/python before running ap.sh.
Score Advanced Test 06: printed key on one page (Paper-1 and Paper-2, key rows are clean in the text). Paper-2 Physics Section-II (8 numericals) has no key rows: solved by hand. p2_phy_s3_q02 (oil over water tank) gives no tank/orifice area ratio, so it is banked as Bonus. p2_chem_s3_q08 asks the initial excited state; the key value 1 means the first excited state (n=2). The three duplicate-matcher hits were exact text matches (ratio 1.0) but p1_phy_s3_q08 matched answer -6 while this key says 6 (work done against friction), so the key value was used for all three.
Score Advanced Test 07: complete printed key on one page (Paper-1 and Paper-2, all sections including Paper-2 Physics numericals); banked as key after computing about 25 items independently (all agreed). Only p2_math_s2_q09: key D lists 1/2 for both fourth-toss probabilities while exact values are 0.536/0.464, kept as key. Three duplicate-matcher hits (p1_math_s2_q09/q10, p1_math_s3_q06) were exact repeats of Score Advanced Test 04 / Test 06 questions and agreed with this key.
Score Advanced Test 08: key page text is scrambled (columns) but the page image is readable and the rows are complete except the following, which were solved by hand: p1_chem_s1_q02, p1_chem_s2_q09, p1_chem_s2_q12, p1_chem_s3_q01, p1_chem_s3_q02, p2_chem_s2_q05, p2_chem_s2_q06. Section order trap: in Paper-2 Chemistry and Mathematics the first numeric block on the key page is Section III (integers) and the decimal block is Section II (check one answer by calculation to tell which is which); in Paper-2 Physics the first numeric block is Section II. Disagreement with the key: p2_math_s1_q05 f(x)=x-3 is one-one, so statement A cannot hold; banked B,C (key printed A,B,C).
Score Advanced Test 09: printed key page text is clean and in order (Paper-1 and Paper-2). Paper-2 Chemistry Section-II key rows list only Q1, Q2, Q3, Q6, so q04 was solved (4 reagents) and q05 (lysine pI = 9.74) came from the matcher, whose text differs only in LaTeX. Answer ranges in the key such as -0.18 to -0.19 are banked as the midpoint.
