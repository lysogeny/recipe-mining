#!/usr/bin/env python3

"""Make metadata csv"""

import argparse

import pandas as pd

import recipes

def get_ingredients(entry):
    """Gets dataframe of ingredients for recipe"""
    ingredients = entry['ingredients']
    ingredient = [ingredient[0] for ingredient in ingredients]
    quantity = [' '.join(ingredient[1]) for ingredient in ingredients]
    base = {'ingredient': ingredient, 'quantity': quantity}
    meta = {key: entry[key]
            for key in entry
            if key not in ['instructions', 'comments', 'ingredients']}
    base.update(meta)
    return pd.DataFrame(base)

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Concatenate recipes into metadata")
    parser.add_argument("input", nargs="+", type=str, help="input files")
    parser.add_argument("-o", "--output", type=str, help="Output recipes to file")
    parser.add_argument("-i", "--ingredients", type=str, help="Output ingredients to file")
    args = parser.parse_args()
    data = map(recipes.read_recipe, args.input)
    data = list(data)
    if 'output' in args:
        outdata = pd.DataFrame(data)
        outdata.drop(["comments", "ingredients"], axis=1).to_csv(args.output, index=False)
    if 'ingredients' in args:
        # get ingredients and put into file
        ingredients = map(get_ingredients, data)
        dataframes = map(pd.DataFrame, ingredients)
        pd.concat(dataframes).to_csv(args.ingredients, index=False)

#files =[f"json/{i}" for i in os.listdir("json")]
#data = map(recipes.read_recipe, files)
#
#onedata = next(data)


if __name__ == "__main__":
    main()
