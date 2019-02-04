import argparse
from typing import List, Tuple

Token = str
Tag = str
Example = List[Tuple[Token, Tag]]


def parse_example(example: str) -> Example:
    """Given an example file in CRF++ format, parses it into
    tokens and tags.

    Args:
        example: A string representing an example, formatted as CRF++ requests.
    Returns:
        A list of (token, tag) tuples.
    """
    pairs = []
    for line in example.split("\n"):
        if line.strip():
            token, _, _, _, _, tag = line.split("\t")
            pairs.append((token, tag))
    return pairs


def parse_crfpp_file(filepath: str) -> List[Example]:
    """Opens and parses a CRF++-formatted file into examples consisting
    of (token, tag) tuples.

    Args:
        filepath: The path to the CRF++ file.
    Returns:
        A list of examples, where each example is a list of tokens and tags.
    """
    sequences = []
    with open(filepath) as crfpp_file:
        examples = crfpp_file.read().split("\n\n")
        for example in examples:
            if example:
                sequences.append(parse_example(example))
    return sequences


def write_to_seqtag_file(sequences: List[Example], dest_filepath: str) -> None:
    """Given a list of examples, formats the examples as requested by AllenNLP,
    and writes them to a file.

    Args:
        sequences: A list of examples
        dest_filepath: The path to the desired file to write the conversion to 
        (will be created if doesn't exist)
    """
    with open(dest_filepath, "w+") as out_file:
        for seq in sequences:
            seq_line = "\t".join(["###".join(pair) for pair in seq])
            out_file.write(seq_line + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="Converts a CRF++-formatted file into a SequenceTagging file as requested by AllenNLP."
    )

    parser.add_argument(
        "in_filepath", type=str, help="Path to the CRF++-formatted file."
    )

    parser.add_argument(
        "out_filepath", type=str, help="Path to the desired output file."
    )

    args = parser.parse_args()
    sequences = parse_crfpp_file(args.in_filepath)
    write_to_seqtag_file(sequences, args.out_filepath)


if __name__ == "__main__":
    main()
