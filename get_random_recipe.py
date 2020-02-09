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
    """Main function"""
    parser = argparse.ArgumentParser(description="Get random recipes from the internet")
    parser.add_argument("-n", "--number", type=int, nargs="?", default=1,
                        help="How many recipes to get")
    parser.add_argument("-e", "--endpoint", type=str, nargs="?", default=RECIPE_ENDPOINT,
                        help="Where to get recipes from")
    parser.add_argument("-f", "--failtime", type=int, nargs="?", default=FAIL_SLEEP_TIME,
                        help="How much time to sleep on failure")
    parser.add_argument("-t", "--time", type=int, nargs="?", default=SLEEP_TIME,
                        help="How much time to sleep between requests")
    parser.add_argument('-i', '--timeout', type=float, nargs="?", default=DEFAULT_TIMEOUT,
                        help="Timout value for requests")
    parser.add_argument("-o", "--out", type=str, nargs="?", default=OUT_DIR,
                        help="where to store recipes")
    parser.add_argument("-p", "--plain", action="store_true", default=False,
                        help="Don't compress recipe")
    args = parser.parse_args()
    recipes = 1
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
            print(f"which already exists. Skipping")
            continue
        file_name = f"{args.out}{os.path.sep}{file_name}"
        open_action = open if args.plain else gzip.open
        with open_action(file_name, "wt") as connection:
            connection.write(response.text)
            print(f"writing to '{file_name}'")
        recipes += 1

if __name__ == '__main__':
    main()
