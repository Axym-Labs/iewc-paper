.PHONY: paper figures regenerate

paper: figures
	tectonic main.tex

figures:
	python scripts/build_cached_figures.py

regenerate:
	python scripts/generate_tikz_figures.py
	python scripts/build_cached_figures.py --force
	tectonic main.tex
