"""Partitions the provided NYT dataset into training and unseen-testing datasets."""

import pandas as pd
from sklearn.model_selection import train_test_split

RATIO = 0.2 # Partition existing dataset into 40% testing

def main():
    """
    Partitions the provided NYT dataset into training and unseen-testing datasets.
    """
    dataframe = pd.read_csv('../data/nyt-ingredients-snapshot-2015.csv')
    dataframe.dropna(subset=['input']) # Drop rows where input text = NaN
    train, test = train_test_split(dataframe, test_size=RATIO)
    train.to_csv('../data/train.csv')
    test.to_csv('../data/test.csv')

if __name__ == "__main__":
    main()
