# CLAUDE.md — DNB Radiodiagnosis Final Theory revision workspace

This file auto-loads each session. Read it before doing anything.

## Project

Revision workspace for the **DNB Radiodiagnosis Final Theory** exam: 4 papers × 100 marks,
each paper = **10 short-note questions × 10 marks**, 3 hours, Parts A & B (5+5). Pass ≥ 200/400.
The owner is a DNB candidate. **Exam date noted in the tracker as 18 Jun (2 PM)** — verify against
the current NBE bulletin; the bulletin is the final word.

**Current focus: Paper I only.** The tracker's completeness scores are filled in for Paper I
categories; Papers II–IV are intentionally blank (not yet scored). Do not treat the blank
Paper II–IV rows as "highest priority" — they are simply unscored.

## Folder structure

```
DNB_Radiodiagnosis_Tracker.xlsx   <- master tracker (binary; read via the script below)
README.md                          <- human-facing repo index
CLAUDE.md                          <- this file
scripts/
  dump_tracker.py                  <- dump the workbook + per-category priority roll-up
  setup_extract.py                 <- one-time: extract/flatten the revision zip (idempotent)
pyproject.toml, uv.lock, .venv/    <- uv-managed Python env (openpyxl)
paper-1-musculoskeletal/           <- Paper I → Musculoskeletal (10 topics) — BUILT
  README.md                        <- category index + frequency weighting
  01-skeletal-trauma/ ... 10-haematological-skeletal/
    reading.md                     <- full revision prose + embedded images
    questions.md                   <- questions WITH complete written answers
    images/                        <- downloaded images for this topic
      images.md                    <- manifest: source URL, license, intended finding, verified?
```

Paper I categories still to build: **Head & Neck** (next), Neuroradiology, Endocrine, Breast.
Papers II–IV: pending (tracker not yet scored).

## File-format conventions (match existing files exactly)

**reading.md** — full, readable revision material the owner can study and revise *from*
(NOT terse pointers). Order:
1. Classification / enumeration (the framework first — marks live in the system).
2. Modality-wise findings in the order **XR → US → CT → MRI → nuclear**.
3. Differentials / comparison tables.
4. Pearls & buzzwords.
5. **What to draw** (diagrams the candidate should reproduce by hand in the exam).
6. Further reading.
- Embed the most important diagrams/images inline with markdown `![alt](images/file.ext)`.
  Alt text states the finding shown.

**questions.md** — order:
1. **Previously asked (NBE)** — real past questions, tagged with the session (paper + month/year + Q#)
   where known. **NEVER fabricate a citation.** If unsure of the exact session, mark it
   `(session unconfirmed)` rather than inventing one.
2. **Practice questions** — DNB subjective format with mark splits, e.g. `[4+6]`, `[3+(4+3)]`.
3. **Complete answers** — full, correct, exam-ready written answers (NOT skeleton pointers),
   one per question, structured the way a candidate should write them.

## Images

- Stored per-topic in `<topic>/images/`, logged in `<topic>/images/images.md`.
- Manifest columns: filename · source URL · license · finding it is meant to show · `verified?`.
- Images are **downloaded**, not generated. **Embed every image inline** with
  `![alt](images/file)` so it renders in the GitHub markdown UI — avoid broken/missing links.
- **Copyright is not a concern**: the repo is private and for the owner's personal exam study
  only. Prefer the most *correct* image (Radiopaedia, PMC open-access, textbook figures) —
  quality over licence.
- **Verify visually**: read each downloaded image (the Read tool renders it) and confirm it
  shows the stated finding; set `verified? = YES` when confirmed, else leave `NO` with a note.
- Reusable downloader: `uv run scripts/fetch_images.py <topic_dir> <sources.json>`
  (source lists live in `scripts/sources/`). It downloads files and rebuilds `images.md`.

## Prioritisation logic

`Priority = question frequency (tracker 'Cat marks/session' weight) × my gap (10 − completeness)`.
Highest first. Build in priority order **within Paper I**. MSK is #1 (highest weight ~33 AND
largest gap, completeness ~3/10).

## Honesty rules (non-negotiable)

- There is **NO official per-topic mark allocation.** The weights are *empirical frequency*
  from a small sample of past papers — treat as **emphasis, not prediction**.
- Content is exam **scaffolding to pair with image plates**, not a substitute for textbook films.
- **Flag anything uncertain** rather than inventing specifics (numbers, classifications, eponyms).
- **NEVER fabricate a past-paper citation.** Real session or `(unconfirmed)` — nothing in between.

## How to read the tracker

Binary `.xlsx`, so use the script (uv handles the env automatically):

```
uv run scripts/dump_tracker.py                 # all sheets + per-category priority roll-up
uv run scripts/dump_tracker.py --sheet Tracker # one sheet
```

Sheets: **Tracker** (Paper → Category → Sub-category → Topic, with weight, freq tier, est min,
Status, Priority, Completeness), **Dashboard** (per-category counts / % done),
**Sources & Method** (how weights were derived + caveats). The roll-up treats blank completeness
as a full gap of 10 — meaningful only for the scored Paper I rows; ignore the inflated
Paper II–IV priorities until those are scored.
