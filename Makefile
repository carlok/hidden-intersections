# hidden-intersections: build PDFs, run the verification scripts, assemble the static site.
PYTHON ?= python3
TECTONIC ?= tectonic

THEORY_PDFS := pdf/theory.pdf pdf/writeup.pdf pdf/alt_quandle_note.pdf
.PHONY: all pdf verify site clean help

all: verify pdf site

help:
	@echo "make verify  - run every verification script (logs in verify/)"
	@echo "make pdf     - compile theory, writeup, alt note, examples, transcript, classification into pdf/"
	@echo "make site    - assemble _site/ (app + pdf) exactly as GitHub Pages serves it"
	@echo "make clean   - remove _site/ and LaTeX by-products"

pdf:
	mkdir -p pdf
	cd theory && for f in theory writeup alt_quandle_note; do $(TECTONIC) -o ../pdf $$f.tex; done
	cd exercises && $(TECTONIC) -o ../pdf examples16.tex
	cd video && $(TECTONIC) -o ../pdf quilez_transcript.tex
	cd classification && $(PYTHON) classification_build.py && $(TECTONIC) -o ../pdf classification.tex
	@echo "Storyboard PDFs in pdf/ are committed: they need locally rendered frame dumps (not in git)."

verify:
	cd verify && $(PYTHON) verify.py
	cd verify && $(PYTHON) verify_inversive.py
	cd verify && $(PYTHON) alt_verify.py
	cd verify && $(PYTHON) alt3_verify.py
	cd verify && $(PYTHON) ../exercises/examples16.py
	cd verify && PYTHONPATH=../exercises $(PYTHON) theory_verify.py
	cd verify && $(PYTHON) classification_verify.py
	$(PYTHON) verify/check_logs.py

site:
	rm -rf _site && mkdir -p _site/pdf _site/docs
	cp app/index.html _site/
	cp pdf/*.pdf _site/pdf/
	cp docs/*.png _site/docs/
	touch _site/.nojekyll

clean:
	rm -rf _site
	find . \( -name '*.aux' -o -name '*.log' -o -name '*.out' -o -name '*.toc' -o -name '*.synctex.gz' \) -not -path './.git/*' -delete
	find . -name __pycache__ -type d -prune -exec rm -rf {} +
