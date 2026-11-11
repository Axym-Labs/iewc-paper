SOURCE_DATE_EPOCH ?= 0
export SOURCE_DATE_EPOCH

TECTONIC_FLAGS ?= -Z deterministic-mode

.PHONY: paper tmlr regenerate

paper: figures/overview.pdf
	tectonic $(TECTONIC_FLAGS) main.tex

tmlr: figures/overview.pdf
	cd tmlr && tectonic $(TECTONIC_FLAGS) main.tex

figures/overview.pdf: figures/build_overview.py
	python figures/build_overview.py

regenerate:
	python figures/build_overview.py
	python scripts/generate_tikz_figures.py
	tectonic $(TECTONIC_FLAGS) main.tex
