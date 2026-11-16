# AISTATS 2027 build (archived)

The paper moved from AISTATS 2027 to TMLR on 2026-09-29 (see
`iewc-paper-internal/resubmission-1/progress.md`). These files are the
AISTATS-only parts of the source, removed from the active build:

- `main.tex`: the anonymous AISTATS `main.tex` as of commit `9693870`
  (two-column `aistats2027` layout, lead figure in the title block, checklist,
  supplementary title).
- `aistats2027.sty`, `fancyhdr.sty`: the AISTATS style files.
- `sec17_reproducibility_checklist.tex`: the AISTATS checklist.

To rebuild, check out commit `20dc3bf` (last commit with the AISTATS build in
`main.tex`, default `\arxivfalse`) and run `make paper`, or copy these files
back to the repository root and `sections/`.
