#!/usr/bin/env python3
"""Gets a random recipe from chefkoch.de"""

import time
import argparse
import base64
import os
import gzip

import requests

RECIPE_ENDPOINT = "https://www.chefkoch.de/rezepte/zufallsrezept/"
OUT_DIR = "html"
SLEEP_TIME = 10
FAIL_SLEEP_TIME = 300
DEFAULT_TIMEOUT = 3

def main():
    """Main function. Handle arguments, contains main loop."""
    # Consider moving getting loop to different function.
    parser = argparse.ArgumentParser(
        description="Get random recipes from the internet. Unless otherwise\
        specified, recipes are stored as gzip compressed html."
    )
    parser.add_argument("-n", "--number", type=int, nargs="?", default=1,
                        help=f"How many recipes to get. Default 1")
    parser.add_argument("-e", "--endpoint", type=str, nargs="?", default=RECIPE_ENDPOINT,
                        help=f"Where to get recipes from. Default '{RECIPE_ENDPOINT}'.")
    parser.add_argument("-f", "--failtime", type=int, nargs="?", default=FAIL_SLEEP_TIME,
                        help=f"How much time to sleep on failure. Default {FAIL_SLEEP_TIME}s.")
    parser.add_argument("-t", "--time", type=int, nargs="?", default=SLEEP_TIME,
                        help=f"How much time to sleep between requests. Default {SLEEP_TIME}s.")
    parser.add_argument('-i', '--timeout', type=float, nargs="?", default=DEFAULT_TIMEOUT,
                        help=f"Timout value for requests. Default {DEFAULT_TIMEOUT}s.")
    parser.add_argument("-o", "--out", type=str, nargs="?", default=OUT_DIR,
                        help=f"Storage direcotory for recipes. Default {OUT_DIR}.")
    parser.add_argument("-p", "--plain", action="store_true", default=False,
                        help="Don't compress recipe")
    parser.add_argument('-r', "--population", action='store_true', default=False,
                        help="Estimate population size")
    args = parser.parse_args()
    recipes = 1
    if args.population:
        existing = len(os.listdir(args.out))
        seen = 0
    while recipes <= args.number:
        if recipes > 1:
            time.sleep(args.time)
        print(f"{time.asctime()} [{recipes:>4}/{args.number:>4}]", end=" ")
        try:
            response = requests.get(args.endpoint, timeout=args.timeout)
        except requests.exceptions.Timeout:
            print(f"Timeout getting recipe. Try again...")
            continue
        except requests.exceptions.ConnectionError:
            print(f"Connection error getting recipe. Try again...")
            continue
        print(f"Got status {response.status_code}", end=" ")
        if not response.ok:
            print("This was not okay. Sleeping...", end=" ")
            time.sleep(args.failtime)
            print("Try again")
            continue
        print(f"for recipe '{response.url}'", end=" ")
        url_id = base64.urlsafe_b64encode(response.url.encode("utf-8")).decode("utf-8")
        file_name = f"{url_id}"
        if file_name in os.listdir(args.out):
            print(f"which already exists. Skipping.", end=' ')
            if args.population:
                seen += 1
                population = (existing+recipes)/(seen/recipes)
                print(f"This puts population estimate at {population}", end='')
            print('', end='\n')
            continue
        file_name = f"{args.out}{os.path.sep}{file_name}"
        open_action = open if args.plain else gzip.open
        try:
            with open_action(file_name, "wt") as connection:
                connection.write(response.text)
                print(f"writing to '{file_name}'", end=' ')
            recipes += 1
            if args.population:
                seen += 1
        except OSError as error:
            print(f"Something went wrong writing file: {error}")
        print("\n", end='')

if __name__ == '__main__':
    main()
