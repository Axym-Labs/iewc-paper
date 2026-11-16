#!/usr/bin/env bash
# Pack the arXiv version (the default build of main.tex): copy the sources to
# dist/arxiv, compile once there to produce main.bbl, and pack
# dist/iewc-arxiv.zip (sources, main.bbl, figures, link symbols; no .bib, TMLR
# files or auxiliary files). The compiled preview is dist/iewc-arxiv.pdf.
set -euo pipefail
cd "$(dirname "$0")/.."
out=dist/arxiv
rm -rf "$out" dist/iewc-arxiv.zip dist/iewc-arxiv.pdf
mkdir -p "$out/figures/tikz" "$out/sections" "$out/appendices"
cp main.tex abstract.tex arxiv.sty axym-links.sty references.bib "$out"/
cp -r axym-emoji "$out"/
cp figures/overview.pdf figures/iewc_plot_styles.tex "$out/figures"/
cp figures/tikz/*.tex "$out/figures/tikz"/
cp appendices/*.tex "$out/appendices"/
cp sections/*.tex "$out/sections"/
(cd "$out" && tectonic -X compile --keep-intermediates main.tex)
mv "$out/main.pdf" dist/iewc-arxiv.pdf
(cd "$out" && rm -f references.bib main.aux main.blg main.log main.out)
(cd "$out" && zip -qrX ../iewc-arxiv.zip .)
echo "Wrote dist/iewc-arxiv.zip and dist/iewc-arxiv.pdf"
