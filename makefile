parser=./parse_recipe.py
typer=./set_recipe.py

html_files:=$(shell find html -type f)

json_targets:=$(html_files:html/%=json/%)
md_targets:=$(html_files:html/%=md/%.md)
pdf_targets:=$(html_files:html/%=pdf/%.pdf)

json/%: html/%
	$(parser) $< -o $@

md/%.md: json/%
	$(typer) $< -o $@

pdf/%.pdf: md/%.md
	pandoc --pdf-engine=xelatex $< -o $@

metadata.csv: $(json_targets)
	./metadata.py $(json_targets) -o $@

ingredients.csv: $(json_targets)
	./metadata.py $(json_targets) -i $@

.PHONY: json pdf md
json: $(json_targets)

md: $(md_targets)

pdf: $(pdf_targets)

all: json metadata.csv ingredients.csv
