#!/usr/bin/env python3

"""Make metadata csvs"""

import os
import argparse

import numpy as np
import pandas as pd

import recipes

def get_ingredients(entry):
    """Gets dataframe of ingredients for recipe"""
    ingredients = entry['ingredients']
    ingredient = [ingredient[0] for ingredient in ingredients]
    quantity = [' '.join(ingredient[1]) for ingredient in ingredients]
    base = {'filename': entry['filename'], 'ingredient': ingredient, 'quantity': quantity}
    #meta = {key: entry[key]
    #        for key in entry
    #        if key not in ['instructions', 'comments', 'ingredients', 'categories']}
    #base.update(meta)
    return pd.DataFrame(base)

def get_comments(entry):
    """Gets dataframe of ingredients for recipe"""
    comments = entry['comments']
    if comments:
        base = {'filename': entry['filename']}
    else:
        base = {}
    for comment in comments:
        for key in comment:
            if key not in base:
                base[f"comment_{key}"] = []
            base[f"comment_{key}"].append(comment[key])
    # need to turn a list of dicts into a dict of lists
    #meta = {key: entry[key]
    #        for key in entry
    #        if key not in ['instructions', 'comments', 'ingredients', 'categories']}
    #base.update(meta)
    return pd.DataFrame(base)

def get_categories(entry):
    """Gets dataframe of ingredients for recipe"""
    categories = entry['categories']
    base = {'category': categories, 'filename': entry['filename']}
    #meta = {key: entry[key]
    #        for key in entry
    #        if key not in ['instructions', 'comments', 'ingredients', 'categories']}
    #base.update(meta)
    return pd.DataFrame(base)

def get_ingredient_matrix(entries, numeric=False):
    """Gets an ingredient matrix for a collection of recipes

    The ingredient matrix can either be numeric (by parsing ingredient values)
    or boolean (a matrix of ingredient presence)
    """
    # pylint: disable=no-else-raise
    ingredients = list(set(entries.ingredient))
    recipe_names = list(set(entries.filename))
    if numeric:
        raise NotImplementedError("I haven't bothered to implement this yet")
    else:
        output = np.zeros((len(recipe_names), len(ingredients)))
        for recipe_id, recipe in enumerate(recipe_names):
            these_ingredients = entries.ingredient[entries.filename == recipe]
            for ingredient_id, ingredient in enumerate(ingredients):
                output[recipe_id, ingredient_id] = ingredient in these_ingredients
    return pd.DataFrame(output, index=recipe_names, columns=ingredients)

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Concatenate recipes into metadata")
    parser.add_argument("input", nargs="+", type=str, help="input folder")
    parser.add_argument("-o", "--output", type=str, help="Output recipes to file")
    parser.add_argument("-i", "--ingredients", type=str, help="Output ingredients to file")
    parser.add_argument("-c", "--categories", type=str, help="Output categories to file")
    parser.add_argument("-m", "--comments", type=str, help="Output comments to file")
    parser.add_argument("-x", "--matrix", type=str, help="Output Ingredient matrix to file")
    args = parser.parse_args()
    inputs = [f"{args.input[0]}{os.path.sep}{i}" for i in os.listdir(args.input[0])]
    data = map(recipes.read_recipe, inputs)
    data = list(data)
    if args.output:
        outdata = pd.DataFrame(data)
        outdata.drop(["categories", "comments", "ingredients"],
                     axis=1).to_csv(args.output, index=False)
    if args.ingredients:
        # get ingredients and put into file
        ingredients = map(get_ingredients, data)
        dataframes = map(pd.DataFrame, ingredients)
        pd.concat(dataframes).to_csv(args.ingredients, index=False)
    if args.categories:
        categories = map(get_categories, data)
        dataframes = map(pd.DataFrame, categories)
        pd.concat(dataframes).to_csv(args.categories, index=False)
    if args.comments:
        comments = map(get_comments, data)
        dataframes = map(pd.DataFrame, comments)
        pd.concat(dataframes).to_csv(args.comments, index=False)
    if args.matrix:
        ingredients = map(get_ingredients, data)
        dataframes = map(pd.DataFrame, ingredients)
        mat = get_ingredient_matrix(pd.concat(dataframes))
        mat.to_csv(args.matrix, index=False)

#files =[f"json/{i}" for i in os.listdir("json")]
#data = map(recipes.read_recipe, files)
#
#onedata = next(data)


if __name__ == "__main__":
    main()
