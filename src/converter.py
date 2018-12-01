"""Converts full_format_recipes.json into test.csv"""

import json

import pandas as pd

def main():
    """Converts full_format_recipes.json into test.csv"""
    # full_format_recipes.json from
    # https://www.kaggle.com/hugodarwood/epirecipes#full_format_recipes.json

    test_data = {
        "input": [],
        "name": [],
        "qty": [],
        "range_end": [],
        "unit": [],
        "comment": [],
    }
    with open("../data/full_format_recipes.json") as f:
        recipes = json.load(f)
        recipes = [r for r in recipes if r != {}]
        for recipe in recipes:
            for ingredient in recipe["ingredients"]:
                test_data["input"].append(ingredient)
                test_data["name"].append(None)
                test_data["qty"].append(None)
                test_data["range_end"].append(None)
                test_data["unit"].append(None)
                test_data["comment"].append(None)

    df = pd.DataFrame(data=test_data)
    df.to_csv("../data/test.csv")

if __name__ == "__main__":
    main()
