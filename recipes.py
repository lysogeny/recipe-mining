"""
Recipe library

A recipe is a gzip compressed json file with a predefined structure.
"""

import gzip
import json

def read_recipe(file_name):
    """Reads a recipe"""
    with gzip.open(file_name, 'rt') as connection:
        recipe = json.load(connection)
    return recipe

def write_recipe(file_name, recipe):
    """Writes a recipe"""
    with gzip.open(file_name, "wt") as connection:
        json.dump(recipe, connection)
