Recipe Mining
=============

Tools for mining recipes from the internet.

A couple of tools are provided here to automatically fetch recipes, and parse
them into a common format.

Recipes can be downloaded from a random-recipe-endpoint as `gzip` compressed
(default) `html` into a directory (default `html`) using `get_random_recipes.py`.

With `parse_recipe.py` Recipes from the default endpoint can be parsed into
a `gzip` compressed `json` structure.

`metadata.py` can concatenate the recipes into two types of `csv`.

Requirements
------------

- python3
- BeautifulSoup (for parsing)
- requests (for fetching)
- pandas (for creating csvs)

