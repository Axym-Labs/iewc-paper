# IEWC paper

LaTeX source for *Improved Elastic Weight Consolidation as an Optimization Constraint for Continual Learning*.

Build with:

```bash
make paper
```

All quantitative plots are PGFPlots/TikZ sources in `figures/tikz/`, drawn
inline at their final width with the shared styles in
`figures/iewc_plot_styles.tex`. They are generated from the retained experiment
records by `scripts/generate_tikz_figures.py`; use `make regenerate` after
changing data, plot styles, or the generator. The front-page conceptual
illustration is a vector PDF built by `figures/build_overview.py`, which the
standard build refreshes when needed.

- [Project page](https://axym.org/work/iewc)
- [Code](https://github.com/Axym-Labs/iewc)
