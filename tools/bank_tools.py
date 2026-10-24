#!/usr/bin/env python3
"""bank_tools.py - chapter-wise question bank built from the converted test LaTeX.

Commands (run with -h for options):
  chapters                      list the fixed chapter codes (Physics P.., Chemistry C.., Mathematics M..)
  parse  <test.tex> -o work     split a converted test into questions -> work/questions.json, work/list.txt, work/img/
  keyprep <src.pdf> -o key [--work work]
                                find the printed ANSWER KEY / solution pages, render them (key/page-N.png),
                                dump their text (key/text.txt) and, if the key table lines up with the parsed
                                questions, write key/proposed_answers.tsv (VERIFY it against the page images)
  apply  work --chapters chapters.tsv --answers answers.tsv
                                chapters.tsv: <qid or passage group id>\t<chapter code>\t<subtopic from the list>
                                merge the agent's chapter + answer decisions into work/questions.json and validate
  pack   work -o <Test Name>.zip
                                refuse unless every question has a valid chapter and an answer; zip json + images
  build  <dir with test zips> -o out
                                build one editable LaTeX file per chapter, zipped with its img/ folder
                                (out/Physics|Chemistry|Mathematics/<code title>.zip), merge duplicates,
                                write out/index.csv, and compile-check every chapter
  sync <bank-manifest.json> <conversion progress-manifest.json>...
                                add every newly converted test (status done) to the bank manifest as pending
  manifest <manifest.json> show|set|verify  (same semantics as score2_tools manifest)
"""
import argparse, collections, datetime, glob, hashlib, json, os, re, shutil, subprocess, sys, zipfile

# --------------------------------------------------------------------------------------------- chapters
CHAPTERS = [
 ('P01', 'phy', 'Kinematics'),
 ('P02', 'phy', 'NLM'),
 ('P03', 'phy', 'WPE'),
 ('P04', 'phy', 'COM'),
 ('P05', 'phy', 'RBD'),
 ('P06', 'phy', 'Gravitation'),
 ('P07', 'phy', 'Fluids'),
 ('P08', 'phy', 'Electrostatics'),
 ('P09', 'phy', 'Capacitance'),
 ('P10', 'phy', 'Current Electricity'),
 ('P11', 'phy', 'Magnetism'),
 ('P12', 'phy', 'EMI + AC'),
 ('P13', 'phy', 'Thermal Expansion & Calorimetry'),
 ('P14', 'phy', 'KTG & Gas Laws'),
 ('P15', 'phy', 'Thermodynamics'),
 ('P16', 'phy', 'Heat Transfer'),
 ('P17', 'phy', 'SHM'),
 ('P18', 'phy', 'Waves'),
 ('P19', 'phy', 'Ray Optics'),
 ('P20', 'phy', 'Wave Optics'),
 ('P21', 'phy', 'Modern Physics'),
 ('P22', 'phy', 'EM Waves'),
 ('P23', 'phy', 'Properties of Matter'),
 ('P24', 'phy', 'Semiconductors'),
 ('P25', 'phy', 'Units, Errors & Experiments'),
 ('M01', 'math', 'Theory of Equations'),
 ('M02', 'math', 'Complex Numbers'),
 ('M03', 'math', 'Sequences & Series + Means'),
 ('M04', 'math', 'PnC'),
 ('M05', 'math', 'BT'),
 ('M06', 'math', 'Probability I + II'),
 ('M07', 'math', 'Matrices'),
 ('M08', 'math', 'Determinants'),
 ('M09', 'math', 'Statistics'),
 ('M10', 'math', 'Logarithms'),
 ('M11', 'math', 'Trig Ratios & Transformation'),
 ('M12', 'math', 'Trig Functions & Equations'),
 ('M13', 'math', 'SOT'),
 ('M14', 'math', 'ITF'),
 ('M15', 'math', 'Straight Line & Pair'),
 ('M16', 'math', 'Circles'),
 ('M17', 'math', 'Parabola'),
 ('M18', 'math', 'Ellipse'),
 ('M19', 'math', 'Hyperbola'),
 ('M20', 'math', 'Functions'),
 ('M21', 'math', 'Limits'),
 ('M22', 'math', 'Differentiation'),
 ('M23', 'math', 'Continuity & Differentiability'),
 ('M24', 'math', 'AOD'),
 ('M25', 'math', 'Monotonicity – Max/Min'),
 ('M26', 'math', 'Indefinite Integration'),
 ('M27', 'math', 'Definite Integration'),
 ('M28', 'math', 'Area Under the Curve'),
 ('M29', 'math', 'Differential Equations'),
 ('M30', 'math', 'Intro to Vectors'),
 ('M31', 'math', 'Products of Vectors'),
 ('M32', 'math', '3D Geometry'),
 ('C01', 'chem', 'Mole Concept'),
 ('C02', 'chem', 'Atomic Structure'),
 ('C03', 'chem', 'Gaseous State'),
 ('C04', 'chem', 'Thermodynamics'),
 ('C05', 'chem', 'Thermochemistry'),
 ('C06', 'chem', 'Chemical Equilibrium'),
 ('C07', 'chem', 'Ionic Equilibrium'),
 ('C08', 'chem', 'Redox Reactions'),
 ('C09', 'chem', 'Chemical Kinetics'),
 ('C10', 'chem', 'Electrochemistry'),
 ('C11', 'chem', 'Solutions'),
 ('C12', 'chem', 'Solid State'),
 ('C13', 'chem', 'Surface Chemistry'),
 ('C14', 'chem', 'GOC'),
 ('C15', 'chem', 'Isomerism'),
 ('C16', 'chem', 'Grignard'),
 ('C17', 'chem', 'Hydrocarbons'),
 ('C18', 'chem', 'Alkyl Halides'),
 ('C19', 'chem', 'Alcohol, Ether, Phenol'),
 ('C20', 'chem', 'Aldehydes & Ketones'),
 ('C21', 'chem', 'Carboxylic Acids'),
 ('C22', 'chem', 'Amines'),
 ('C23', 'chem', 'Aromatic'),
 ('C24', 'chem', 'POC'),
 ('C25', 'chem', 'Biomolecules'),
 ('C26', 'chem', 'IUPAC'),
 ('C27', 'chem', 'Polymers'),
 ('C28', 'chem', 'Chemistry in Everyday Life'),
 ('C29', 'chem', 'Periodic Table'),
 ('C30', 'chem', 'Chemical Bonding'),
 ('C31', 'chem', 'Coordination Compounds'),
 ('C32', 'chem', 'Metallurgy'),
 ('C33', 'chem', 'Salt Analysis'),
 ('C34', 'chem', 'Environmental Chemistry'),
 ('C35', 'chem', 's-block'),
 ('C36', 'chem', 'p-block'),
 ('C37', 'chem', 'd & f block'),
 ('C38', 'chem', 'Hydrogen and its Compounds'),
]
CH = {c: (s, t) for c, s, t in CHAPTERS}
SUBJ_NAME = {"phy": "Physics", "chem": "Chemistry", "math": "Mathematics"}
SUBJ_OF_PART = {"PHYSICS": "phy", "CHEMISTRY": "chem", "MATHEMATICS": "math", "MATHS": "math", "MATHEMATIC": "math"}
# series = the test-name part before " - Test"; order, display names and id prefixes for every series in the bank
SERIES = [  # (series key as in file names, short id prefix)
    ("Score-I", "SI"), ("Score-II", "SII"), ("Score Advanced", "SA"), ("SRG (Enthusiast)", "SRG"), ("SRGBT", "SRGBT"),
    ("Nurture SRG", "NSRG"), ("Pre-Score (2023-24)", "PS"), ("Enthusiast Pre-Score", "EPS"),
    ("JEE Advanced (2021 Series)", "JA"), ("TOAS", "TOAS"), ("TAAS", "TAAS"), ("TOPS", "TOPS"), ("TEAS", "TEAS"),
    ("TMAS", "TMAS"), ("TNAS", "TNAS"), ("Star Review (Other)", "STAR"), ("Internal Test", "INT"),
    ("Nurture (General)", "NUR"), ("FIITJEE AITS", "FIIT"),
]
SERIES_ORDER = [k for k, _ in SERIES]
SERIES_ABBR = dict(SERIES)
SERIES_FULL = {k: k for k, _ in SERIES}


def series_of(name):
    s = name.split(" - Test")[0].strip()
    return s


def test_no(name):
    m = re.search(r"Test (\d+)", name)
    return int(m.group(1)) if m else 0


def test_digits(name):
    m = re.search(r"Test (\d+(?:-\d+)?)", name)        # 'Test 034-2' = 2nd test split out of the FIITJEE 034 compilation
    return m.group(1) if m else "00"


def tag_of(name):
    """short source tag: '<series> - Test NN' (+ FIITJEE paper code, e.g. 'FIITJEE AITS - Test 034 FT-V')"""
    m = re.match(r"(.*? - Test \d+(?:-\d+)?)(?: - ([^()]+?))?\s*(?:\(.*\))?$", name)
    if not m: return name
    return m.group(1) + (f" {m.group(2).strip()}" if m.group(2) else "")


# --------------------------------------------------------------------------------------------- parse
COL_CM = 8.65      # column width of the converted two-column tests (A4, 1.5 cm margins, 0.7 cm gap)
TEXT_CM = 18.0     # text width of the converted tests
STRIP_CMDS = [r"\\qfullbegin", r"\\qfullend", r"\\qfullsplit", r"\\qfullstart", r"\\qfulldone", r"\\raggedcolumns",
              r"\\columnbreak", r"\\fwstart", r"\\fwend", r"\\newpage", r"\\clearpage", r"\\pagebreak", r"\\vfill", r"\\end\{multicols\*?\}",
              r"\\begin\{multicols\*?\}\{\d\}", r"\\end\{document\}", r"\\twocolumn(\[[^\]]*\])?", r"\\onecolumn"]


def read_body(tex):
    s = open(tex, encoding="utf-8", errors="replace").read()
    figdefs = {m.group(1): (m.group(2), float(m.group(3)))
               for m in re.finditer(r"\\qfigdef\{([^}]*)\}\{([^}]*)\}\{([\d.]+)\}\{\d\}", s)}
    i = s.find("\\begin{document}")
    body = s[i + len("\\begin{document}"):] if i >= 0 else s
    body = "\n".join(l for l in body.split("\n") if not l.lstrip().startswith("%"))
    # drop the title block
    body = re.sub(r"\\begin\{center\}.*?\\end\{center\}", "", body, count=1, flags=re.S)
    body = re.sub(r"\\twocolumn\[.*?\n\]", "", body, count=1, flags=re.S)
    return s, body, figdefs


KNOWN_MACROS = {"opt", "qfigdef", "qfig", "qfigi", "papersec", "partsec", "sect", "qn", "paraq", "sectionhdr",
                "subsectionhdr", "fwstart", "fwend", "arraystretch", "qfullsplit", "qfullbegin", "qfullend",
                "qfullstart", "qfulldone"}


def extra_preamble(src):
    """column types and macros a converted test defines in its own preamble (its question text may use them)"""
    k = src.find("\\begin{document}")
    pre = src[:k] if k >= 0 else ""
    out = []
    for m in re.finditer(r"\\newcolumntype\{(.)\}(\[\d\])?", pre):
        e = balanced(pre, m.end()) if m.end() < len(pre) and pre[m.end()] == "{" else m.end()
        out.append(pre[m.start():e])
    for m in re.finditer(r"\\(?:newcommand|providecommand|DeclareMathOperator)\*?\s*\{?\\([A-Za-z]+)\}?", pre):
        if m.group(1) in KNOWN_MACROS:
            continue
        i = m.end()
        while i < len(pre) and pre[i] == " ":
            i += 1
        while i < len(pre) and pre[i] == "[":
            i = pre.index("]", i) + 1
        if i < len(pre) and pre[i] == "{":
            e = balanced(pre, i)
            out.append(pre[m.start():e].replace("\\newcommand", "\\providecommand", 1))
    return out


def balanced(s, i):
    """s[i] == '{' -> index after the matching '}'"""
    d = 0
    for j in range(i, len(s)):
        if s[j] == "{": d += 1
        elif s[j] == "}":
            d -= 1
            if d == 0: return j + 1
    return len(s)


def tokens(body, alt):
    """yield (kind, arg, start, end) structural tokens in order"""
    out = []
    if not alt:
        pats = [("paper", r"\\papersec\{(\d)\}"), ("part", r"\\partsec\{\d\}\{([A-Z ]+)\}"), ("sect", r"\\sect\{"),
                ("q", r"\\qn\{(\d+)\}"), ("para", r"\\paraq\{(\d+)\}\{(\d+)\}")]
    else:
        pats = [("hdr", r"\\sectionhdr\{"), ("sect", r"\\subsectionhdr\{"),
                ("q", r"(?m)^[ \t]*\\textbf\{(\d+)\.\}"),
                ("para", r"\\textit\{\s*Paragraph\s+for\s+Questions?\s+(\d+)\s*(?:and|to|&|-|–)\s*(\d+)\s*:?\s*\}\s*:?")]
    for kind, p in pats:
        for m in re.finditer(p, body):
            out.append([kind, m, m.start(), m.end()])
    out.sort(key=lambda t: t[2])
    res = []
    for kind, m, a, b in out:
        if kind in ("sect", "hdr"):
            e = balanced(body, b - 1)
            arg = body[b:e - 1]
            if kind == "hdr":
                if re.search(r"PAPER", arg, re.I):
                    res.append(("paper", re.search(r"(\d)", arg).group(1) if re.search(r"\d", arg) else "1", a, e))
                else:
                    mm = re.search(r"(PHYSICS|CHEMISTRY|MATHEMATICS|MATHS)", arg, re.I)
                    if mm:
                        res.append(("part", mm.group(1).upper(), a, e))
                    else:
                        res.append(("sect", arg, a, e))
                continue
            res.append(("sect", arg, a, e))
        elif kind == "part":
            res.append(("part", m.group(1).strip().upper(), a, b))
        elif kind == "paper":
            res.append(("paper", m.group(1), a, b))
        elif kind == "q":
            res.append(("q", int(m.group(1)), a, b))
        elif kind == "para":
            res.append(("para", (int(m.group(1)), int(m.group(2))), a, b))
    return res


def convert_figs(text, figdefs, imgdir, used, alt):
    def put(src):
        base = os.path.basename(src)
        p = os.path.join(imgdir, base)
        if not os.path.exists(p):
            return None
        used.add(base)
        return base

    def qf(m):
        scale = float(m.group(2) or 1)
        fid = m.group(3)
        if fid not in figdefs:
            return f"\\bmissing{{{fid}}}"
        f, w = figdefs[fid]
        b = put(f)
        if not b:
            return f"\\bmissing{{{fid}}}"
        inline = m.group(1) == "qfigi"
        return f"\\b{'figi' if inline else 'fig'}{{{w * scale:.1f}}}{{{b}}}"
    text = re.sub(r"\\(qfigi|qfig)(?:\[([\d.]+)\])?\{([^}]+)\}", qf, text)

    def ig(m):
        opts, src = m.group(1) or "", m.group(2)
        b = put(src)
        if not b:
            return f"\\bmissing{{{os.path.basename(src)}}}"
        w = None
        mm = re.search(r"width\s*=\s*([\d.]*)\s*\\(linewidth|columnwidth|textwidth|hsize)", opts)
        if mm:
            f = float(mm.group(1) or 1)
            w = f * (TEXT_CM if mm.group(2) == "textwidth" and not alt else COL_CM) * 28.45
        mm = re.search(r"width\s*=\s*([\d.]+)\s*(cm|mm|pt|in)", opts)
        if mm:
            w = float(mm.group(1)) * {"cm": 28.45, "mm": 2.845, "pt": 1, "in": 72.27}[mm.group(2)]
        mm = re.search(r"scale\s*=\s*([\d.]+)", opts)
        if w is None:
            w = 140.0
        return f"\\bfigi{{{w:.1f}}}{{{b}}}"
    text = re.sub(r"\\includegraphics(?:\[([^\]]*)\])?\{([^}]+)\}", ig, text)
    return text


ENV_RE = re.compile(r"\\(begin|end)\{([a-zA-Z*]+)\}((?:\[[^\]]*\])?(?:\{[^{}]*\})*)")
WRAP_ENVS = {"minipage", "center", "flushleft", "flushright", "small", "footnotesize", "samepage", "minipage*"}


def balance_envs(text):
    """drop wrapper environments that a question/passage segment opens or closes without the other half
    (the converted tests sometimes wrap a passage + its first question in one minipage)"""
    stack, drop = [], []
    for m in ENV_RE.finditer(text):
        kind, env = m.group(1), m.group(2)
        if kind == "begin":
            stack.append((env, m))
        else:
            if stack and stack[-1][0] == env:
                stack.pop()
            elif env in WRAP_ENVS:
                drop.append(m)
            else:
                # mismatched non-wrapper: pop through wrappers
                while stack and stack[-1][0] in WRAP_ENVS and stack[-1][0] != env:
                    drop.append(stack.pop()[1])
                if stack and stack[-1][0] == env: stack.pop()
                else: drop.append(m)
    drop += [m for env, m in stack]
    for m in sorted(drop, key=lambda m: -m.start()):
        text = text[:m.start()] + text[m.end():]
    return text


def clean(text):
    for c in STRIP_CMDS:
        text = re.sub(c, "", text)
    text = balance_envs(text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def plain(text, n=320):
    t = re.sub(r"\\b(fig|figi)\{[^}]*\}\{[^}]*\}", " [FIG] ", text)
    t = re.sub(r"\\opt\{([A-D])\}", r" (\1) ", t)
    t = re.sub(r"\\(begin|end)\{[^}]*\}", " ", t)
    t = re.sub(r"\\(text|mathrm|textbf|textit|mathbf|ce|mathit)\{([^}]*)\}", r"\2", t)
    t = re.sub(r"\\[a-zA-Z]+\*?", " ", t)
    t = re.sub(r"[{}$]", "", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t[:n]


def parse(tex, out, name=None, imgdir=None):
    name = name or os.path.splitext(os.path.basename(tex))[0]
    imgdir = imgdir or os.path.join(os.path.dirname(tex), name + "-img")
    src, body, figdefs = read_body(tex)
    alt = "\\qn{" not in body
    extra_pre = extra_preamble(src)
    toks = tokens(body, alt)
    os.makedirs(os.path.join(out, "img"), exist_ok=True)
    used = set()
    paper, subj, sect, secno = 1, None, "", 0
    qs, groups, seen = [], {}, collections.Counter()
    cur_group, group_range = None, None
    warn = []
    for k, (kind, arg, a, b) in enumerate(toks):
        nxt = toks[k + 1][2] if k + 1 < len(toks) else len(body)
        seg = body[b:nxt]
        if kind == "paper":
            paper, subj, secno, cur_group = int(arg), None, 0, None
        elif kind == "part":
            subj = SUBJ_OF_PART.get(arg.split()[0], None)
            secno, cur_group, sect = 0, None, ""
            if subj is None: warn.append(f"unknown PART name {arg}")
        elif kind == "sect":
            sect = re.sub(r"\s+", " ", re.sub(r"\\[a-zA-Z]+|[{}]", " ", arg)).strip()
            secno += 1
            cur_group = None
        elif kind == "para":
            gid = f"p{paper}_{subj}_s{secno}_g{arg[0]}_{arg[1]}"
            txt = clean(convert_figs(seg, figdefs, imgdir, used, alt))
            groups[gid] = dict(id=gid, first=arg[0], last=arg[1], text=txt)
            cur_group, group_range = gid, arg
        elif kind == "q":
            if subj is None:
                warn.append(f"question {arg} before any PART - skipped")
                continue
            if secno == 0: secno = 1
            qid = f"p{paper}_{subj}_s{secno}_q{arg:02d}"
            seen[qid] += 1
            if seen[qid] > 1:
                qid += f"_{seen[qid]}"
            g = cur_group if cur_group and group_range[0] <= arg <= group_range[1] else None
            if cur_group and not g:
                cur_group = None
            text = clean(convert_figs(seg, figdefs, imgdir, used, alt))
            qs.append(dict(qid=qid, test=name, tag=tag_of(name), series=series_of(name), testno=test_no(name),
                           paper=paper, subject=subj, section=sect, secno=secno, qnum=arg, group=g,
                           text=text, has_options=bool(re.search(r"\\opt\{|\(A\)", text)),
                           chapter=None, answer=None, answer_src=None, working=None))
    for f in used:
        shutil.copy(os.path.join(imgdir, f), os.path.join(out, "img", f))
    missing = sorted({m for q in qs for m in re.findall(r"\\bmissing\{([^}]*)\}", q["text"])} |
                     {m for g in groups.values() for m in re.findall(r"\\bmissing\{([^}]*)\}", g["text"])})
    data = dict(test=name, tag=tag_of(name), series=series_of(name), questions=qs, groups=groups,
                source_format="alt" if alt else "standard", preamble=extra_pre)
    json.dump(data, open(os.path.join(out, "questions.json"), "w"), indent=1, ensure_ascii=False)
    write_list(data, os.path.join(out, "list.txt"))
    per = collections.Counter((q["paper"], q["subject"]) for q in qs)
    print(f"{name}: {len(qs)} questions, {len(groups)} paragraph groups, {len(used)} images "
          f"({'alt' if alt else 'standard'} format)")
    print("  per paper/subject: " + ", ".join(f"P{p} {s} {n}" for (p, s), n in sorted(per.items())))
    for w in warn: print("  WARN", w)
    if missing: print("  WARN missing images:", ", ".join(missing))
    print(f"  wrote {out}/questions.json, {out}/list.txt, {out}/img/ - classify from list.txt")


def write_list(data, path):
    lines = [f"# {data['test']} - one line per question: qid | section | text (plain, truncated)",
             "# chapters.tsv: one line per qid (or per paragraph group id gNN: all its questions get it): <qid>\\t<code>",
             "# codes: run `bank_tools.py chapters`", ""]
    shown = set()
    for q in data["questions"]:
        if q["group"] and q["group"] not in shown:
            shown.add(q["group"])
            lines.append(f"  [{q['group']}] PASSAGE: {plain(data['groups'][q['group']]['text'], 400)}")
        lines.append(f"{q['qid']} | {q['section'][:28]} | {plain(q['text'])}")
    open(path, "w").write("\n".join(lines) + "\n")


# --------------------------------------------------------------------------------------------- answer keys
ANS_RE = re.compile(r"^(?:[A-D](?:\s*,\s*[A-D])*|[–\-−]?\d+(?:\.\d+)?(?:\s*(?:to|or|OR|&)\s*[–\-−]?\d+(?:\.\d+)?)*|Bonus|BONUS|"
                    r"[PQRST]\s*[→\-]>?\s*\d.*)$")


def keyprep(src, out, work=None):
    import pymupdf
    os.makedirs(out, exist_ok=True)
    d = pymupdf.open(src)
    kp = [i for i, p in enumerate(d) if re.search(r"ANSWER\s*KEY", p.get_text(), re.I)]
    sp = [i for i, p in enumerate(d) if re.search(r"\bSOLUTIONS?\b|\bAns\.?\s*\(", p.get_text())]
    txt = []
    for i in kp:
        d[i].get_pixmap(dpi=110).save(os.path.join(out, f"page-{i + 1}.png"))
        txt.append(f"===== page {i + 1} =====\n" + d[i].get_text())
    open(os.path.join(out, "text.txt"), "w").write("\n".join(txt))
    print(f"answer-key pages: {[i + 1 for i in kp] or 'NONE'}")
    if not kp and sp:
        print(f"no key table, but solution pages exist: {[i + 1 for i in sp][:12]}{' ...' if len(sp) > 12 else ''} "
              "- answers ('Ans (B)') are printed in the solutions: render those pages and read them")
    if not kp and not sp:
        print("no printed key and no solutions: SOLVE every question (answer_src=solved, with short working)")
    if kp and work:
        propose(" ".join(txt), work, out)


def propose(text, work, out):
    data = json.load(open(os.path.join(work, "questions.json")))
    cells = [c.strip() for c in text.split("\n") if c.strip()]
    # collect (qnum, answer) pairs: 'Q1 Q2 ... Qn' header rows followed by n answers, or 'Q. 1 2 ..' / 'A. ..'
    pairs, i = [], 0
    while i < len(cells):
        if re.fullmatch(r"Q\.?\s*\d+", cells[i]) or cells[i] == "Q.":
            hdr = []
            if cells[i] == "Q.":
                i += 1
                while i < len(cells) and re.fullmatch(r"\d+", cells[i]):
                    hdr.append(int(cells[i])); i += 1
                if i < len(cells) and cells[i] == "A.": i += 1
            else:
                while i < len(cells) and re.fullmatch(r"Q\.?\s*\d+", cells[i]):
                    hdr.append(int(re.sub(r"\D", "", cells[i]))); i += 1
            ans = []
            while i < len(cells) and len(ans) < len(hdr) and ANS_RE.match(cells[i].replace(" ", "")):
                ans.append(cells[i]); i += 1
            if len(ans) == len(hdr):
                pairs += list(zip(hdr, ans))
            continue
        i += 1
    # split into runs at qnum resets
    runs, cur = [], []
    for q, a in pairs:
        if cur and q <= cur[-1][0]:
            runs.append(cur); cur = []
        cur.append((q, a))
    if cur: runs.append(cur)
    # our sections in order
    secs = collections.OrderedDict()
    for q in data["questions"]:
        secs.setdefault((q["paper"], q["subject"], q["secno"]), []).append(q)
    ours = list(secs.values())
    ok = len(runs) == len(ours) and all(len(r) == len(s) for r, s in zip(runs, ours))
    if not ok:
        # tolerate merged runs (key prints one subject's sections back to back with continuous numbering)
        print(f"  key text -> {len(runs)} runs {[len(r) for r in runs]}; questions -> {len(ours)} sections "
              f"{[len(s) for s in ours]}: do NOT match - write answers.tsv by hand from the page images")
        return
    lines = ["# proposed from the key text layer - CHECK EVERY LINE against key/page-*.png, then save as answers.tsv"]
    for r, s in zip(runs, ours):
        for (qn, a), q in zip(r, s):
            flag = "" if qn == q["qnum"] else f"   # key Q{qn} vs question {q['qnum']} - check"
            lines.append(f"{q['qid']}\t{norm_ans(a)}\tkey{flag}")
    open(os.path.join(out, "proposed_answers.tsv"), "w").write("\n".join(lines) + "\n")
    print(f"  wrote {out}/proposed_answers.tsv ({sum(len(r) for r in runs)} answers) - verify against the images")


def norm_ans(a):
    a = a.replace("–", "-").replace("−", "-")
    return re.sub(r"\s*,\s*", ",", a.strip())


# --------------------------------------------------------------------------------------------- apply / pack
def read_tsv(path):
    rows = []
    for l in open(path, encoding="utf-8"):
        if not l.strip() or l.lstrip().startswith("#"):
            continue
        rows.append([c.strip() for c in l.rstrip("\n").split("\t")])
    return rows


DIFF_RUBRIC = """DIFFICULTY RUBRIC (same for every question, subject and series). Score the SHORTEST CORRECT SOLUTION you have
actually worked out, as it would be for a well-prepared JEE Advanced aspirant. Ignore the source series, the question's
position in the paper, the marks and the topic's reputation. Paragraph questions are scored one by one (reading the
passage itself is not counted).
  K  concepts  - distinct laws / results / methods that must be combined:
       1 = one   2 = two   3 = three or more, or ideas from two different chapters
  S  steps     - non-trivial steps of the shortest solution (setting up an equation, solving it, each case, each
                 option that needs its own working, each intermediate quantity):
       1 = 1-2   2 = 3-4   3 = 5-7   4 = 8 or more
  I  insight   - how obvious the route is once the concepts are known:
       0 = direct, standard application
       1 = a known JEE technique must be recognised (symmetry, standard substitution, limiting case, known trick)
       2 = a non-standard key idea, construction or reinterpretation
  C  computation - algebra / arithmetic / calculus load and error-proneness:
       0 = light (a few lines)   1 = moderate   2 = heavy (long integrals, messy numbers, many terms or cases)
  F  format    - set by the tool from the question type: 0 = single correct; 1 = multiple correct, matching, or
                 numerical with no options
  D = min(10, K + S + I + C + F - 1), from 1 to 10.  Bands: 1-3 Easy, 4-5 Medium, 6-7 Hard, 8-10 Very hard.
  A STEP is one equation set up and solved, one case, one option that needs its own working, or one intermediate
  quantity that takes real work. Reading data, substituting into a formula, unit conversion and one-line arithmetic
  are NOT steps. Most single-concept JEE questions are S1-S2; S3 needs 5-7 genuine steps and S4 is rare.
  Typical tests spread over all bands; a test where most questions get the same S or I was not really worked out.
difficulty.tsv: one line per question id (never per passage group): <qid> TAB <K S I C> TAB <reason>, where the reason
LISTS what was counted and the tool checks the counts:
    concepts: <concept 1>, <concept 2> | steps: <step 1>; <step 2>; <step 3> | <optional note on I or C>
K must equal the number of concepts listed (3 = three or more) and S must match the number of steps listed
(1-2 -> 1, 3-4 -> 2, 5-7 -> 3, 8+ -> 4). Example:
    p1_phy_s1_q02<TAB>2 2 1 0<TAB>concepts: angular momentum conservation, energy with shell potential | steps: L
    about centre gives v=u/2 at grazing; energy equation at surface; solve for u | I: grazing => velocity tangential
Calibrated examples: BANK_LEARNINGS.md, section CALIBRATION."""
DIFF_RANGES = dict(K=(1, 3), S=(1, 4), I=(0, 2), C=(0, 2))
# reasons that describe no particular question (templates seen in the 24 Oct audit)
GENERIC_RE = re.compile(r"apply(ing)? (the )?relevant (results?|formulae?|concepts?|laws?)|standard (problem|question|result)s?"
                        r"( in this chapter)?|relevant results?|as per (the )?(standard )?(method|formula)|"
                        r"use (the )?(standard|given) (formula|method)|straightforward application", re.I)
GENERIC_STEP_RE = re.compile(r"^(compute|calculate|solve|simplify|substitute|evaluate|apply( the)? formula|find (the )?answer|"
                             r"get (the )?answer|check options?|conclude|answer|result)\.?$", re.I)


def diff_band(d):
    return "Easy" if d <= 3 else "Medium" if d <= 5 else "Hard" if d <= 7 else "Very hard"


def diff_score(parts, qt):
    """parts = {'K':..,'S':..,'I':..,'C':..}; qt = question type -> (D, 'K2 S3 I1 C1 F0')"""
    f = 0 if qt == "single" else 1
    d = max(1, min(10, parts["K"] + parts["S"] + parts["I"] + parts["C"] + f - 1))
    return d, f"K{parts['K']} S{parts['S']} I{parts['I']} C{parts['C']} F{f}"


def finish_difficulty(data):
    """compute F, D and the band for every question that has K S I C (needs answers for the question type)"""
    secs = collections.defaultdict(list)
    for q in data["questions"]:
        secs[(q["paper"], q["subject"], q["secno"])].append(q)
    for q in data["questions"]:
        if q.get("diff_kSIC"):
            d, parts = diff_score(q["diff_kSIC"], qtype(secs[(q["paper"], q["subject"], q["secno"])]))
            q["difficulty"], q["diff_parts"], q["diff_band"] = d, parts, diff_band(d)


def apply(work, chapters=None, answers=None, difficulty=None):
    p = os.path.join(work, "questions.json")
    data = json.load(open(p))
    byid = {q["qid"]: q for q in data["questions"]}
    errs = []
    if chapters:
        for r in read_tsv(chapters):
            key, code = r[0], r[1].upper() if len(r) > 1 else ""
            if code not in CH:
                errs.append(f"unknown chapter code {code!r} for {key}"); continue
            targets = [q for q in data["questions"] if q["group"] == key] if key in data["groups"] else [byid.get(key)]
            if targets == [None]:
                errs.append(f"unknown qid {key}"); continue
            sub = r[2] if len(r) > 2 else ""
            if not sub:
                errs.append(f"{key}: subtopic missing (3rd column)")
            elif sub.startswith("new:"):
                sub = sub[4:].strip()
                print(f"  NOTE new subtopic for {code}: {sub!r} (log it in BANK_LEARNINGS.md)")
            elif sub not in SUBTOPICS.get(code, []):
                errs.append(f"{key}: subtopic {sub!r} is not in the {code} list (`chapters --subtopics {code}`); "
                            "pick one, or write new:<label> only if none fits")
            for q in targets:
                if CH[code][0] != q["subject"]:
                    errs.append(f"{q['qid']}: chapter {code} is {CH[code][0]}, question is {q['subject']}")
                q["chapter"] = code
                q["subtopic"] = sub
    if answers:
        for r in read_tsv(answers):
            qid = r[0]
            if qid not in byid:
                errs.append(f"unknown qid {qid}"); continue
            q = byid[qid]
            if len(r) < 2 or not r[1]:
                errs.append(f"{qid}: empty answer"); continue
            q["answer"] = r[1]
            q["answer_src"] = (r[2] if len(r) > 2 and r[2] else "key").split()[0]
            if q["answer_src"] not in ("key", "solved"):
                errs.append(f"{qid}: answer source must be key or solved"); q["answer_src"] = "key"
            q["working"] = r[3] if len(r) > 3 and r[3] else None
            if q["answer_src"] == "solved" and not q["working"]:
                errs.append(f"{qid}: solved answers need a short working (4th column)")
    if difficulty:
        # a new difficulty file replaces every earlier score: a question whose line is rejected has NO difficulty
        # afterwards, so `pack` refuses until it is fixed
        for q in data["questions"]:
            for k in ("diff_kSIC", "diff_note", "difficulty", "diff_parts", "diff_band"):
                q.pop(k, None)
        seen_reasons, seen_steps = collections.defaultdict(list), collections.defaultdict(list)
        for r in read_tsv(difficulty):
            qid = r[0]
            if qid not in byid:
                errs.append(f"unknown qid {qid} in difficulty file (score questions, not passage groups)"); continue
            nums = (r[1] if len(r) > 1 else "").replace(",", " ").split()
            if len(nums) != 4 or not all(n.isdigit() for n in nums):
                errs.append(f"{qid}: difficulty needs four integers 'K S I C' (2nd column), got {r[1:2]}"); continue
            parts = dict(zip("KSIC", map(int, nums)))
            bad = [f"{k}={v} (allowed {lo}-{hi})" for k, v in parts.items()
                   for lo, hi in [DIFF_RANGES[k]] if not lo <= v <= hi]
            if bad:
                errs.append(f"{qid}: difficulty out of range: " + ", ".join(bad)); continue
            if len(r) < 3 or len(r[2]) < 8:
                errs.append(f"{qid}: difficulty needs a one-line reason (3rd column)"); continue
            m_c = re.search(r"concepts?\s*:\s*([^|]*)", r[2], re.I)
            m_s = re.search(r"steps?\s*:\s*([^|]*)", r[2], re.I)
            if not (m_c and m_s):
                errs.append(f"{qid}: reason must list 'concepts: a, b | steps: s1; s2; ...' (see `bank_tools.py "
                            "difficulty` and BANK_LEARNINGS.md CALIBRATION)"); continue
            nc = len([c for c in re.split(r"[,;]", m_c.group(1)) if c.strip()])
            ns = len([c for c in m_s.group(1).split(";") if c.strip()])
            want_s = 1 if ns <= 2 else 2 if ns <= 4 else 3 if ns <= 7 else 4
            if min(nc, 3) != parts["K"] and not (parts["K"] == 3 and nc == 2):   # K3 also = two different chapters
                errs.append(f"{qid}: K={parts['K']} but {nc} concept(s) listed"); continue
            if want_s != parts["S"]:
                errs.append(f"{qid}: S={parts['S']} but {ns} step(s) listed (1-2 -> 1, 3-4 -> 2, 5-7 -> 3, 8+ -> 4)"); continue
            bad_txt = GENERIC_RE.search(r[2])
            if bad_txt:
                errs.append(f"{qid}: reason contains the generic phrase {bad_txt.group(0)!r} - name this question's own "
                            "concepts and the actual steps of its solution"); continue
            steps = [st.strip() for st in m_s.group(1).split(";") if st.strip()]
            if all(GENERIC_STEP_RE.match(st) for st in steps):
                errs.append(f"{qid}: the steps {steps[:3]} say nothing about this question - state what is set up, "
                            "found or checked in each step"); continue
            seen_reasons[re.sub(r"\s+", " ", r[2].strip().lower())].append(qid)
            seen_steps[re.sub(r"\s+", " ", m_s.group(1).strip().lower())].append(qid)
            byid[qid]["diff_kSIC"] = parts
            byid[qid]["diff_note"] = r[2]
        # copied reasons: the same reason or the same step list for several questions means they were not worked out
        for dct, what in ((seen_reasons, "reason"), (seen_steps, "step list")):
            for txt, ids in dct.items():
                if len(ids) > 2:
                    errs.append(f"the same {what} is used for {len(ids)} questions ({', '.join(ids[:4])}...): write each "
                                "question's own concepts and steps")
                    for i in ids:
                        for k in ("diff_kSIC", "diff_note"):
                            byid[i].pop(k, None)
        # a 2 for I or C must say why (I: the non-standard idea / C: what makes the computation heavy)
        for q in data["questions"]:
            k, note = q.get("diff_kSIC"), q.get("diff_note") or ""
            if not k:
                continue
            miss = [f for f in ("I", "C") if k[f] == 2 and not re.search(rf"\|\s*{f}\s*:", note)]
            if miss:
                errs.append(f"{q['qid']}: {' and '.join(f + '=2' for f in miss)} needs '| {miss[0]}: <why>' in the reason "
                            "(non-standard idea / genuinely heavy computation); otherwise use 1")
                for kk in ("diff_kSIC", "diff_note"):
                    q.pop(kk, None)
        scored = [q for q in data["questions"] if q.get("diff_kSIC")]
        # calibration guard-rails (audit 24 Oct 09:45): inflated tests had C2 on 40%+, K3 on 25%+ and Very hard on 30%+
        if len(scored) >= 20:
            n = len(scored)
            share = lambda f, v: sum(1 for q in scored if q["diff_kSIC"][f] == v) / n
            over = [f"{lab} {share(f, v):.0%} (max {mx:.0%})" for f, v, mx, lab in
                    (("C", 2, 0.25, "C2"), ("K", 3, 0.20, "K3"), ("I", 2, 0.30, "I2")) if share(f, v) > mx]
            if over:
                errs.append("difficulty looks inflated: " + ", ".join(over) + " - K counts distinct laws/methods "
                            "(the first law is ONE concept even if work, dU and heat all appear), C2 is for genuinely "
                            "long or messy calculation, I2 for a truly non-standard idea; compare with BANK_LEARNINGS.md "
                            "CALIBRATION and rescore the whole test")
                for q in scored:
                    for kk in ("diff_kSIC", "diff_note"):
                        q.pop(kk, None)
                scored = []
        if len(scored) >= 20:
            sc = collections.Counter(q["diff_kSIC"]["S"] for q in scored)
            ic = collections.Counter(q["diff_kSIC"]["I"] for q in scored)
            if max(sc.values()) > 0.85 * len(scored) or max(ic.values()) > 0.9 * len(scored):
                errs.append(f"difficulty is uniform across the test (S {dict(sorted(sc.items()))}, I {dict(sorted(ic.items()))}): "
                            "real papers spread over S1-S3 and I0-I2 - work the questions out and score each one")
                for q in scored:
                    for k in ("diff_kSIC", "diff_note"):
                        q.pop(k, None)
    finish_difficulty(data)
    # a paragraph group keeps one chapter
    for g in data["groups"]:
        ch = {q["chapter"] for q in data["questions"] if q["group"] == g and q["chapter"]}
        if len(ch) > 1:
            errs.append(f"group {g} has several chapters {sorted(ch)} - give the group one chapter")
    json.dump(data, open(p, "w"), indent=1, ensure_ascii=False)
    report(data, errs)
    return data, errs


def report(data, errs):
    qs = data["questions"]
    noch = [q["qid"] for q in qs if not q["chapter"]]
    noans = [q["qid"] for q in qs if not q["answer"]]
    nodiff = [q["qid"] for q in qs if not q.get("difficulty")]
    print(f"{data['test']}: {len(qs)} questions; chapter missing {len(noch)}; answer missing {len(noans)}; "
          f"difficulty missing {len(nodiff)}")
    if nodiff and len(nodiff) < len(qs): print("  no difficulty:", " ".join(nodiff[:30]), "..." if len(nodiff) > 30 else "")
    dd = collections.Counter(q["difficulty"] for q in qs if q.get("difficulty"))
    if dd:
        print("  difficulty:", " ".join(f"D{k}:{dd[k]}" for k in sorted(dd)),
              "| bands:", ", ".join(f"{b} {sum(v for k, v in dd.items() if diff_band(k) == b)}"
                                   for b in ("Easy", "Medium", "Hard", "Very hard")))
    sc = collections.Counter(q["diff_parts"].split()[1] for q in qs if q.get("diff_parts"))
    ic = collections.Counter(q["diff_parts"].split()[2] for q in qs if q.get("diff_parts"))
    n = sum(sc.values())
    if n >= 20 and (max(sc.values()) > 0.6 * n or max(ic.values()) > 0.75 * n):
        print(f"  WARNING difficulty looks uniform (S {dict(sorted(sc.items()))}, I {dict(sorted(ic.items()))}): "
              "re-check that every question was really worked out - most papers spread over S1-S3")
    if noch: print("  no chapter:", " ".join(noch[:30]), "..." if len(noch) > 30 else "")
    if noans: print("  no answer:", " ".join(noans[:30]), "..." if len(noans) > 30 else "")
    for e in errs: print("  ERROR", e)
    cnt = collections.Counter(q["chapter"] for q in qs if q["chapter"])
    if cnt: print("  chapters:", ", ".join(f"{c} {n}" for c, n in sorted(cnt.items())))


def pack(work, out):
    data = json.load(open(os.path.join(work, "questions.json")))
    finish_difficulty(data)
    json.dump(data, open(os.path.join(work, "questions.json"), "w"), indent=1, ensure_ascii=False)
    errs = []
    for q in data["questions"]:
        if q["chapter"] not in CH: errs.append(f"{q['qid']}: no valid chapter")
        if not q["answer"]: errs.append(f"{q['qid']}: no answer")
        if not q.get("subtopic"): errs.append(f"{q['qid']}: no subtopic")
        if not q.get("difficulty"): errs.append(f"{q['qid']}: no difficulty (difficulty.tsv)")
    if errs:
        print("NOT PACKED:\n  " + "\n  ".join(errs[:40]))
        sys.exit(1)
    used = set()
    for t in [q["text"] for q in data["questions"]] + [g["text"] for g in data["groups"].values()]:
        used |= set(re.findall(r"\\bfigi?\{[^}]*\}\{([^}]*)\}", t))
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(os.path.join(work, "questions.json"), "questions.json")
        for f in sorted(used):
            z.write(os.path.join(work, "img", f), "img/" + f)
    print(f"packed {out}: {len(data['questions'])} questions, {len(used)} images")


# --------------------------------------------------------------------------------------------- build
SUBTOPICS = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "subtopics.json")))

PREAMBLE = r"""%% Question bank chapter file - generated by bank_tools.py build (do not edit while the bank is still being built:
%% it is regenerated from the per-test data in Question Bank\data). Every question is one bankq block:
%%   \begin{bankq}[id=..., source={...}, paper=.., qno=.., type=..., subtopic={...}, answer={...}, answer_src=key|solved,
%%                 working={...}, difficulty=1-10, diff_parts={K S I C F}, diff_note={...},
%%                 group=<passage id or empty>, also_in={duplicate copies in other tests}]
%% difficulty = min(10, K+S+I+C+F-1): K concepts 1-3, S steps 1-4, I insight 0-2, C computation 0-2, F format 0-1
%%   ...question LaTeX, options, figures (\bfig / \bfigi -> img/)...
%%   \end{bankq}
%% Passages shared by several questions are bankpassage blocks; their questions carry group=<passage id>.
\documentclass[10pt]{article}
\usepackage[a4paper,margin=1.8cm]{geometry}
\usepackage[T1]{fontenc}
\usepackage{amsmath,amssymb,mathtools}
\usepackage{graphicx}
\usepackage[export]{adjustbox}
\usepackage{xcolor,needspace,keyval}
\usepackage{enumitem}
\usepackage{booktabs,array,tabularx}
\usepackage[hidelinks]{hyperref}
\setlength{\parindent}{0pt}
\setlength{\parskip}{3pt}
\makeatletter
\define@key{bq}{id}{\def\bq@id{#1}}\define@key{bq}{source}{\def\bq@src{#1}}\define@key{bq}{paper}{\def\bq@paper{#1}}
\define@key{bq}{qno}{\def\bq@qno{#1}}\define@key{bq}{type}{\def\bq@type{#1}}\define@key{bq}{subtopic}{\def\bq@sub{#1}}
\define@key{bq}{answer}{\def\bq@ans{#1}}\define@key{bq}{answer_src}{\def\bq@asrc{#1}}\define@key{bq}{working}{\def\bq@work{#1}}
\define@key{bq}{group}{\def\bq@group{#1}}\define@key{bq}{also_in}{\def\bq@also{#1}}
\define@key{bq}{difficulty}{\def\bq@diff{#1}}\define@key{bq}{diff_parts}{\def\bq@dparts{#1}}\define@key{bq}{diff_note}{\def\bq@dnote{#1}}
\newenvironment{bankq}[1][]{\def\bq@work{}\def\bq@also{}\def\bq@group{}\def\bq@diff{?}\def\bq@dparts{}\def\bq@dnote{}\setkeys{bq}{#1}%
  \par\needspace{4\baselineskip}\medskip\noindent{\small\textbf{\bq@id}\hfill\color{gray}[\bq@src, Paper \bq@paper, Q\bq@qno]
  \bq@type\ $\cdot$ \bq@sub\ $\cdot$ \textbf{D\bq@diff}}\par\nopagebreak\relax}
  {\par{\small\color{teal}Answer: \textbf{\bq@ans}\ifx\bq@work\@empty\else\ (solved: \bq@work)\fi
  \ifx\bq@also\@empty\else\par\color{gray}Also in: \bq@also\fi}\par}
\define@key{bp}{id}{\def\bp@id{#1}}\define@key{bp}{source}{\def\bp@src{#1}}\define@key{bp}{questions}{\def\bp@qs{#1}}
\newenvironment{bankpassage}[1][]{\setkeys{bp}{#1}\par\needspace{4\baselineskip}\bigskip\noindent
  {\small\textbf{Passage \bp@id}\hfill\color{gray}[\bp@src; questions \bp@qs]}\par\nopagebreak\relax\itshape}{\par}
\makeatother
\newcommand{\bfig}[2]{\par\smallskip{\centering\includegraphics[width=#1pt,max width=0.62\linewidth,max height=0.32\textheight]{img/#2}\par}\smallskip}
\newcommand{\bfigi}[2]{\includegraphics[width=#1pt,max width=\linewidth,max height=0.32\textheight,valign=c]{img/#2}}
\newcommand{\bmissing}[1]{\textit{[figure missing in the source conversion: \detokenize{#1}]}}
\newenvironment{qoptions}{\begin{itemize}[leftmargin=1.8em,itemsep=1pt,topsep=2pt,label={}]}{\end{itemize}}
\newcommand{\opt}[2]{\item[(#1)] #2}
\providecommand{\fwstart}{}\providecommand{\fwend}{}\providecommand{\qfullsplit}{}
\newcolumntype{L}[1]{>{\raggedright\arraybackslash}p{#1}}
\newcolumntype{C}[1]{>{\centering\arraybackslash}p{#1}}
\newcolumntype{R}[1]{>{\raggedleft\arraybackslash}p{#1}}
\providecommand{\sectionhdr}[1]{}\providecommand{\subsectionhdr}[1]{}
"""


def qtype(section_qs):
    """section type from its header, options and answers"""
    anyopt = any(q["has_options"] for q in section_qs)
    lab = (section_qs[0]["section"] or "").lower()
    if "numer" in lab or "integer" in lab: return "numerical"
    if any(re.search(r"List-?\s*I\b|Column-?\s*I\b|Column\s*1", q["text"]) for q in section_qs) and \
            any(re.search(r"\$\\to\$|→", q["answer"] or "") for q in section_qs): return "matching"
    if "more" in lab or "multiple" in lab: return "multi"
    if "single" in lab: return "single"
    if not anyopt: return "numerical"
    if any("," in (q["answer"] or "") for q in section_qs): return "multi"
    return "single"


def bid(q):
    s = SERIES_ABBR.get(q["series"]) or re.sub(r"[^A-Z0-9]", "", q["series"].upper())[:6] or "X"
    sub = {"phy": "PHY", "chem": "CHEM", "math": "MATH"}[q["subject"]]
    extra = q["qid"].split("_q", 1)[1][2:].replace("_", "-") if "_" in q["qid"].split("_q", 1)[1] else ""
    return f"{s}{test_digits(q['test'])}-P{q['paper']}-{sub}-S{q['secno']}-Q{q['qnum']:02d}{extra}"


def fingerprint(text):
    t = plain(text, 100000).lower()
    t = re.sub(r"\[fig\]", " ", t)
    return re.sub(r"[^a-z0-9]+", " ", t).split()


def img_hash(path):
    try:
        from PIL import Image
        im = Image.open(path).convert("L").resize((16, 16))
        px = list(im.get_flattened_data() if hasattr(im, "get_flattened_data") else im.getdata()); m = sum(px) / len(px)
        return "".join("1" if p < m else "0" for p in px)
    except Exception:
        return ""


def similar(a, b):
    """token-sequence similarity in [0,1] (difflib on word lists)"""
    import difflib
    if not a or not b: return 0.0
    if abs(len(a) - len(b)) > 0.25 * max(len(a), len(b)): return 0.0
    return difflib.SequenceMatcher(None, a, b, autojunk=False).ratio()


def find_duplicates(qs, imgdir):
    """mark later copies of the same question (same chapter): text >= 0.93 similar incl. numbers, same figure count,
    figures alike; options must match too. Returns {dup_index: kept_index}."""
    fps = [fingerprint(q["text"]) for q in qs]
    figs = [re.findall(r"\\bfigi?\{[^}]*\}\{([^}]*)\}", q["text"]) for q in qs]
    hashes = [[img_hash(os.path.join(imgdir, f)) for f in fl] for fl in figs]
    sets = [set(f) for f in fps]
    nums = [re.findall(r"\d+(?:\.\d+)?", plain(q["text"], 100000)) for q in qs]
    ans = [re.sub(r"[^A-Za-z0-9.\-]+", "", (q.get("answer") or "")).upper() for q in qs]
    dup = {}
    for j in range(len(qs)):
        for i in range(j):
            if i in dup: continue
            if qs[i]["test"] == qs[j]["test"]: continue            # never merge two questions of one paper
            if nums[i] != nums[j]: continue                         # same wording, different data = different question
            if ans[i] and ans[j] and ans[i] != ans[j]: continue    # answers disagree: keep both
            if len(figs[i]) != len(figs[j]): continue
            if len(fps[j]) < 8 and not figs[j]: continue           # too short to judge
            u = len(sets[i] | sets[j])
            if not u or len(sets[i] & sets[j]) / u < 0.85: continue   # cheap pre-filter
            if similar(fps[i], fps[j]) < 0.93: continue
            if figs[j] and any(sum(x != y for x, y in zip(h1, h2)) > 40 for h1, h2 in zip(hashes[i], hashes[j]) if h1 and h2):
                continue
            dup[j] = i
            break
    return dup


PRE_BY_TEST = {}


def build(zdir, out, only=None, compile_check=True):
    tmp = os.path.join(out, "_img_all")
    shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
    allq, groups, tests = [], {}, []
    for z in sorted(glob.glob(os.path.join(zdir, "*.zip"))):
        with zipfile.ZipFile(z) as zf:
            data = json.loads(zf.read("questions.json"))
            pre = (SERIES_ABBR.get(data["series"]) or "X") + test_digits(data["test"]) + "_"
            for n in zf.namelist():
                if n.startswith("img/") and not n.endswith("/"):
                    open(os.path.join(tmp, pre + os.path.basename(n)), "wb").write(zf.read(n))
        ren = lambda t: re.sub(r"(\\bfigi?\{[^}]*\}\{)([^}]*)\}", lambda m: m.group(1) + pre + m.group(2) + "}", t)
        secs = collections.defaultdict(list)
        for q in data["questions"]:
            secs[(q["paper"], q["subject"], q["secno"])].append(q)
        for q in data["questions"]:
            q["type"] = qtype(secs[(q["paper"], q["subject"], q["secno"])])
            q["text"] = ren(q["text"])
            q["bid"] = bid(q)
            q["gkey"] = (data["test"], q["group"]) if q["group"] else None
        for g, gd in data["groups"].items():
            first = next((q for q in data["questions"] if q["group"] == g), None)
            gid = (first["bid"].rsplit("-Q", 1)[0] + f"-G{gd['first']}-{gd['last']}") if first else g
            groups[(data["test"], g)] = dict(id=gid, text=ren(gd["text"]), source=data["test"],
                                             qs=f"{gd['first']}-{gd['last']}")
        allq += data["questions"]
        tests.append(data["test"])
        PRE_BY_TEST[data["test"]] = data.get("preamble", [])
    bych = collections.defaultdict(list)
    for q in allq:
        bych[q["chapter"]].append(q)
    index, built, ndup = [], [], 0
    for code, subj, title in CHAPTERS:
        if only and code not in only: continue
        qs = bych.get(code, [])
        if not qs: continue
        qs.sort(key=lambda q: (SERIES_ORDER.index(q["series"]) if q["series"] in SERIES_ORDER else 9, q["testno"],
                               q["paper"], q["secno"], q["qnum"]))
        # duplicates: only stand-alone questions are merged (passage questions stay with their passage)
        solo = [q for q in qs if not q["gkey"]]
        dmap = find_duplicates(solo, tmp)
        for j, i in dmap.items():
            solo[j]["dup_of"] = solo[i]["bid"]
            solo[i].setdefault("also", []).append(f"{solo[j]['test']} P{solo[j]['paper']} Q{solo[j]['qnum']}")
        ndup += len(dmap)
        name = f"{code} {title}".replace("/", "-").replace(":", "-")
        cdir = os.path.join(out, "_build", name)
        shutil.rmtree(cdir, ignore_errors=True); os.makedirs(os.path.join(cdir, "img"))
        extra, seen_pre = [], set()
        for q in qs:
            for line in PRE_BY_TEST.get(q["test"], []):
                key = re.sub(r"\s+", "", line)
                head = re.match(r"\\(?:newcolumntype\{.\}|providecommand\*?\s*\{?\\[A-Za-z]+|DeclareMathOperator\*?\s*\{?\\[A-Za-z]+)", line)
                hk = head.group(0) if head else key
                if hk in seen_pre:
                    continue
                seen_pre.add(hk)
                if hk.startswith("\\newcolumntype") and hk[-2] in "LCR":
                    continue          # L/C/R are defined in PREAMBLE already
                extra.append(line.replace("\\newcolumntype", "\\providecolumntype") if False else line)
        L = [PREAMBLE, "\n".join(extra), "\\begin{document}",
             f"{{\\Large\\bfseries {tex_esc(title)} --- Question Bank}}\\par\\smallskip",
             f"{{\\small {SUBJ_NAME[subj]} chapter {code}. Questions from all converted test papers, grouped by source series. Answers: printed key where it matches the paper, "
             "otherwise solved (answer\\_src=solved, with working). Exact repeats across papers appear once, with "
             "also\\_in listing the other copies.}\\par\\medskip\\hrule"]
        cur, shown, used_imgs, n = None, set(), set(), 0
        for q in qs:
            if q.get("dup_of"):
                index.append(row(q, code, title, dup=q["dup_of"])); continue
            if q["series"] != cur:
                cur = q["series"]
                L.append(f"\n\\section*{{{SERIES_FULL.get(cur, cur)} papers}}")
            if q["gkey"] and q["gkey"] not in shown:
                shown.add(q["gkey"]); g = groups[q["gkey"]]
                L.append(f"\\begin{{bankpassage}}[id={g['id']}, source={{{g['source']}}}, questions={{{g['qs']}}}]\n"
                         f"{g['text']}\n\\end{{bankpassage}}")
                used_imgs |= set(re.findall(r"\\bfigi?\{[^}]*\}\{([^}]*)\}", g["text"]))
            keys = [f"id={q['bid']}", f"source={{{q['test']}}}", f"paper={q['paper']}", f"qno={q['qnum']}",
                    f"type={q['type']}", f"subtopic={{{q.get('subtopic') or ''}}}", f"answer={{{tex_ans(q['answer'])}}}",
                    f"answer_src={q['answer_src']}"]
            if q.get("working"): keys.append(f"working={{{pct_esc(q['working'])}}}")
            if q.get("diff_kSIC"):
                q["difficulty"], q["diff_parts"] = diff_score(q["diff_kSIC"], q["type"])
                keys.append(f"difficulty={q['difficulty']}")
                keys.append(f"diff_parts={{{q['diff_parts']}}}")
                if q.get("diff_note"): keys.append(f"diff_note={{{pct_esc(q['diff_note'])}}}")
            if q["gkey"]: keys.append(f"group={groups[q['gkey']]['id']}")
            if q.get("also"): keys.append("also_in={" + "; ".join(q["also"]) + "}")
            L.append("\\begin{bankq}[" + ", ".join(keys) + "]\n" + q["text"] + "\n\\end{bankq}")
            used_imgs |= set(re.findall(r"\\bfigi?\{[^}]*\}\{([^}]*)\}", q["text"]))
            index.append(row(q, code, title)); n += 1
        L.append("\\end{document}")
        tp = os.path.join(cdir, name + ".tex")
        open(tp, "w").write("\n".join(L) + "\n")
        for f in used_imgs:
            if os.path.exists(os.path.join(tmp, f)): shutil.copy(os.path.join(tmp, f), os.path.join(cdir, "img", f))
        ok, err = True, ""
        if compile_check:
            for _ in range(2):
                r = subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", os.path.basename(tp)],
                                   cwd=cdir, capture_output=True, text=True, errors="replace")
            ok = r.returncode == 0
            if not ok:
                err = " | ".join(l for l in r.stdout.split("\n") if l.startswith("!") or l.startswith("l."))[:300]
            for ext in (".pdf", ".aux", ".log", ".out"):
                if os.path.exists(tp[:-4] + ext): os.remove(tp[:-4] + ext)
        sdir = os.path.join(out, SUBJ_NAME[subj]); os.makedirs(sdir, exist_ok=True)
        with zipfile.ZipFile(os.path.join(sdir, name + ".zip"), "w", zipfile.ZIP_DEFLATED) as z:
            z.write(tp, name + "/" + name + ".tex")
            for f in sorted(os.listdir(os.path.join(cdir, "img"))):
                z.write(os.path.join(cdir, "img", f), name + "/img/" + f)
        built.append((code, title, n, len(dmap), ok, err))
    import csv
    with open(os.path.join(out, "index.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["id", "chapter", "chapter_title", "subtopic", "source_test", "paper", "section", "qno", "type", "answer",
                    "answer_src", "has_figure", "passage", "duplicate_of", "also_in", "difficulty", "difficulty_band",
                    "diff_parts"])
        w.writerows(index)
    print(f"built {sum(1 for b in built if b[4])}/{len(built)} chapters from {len(tests)} tests: "
          f"{len(allq)} questions, {ndup} duplicates merged")
    for code, title, n, d, ok, err in built:
        print(f"  {'ok  ' if ok else 'FAIL'} {code} {title}: {n} questions" + (f", {d} duplicates" if d else "") +
              (f"  -- {err}" if err else ""))
    shutil.rmtree(tmp, ignore_errors=True)
    shutil.rmtree(os.path.join(out, "_build"), ignore_errors=True)
    if any(not b[4] for b in built): sys.exit(1)


def row(q, code, title, dup=""):
    return [q["bid"], code, title, q.get("subtopic") or "", q["test"], q["paper"], q["section"], q["qnum"], q["type"],
            plain(q["answer"] or "", 60), q["answer_src"], int(bool(re.search(r"\\bfigi?\{", q["text"]))),
            "yes" if q["gkey"] else "", dup, "; ".join(q.get("also", [])), q.get("difficulty") or "",
            diff_band(q["difficulty"]) if q.get("difficulty") else "", q.get("diff_parts") or ""]


def pct_esc(s):
    return re.sub(r"(?<!\\)%", r"\\%", s)


def tex_esc(s):
    return s.replace("&", "\\&").replace("%", "\\%").replace("#", "\\#")


def tex_ans(a):
    a = (a or "").replace("->", "$\\to$").replace("→", "$\\to$").replace("&", "\\&").replace("%", "\\%").replace("_", "\\_")
    return a


FO_ROOT = "D:\\Aryan DOWNLOADS\\Final Output\\"


def part_of(name):
    """fixed half of the bank a test belongs to (two question-bank tasks run in parallel): 'A' or 'B'"""
    return "AB"[int(hashlib.sha1(name.encode("utf-8")).hexdigest(), 16) % 2]


def sync(bank_path, conv_paths, part=None):
    """add every test that a conversion manifest marks done (and that is not yet in the bank manifest) to the bank
    manifest as pending, with its paths relative to Final Output: tex_rel, img_rel, src_rel"""
    bank = json.load(open(bank_path)) if os.path.exists(bank_path) else {"root": FO_ROOT, "tests": []}
    have = {t["name"] for t in bank["tests"]}
    added = []
    for cp in conv_paths:
        if not os.path.exists(cp):
            print(f"  (skipped {cp}: not found)"); continue
        m = json.load(open(cp))
        ro, rs = m["root_output"].rstrip("\\") + "\\", m["root_source"].rstrip("\\") + "\\"
        for t in m["tests"]:
            if t.get("status") != "done":
                continue
            srcs = t["source_rel"] if isinstance(t["source_rel"], list) else [t["source_rel"]]
            folder, base = srcs[0].rsplit("\\", 1) if "\\" in srcs[0] else ("", srcs[0])
            name = t.get("output_name") or base[:-4]
            if name in have or (part and part_of(name) != part):
                continue
            outdir = (ro + folder + "\\") if folder else ro
            rel = lambda x: x[len(FO_ROOT):] if x.startswith(FO_ROOT) else x
            e = dict(name=name, tex_rel=rel(outdir + name + ".tex"), img_rel=rel(outdir + name + "-img"),
                     src_rel=[rel(rs + x) for x in srcs], status="pending",
                     conv_note=(t.get("note") or "")[:200])
            bank["tests"].append(e); have.add(name); added.append(name)
    json.dump(bank, open(bank_path, "w"), indent=1, ensure_ascii=False)
    print(f"added {len(added)} tests to {bank_path} (now {len(bank['tests'])})")
    for a in added[:200]: print("  +", a)


# --------------------------------------------------------------------------------------------- manifest
def _fp(e):
    return hashlib.sha1(json.dumps(e, sort_keys=True).encode()).hexdigest()[:12]


def _find(m, test):
    """--test "<series keyword(s)> <number>", e.g. "SRG 04", "Nurture SRG 03", "FIITJEE 034", "Score-I 05" """
    mm = re.match(r"^(.*?)[\s_]*(\d+)(?:-(\d+))?$", str(test).strip())
    if not mm: sys.exit(f"bad --test {test!r}")
    key, num = mm.group(1).strip(" -").lower(), int(mm.group(2))
    want = f"{num}-{int(mm.group(3))}" if mm.group(3) else str(num)
    cand = [t for t in m["tests"] if re.sub(r"^0+(?=\d)", "", test_digits(t["name"])) == want]
    if key:
        nk = lambda x: re.sub(r"[^a-z0-9]", "", x.lower())          # 'Nurture General' = 'Nurture (General)'
        key = nk(key)
        exact = [t for t in cand if nk(series_of(t["name"])) == key or
                 nk(SERIES_ABBR.get(series_of(t["name"]), "")) == key]
        starts = [t for t in cand if nk(series_of(t["name"])).startswith(key)]
        cont = [t for t in cand if key in nk(series_of(t["name"]))]
        cand = exact or (starts if len(starts) == 1 else []) or cont
    if len(cand) != 1:
        sys.exit(f"test {test}: {len(cand)} manifest entries match - use the full series name, e.g. "
                 f"'{series_of(cand[0]['name']) if cand else 'SRG (Enthusiast)'} {num:02d}'")
    return cand[0]


def manifest_cmd(path, action, test=None, sets=(), unset=(), expect=None, previous=None):
    m = json.load(open(path))
    if action == "show":
        print("parts:", dict(collections.Counter(part_of(t["name"]) for t in m["tests"])))
        c = collections.Counter(t["status"] for t in m["tests"])
        print(dict(c))
        for t in m["tests"]:
            if t["status"] != "done" or t.get("fix_note"):
                print("  " + json.dumps(t, ensure_ascii=False))
        return
    e = _find(m, test)
    if action == "set":
        for s in sets:
            k, v = s.split("=", 1)
            if v == "now": v = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
            e[k] = v
        for k in unset: e.pop(k, None)
        json.dump(m, open(path, "w"), indent=1, ensure_ascii=False)
        print("fingerprint", _fp(e)); print(json.dumps(e, ensure_ascii=False))
    elif action == "verify":
        ok = _fp(e) == expect
        print("OK" if ok else f"MISMATCH (now {_fp(e)}): {json.dumps(e, ensure_ascii=False)}")
        if previous and os.path.exists(previous):
            pv = {t["name"]: t for t in json.load(open(previous))["tests"]}
            rank = {"pending": 0, "in_progress": 1, "done": 2, "skipped": 2, "failed": 2}
            for t in m["tests"]:
                o = pv.get(t["name"])
                if o and o != t and t is not e:
                    bad = rank.get(t["status"], 0) < rank.get(o["status"], 0)
                    print(("SUSPICIOUS (status went backwards) " if bad else "info: changed ") + t["name"])
        if not ok: sys.exit(1)


# --------------------------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("chapters"); p.add_argument("--subtopics", nargs="*", help="print subtopic lists (all, or these codes)")
    p = sp.add_parser("parse"); p.add_argument("tex"); p.add_argument("-o", "--out", required=True)
    p.add_argument("--name"); p.add_argument("--img")
    p = sp.add_parser("keyprep"); p.add_argument("pdf"); p.add_argument("-o", "--out", required=True); p.add_argument("--work")
    p = sp.add_parser("apply"); p.add_argument("work"); p.add_argument("--chapters"); p.add_argument("--answers")
    p.add_argument("--difficulty", help="difficulty.tsv: <qid> TAB <K S I C> TAB <reason> (see `difficulty`)")
    sp.add_parser("difficulty", help="print the difficulty rubric")
    p = sp.add_parser("pack"); p.add_argument("work"); p.add_argument("-o", "--out", required=True)
    p = sp.add_parser("build"); p.add_argument("zipdir"); p.add_argument("-o", "--out", required=True)
    p.add_argument("--only", nargs="*"); p.add_argument("--no-compile", action="store_true")
    p = sp.add_parser("sync"); p.add_argument("bank_manifest"); p.add_argument("conv_manifests", nargs="+")
    p.add_argument("--part", choices=["A", "B"], help="only tests of this half of the bank (see part_of)")
    p = sp.add_parser("manifest"); p.add_argument("path"); p.add_argument("action", choices=["show", "set", "verify"])
    p.add_argument("--test"); p.add_argument("--set", action="append", default=[]); p.add_argument("--unset", action="append", default=[])
    p.add_argument("--expect"); p.add_argument("--previous")
    a = ap.parse_args()
    if a.cmd == "chapters":
        for s in ("phy", "chem", "math"):
            print(f"== {SUBJ_NAME[s]}")
            for c, ss, t in CHAPTERS:
                if ss == s:
                    print(f"  {c}  {t}")
                    if a.subtopics is not None and (not a.subtopics or c in a.subtopics):
                        for x in SUBTOPICS.get(c, []): print(f"         - {x}")
    elif a.cmd == "parse": parse(a.tex, a.out, a.name, a.img)
    elif a.cmd == "difficulty": print(DIFF_RUBRIC)
    elif a.cmd == "keyprep": keyprep(a.pdf, a.out, a.work)
    elif a.cmd == "apply":
        _, errs = apply(a.work, a.chapters, a.answers, a.difficulty)
        if errs: sys.exit(1)
    elif a.cmd == "pack": pack(a.work, a.out)
    elif a.cmd == "build": build(a.zipdir, a.out, a.only, not a.no_compile)
    elif a.cmd == "sync": sync(a.bank_manifest, a.conv_manifests, a.part)
    elif a.cmd == "manifest": manifest_cmd(a.path, a.action, a.test, a.set, a.unset, a.expect, a.previous)


if __name__ == "__main__":
    main()
