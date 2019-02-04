import pandas as pd
from sklearn.model_selection import train_test_split
import argparse


def main():
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    nyt_df = pd.read_csv("data/nyt-ingredients-snapshot-2015.csv")
    nyt_df = nyt_df.dropna(subset=["input"])
    print(nyt_df.isna().sum())

    train_df, test_df = train_test_split(nyt_df, train_size=130000)
    test_df, valid_df = train_test_split(test_df, train_size=481)

    train_df.to_csv("data/train.csv")
    test_df.to_csv("data/test.csv")
    valid_df.to_csv("data/valid.csv")


if __name__ == "__main__":
    main()
