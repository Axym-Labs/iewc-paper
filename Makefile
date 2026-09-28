.PHONY: paper figures regenerate

paper: figures figures/overview.pdf
	tectonic main.tex

figures:
	python scripts/build_cached_figures.py

figures/overview.pdf: figures/build_overview.py
	python figures/build_overview.py

regenerate:
	python figures/build_overview.py
	python scripts/generate_tikz_figures.py
	python scripts/build_cached_figures.py --force
	tectonic main.tex
