parser=./parse_recipe.py
typer=./set_recipe.py

html_files:=$(shell find -L html -type f)

json_targets:=$(html_files:html/%=json/%)
md_targets:=$(html_files:html/%=md/%.md)
pdf_targets:=$(html_files:html/%=pdf/%.pdf)

json/%: html/%
	$(parser) $< -o $@

md/%.md: json/%
	$(typer) $< -o $@

pdf/%.pdf: md/%.md
	pandoc --pdf-engine=xelatex $< -o $@

data/metadata.csv: $(json_targets)
	./metadata.py json -o $@

data/ingredients.csv: $(json_targets)
	./metadata.py json -i $@

data/comments.csv: $(json_targets)
	./metadata.py json -m $@

data/categories.csv: $(json_targets)
	./metadata.py json -c $@

.PHONY: json pdf md
json: $(json_targets)

md: $(md_targets)

pdf: $(pdf_targets)
	
all: json data/metadata.csv data/ingredients.csv data/comments.csv data/categories.csv
