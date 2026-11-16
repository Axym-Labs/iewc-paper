# IEWC paper

LaTeX source for *Improved Elastic Weight Consolidation as an Optimization Constraint for Continual Learning*.

`main.tex` is the single source for the arXiv version (default) and the
anonymous TMLR submission (`tmlr.tex` sets the TMLR switch: official
unmodified `tmlr.sty`, no authors or links line, first-page AI-assistance
footnote instead of the AI-use subsection). Build with:

```bash
make paper   # arXiv version, main.pdf
make tmlr    # anonymous TMLR submission, tmlr.pdf
make arxiv   # arXiv package dist/iewc-arxiv.zip and preview dist/iewc-arxiv.pdf
```

The former AISTATS 2027 build and the previous `tmlr/` build are in
`archive/`.

All quantitative plots are PGFPlots/TikZ sources in `figures/tikz/`, drawn
inline at their final width with the shared styles in
`figures/iewc_plot_styles.tex`. They are generated from the retained experiment
records by `scripts/generate_tikz_figures.py`; use `make regenerate` after
changing data, plot styles, or the generator. The front-page conceptual
illustration is a vector PDF built by `figures/build_overview.py`, which the
standard build refreshes when needed.

- [Paper (arXiv:2611.16039)](https://arxiv.org/abs/2611.16039)
- [Project page](https://axym.org/work/iewc/)
- [Code](https://github.com/Axym-Labs/iewc)
