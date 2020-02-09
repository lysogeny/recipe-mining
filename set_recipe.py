#!/usr/bin/env python3
"""
Typeset a recipe
"""

import argparse
import gzip
import json
import pprint

RECIPE_TEMPLATE = """---
title: {title}
author: {author}
date: {date}
papersize: a4
---

Dauer
: {preptime}

Schwierigkeit
: {difficulty}

Bewertung
: {rating} ({rates} Bewertungen)

## Zutaten (für {servings} Portionen)

{ingredients}

## Zubereitung

{instructions}
"""

def format_comments(comments):
    """Formats ingredients"""
    out = ""
    for comment in comments:
        out += f"{comment['user']}\n:{' '.join(comment['text'].split())}\n\n"
    return out.strip()

def format_ingredients(ingredients):
    """Formats ingredients"""
    out = ""
    for ingredient in ingredients:
        out += f"{ingredient[0]}\n: {' '.join(ingredient[1])}\n\n"
    return out.strip()

def recipe_to_markdown(recipe):
    """Converts recipe to markdown"""
    recipe['ingredients'] = format_ingredients(recipe['ingredients'])
    return RECIPE_TEMPLATE.format(**recipe)

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Typeset a recipe")
    parser.add_argument("input", nargs=1, type=str, help="Recipe to typeset")
    parser.add_argument("-o", "--output", nargs="?", type=str, help="File to output recipe at")
    args = parser.parse_args()
    with gzip.open(args.input[0], 'rt') as connection:
        recipe = json.load(connection)
    if args.output:
        with open(args.output, 'w') as connection:
            connection.write(recipe_to_markdown(recipe))
    else:
        print(recipe_to_markdown(recipe))


if __name__ == "__main__":
    main()
