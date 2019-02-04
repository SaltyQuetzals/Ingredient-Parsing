import pandas as pd


def main():
    test_df = pd.read_csv("data/test.csv")
    with open("data/test.txt", "w+") as f:
        f.write("\n".join(test_df["input"].values))


if __name__ == "__main__":
    main()
