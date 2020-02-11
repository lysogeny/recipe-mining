#!/usr/bin/env python3
# I don't think these long lines can easily be avoided...
#pylint: disable=line-too-long

"""Parse the structure of a recipe"""

import json
import gzip
import argparse
import pprint

from bs4 import BeautifulSoup

FILE = "test.html"

def html_to_dict(string):
    """Converts the recipe html to a dict"""
    soup = BeautifulSoup(string, 'html.parser')
    recipe = {}
    recipe['title'] = soup.find("h1").string
    try:
        recipe['text'] = soup.select("h1 + p")[0].string.strip()
    except IndexError:
        recipe['text'] = None
    try:
        # Case one, author still exists
        recipe['author'] = soup.find("div", class_="recipe-author").find_all("span")[-1].text.strip()
    except IndexError:
        # author was deleted
        recipe['author'] = soup.find("div", class_="recipe-author").find("div", class_="ds-mb-right").text.strip()
    ingredients = soup.find("table", class_="ingredients").find_all("tr")
    recipe['ingredients'] = [(i.find('td', class_="td-right").text.strip(),
                              i.find('td', class_="td-left").text.strip().split()
                              )
                             for i in ingredients
                             if i.find("th") is None]
    recipe["servings"] = soup.find("div", class_="recipe-servings").find("input").attrs['value']
    recipe["rating"] = soup.find("div", class_="ds-rating-avg").find("strong").text
    recipe["rates"] = soup.find("div", class_="ds-rating-count").find("strong").text
    # any and all of these might actually be optional. Currently it only looked
    # like kcal is optional.
    recipe["preptime"] = soup.find("span", class_="recipe-preptime").find(text=True, recursive=False).strip()
    recipe["difficulty"] = soup.find("span", class_="recipe-difficulty").find(text=True, recursive=False).strip()
    recipe["date"] = soup.find("span", class_="recipe-date").find(text=True, recursive=False).strip()
    try:
        recipe["kcal"] = soup.find("span", class_="recipe-kcalories").find(text=True, recursive=False).strip()
    except AttributeError:
        recipe["kcal"] = None
    # instruction_meta = soup.find("small", class_="ds-recipe-meta")
    # instruction_meta doesn't seem reliable.
    instructions = soup.select("small.ds-recipe-meta + div.ds-box")[0]
    recipe["instructions"] = instructions.text.strip()
    recipe["comment_count"] = soup.find("button", class_="recipe-comments-anchor").find("span").text
    comments = soup.find("article", class_="recipe-comments")
    comments = comments.find_all("div", class_="comment-item")
    recipe['comments'] = []
    for comment in comments:
        comment = {
            "user": comment.find("strong").text.strip(),
            "text": comment.find("p").text.strip(),
            "date": comment.find("div", class_="comment-date").text.strip(),
        }
        recipe["comments"].append(comment)
    # Get the categories
    recipe['categories'] = [tag.text.strip() for tag in soup.select("div > a.ds-tag")]
    return recipe


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Parse a chefkoch recipe")
    parser.add_argument("input", type=str, nargs=1, help="Input file")
    parser.add_argument("-o", "--output", type=str, nargs="?", help="Output file")
    args = parser.parse_args()

    with gzip.open(args.input[0], "rt") as connection:
        content = connection.read()
    recipe = html_to_dict(content)
    recipe['filename'] = args.input[0]
    print(f"Parsed recipe for '{recipe['title']}'")
    if args.output:
        with gzip.open(args.output, 'wt') as connection:
            json.dump(recipe, connection)
    else:
        pprint.pprint(recipe)


if __name__ == "__main__":
    main()
