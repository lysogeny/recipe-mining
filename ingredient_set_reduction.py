#!/usr/bin/env python3

"""
Reduce an ingredient set by common strings

"""

import argparse
from collections import deque
import csv
from pprint import pprint

import pandas as pd

def get_ingredients(file_handle: str, key='ingredient') -> list:
    """Loads ingredients from csv file

    `key` specifies the key to return from the dict
    """
    with open(file_handle, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        return [d[key] for d in reader]

def set_reduction(ingredients: list, invert=False, long_first=True) -> dict:
    """Perform ingredient set reduction

    `invert` allows for creation of an inverse mapping which is handy for
    inspecting the mapping
    `long_first` sets the ordering for the lookup. if long_first is set, long
    keys are searched first. This may reduce the chance of erraneous matches.

    This method seems to work fairly well. Most instances of onions are grouped
    together and similar.

    Difficulty is however posed by
    similar ingredients never using the basename. If the basename never occurs
    several entries are still created. (e.g. Sausages, apparently germans don't
    just write 'Wurst', but always 'Bratwurst', 'Mettwurst, ...)

    Mismatches can also happen if a short ingredient name is used as a qualifier
    in an unrelated ingredient. for example, 'Tomaten mit Basilikum' will likely
    end up with 'Basilikum' (although this is because of alphabetic ordering
    and also because germans capitalise nouns.)
    """
    ingredients.sort(key=len)
    solution = dict()
    # For speed improvements with long_first set, keys are also stored in a
    # deque, which is used for the inner for loop. This way, less sorting needs
    # to be done, as items are inserted in their correct sort order.
    keys = deque()
    for ingredient in ingredients:
        for solved in keys:
            if solved in ingredient:
                solution[solved].append(ingredient)
                break
        else:
            if long_first:
                keys.appendleft(ingredient)
            else:
                keys.append(ingredient)
            solution[ingredient] = []
    if not invert:
        # provides a real (true function) mapping.
        singular = {k: k for k in solution}
        solution = {vi: k
                    for k, v in solution.items()
                    for vi in v}
        solution.update(singular)
    return solution

def main():
    """Main function. Argument parsing and calling function"""
    # Argument parsing bit
    parser = argparse.ArgumentParser(description="Print a recipe")
    parser.add_argument("input", nargs=1, type=str, help="ingredient csv")
    parser.add_argument("-m", "--mapping", type=str, help="Where to save mapping")
    parser.add_argument("-o", "--output", type=str, help="Where to save output")
    parser.add_argument("-v", "--verbose", action="store_true", help="Be more verbose")
    args = parser.parse_args()
    # ingredient reading bit

    ingredients = pd.read_csv(args.input[0])
    ingredient_set = list(set(ingredients.ingredient))
    solution = set_reduction(ingredient_set, invert=False, long_first=True)
    if args.verbose:
        pprint(solution)
    new_set = set(solution[key] for key in solution)
    print(f"Remaining: {len(new_set)} ingredients")
    ingredients['ingredient_reduced'] = [solution[key] for key in ingredients.ingredient]
    if args.mapping:
        raise NotImplementedError("I haven't implemented the json output yet")
    if args.output:
        ingredients.to_csv(args.output)

if __name__ == "__main__":
    main()
