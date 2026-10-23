# JEE question bank - Batch 4 (ALLEN) and earlier batches (cloud)

Builds a chapter-wise question bank (chapter, subtopic, answer, difficulty for every question) from the converted
tests of Batch 4, Score 2, Batch 3 and Batch 2 (214 tests), using Claude cloud sessions.

## Start a session
1. Open **claude.ai/code** (or the desktop app, choosing **Cloud**) and start a new session on this repository
   (`Aryan2802/jee-batch-4-and-previous-batched`), environment **Converter**.
2. Paste this and send:

   > Read INSTRUCTIONS.md in this repository and follow it exactly. Run fully autonomously until no work is left or you are cut off.

3. Leave it running. When it ends, start another the same way. Several can run at the same time;
   `cloud/repo_sync.py` stops them from taking the same test.

## Layout
- `<Batch> Converted/` - converted tests (.tex + images); `<Batch>/Source/` - source PDFs (mostly trimmed to the answer key)
- `bank-manifest.json` - progress (edit only through `cloud/repo_sync.py`); `BANK_LEARNINGS*.md` - notes for the sessions
- `data/` - finished per-test results; `WIP/` - checkpoints; `Chapters/`, `index.csv`, `BUILD_STATUS.txt` - the published bank
- `tools/bank_tools.py` - the bank tool; `cloud/` - session setup and safe shared-state updates
