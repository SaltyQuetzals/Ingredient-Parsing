"""Opens a CRF++-formatted datafile, returns sequences inside of it."""
from typing import List, Tuple

TAG_MAP = {
    "OTHER": 0,
    "B-NAME": 1,
    "I-NAME": 2,
    "B-COMMENT": 3,
    "I-COMMENT": 4,
    "B-RANGE_END": 5,
    "B-UNIT": 6,
    "I-UNIT": 7,
    "B-QTY": 8
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
