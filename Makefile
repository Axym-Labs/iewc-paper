# Every build uses pdflatex (the arXiv engine) through scripts/pdflatex.sh.

.PHONY: paper arxiv tmlr regenerate

paper: figures/overview.pdf
	scripts/pdflatex.sh main.tex

arxiv: figures/overview.pdf
	./scripts/build_arxiv.sh

tmlr: figures/overview.pdf
	scripts/pdflatex.sh tmlr.tex

figures/overview.pdf: figures/build_overview.py
	python figures/build_overview.py

regenerate:
	python figures/build_overview.py
	python scripts/generate_tikz_figures.py
	scripts/pdflatex.sh main.tex
