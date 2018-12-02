"""Partitions the provided NYT dataset into training and unseen-testing datasets."""

import pandas as pd
from sklearn.model_selection import train_test_split

PARTITION_SIZE = 500 # Partition existing dataset into 500 testing

def main():
    """
    Partitions the provided NYT dataset into training and unseen-testing datasets.
    """
    dataframe = pd.read_csv('../data/nyt-ingredients-snapshot-2015.csv', index_col=0)
    dataframe = dataframe.dropna(subset=['input'])
    print(dataframe.shape)
    train, test = train_test_split(dataframe, test_size=PARTITION_SIZE)
    train.to_csv('../data/train.csv', index=False)
    print(test.shape)
    test.dropna(subset=['input'])
    print(test.shape)
    test.to_csv('../data/test.csv', index=False)

if __name__ == "__main__":
    main()
