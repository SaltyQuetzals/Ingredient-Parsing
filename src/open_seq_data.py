"""Opens a CRF++-formatted datafile, returns sequences inside of it."""
from typing import List, Tuple

TAG_MAP = {
    "OTHER": -1,
    "B-NAME": 0,
    "I-NAME": 1,
    "B-COMMENT": 2,
    "I-COMMENT": 3,
    "B-RANGE_END": 4,
    "B-UNIT": 5,
    "I-UNIT": 6,
    "B-QTY": 7,
}


def parse_recipe(recipe: str) -> Tuple[List[str], List[int]]:
    """Given a CRF-tagged recipe string, converts it into a token/tag sequence.

    Args:
        recipe: A newline-delimited CRF recipe.
    Returns:
        A tuple of (tokens, tags) where tokens are List[str], and tags are List[int]
    """
    rows = recipe.split("\n")
    tokens = []
    tags = []
    for row in rows:
        if not row:
            continue
        token, _, _, _, _, tag = row.split("\t")
        tokens.append(token)
        tags.append(TAG_MAP[tag])
    return tokens, tags


def read_crf_file(filename):
    with open(filename) as f:
        lines = f.read()
        recipes = lines.split("\n\n")

        values = []
        for recipe in recipes:
            parsed = parse_recipe(recipe)
            values.append(parsed)
        return values