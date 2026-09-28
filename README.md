# IEWC paper

LaTeX source for *Improved Elastic Weight Consolidation as an Optimization Constraint for Continual Learning*.

Build with:

```bash
make paper
```

All quantitative plots have editable PGFPlots/TikZ sources in
`figures/tikz/`. They are generated from the retained experiment records by
`scripts/generate_tikz_figures.py` and compiled once into cached vector PDFs in
`figures/rendered/`, following the space-efficient KPSA paper workflow. Use
`make regenerate` after changing data, plot styles, or the generator. The
front-page conceptual illustration remains a custom vector PDF, and the
qualitative diffusion sample grid remains an image. Its editable generator is
`figures/build_overview.py`, and the standard build refreshes it when needed.

- [Project page](https://axym.org/work/iewc)
- [Code](https://github.com/Axym-Labs/iewc)
