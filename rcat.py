#!/usr/bin/env python3
"""
Cat a recipe
"""
import argparse
import gzip
import json
import pprint

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Print a recipe")
    parser.add_argument("input", nargs="+", type=str, help="recipe file")
    args = parser.parse_args()
    for input_file in args.input:
        with gzip.open(input_file, 'rt') as connection:
            recipe = json.load(connection)
        pprint.pprint(recipe)

if __name__ == "__main__":
    main()
