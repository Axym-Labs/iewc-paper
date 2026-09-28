#!/usr/bin/env python3
"""Compile editable TikZ/PGFPlots sources into cached vector PDFs."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "figures" / "tikz"
OUT = ROOT / "figures" / "rendered"
STYLE = ROOT / "figures" / "iewc_plot_styles.tex"

FIGURES = (
    "classification_distribution_retention",
    "nlp_distribution_retention",
    "forecast_rollouts_longhorizon_tasknorm_selected",
    "damping_sensitivity",
    "summand_norm_ecdf",
    "contamination_diagonal_spectra",
)


def wrapper(source: Path) -> str:
    source_rel = source.relative_to(ROOT).as_posix()
    return rf"""\documentclass[tikz,border=.5pt]{{standalone}}
\usepackage{{amsmath,amssymb}}
\usepackage{{tikz}}
\usepackage{{pgfplots}}
\usetikzlibrary{{calc}}
\usepgfplotslibrary{{groupplots,fillbetween}}
\input{{figures/iewc_plot_styles.tex}}
\begin{{document}}
\setlength{{\columnwidth}}{{3.25in}}
\setlength{{\textwidth}}{{6.75in}}
\setlength{{\linewidth}}{{6.75in}}
\input{{{source_rel}}}
\end{{document}}
"""


def stale(target: Path, source: Path) -> bool:
    if not target.exists():
        return True
    target_time = target.stat().st_mtime
    return source.stat().st_mtime > target_time or STYLE.stat().st_mtime > target_time


def build(name: str) -> None:
    source = SOURCE / f"{name}.tex"
    wrapper_path = ROOT / f".iewc_build_{name}.tex"
    wrapper_pdf = OUT / f".iewc_build_{name}.pdf"
    target = OUT / f"{name}.pdf"
    wrapper_path.write_text(wrapper(source))
    try:
        subprocess.run(
            ["tectonic", "--outdir", str(OUT), str(wrapper_path)],
            cwd=ROOT,
            check=True,
        )
        wrapper_pdf.replace(target)
    finally:
        wrapper_path.unlink(missing_ok=True)
        wrapper_pdf.unlink(missing_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    rebuilt = []
    for name in FIGURES:
        source = SOURCE / f"{name}.tex"
        target = OUT / f"{name}.pdf"
        if args.force or stale(target, source):
            print(f"building {name}")
            build(name)
            rebuilt.append(name)
    if not rebuilt:
        print("cached figures are current")


if __name__ == "__main__":
    main()
