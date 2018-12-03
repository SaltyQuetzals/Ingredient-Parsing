"""Opens a CRF++-formatted datafile, returns sequences inside of it."""
from typing import List, Tuple

TAG_MAP = {
    'OTHER': -1,
    'B-NAME': 0,
    'I-NAME': 1,
    'B-COMMENT': 2,
    'I-COMMENT': 3,
    'B-RANGE_END': 4,
    'B-UNIT': 5,
    'B-QTY': 6
}

def parse_recipe(recipe: str) -> Tuple[List[str], List[int]]:
    rows = recipe.split('\n')
    tokens = []
    tags = []
    for row in rows:
        if not row:
            continue
        token, _, _, _, _, tag = row.split('\t')
        tokens.append(token)
        tags.append(TAG_MAP[tag])
    return tokens, tags

def read_crf_file(filename):
    with open(filename) as f:
        lines = f.read()
        recipes = lines.split('\n\n')

        values = []
        for recipe in recipes:
            parsed = parse_recipe(recipe)
            values.append(parsed)
        return values